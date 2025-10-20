"""Number entities para AC Filter Reminder."""
from __future__ import annotations
from typing import Any

from homeassistant.components.number import NumberEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN, ATTR_INTERVAL_DAYS, DEFAULT_INTERVAL_DAYS, 
    DEVICE_MANUFACTURER, DEVICE_MODEL
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurar entidades number da entrada."""
    dev_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.data.get("name"),
        manufacturer=DEVICE_MANUFACTURER,
        model=DEVICE_MODEL,
    )
    
    ent = IntervalDaysNumber(hass, entry, dev_info)
    async_add_entities([ent])
    
    # Armazenar referência da entidade
    hass.data[DOMAIN][entry.entry_id]["entities"]["interval_days"] = ent


class IntervalDaysNumber(RestoreEntity, NumberEntity):
    """Entidade number para configurar o intervalo de dias entre limpezas."""

    _attr_has_entity_name = True
    _attr_name = "Intervalo (dias)"
    _attr_icon = "mdi:counter"
    _attr_native_min_value = 1
    _attr_native_max_value = 365
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "d"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, device_info: DeviceInfo) -> None:
        """Initialize the number entity."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_interval_days"
        self._attr_device_info = device_info
        self._val = DEFAULT_INTERVAL_DAYS

    @property
    def native_value(self) -> float:
        """Return the current value."""
        return self._val

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "min_value": self._attr_native_min_value,
            "max_value": self._attr_native_max_value,
            "step": self._attr_native_step,
            "description": "Intervalo em dias entre as limpezas do filtro"
        }

    async def async_set_native_value(self, value: float) -> None:
        """Set the native value."""
        self._val = int(value)
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Handle entity being added to hass."""
        await super().async_added_to_hass()
        
        if (state := await self.async_get_last_state()) and state.state not in ("unknown", "unavailable"):
            try:
                self._val = int(float(state.state))
                # Validar limites
                if self._val < self._attr_native_min_value:
                    self._val = int(self._attr_native_min_value)
                elif self._val > self._attr_native_max_value:
                    self._val = int(self._attr_native_max_value)
            except (ValueError, TypeError):
                self._val = DEFAULT_INTERVAL_DAYS