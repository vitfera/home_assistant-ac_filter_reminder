# Estrutura do Projeto AC Filter Reminder

```
home_assistant-ac_filter_reminder/
├── custom_components/
│   └── ac_filter_reminder/
│       ├── __init__.py              # Inicialização da integração
│       ├── manifest.json            # Metadados da integração  
│       ├── const.py                 # Constantes e configurações
│       ├── config_flow.py           # Interface de configuração
│       ├── sensor.py                # Sensores (última limpeza, dias restantes)
│       ├── binary_sensor.py         # Sensor binário (limpeza vencida)
│       ├── number.py                # Entidade numérica (intervalo dias)
│       ├── button.py                # Botão (marcar como limpo)
│       └── services.yaml            # Definição de serviços
├── hacs.json                        # Configuração HACS
├── README.md                        # Documentação completa
├── LICENSE                          # Licença MIT
└── CHANGELOG.md                     # Histórico de mudanças
```

## Arquivos Principais

### Core da Integração
- **`manifest.json`**: Define metadados, dependências e tipo da integração
- **`__init__.py`**: Controla setup, unload e gerenciamento de lembretes diários
- **`const.py`**: Centraliza todas as constantes e configurações padrão
- **`config_flow.py`**: Interface para adicionar/configurar dispositivos

### Entidades
- **`sensor.py`**: Última limpeza (timestamp) + Dias até vencer
- **`binary_sensor.py`**: Status binário se limpeza está vencida  
- **`number.py`**: Configuração do intervalo de dias (1-365)
- **`button.py`**: Botão para marcar filtro como limpo

### Configuração
- **`hacs.json`**: Compatibilidade com HACS (Home Assistant Community Store)
- **`services.yaml`**: Define serviços customizados (futuro)

### Documentação
- **`README.md`**: Guia completo de instalação e uso
- **`LICENSE`**: Licença MIT para uso libre
- **`CHANGELOG.md`**: Histórico de versões e mudanças

## Status do Projeto: ✅ COMPLETO

Todas as funcionalidades estão implementadas e prontas para uso!