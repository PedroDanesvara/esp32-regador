#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a API do sistema de monitoramento ESP32
Simula dados de umidade do solo
"""

import requests
import json
import time
import random
from datetime import datetime

class APITester:
    def __init__(self, api_url):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'ESP32-Tester/1.0'
        })
    
    def gerar_dados_simulados(self):
        """Gera dados simulados do ESP32"""
        return {
            "umidade_solo": random.randint(20, 90),
            "timestamp": int(time.time() * 1000),
            "device_id": "ESP32_001"
        }
    
    def enviar_dados(self, dados):
        """Envia dados para a API"""
        try:
            response = self.session.post(self.api_url, json=dados)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar dados: {e}")
            return None
    
    def testar_api(self, num_requisicoes=5, intervalo=5):
        """Testa a API com múltiplas requisições"""
        print(f"Iniciando teste da API: {self.api_url}")
        print(f"Número de requisições: {num_requisicoes}")
        print(f"Intervalo entre requisições: {intervalo} segundos")
        print("-" * 50)
        
        sucessos = 0
        falhas = 0
        
        for i in range(num_requisicoes):
            dados = self.gerar_dados_simulados()
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"\n[{timestamp}] Requisição {i+1}/{num_requisicoes}")
            print(f"Dados: {json.dumps(dados, indent=2)}")
            
            response = self.enviar_dados(dados)
            
            if response is not None:
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    print("✅ Sucesso!")
                    sucessos += 1
                    try:
                        resposta_json = response.json()
                        print(f"Resposta: {json.dumps(resposta_json, indent=2)}")
                    except:
                        print(f"Resposta: {response.text}")
                else:
                    print(f"❌ Falha - Status: {response.status_code}")
                    print(f"Resposta: {response.text}")
                    falhas += 1
            else:
                print("❌ Falha - Sem resposta")
                falhas += 1
            
            if i < num_requisicoes - 1:
                print(f"Aguardando {intervalo} segundos...")
                time.sleep(intervalo)
        
        print("\n" + "=" * 50)
        print("RESULTADO DO TESTE")
        print("=" * 50)
        print(f"Total de requisições: {num_requisicoes}")
        print(f"Sucessos: {sucessos}")
        print(f"Falhas: {falhas}")
        print(f"Taxa de sucesso: {(sucessos/num_requisicoes)*100:.1f}%")

def testar_apis_gratuitas():
    """Testa APIs gratuitas para demonstração"""
    print("=== TESTANDO APIs GRATUITAS ===")
    
    # Teste com JSONPlaceholder
    print("\n1. Testando JSONPlaceholder...")
    tester1 = APITester("https://jsonplaceholder.typicode.com/posts")
    tester1.testar_api(3, 2)
    
    # Teste com httpbin
    print("\n2. Testando httpbin...")
    tester2 = APITester("https://httpbin.org/post")
    tester2.testar_api(3, 2)

def main():
    print("🧪 TESTADOR DE API - ESP32 MONITORAMENTO")
    print("=" * 50)
    
    # Configurações
    api_url = "https://webhook.site/a150e4c3-67ff-488e-8cad-c18219ff498a"
    
    if not api_url:
        testar_apis_gratuitas()
        return
    
    # Testar API personalizada
    tester = APITester(api_url)
    
    try:
        num_requisicoes = int(input("Número de requisições (padrão: 5): ") or "5")
        intervalo = int(input("Intervalo entre requisições em segundos (padrão: 5): ") or "5")
    except ValueError:
        num_requisicoes = 5
        intervalo = 5
    
    tester.testar_api(num_requisicoes, intervalo)

if __name__ == "__main__":
    main() 