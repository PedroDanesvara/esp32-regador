# 🧪 Guia de Teste - Sistema ESP32 Monitoramento

Este guia irá ajudá-lo a testar o sistema de monitoramento de temperatura e umidade do solo com ESP32.

## 📋 Pré-requisitos

### Hardware
- [ ] ESP32 (qualquer modelo)
- [ ] Sensor de Umidade do Solo Capacitivo v2.0
- [ ] Sensor de Temperatura DS18B20 (opcional)
- [ ] Protoboard e jumpers
- [ ] Cabo USB

### Software
- [ ] Arduino IDE 2.x
- [ ] ESP32 Board Package instalado
- [ ] Bibliotecas necessárias instaladas

## 🔧 Passo 1: Instalação das Bibliotecas

1. Abra o Arduino IDE
2. Vá em **Sketch > Include Library > Manage Libraries**
3. Instale as seguintes bibliotecas:
   - **ArduinoJson** (versão 6.x)
   - **OneWire**
   - **DallasTemperature**

## 🔌 Passo 2: Conexões Físicas

### Sensor de Umidade do Solo
```
ESP32          Sensor v2.0
3.3V    →      VCC
GND     →      GND
GPIO 36 →      AOUT
```

### Sensor de Temperatura (opcional)
```
ESP32          DS18B20
3.3V    →      VCC
GND     →      GND
GPIO 4  →      DATA
4.7kΩ   →      Resistor pull-up (DATA ↔ VCC)
```

## ⚙️ Passo 3: Configuração do Código

1. Abra o arquivo `main.ino` no Arduino IDE
2. Configure suas credenciais WiFi:
   ```cpp
   const char* ssid = "SUA_REDE_WIFI";
   const char* password = "SUA_SENHA_WIFI";
   ```
3. Configure a URL da sua API:
   ```cpp
   const char* apiUrl = "http://sua-api.com/dados";
   ```

## 🧪 Passo 4: Teste Básico (Sem API)

### 4.1 Upload do Código
1. Conecte o ESP32 via USB
2. Selecione a placa correta em **Tools > Board**
3. Selecione a porta correta em **Tools > Port**
4. Clique em **Upload**

### 4.2 Monitoramento Serial
1. Abra o **Monitor Serial** (Tools > Serial Monitor)
2. Configure a velocidade para **115200 baud**
3. Você deve ver:
   ```
   Iniciando sistema de monitoramento...
   Conectando ao WiFi: SUA_REDE_WIFI
   ................
   WiFi conectado!
   Endereço IP: 192.168.1.100
   Sistema inicializado com sucesso!
   === Medindo sensores ===
   Valor Raw do Sensor: 2500
   Temperatura: 25.5 °C
   Umidade do Solo: 65%
   ========================
   ```

### 4.3 Verificação dos Sensores
- **LED**: Deve acender quando WiFi conectar
- **Temperatura**: Deve mostrar valores entre -40°C e +125°C
- **Umidade**: Deve mostrar valores entre 0% e 100%

## 🌐 Passo 5: Teste com API

### 5.1 Usando Webhook.site (Recomendado para teste)
1. Acesse [webhook.site](https://webhook.site)
2. Copie a URL única gerada
3. Substitua no código:
   ```cpp
   const char* apiUrl = "https://webhook.site/SUA_URL_UNICA";
   ```
4. Faça upload do código novamente
5. Verifique se os dados aparecem no webhook.site

### 5.2 Usando o Script Python
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o script:
   ```bash
   python test_api.py
   ```
3. Siga as instruções no terminal

### 5.3 Verificação da API
No Monitor Serial, você deve ver:
```
Enviando dados para API:
{"temperatura":25.5,"umidade_solo":65,"timestamp":1234567890,"device_id":"ESP32_001"}
Resposta da API (código 200):
{"status":"success","message":"Data received"}
```

## 🔧 Passo 6: Calibração do Sensor de Umidade

### 6.1 Calibração Manual
1. Adicione esta linha no `setup()`:
   ```cpp
   calibrarSensor();
   ```
2. Faça upload do código
3. Siga as instruções no Monitor Serial:
   - Coloque o sensor no solo seco e pressione qualquer tecla
   - Coloque o sensor no solo molhado e pressione qualquer tecla
4. Anote os valores e atualize no código:
   ```cpp
   const int VALOR_SECO = 4095;    // Seu valor
   const int VALOR_MOLHADO = 1800; // Seu valor
   ```

### 6.2 Teste de Calibração
- **Solo seco**: Deve mostrar ~0-10%
- **Solo úmido**: Deve mostrar ~80-100%
- **Solo moderado**: Deve mostrar ~40-60%

## 🚨 Solução de Problemas

### Problema: WiFi não conecta
**Sintomas**: "Falha na conexão WiFi!"
**Soluções**:
1. Verifique o nome da rede e senha
2. Certifique-se de que a rede é 2.4GHz
3. Verifique se o ESP32 está próximo ao roteador

### Problema: Sensor de umidade não funciona
**Sintomas**: Valores sempre 0% ou 100%
**Soluções**:
1. Verifique as conexões
2. Calibre o sensor
3. Verifique se está usando o pino ADC correto (GPIO 36)

### Problema: API não recebe dados
**Sintomas**: "Erro ao enviar dados"
**Soluções**:
1. Verifique a URL da API
2. Teste a API separadamente
3. Verifique se o ESP32 tem acesso à internet

### Problema: Sensor de temperatura não funciona
**Sintomas**: Temperatura = -999
**Soluções**:
1. Verifique as conexões do DS18B20
2. Verifique o resistor pull-up
3. Teste com multímetro

## 📊 Verificação Final

### Checklist de Teste
- [ ] ESP32 conecta ao WiFi
- [ ] LED acende quando conectado
- [ ] Sensor de umidade mostra valores variados
- [ ] Sensor de temperatura mostra valores realistas
- [ ] Dados são enviados para API
- [ ] API responde com sucesso
- [ ] Medições ocorrem a cada 30 segundos

### Valores Esperados
- **Temperatura**: 15°C - 40°C (ambiente)
- **Umidade do Solo**: 0% - 100% (depende do solo)
- **Intervalo**: 30 segundos entre medições
- **Formato JSON**: Estrutura correta

## 🎯 Próximos Passos

Após o teste bem-sucedido:
1. **Implemente sua API real**
2. **Adicione autenticação**
3. **Configure alertas**
4. **Crie dashboard**
5. **Implemente modo sleep**

## 📞 Suporte

Se encontrar problemas:
1. Verifique o Monitor Serial para mensagens de erro
2. Teste cada componente individualmente
3. Consulte a documentação das bibliotecas
4. Verifique as conexões físicas

---

**Boa sorte com seu projeto! 🚀** 