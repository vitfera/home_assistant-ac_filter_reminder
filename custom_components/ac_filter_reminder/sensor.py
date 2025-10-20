"""Sensores para AC Filter Reminder."""
from __future__ import annotations
import logging
from datetime import datetime, timezone
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import UnitOfTime
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN, ATTR_LAST_CLEANED, DEVICE_MANUFACTURER, DEVICE_MODEL
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurar sensores da entrada."""
    dev_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.data.get("name"),
        manufacturer=DEVICE_MANUFACTURER,
        model=DEVICE_MODEL,
        configuration_url=None,
    )

    last = LastCleanedSensor(hass, entry, dev_info)
    days = DaysUntilDueSensor(hass, entry, dev_info)

    async_add_entities([last, days])

    # Armazenar referências das entidades
    hass.data[DOMAIN][entry.entry_id]["entities"]["last_cleaned"] = last
    hass.data[DOMAIN][entry.entry_id]["entities"]["days_until_due"] = days


class LastCleanedSensor(RestoreEntity, SensorEntity):
    """Sensor da última limpeza do filtro."""

    _attr_has_entity_name = True
    _attr_name = "Última limpeza"
    _attr_icon = "mdi:calendar-clock"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_last_cleaned"
        self._attr_device_info = device_info
        self._last_value: datetime | None = None

    @property
    def native_value(self) -> datetime | None:
        """Return the state of the sensor."""
        return self._last_value

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        if self._last_value:
            return {
                "last_cleaned_formatted": self._last_value.strftime("%d/%m/%Y às %H:%M"),
                "days_since_cleaned": self._calculate_days_since()
            }
        return {"last_cleaned_formatted": "Nunca", "days_since_cleaned": None}

    def _calculate_days_since(self) -> int | None:
        """Calculate days since last cleaning."""
        if not self._last_value:
            return None
        now = datetime.now(timezone.utc)
        delta = now - self._last_value
        return delta.days

    async def async_added_to_hass(self) -> None:
        """Handle entity being added to hass with improved error handling."""
        await super().async_added_to_hass()
        
        if (state := await self.async_get_last_state()) and state.state not in ("unknown", "unavailable"):
            try:
                # Tentar diferentes formatos de data com melhor tratamento
                state_value = state.state.strip()
                
                if state_value.endswith("Z"):
                    self._last_value = datetime.fromisoformat(state_value.replace("Z", "+00:00"))
                elif "+" in state_value or state_value.endswith("UTC"):
                    self._last_value = datetime.fromisoformat(state_value.replace("UTC", "+00:00"))
                elif "T" in state_value:
                    self._last_value = datetime.fromisoformat(state_value)
                else:
                    # Tentar formato brasileiro dd/mm/yyyy
                    try:
                        self._last_value = datetime.strptime(state_value, "%d/%m/%Y às %H:%M")
                    except ValueError:
                        self._last_value = datetime.fromisoformat(state_value)
                    
                # Garantir que tenha timezone UTC
                if self._last_value and self._last_value.tzinfo is None:
                    self._last_value = self._last_value.replace(tzinfo=timezone.utc)
                    
            except Exception as err:
                _LOGGER.warning(
                    "Erro ao restaurar estado do sensor %s: %s. Usando valor padrão.",
                    self.entity_id, err
                )
                self._last_value = None

    async def async_mark_cleaned_now(self) -> None:
        """Mark as cleaned now."""
        self._last_value = datetime.now(timezone.utc)
        self.async_write_ha_state()


class DaysUntilDueSensor(SensorEntity):
    """Sensor dos dias até vencer a limpeza."""

    _attr_has_entity_name = True
    _attr_name = "Dias até vencer limpeza"
    _attr_icon = "mdi:calendar-range"
    _attr_native_unit_of_measurement = "d"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_days_until_due"
        self._attr_device_info = device_info

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        try:
            data = self.hass.data[DOMAIN][self._entry.entry_id]["entities"]
            last = data.get("last_cleaned")
            interval_ent = data.get("interval_days")
            
            if not last or not last.native_value or not interval_ent or interval_ent.native_value is None:
                return None
                
            days_since = self._days_since(last.native_value)
            delta_days = int(interval_ent.native_value) - days_since
            
            return max(delta_days, 0)
        except Exception:
            return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        try:
            data = self.hass.data[DOMAIN][self._entry.entry_id]["entities"]
            last = data.get("last_cleaned")
            interval_ent = data.get("interval_days")
            
            if last and last.native_value and interval_ent and interval_ent.native_value is not None:
                days_since = self._days_since(last.native_value)
                interval = int(interval_ent.native_value)
                is_overdue = days_since >= interval
                
                return {
                    "days_since_cleaned": days_since,
                    "interval_days": interval,
                    "is_overdue": is_overdue,
                    "overdue_days": max(0, days_since - interval) if is_overdue else 0
                }
        except Exception:
            pass
            
        return {}

    def _days_since(self, dt: datetime) -> int:
        """Calculate days since given datetime."""
        if not dt:
            return 10**6  # força "vencido" quando não há histórico
        now = datetime.now(timezone.utc)
        return int((now - dt).total_seconds() // 86400)