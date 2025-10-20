# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-12

### Added
- Initial release of AC Filter Reminder integration
- Support for multiple air conditioning units
- Configurable cleaning intervals (1-365 days)
- Daily reminder notifications at specified time
- Persistent notifications in Home Assistant
- Optional mobile push notifications
- Button to mark filter as cleaned
- Binary sensor to indicate overdue cleaning
- Sensors for last cleaned date and days until due
- Number entity for configurable interval
- Support for Home Assistant Areas
- State restoration after HA restart
- HACS compatibility
- Complete documentation and setup guide

### Features
- **Device per AC**: Each air conditioner gets its own device with all entities
- **Smart notifications**: Only notifies when cleaning is actually due
- **Easy management**: One-click button to mark as cleaned
- **Flexible scheduling**: Configure reminder time per device
- **Multi-platform**: Works with mobile apps and web interface
- **Robust**: Handles edge cases and state restoration

### Entities Created
- `sensor.ultima_limpeza` - Last cleaning timestamp
- `number.intervalo_dias` - Configurable interval in days
- `sensor.dias_ate_vencer` - Days until next cleaning due
- `binary_sensor.limpeza_vencida` - Overdue cleaning indicator
- `button.marcar_como_limpo_agora` - Mark as cleaned button

### Technical Details
- Supports Home Assistant 2023.1.0+
- Uses UTC timezone for consistent date handling
- Implements proper state restoration
- Follows HA integration best practices
- Full config flow support with options
- Comprehensive error handling