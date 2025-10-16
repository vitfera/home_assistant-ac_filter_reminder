# AC Filter Reminder 🌬️

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/vitfera/home_assistant-ac_filter_reminder.svg)](https://github.com/vitfera/home_assistant-ac_filter_reminder/releases/)
[![License](https://img.shields.io/github/license/vitfera/home_assistant-ac_filter_reminder.svg)](LICENSE)

Integração personalizada para o Home Assistant que te ajuda a lembrar de **limpar (não trocar)** o filtro do ar-condicionado em intervalos regulares.

## ✨ Recursos

- 🏠 **Um dispositivo por ar-condicionado** com entidades completas
- 📅 **Lembrete diário configurável** no horário que você escolher  
- 📱 **Notificações múltiplas**: persistente no HA + push mobile opcional
- 🏃‍♂️ **Fácil de usar**: botão para marcar como limpo
- 🎯 **Compatível com Áreas** do Home Assistant
- 💾 **Persistente**: mantém o histórico após reinicializações

### Entidades criadas por dispositivo:

- 📊 **`sensor.ultima_limpeza`** - Data/hora da última limpeza (timestamp)
- ⏰ **`sensor.dias_ate_vencer`** - Quantos dias restam até a próxima limpeza
- ⚠️ **`binary_sensor.limpeza_vencida`** - Indica se a limpeza está atrasada
- 🧹 **`button.marcar_como_limpo_agora`** - Botão para registrar limpeza

> **⚙️ Configuração de intervalo:** A entidade `number.intervalo_dias` fica disponível nas configurações do dispositivo, não no dashboard principal.

## 📦 Instalação

### Via HACS (Recomendado)

1. Abra o **HACS** no seu Home Assistant
2. Vá em **Integrations** → menu **⋯** → **Custom repositories**
3. Adicione esta URL: `https://github.com/vitfera/home_assistant-ac_filter_reminder`
4. Selecione a categoria **Integration**
5. Procure por **AC Filter Reminder** e clique em **Install**
6. **Reinicie** o Home Assistant

### Instalação Manual

1. Baixe os arquivos deste repositório
2. Copie a pasta `custom_components/ac_filter_reminder` para `config/custom_components/`
3. **Reinicie** o Home Assistant

## ⚙️ Configuração

### Passo 1: Adicionar a Integração

1. Vá em **Configurações** → **Dispositivos e Serviços**
2. Clique em **Adicionar Integração**
3. Procure por **AC Filter Reminder**
4. Preencha os dados:
   - **Nome do AC**: ex. "AC Sala", "AC Quarto Master"
   - **Horário do lembrete**: hora e minuto (ex.: 09:00)
   - **Serviço de notificação** (opcional): ex. `notify.mobile_app_seu_celular`

### Passo 2: Configurar o Dispositivo

1. Após a criação, vá em **Dispositivos e Serviços** → **AC Filter Reminder**
2. Clique no dispositivo criado
3. Ajuste o **Intervalo (dias)** conforme necessário (padrão: 60 dias)
4. **Atribua o dispositivo à Área** correspondente (ex.: Sala, Quarto)

### Passo 3: Notificações Mobile (Opcional)

Para receber notificações no celular:
1. Instale o app **Home Assistant Companion**
2. Na configuração da integração, use: `notify.mobile_app_nome_do_seu_dispositivo`
3. Para descobrir o nome exato, vá em **Configurações** → **Dispositivos e Serviços** → **Mobile App**

## 🎯 Como Usar

### Registrar uma Limpeza
Após limpar o filtro, simplesmente clique no botão **"Marcar como limpo agora"** na entidade do dispositivo. Isso irá:
- ✅ Atualizar a data/hora da última limpeza
- 🔄 Reiniciar o contador de dias
- 🗑️ Limpar qualquer notificação pendente

### Monitorar o Status
- **Verde**: `binary_sensor.limpeza_vencida` = OFF (filtro limpo)
- **Vermelho**: `binary_sensor.limpeza_vencida` = ON (precisa limpar)
- **Contador**: `sensor.dias_ate_vencer` mostra quantos dias restam

### Lembretes Automáticos
- O sistema verifica diariamente no horário configurado
- Se a limpeza estiver vencida, você receberá:
  - 📝 Notificação persistente no Home Assistant
  - 📱 Push notification no celular (se configurado)

## 🛠️ Personalização

### Alterar Configurações
1. Vá em **Dispositivos e Serviços** → **AC Filter Reminder**
2. Clique em **Configurar** no dispositivo
3. Ajuste horário, notificações, etc.

### Automações Personalizadas
Você pode criar automações usando as entidades:

```yaml
automation:
  - alias: "Lembrete AC - Luz Vermelha"
    trigger:
      - platform: state
        entity_id: binary_sensor.ac_sala_limpeza_vencida
        to: "on"
    action:
      - service: light.turn_on
        target:
          entity_id: light.led_sala
        data:
          color_name: red
```

## 📱 Dashboard Recomendado

### **Card: Status dos Filtros**
```yaml
type: entities
title: "🌬️ Status dos Filtros"
entities:
  - entity: binary_sensor.ac_sala_limpeza_vencida
    name: "AC Sala"
  - entity: binary_sensor.ac_quarto_master_limpeza_vencida  
    name: "AC Quarto Master"
  - entity: binary_sensor.ac_quarto_filhos_limpeza_vencida
    name: "AC Quarto Filhos"
```

### **Card: Próximas Limpezas**
```yaml
type: entities
title: "📅 Próximas Limpezas"
entities:
  - entity: sensor.ac_sala_dias_ate_vencer
    name: "AC Sala"
    icon: mdi:air-filter
  - entity: sensor.ac_quarto_master_dias_ate_vencer
    name: "AC Quarto Master"
    icon: mdi:air-filter
  - entity: sensor.ac_quarto_filhos_dias_ate_vencer
    name: "AC Quarto Filhos"
    icon: mdi:air-filter
```

### **Card: Última Limpeza**
```yaml
type: entities
title: "🕐 Última Limpeza"
entities:
  - entity: sensor.ac_sala_ultima_limpeza
    name: "AC Sala"
    icon: mdi:calendar-check
  - entity: sensor.ac_quarto_master_ultima_limpeza
    name: "AC Quarto Master"
    icon: mdi:calendar-check
  - entity: sensor.ac_quarto_filhos_ultima_limpeza
    name: "AC Quarto Filhos"
    icon: mdi:calendar-check
```

### **Card: Botões de Limpeza**
```yaml
type: entities  
title: "🧹 Marcar como Limpo"
entities:
  - entity: button.ac_sala_marcar_como_limpo_agora
    name: "✅ AC Sala"
  - entity: button.ac_quarto_master_marcar_como_limpo_agora
    name: "✅ AC Quarto Master"
  - entity: button.ac_quarto_filhos_marcar_como_limpo_agora
    name: "✅ AC Quarto Filhos"
```

### **Card: Dashboard Compacto (Alternativa)**
```yaml
type: glance
title: "🌬️ Filtros AC - Resumo"
entities:
  - entity: binary_sensor.ac_sala_limpeza_vencida
    name: "Sala"
  - entity: binary_sensor.ac_quarto_master_limpeza_vencida
    name: "Quarto Master"
  - entity: binary_sensor.ac_quarto_filhos_limpeza_vencida
    name: "Quarto Filhos"
```

> **💡 Nota:** As configurações de intervalo (dias) ficam nas **opções do dispositivo**, não no dashboard. Para alterar, vá em `Dispositivos e Serviços → AC Filter Reminder → Configurar`.

## 🐛 Problemas Conhecidos

- A primeira execução pode não ter histórico - isso é normal
- Certifique-se de que o serviço de notificação está correto
- Fusos horários são tratados automaticamente em UTC

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 💡 Roadmap

- [ ] Suporte a múltiplos lembretes por dia
- [ ] Interface gráfica para configuração
- [ ] Histórico de limpezas
- [ ] Integração com calendário
- [ ] Lembretes por voz (TTS)
- [ ] Métricas avançadas

## 🙋‍♂️ Suporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/vitfera/home_assistant-ac_filter_reminder/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/vitfera/home_assistant-ac_filter_reminder/discussions)
- 📧 **Email**: Criar issue no GitHub

---

⭐ **Gostou do projeto?** Dê uma estrela no GitHub!

**Feito com ❤️ para a comunidade Home Assistant brasileira**
