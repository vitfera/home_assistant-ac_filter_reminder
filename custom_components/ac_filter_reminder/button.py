"""Button entities para AC Filter Reminder."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
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
    """Configurar buttons da entrada."""
    dev_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.data.get("name"),
        manufacturer=DEVICE_MANUFACTURER,
        model=DEVICE_MODEL,
    )
    
    ent = MarkCleanedButton(hass, entry, dev_info)
    async_add_entities([ent])
    
    # Armazenar referência da entidade
    hass.data[DOMAIN][entry.entry_id]["entities"]["mark_cleaned"] = ent


class MarkCleanedButton(ButtonEntity):
    """Button para marcar como limpo agora."""

    _attr_has_entity_name = True
    _attr_name = "Marcar como limpo agora"
    _attr_icon = "mdi:broom"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, device_info: DeviceInfo) -> None:
        """Initialize the button."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_mark_cleaned"
        self._attr_device_info = device_info

    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            # Obter a entidade last_cleaned e marcar como limpo agora
            entities = self.hass.data[DOMAIN][self._entry.entry_id]["entities"]
            last_cleaned_entity = entities.get("last_cleaned")
            
            if last_cleaned_entity:
                await last_cleaned_entity.async_mark_cleaned_now()
                
                # Limpar notificação persistente se existir
                await self.hass.services.async_call(
                    "persistent_notification", "dismiss",
                    {"notification_id": f"ac_filter_{self._entry.entry_id}"},
                    blocking=False,
                )
                
                # Log da ação
                ac_name = self._entry.data.get("name", "AC")
                self.hass.async_create_task(
                    self.hass.services.async_call(
                        "system_log", "write",
                        {
                            "message": f"Filtro do {ac_name} marcado como limpo via botão",
                            "level": "info",
                            "logger": f"{DOMAIN}.button"
                        },
                        blocking=False,
                    )
                )
                
        except Exception as err:
            # Log do erro
            self.hass.async_create_task(
                self.hass.services.async_call(
                    "system_log", "write",
                    {
                        "message": f"Erro ao marcar filtro como limpo: {err}",
                        "level": "error",
                        "logger": f"{DOMAIN}.button"
                    },
                    blocking=False,
                )
            )