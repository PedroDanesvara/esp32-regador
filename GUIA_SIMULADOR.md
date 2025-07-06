# 🤖 Guia do Simulador ESP32

Este guia explica como usar os scripts de simulação para testar o sistema de monitoramento.

## 📋 Scripts Disponíveis

### 1. `simulador_esp32.py` - Simulação Completa
Simula um ESP32 real enviando dados continuamente e controlando a bomba automaticamente.

### 2. `teste_rapido.py` - Teste Rápido
Script simples para testes rápidos da API.

## 🚀 Como Usar

### Pré-requisitos
1. **API rodando**: `cd api && npm run dev`
2. **Python instalado** com biblioteca `requests`
3. **Device criado**: Use um device existente (ex: ESP32_002)

### Instalar Dependências
```bash
pip install requests
```

## 🧪 Teste Rápido

Execute o teste rápido para verificar se tudo está funcionando:

```bash
cd esp32
python teste_rapido.py
```

**O que o teste faz:**
1. ✅ Verifica se a API está rodando
2. 📊 Envia dados dos sensores
3. 🚰 Verifica status da bomba
4. 🚰 Ativa a bomba
5. ⏳ Aguarda 3 segundos
6. 🚰 Verifica status novamente
7. 🚰 Desativa a bomba
8. 📈 Busca estatísticas

## 🔄 Simulação Contínua

Para simular um ESP32 real enviando dados continuamente:

```bash
cd esp32
python simulador_esp32.py
```

**Configurações:**
- **URL da API**: `http://localhost:3000/api` (padrão)
- **Device ID**: `ESP32_002` (padrão)
- **Duração**: 10 minutos (padrão)

**O que a simulação faz:**
1. 🔄 Envia dados a cada 5 segundos
2. 🤖 Controle automático da bomba baseado na umidade
3. 🎲 Eventos aleatórios (10% de chance)
4. 📊 Mostra status em tempo real
5. 📈 Estatísticas ao final

## 🎯 Lógica de Controle Automático

A simulação controla a bomba automaticamente baseado na umidade do solo:

- **Umidade < 30%**: Ativa a bomba
- **Umidade > 70%**: Desativa a bomba
- **Verificação**: A cada 3 ciclos (15 segundos)

## 📱 Testando no App

### 1. Conectar ao Device
- Abra o app Flutter
- Conecte ao device `ESP32_002`
- Os dados devem aparecer automaticamente

### 2. Monitorar Dados
- Umidade atualiza a cada 5 segundos
- Status da bomba atualiza em tempo real
- Histórico é mantido no banco de dados

### 3. Controlar Bomba
- Use o botão no app para ativar/desativar
- Veja o status mudar em tempo real
- Observe o histórico de ativações

## 🔧 Personalização

### Alterar Device ID
Edite o arquivo `simulador_esp32.py`:
```python
self.device_id = "ESP32_003"  # Seu device ID
```

### Alterar Intervalos
```python
# Enviar dados a cada 3 segundos
time.sleep(3)

# Verificar bomba a cada 5 ciclos
if ciclo % 5 == 0:
```

### Alterar Valores Base
```python
# Umidade base
self.base_humidity = 60

# Variações
self.humidity_variation = 20
```

## 🚨 Troubleshooting

### API não responde
```bash
# Verificar se está rodando
curl http://localhost:3000/health

# Reiniciar API
cd api
npm run dev
```

### Device não encontrado
```bash
# Listar devices
curl http://localhost:3000/api/devices

# Criar novo device se necessário
npm run create-device
```

### Erro de conexão
- Verifique se a API está na porta 3000
- Confirme o IP se testando em dispositivo físico
- Verifique firewall/antivírus

## 📊 Monitoramento

### Logs da API
```bash
cd api
npm run dev
# Observe os logs no terminal
```

### Logs do Simulador
O simulador mostra:
- Dados enviados
- Status da bomba
- Erros de conexão
- Estatísticas finais

### Banco de Dados
```bash
# Verificar dados salvos
sqlite3 api/data/monitoring.db
.tables
SELECT * FROM sensor_data ORDER BY created_at DESC LIMIT 5;
SELECT * FROM pump_history ORDER BY created_at DESC LIMIT 5;
```

## 🎉 Próximos Passos

1. **Teste básico**: Execute `teste_rapido.py`
2. **Simulação contínua**: Execute `simulador_esp32.py`
3. **Teste no app**: Conecte ao device no app Flutter
4. **Personalize**: Ajuste parâmetros conforme necessário
5. **Monitore**: Observe logs e dados em tempo real

## 📞 Suporte

Se encontrar problemas:
1. Verifique se a API está rodando
2. Confirme o device ID está correto
3. Verifique logs da API
4. Teste com `teste_rapido.py` primeiro 