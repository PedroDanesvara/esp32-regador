#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configurações WiFi
const char* ssid = "SUA_REDE_WIFI";
const char* password = "SUA_SENHA_WIFI";

// Configurações da API
const char* apiUrl = "http://sua-api.com/dados"; // Substitua pela URL da sua API
const int apiPort = 80;

// Pinos do ESP32
#define SOIL_MOISTURE_PIN 36  // Pino ADC para o sensor de umidade do solo
#define LED_PIN 2             // LED para indicar status

// Variáveis globais
int umidadeSolo = 0;
unsigned long ultimaMedicao = 0;
const unsigned long intervaloMedicao = 30000; // 30 segundos

// Configurações do sensor de umidade do solo
const int VALOR_SECO = 4095;    // Valor quando o solo está seco
const int VALOR_MOLHADO = 1800; // Valor quando o solo está molhado

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println("Iniciando sistema de monitoramento...");
  
  // Conectar ao WiFi
  conectarWiFi();
  
  Serial.println("Sistema inicializado com sucesso!");
}

void loop() {
  // Verificar conexão WiFi
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Conexão WiFi perdida. Reconectando...");
    conectarWiFi();
  }
  
  // Medir a cada intervalo definido
  if (millis() - ultimaMedicao >= intervaloMedicao) {
    medirSensores();
    enviarDadosAPI();
    ultimaMedicao = millis();
  }
  
  delay(1000);
}

void conectarWiFi() {
  Serial.print("Conectando ao WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("WiFi conectado!");
    Serial.print("Endereço IP: ");
    Serial.println(WiFi.localIP());
    digitalWrite(LED_PIN, HIGH);
  } else {
    Serial.println();
    Serial.println("Falha na conexão WiFi!");
    digitalWrite(LED_PIN, LOW);
  }
}

void medirSensores() {
  Serial.println("=== Medindo sensores ===");
  
  // Medir umidade do solo
  medirUmidadeSolo();
  
  // Exibir resultados
  Serial.print("Umidade do Solo: ");
  Serial.print(umidadeSolo);
  Serial.println("%");
  Serial.println("========================");
}

void medirUmidadeSolo() {
  int valorRaw = analogRead(SOIL_MOISTURE_PIN);
  
  // Converter valor raw para porcentagem
  // O sensor capacitivo v2.0 tem valores invertidos (maior valor = mais seco)
  umidadeSolo = map(valorRaw, VALOR_SECO, VALOR_MOLHADO, 0, 100);
  
  // Limitar valores entre 0 e 100
  umidadeSolo = constrain(umidadeSolo, 0, 100);
  
  Serial.print("Valor Raw do Sensor: ");
  Serial.println(valorRaw);
}

void enviarDadosAPI() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi não conectado. Não foi possível enviar dados.");
    return;
  }
  
  HTTPClient http;
  http.begin(apiUrl);
  http.addHeader("Content-Type", "application/json");
  
  // Criar JSON com os dados
  StaticJsonDocument<200> doc;
  doc["umidade_solo"] = umidadeSolo;
  doc["timestamp"] = millis();
  doc["device_id"] = "ESP32_001"; // Identificador único do dispositivo
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  Serial.println("Enviando dados para API:");
  Serial.println(jsonString);
  
  int httpResponseCode = http.POST(jsonString);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("Resposta da API (código ");
    Serial.print(httpResponseCode);
    Serial.println("):");
    Serial.println(response);
  } else {
    Serial.print("Erro ao enviar dados. Código: ");
    Serial.println(httpResponseCode);
  }
  
  http.end();
}

// Função para calibrar o sensor de umidade do solo
void calibrarSensor() {
  Serial.println("=== Calibração do Sensor de Umidade ===");
  Serial.println("Coloque o sensor no solo seco e pressione qualquer tecla...");
  
  while (!Serial.available()) {
    delay(100);
  }
  Serial.read(); // Limpar buffer
  
  int valorSeco = analogRead(SOIL_MOISTURE_PIN);
  Serial.print("Valor para solo seco: ");
  Serial.println(valorSeco);
  
  Serial.println("Agora coloque o sensor no solo molhado e pressione qualquer tecla...");
  
  while (!Serial.available()) {
    delay(100);
  }
  Serial.read(); // Limpar buffer
  
  int valorMolhado = analogRead(SOIL_MOISTURE_PIN);
  Serial.print("Valor para solo molhado: ");
  Serial.println(valorMolhado);
  
  Serial.println("=== Valores de Calibração ===");
  Serial.print("VALOR_SECO = ");
  Serial.println(valorSeco);
  Serial.print("VALOR_MOLHADO = ");
  Serial.println(valorMolhado);
  Serial.println("Atualize estes valores no código se necessário.");
} 