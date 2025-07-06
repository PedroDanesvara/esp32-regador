#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar conectividade com a API
"""

import requests
import json

def testar_api(api_url):
    """Testa diferentes endpoints da API"""
    print(f"🔍 Testando API: {api_url}")
    print("=" * 60)
    
    # Configurar sessão
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'API-Tester/1.0'
    })
    
    # Lista de endpoints para testar
    endpoints = [
        ("GET", f"{api_url}/sensors", "Listar sensores"),
        ("GET", f"{api_url}/devices", "Listar devices"),
        ("GET", f"{api_url}/pump/ESP32_001/status", "Status da bomba"),
        ("POST", f"{api_url}/sensors", "Enviar dados de sensor (teste)"),
    ]
    
    for method, endpoint, description in endpoints:
        print(f"\n📡 {description}")
        print(f"   {method} {endpoint}")
        
        response = None
        try:
            if method == "GET":
                response = session.get(endpoint, timeout=10)
            elif method == "POST":
                # Dados de teste para POST
                test_data = {
                    "temperatura": 25.5,
                    "umidade_solo": 65,
                    "timestamp": 1234567890,
                    "device_id": "ESP32_001"
                }
                response = session.post(endpoint, json=test_data, timeout=10)
            
            if response:
                print(f"   Status: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    print("   ✅ Sucesso")
                    try:
                        data = response.json()
                        if isinstance(data, dict) and 'data' in data:
                            print(f"   📊 Dados recebidos: {len(data['data'])} registros")
                        else:
                            print(f"   📊 Resposta: {type(data)}")
                    except:
                        print("   📊 Resposta não é JSON válido")
                elif response.status_code == 404:
                    print("   ⚠️  Endpoint não encontrado (404)")
                elif response.status_code == 500:
                    print("   ❌ Erro interno do servidor (500)")
                else:
                    print(f"   ⚠️  Status inesperado: {response.status_code}")
                
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ Erro de conexão: {e}")
        except requests.exceptions.Timeout as e:
            print(f"   ❌ Timeout: {e}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro: {e}")
        except Exception as e:
            print(f"   ❌ Erro inesperado: {e}")

def main():
    print("🧪 TESTE DE CONECTIVIDADE - API REGADOR")
    print("=" * 60)
    
    # URL da API
    api_url = input("URL da API (padrão: https://api-regador.vercel.app/api): ").strip()
    if not api_url:
        api_url = "https://api-regador.vercel.app/api"
    
    print(f"\n🎯 Testando: {api_url}")
    
    # Testar API
    testar_api(api_url)
    
    print("\n" + "=" * 60)
    print("🏁 TESTE CONCLUÍDO")
    print("=" * 60)

if __name__ == "__main__":
    main() 