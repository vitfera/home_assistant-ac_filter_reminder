"""Config flow para AC Filter Reminder."""
from __future__ import annotations
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN, CONF_NAME, CONF_REMINDER_HOUR, CONF_REMINDER_MINUTE, CONF_NOTIFY_SERVICE,
    DEFAULT_HOUR, DEFAULT_MINUTE
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AC Filter Reminder."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            # Validar nome único
            await self.async_set_unique_id(user_input[CONF_NAME])
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=user_input[CONF_NAME], 
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Optional(CONF_REMINDER_HOUR, default=DEFAULT_HOUR): 
                vol.All(int, vol.Range(min=0, max=23)),
            vol.Optional(CONF_REMINDER_MINUTE, default=DEFAULT_MINUTE): 
                vol.All(int, vol.Range(min=0, max=59)),
            vol.Optional(CONF_NOTIFY_SERVICE, default=""): str,
        })
        
        return self.async_show_form(
            step_id="user", 
            data_schema=schema, 
            errors=errors,
            description_placeholders={
                "name_example": "AC Sala",
                "notify_example": "notify.mobile_app_seu_celular"
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for AC Filter Reminder."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_hour = self.config_entry.options.get(
            CONF_REMINDER_HOUR, 
            self.config_entry.data.get(CONF_REMINDER_HOUR, DEFAULT_HOUR)
        )
        current_minute = self.config_entry.options.get(
            CONF_REMINDER_MINUTE, 
            self.config_entry.data.get(CONF_REMINDER_MINUTE, DEFAULT_MINUTE)
        )
        current_notify = self.config_entry.options.get(
            CONF_NOTIFY_SERVICE, 
            self.config_entry.data.get(CONF_NOTIFY_SERVICE, "")
        )

        schema = vol.Schema({
            vol.Optional(CONF_REMINDER_HOUR, default=current_hour): 
                vol.All(int, vol.Range(min=0, max=23)),
            vol.Optional(CONF_REMINDER_MINUTE, default=current_minute): 
                vol.All(int, vol.Range(min=0, max=59)),
            vol.Optional(CONF_NOTIFY_SERVICE, default=current_notify): str,
        })
        
        return self.async_show_form(
            step_id="init", 
            data_schema=schema,
            description_placeholders={
                "notify_example": "notify.mobile_app_seu_celular"
            }
        )