#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador ESP32 para testar o sistema de monitoramento
Envia dados de sensores e simula controle da bomba
"""

import requests
import json
import time
import random
from datetime import datetime
import threading

class ESP32Simulator:
    def __init__(self, api_base_url="http://localhost:3000/api"):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'ESP32-Simulator/1.0'
        })
        
        # Configurações do simulador
        self.device_id = "ESP32_002"  # Usar um device existente
        self.is_running = False
        self.pump_active = False
        self.pump_start_time = None
        
        # Valores base para simulação
        self.base_temperature = 25.0
        self.base_humidity = 60
        self.temperature_variation = 5.0
        self.humidity_variation = 20
        
    def gerar_dados_sensores(self):
        """Gera dados simulados de temperatura e umidade"""
        # Simular variação gradual
        temp_variation = random.uniform(-self.temperature_variation, self.temperature_variation)
        humidity_variation = random.uniform(-self.humidity_variation, self.humidity_variation)
        
        temperatura = round(self.base_temperature + temp_variation, 1)
        umidade_solo = max(0, min(100, int(self.base_humidity + humidity_variation)))
        
        return {
            "temperatura": temperatura,
            "umidade_solo": umidade_solo,
            "timestamp": int(time.time() * 1000),
            "device_id": self.device_id
        }
    
    def enviar_dados_sensores(self, dados):
        """Envia dados dos sensores para a API"""
        try:
            response = self.session.post(f"{self.api_base_url}/sensors", json=dados)
            return response
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Erro de conexão ao enviar dados dos sensores: {e}")
            print(f"   Verifique se a API está online: {self.api_base_url}")
            return None
        except requests.exceptions.Timeout as e:
            print(f"❌ Timeout ao enviar dados dos sensores: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao enviar dados dos sensores: {e}")
            return None
    
    def controlar_bomba_automatico(self):
        """Controle automático da bomba baseado na umidade do solo"""
        try:
            # Buscar dados mais recentes
            response = self.session.get(f"{self.api_base_url}/sensors", params={
                'device_id': self.device_id,
                'limit': 1,
                'order': 'desc'
            })
            
            if response.status_code == 200:
                data = response.json()
                if data['data'] and len(data['data']) > 0:
                    umidade = data['data'][0]['umidade_solo']
                    
                    # Lógica de controle automático
                    if umidade < 30 and not self.pump_active:
                        # Ativar bomba se umidade baixa
                        self.ativar_bomba("Umidade do solo baixa (< 30%)", "automatic")
                    elif umidade > 70 and self.pump_active:
                        # Desativar bomba se umidade alta
                        self.desativar_bomba("Umidade do solo adequada (> 70%)", "automatic")
                        
        except Exception as e:
            print(f"❌ Erro no controle automático: {e}")
    
    def ativar_bomba(self, reason="Controle manual", triggered_by="manual"):
        """Ativa a bomba via API"""
        try:
            response = self.session.post(
                f"{self.api_base_url}/pump/{self.device_id}/control",
                json={
                    "action": "activate",
                    "reason": reason,
                    "triggered_by": triggered_by
                }
            )
            
            if response.status_code == 200:
                self.pump_active = True
                self.pump_start_time = time.time()
                print(f"✅ Bomba ativada: {reason}")
                return True
            else:
                print(f"❌ Erro ao ativar bomba: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao ativar bomba: {e}")
            return False
    
    def desativar_bomba(self, reason="Controle manual", triggered_by="manual"):
        """Desativa a bomba via API"""
        try:
            response = self.session.post(
                f"{self.api_base_url}/pump/{self.device_id}/control",
                json={
                    "action": "deactivate",
                    "reason": reason,
                    "triggered_by": triggered_by
                }
            )
            
            if response.status_code == 200:
                self.pump_active = False
                duration = time.time() - self.pump_start_time if self.pump_start_time else 0
                print(f"✅ Bomba desativada: {reason} (duração: {duration:.1f}s)")
                return True
            else:
                print(f"❌ Erro ao desativar bomba: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao desativar bomba: {e}")
            return False
    
    def verificar_status_bomba(self):
        """Verifica o status atual da bomba"""
        try:
            response = self.session.get(f"{self.api_base_url}/pump/{self.device_id}/status")
            if response.status_code == 200:
                data = response.json()['data']
                self.pump_active = data['is_active']
                return data
            return None
        except Exception as e:
            print(f"❌ Erro ao verificar status da bomba: {e}")
            return None
    
    def simular_ciclo_completo(self, duracao_minutos=10):
        """Simula um ciclo completo de monitoramento"""
        print(f"🚀 Iniciando simulação ESP32 - Device: {self.device_id}")
        print(f"⏱️  Duração: {duracao_minutos} minutos")
        print(f"🌐 API: {self.api_base_url}")
        print("-" * 60)
        
        self.is_running = True
        start_time = time.time()
        ciclo = 0
        
        while self.is_running and (time.time() - start_time) < (duracao_minutos * 60):
            ciclo += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"\n🔄 Ciclo {ciclo} - {timestamp}")
            
            # 1. Enviar dados dos sensores
            dados = self.gerar_dados_sensores()
            print(f"📊 Sensores: {dados['temperatura']}°C, {dados['umidade_solo']}% umidade")
            
            response = self.enviar_dados_sensores(dados)
            if response and response.status_code == 201:
                print("✅ Dados enviados com sucesso")
            else:
                print("❌ Falha ao enviar dados")
            
            # 2. Controle automático da bomba (a cada 3 ciclos)
            if ciclo % 3 == 0:
                print("🤖 Verificando controle automático da bomba...")
                self.controlar_bomba_automatico()
            
            # 3. Mostrar status atual
            status = self.verificar_status_bomba()
            if status:
                pump_status = "🟢 ATIVA" if status['is_active'] else "🔴 INATIVA"
                print(f"🚰 Bomba: {pump_status}")
                if status['is_active']:
                    print(f"   ⏱️  Duração atual: {status['duration_seconds']}s")
            
            # 4. Simular eventos aleatórios
            if random.random() < 0.1:  # 10% de chance
                if not self.pump_active:
                    self.ativar_bomba("Simulação - evento aleatório", "automatic")
                else:
                    self.desativar_bomba("Simulação - evento aleatório", "automatic")
            
            # Aguardar próximo ciclo
            if self.is_running:
                print("⏳ Aguardando 5 segundos...")
                time.sleep(5)
        
        print("\n" + "=" * 60)
        print("🏁 SIMULAÇÃO FINALIZADA")
        print("=" * 60)
        
        # Estatísticas finais
        if self.pump_active:
            self.desativar_bomba("Finalização da simulação", "automatic")
        
        # Buscar estatísticas finais
        try:
            stats_response = self.session.get(f"{self.api_base_url}/pump/{self.device_id}/stats")
            if stats_response.status_code == 200:
                stats = stats_response.json()['data']['stats']
                print(f"📈 Estatísticas da bomba:")
                print(f"   Total de ativações: {stats['total_activations']}")
                print(f"   Duração total: {stats['total_duration_seconds']}s")
                print(f"   Duração média: {stats['avg_duration_seconds']}s")
        except Exception as e:
            print(f"❌ Erro ao buscar estatísticas: {e}")
    
    def parar_simulacao(self):
        """Para a simulação"""
        self.is_running = False
        print("\n⏹️  Parando simulação...")

def main():
    print("🤖 SIMULADOR ESP32 - SISTEMA DE MONITORAMENTO")
    print("=" * 60)
    
    # Configurações
    api_url = input("URL da API (padrão: http://localhost:3000/api): ").strip()
    if not api_url:
        api_url = "http://localhost:3000/api"
    
    device_id = input("Device ID (padrão: ESP32_002): ").strip()
    if not device_id:
        device_id = "ESP32_002"
    
    try:
        duracao = int(input("Duração em minutos (padrão: 10): ") or "10")
    except ValueError:
        duracao = 10
    
    # Criar simulador
    simulator = ESP32Simulator(api_url)
    simulator.device_id = device_id
    
    print(f"\n🎯 Configuração:")
    print(f"   API: {api_url}")
    print(f"   Device: {device_id}")
    print(f"   Duração: {duracao} minutos")
    
    # Verificar se API está disponível
    print("🔍 Verificando conectividade com a API...")
    
    # Tentar diferentes endpoints para verificar conectividade
    endpoints_to_test = [
        f"{api_url}/sensors",  # Endpoint principal
        f"{api_url.replace('/api', '')}/health",  # Endpoint de saúde (se existir)
        f"{api_url.replace('/api', '')}/"  # Endpoint raiz
    ]
    
    api_available = False
    for endpoint in endpoints_to_test:
        try:
            print(f"   Testando: {endpoint}")
            response = requests.get(endpoint, timeout=10)
            if response.status_code in [200, 201, 404]:  # 404 também indica que a API está respondendo
                print(f"✅ API está respondendo (status: {response.status_code})")
                api_available = True
                break
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Falha: {e}")
            continue
    
    if not api_available:
        print("❌ Não foi possível conectar à API")
        print("   Verifique:")
        print("   - Se a URL está correta")
        print("   - Se a API está online no Vercel")
        print("   - Se há problemas de rede")
        print("   - Se o endpoint /api está correto")
        
        # Perguntar se quer continuar mesmo assim
        continuar = input("\nDeseja continuar mesmo assim? (s/N): ").strip().lower()
        if continuar not in ['s', 'sim', 'y', 'yes']:
            return
        else:
            print("⚠️  Continuando com verificação de conectividade desabilitada...")
    
    # Iniciar simulação
    try:
        simulator.simular_ciclo_completo(duracao)
    except KeyboardInterrupt:
        print("\n⏹️  Simulação interrompida pelo usuário")
        simulator.parar_simulacao()

if __name__ == "__main__":
    main() 