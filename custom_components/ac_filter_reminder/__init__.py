"""Integração AC Filter Reminder para Home Assistant."""
from __future__ import annotations

from datetime import datetime
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.const import Platform
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN, PLATFORMS,
    CONF_NAME, CONF_REMINDER_HOUR, CONF_REMINDER_MINUTE, CONF_NOTIFY_SERVICE,
    DEFAULT_HOUR, DEFAULT_MINUTE
)

_LOGGER = logging.getLogger(__name__)

# Estrutura em memória por entry
# hass.data[DOMAIN][entry_id] = {
#   "name": str,
#   "notify_service": str | None,
#   "hour": int, "minute": int,
#   "entities": {
#       "last_cleaned": entity_obj,
#       "interval_days": entity_obj,
#       "days_until_due": entity_obj,
#       "cleaning_due": entity_obj,
#       "mark_cleaned": entity_obj,
#   },
#   "unsub": callable (para descadastrar o lembrete)
# }


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Configuração inicial da integração."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurar uma entrada da integração."""
    hass.data.setdefault(DOMAIN, {})

    name = entry.data.get(CONF_NAME)
    hour = entry.options.get(CONF_REMINDER_HOUR, entry.data.get(CONF_REMINDER_HOUR, DEFAULT_HOUR))
    minute = entry.options.get(CONF_REMINDER_MINUTE, entry.data.get(CONF_REMINDER_MINUTE, DEFAULT_MINUTE))
    notify_service = entry.options.get(CONF_NOTIFY_SERVICE, entry.data.get(CONF_NOTIFY_SERVICE))

    hass.data[DOMAIN][entry.entry_id] = {
        "name": name,
        "notify_service": notify_service,
        "hour": hour,
        "minute": minute,
        "entities": {},
        "unsub": None,
    }

    # Configurar plataformas
    await hass.config_entries.async_forward_entry_setups(
        entry, [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.NUMBER, Platform.BUTTON]
    )

    # Registrar lembrete diário no horário configurado
    @callback
    def _daily_check(now: datetime):
        """Verificação diária para lembretes."""
        data = hass.data[DOMAIN].get(entry.entry_id)
        if not data:
            return
        
        # Verificar se é o horário correto
        if now.hour != hour or now.minute != minute:
            return
            
        ents = data.get("entities", {})
        last_cleaned = ents.get("last_cleaned")
        interval_ent = ents.get("interval_days")
        due = ents.get("cleaning_due")
        days_until = ents.get("days_until_due")

        if not (last_cleaned and interval_ent and due):
            return

        # Se estiver vencido, notifica
        if due.is_on:
            _notify(hass, entry, data["name"], last_cleaned.native_value, 
                   interval_ent.native_value, days_until.native_value)

    # Configurar tracking de tempo para verificação diária
    unsub = async_track_time_change(hass, _daily_check, minute="*", second=0)
    hass.data[DOMAIN][entry.entry_id]["unsub"] = unsub

    return True


def _notify(hass: HomeAssistant, entry: ConfigEntry, ac_name: str, 
           last_cleaned, interval_days, days_until):
    """Enviar notificações de lembrete."""
    title = f"Lembrete: limpar filtro do {ac_name}"
    
    if last_cleaned:
        last_cleaned_str = last_cleaned.strftime("%d/%m/%Y às %H:%M") if hasattr(last_cleaned, 'strftime') else str(last_cleaned)
    else:
        last_cleaned_str = "Nunca"
    
    message = (
        f"Está na hora de LIMPAR (não trocar) o filtro do {ac_name}.\n"
        f"Última limpeza: {last_cleaned_str}\n"
        f"Intervalo: {interval_days} dias\n"
        f"Dias restantes: {days_until if days_until is not None else 'N/A'}"
    )

    # Notificação persistente
    hass.async_create_task(hass.services.async_call(
        "persistent_notification", "create",
        {
            "title": title, 
            "message": message,
            "notification_id": f"ac_filter_{entry.entry_id}"
        },
        blocking=False,
    ))

    # Notificação via notify.* se configurada
    notify_service = hass.data[DOMAIN][entry.entry_id].get("notify_service")
    if notify_service and notify_service.strip():
        if "." in notify_service:
            domain, service = notify_service.split(".", 1)
        else:
            domain, service = "notify", notify_service
            
        hass.async_create_task(hass.services.async_call(
            domain, service, 
            {"title": title, "message": message}, 
            blocking=False
        ))


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descarregar uma entrada da integração."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.NUMBER, Platform.BUTTON]
    )
    
    data = hass.data[DOMAIN].pop(entry.entry_id, None)
    if data and data.get("unsub"):
        data["unsub"]()
        
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Recarregar uma entrada da integração."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)