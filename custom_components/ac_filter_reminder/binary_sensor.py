"""Binary sensors para AC Filter Reminder."""
from __future__ import annotations
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DEVICE_MANUFACTURER, DEVICE_MODEL


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurar binary sensors da entrada."""
    dev_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.data.get("name"),
        manufacturer=DEVICE_MANUFACTURER,
        model=DEVICE_MODEL,
    )
    
    ent = CleaningDueBinary(hass, entry, dev_info)
    async_add_entities([ent])
    
    # Armazenar referência da entidade
    hass.data[DOMAIN][entry.entry_id]["entities"]["cleaning_due"] = ent


class CleaningDueBinary(BinarySensorEntity):
    """Binary sensor para indicar se a limpeza está vencida."""

    _attr_has_entity_name = True
    _attr_name = "Limpeza vencida"
    _attr_icon = "mdi:air-filter"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, device_info: DeviceInfo) -> None:
        """Initialize the binary sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_cleaning_due"
        self._attr_device_info = device_info

    @property
    def is_on(self) -> bool:
        """Return true if cleaning is due."""
        try:
            data = self.hass.data[DOMAIN][self._entry.entry_id]["entities"]
            last = data.get("last_cleaned")
            interval_ent = data.get("interval_days")
            
            if not interval_ent or interval_ent.native_value is None:
                return False
                
            interval = int(interval_ent.native_value)
            
            if not last or not last.native_value:
                return True  # sem histórico => considerar como pendente
                
            days_since = self._days_since(last.native_value)
            return days_since >= interval
        except Exception:
            return False

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        try:
            data = self.hass.data[DOMAIN][self._entry.entry_id]["entities"]
            last = data.get("last_cleaned")
            interval_ent = data.get("interval_days")
            
            if last and interval_ent and interval_ent.native_value is not None:
                days_since = self._days_since(last.native_value) if last.native_value else None
                interval = int(interval_ent.native_value)
                
                attrs = {
                    "interval_days": interval,
                    "days_since_cleaned": days_since,
                }
                
                if days_since is not None:
                    attrs.update({
                        "is_overdue": days_since >= interval,
                        "overdue_days": max(0, days_since - interval),
                        "days_until_due": max(0, interval - days_since)
                    })
                    
                return attrs
        except Exception:
            pass
            
        return {}

    @property
    def icon(self) -> str:
        """Return the icon based on state."""
        if self.is_on:
            return "mdi:air-filter-alert"
        return "mdi:air-filter"

    def _days_since(self, dt) -> int:
        """Calculate days since given datetime."""
        if not dt:
            return 10**6  # força "vencido" quando não há histórico
            
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        return int((now - dt).total_seconds() // 86400)