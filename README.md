# ESP32 - Sistema de Monitoramento IoT

## Descrição
Código para ESP32 que monitora umidade do solo, enviando dados para a API via HTTP. Inclui simulador Python para testes.

## Funcionalidades
- Leitura de sensor de umidade do solo
- Envio de dados para API via HTTP
- Controle de bomba de água
- Simulador Python para testes
- Configuração via WiFi

## Hardware Necessário
- ESP32
- Sensor de umidade do solo
- Relé para controle da bomba
- Módulo WiFi (integrado no ESP32)

## Pinagem
```
Sensor de Umidade do Solo:
- VCC -> 3.3V
- GND -> GND
- DATA -> GPIO36 (ADC)

Relé da Bomba:
- VCC -> 3.3V
- GND -> GND
- IN -> GPIO2
```

## Configuração

1. Instale as bibliotecas necessárias no Arduino IDE:
   - WiFi library (incluída)
   - HTTPClient library (incluída)
   - ArduinoJson

2. Configure as credenciais WiFi no arquivo `config.h`:
```cpp
#define WIFI_SSID "sua_rede_wifi"
#define WIFI_PASSWORD "sua_senha_wifi"
```

3. Configure a URL da API:
```cpp
#define API_URL "http://localhost:3000/api/sensors"
```

4. Faça upload do código para o ESP32

## Estrutura do Projeto
```
esp32/
├── main.ino           # Código principal do ESP32
├── config.h           # Configurações (WiFi, API, etc.)
├── simulador_esp32.py # Simulador Python para testes
├── test_api.py        # Script de teste da API
├── teste_rapido.py    # Teste rápido do sistema
├── requirements.txt   # Dependências Python
└── README.md          # Este arquivo
```

## Funcionamento

### Loop Principal
1. Conecta ao WiFi
2. Lê dados dos sensores
3. Envia dados para a API
4. Aguarda intervalo configurado
5. Repete o processo

### Envio de Dados
Os dados são enviados no formato JSON:
```json
{
  "umidade_solo": 65,
  "timestamp": 1234567890,
  "device_id": "ESP32_001"
}
```

## Simulador Python

Para testar sem hardware físico:

1. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

2. Execute o simulador:
```bash
python simulador_esp32.py
```

O simulador irá:
- Gerar dados aleatórios de umidade
- Enviar dados para a API
- Simular o comportamento do ESP32

## Testes

### Teste Rápido
```bash
python teste_rapido.py
```

### Teste da API
```bash
python test_api.py
```

## Configurações Avançadas

### Intervalo de Envio
Modifique no `config.h`:
```cpp
#define SEND_INTERVAL 30000  // 30 segundos
```

### Calibração do Sensor de Solo
Ajuste os valores no código:
```cpp
#define SOIL_DRY_VALUE 4095
#define SOIL_WET_VALUE 0
```

### Controle da Bomba
A bomba é ativada quando a umidade está abaixo do limite:
```cpp
#define UMIDADE_MINIMA 30  // 30%
```

## Troubleshooting

### Problemas de Conexão WiFi
- Verifique as credenciais no `config.h`
- Certifique-se de que a rede está disponível
- Verifique a distância do roteador

### Problemas de Envio de Dados
- Verifique se a API está rodando
- Confirme a URL no `config.h`
- Verifique a conectividade de rede

### Problemas com Sensores
- Verifique as conexões físicas
- Confirme a alimentação (3.3V)
- Teste os sensores individualmente

## Documentação Adicional
- `GUIA_SIMULADOR.md` - Guia detalhado do simulador
- `GUIA_TESTE.md` - Guia de testes e troubleshooting

## Contribuição
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request 