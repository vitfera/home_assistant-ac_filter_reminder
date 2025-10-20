"""Constantes para a integração AC Filter Reminder."""

DOMAIN = "ac_filter_reminder"

CONF_NAME = "name"
CONF_REMINDER_HOUR = "reminder_hour"
CONF_REMINDER_MINUTE = "reminder_minute"
CONF_NOTIFY_SERVICE = "notify_service"  # ex.: notify.mobile_app_meu_celular

PLATFORMS = ["sensor", "binary_sensor", "number", "button"]
DEVICE_MANUFACTURER = "VictorFS"
DEVICE_MODEL = "AC Filter Reminder"

ATTR_LAST_CLEANED = "last_cleaned"
ATTR_INTERVAL_DAYS = "interval_days"
DEFAULT_INTERVAL_DAYS = 60
DEFAULT_HOUR = 9
DEFAULT_MINUTE = 0

# Chaves de tradução
CONF_AC_NAME = "ac_name"
CONF_INTERVAL_DAYS = "interval_days"