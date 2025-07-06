#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Rápido - Simulador ESP32
Script simples para testar a API rapidamente
"""

import requests
import json
import time
import random
from datetime import datetime

def testar_api():
    """Teste rápido da API"""
    api_url = "http://localhost:3000/api"
    device_id = "ESP32_002"
    
    print("🚀 TESTE RÁPIDO - SIMULADOR ESP32")
    print("=" * 50)
    print(f"API: {api_url}")
    print(f"Device: {device_id}")
    print()
    
    # Verificar se API está rodando
    try:
        health = requests.get("http://localhost:3000/health", timeout=5)
        if health.status_code == 200:
            print("✅ API está funcionando")
        else:
            print("❌ API não está respondendo corretamente")
            return
    except:
        print("❌ Não foi possível conectar à API")
        print("   Execute: cd api && npm run dev")
        return
    
    # 1. Enviar dados dos sensores
    print("\n📊 Enviando dados dos sensores...")
    dados = {
        "umidade_solo": random.randint(30, 80),
        "timestamp": int(time.time() * 1000),
        "device_id": device_id
    }
    
    try:
        response = requests.post(f"{api_url}/sensors", json=dados)
        if response.status_code == 201:
            print(f"✅ Dados enviados: {dados['umidade_solo']}%")
        else:
            print(f"❌ Erro ao enviar dados: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 2. Verificar status da bomba
    print("\n🚰 Verificando status da bomba...")
    try:
        response = requests.get(f"{api_url}/pump/{device_id}/status")
        if response.status_code == 200:
            status = response.json()['data']
            pump_status = "🟢 ATIVA" if status['is_active'] else "🔴 INATIVA"
            print(f"✅ Status da bomba: {pump_status}")
            print(f"   Total de ativações: {status['total_activations']}")
        else:
            print(f"❌ Erro ao verificar status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 3. Ativar bomba
    print("\n🚰 Ativando bomba...")
    try:
        response = requests.post(
            f"{api_url}/pump/{device_id}/control",
            json={
                "action": "activate",
                "reason": "Teste rápido via script",
                "triggered_by": "manual"
            }
        )
        if response.status_code == 200:
            print("✅ Bomba ativada com sucesso")
        else:
            print(f"❌ Erro ao ativar bomba: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Aguardar 3 segundos
    print("\n⏳ Aguardando 3 segundos...")
    time.sleep(3)
    
    # 4. Verificar status novamente
    print("\n🚰 Verificando status após ativação...")
    try:
        response = requests.get(f"{api_url}/pump/{device_id}/status")
        if response.status_code == 200:
            status = response.json()['data']
            pump_status = "🟢 ATIVA" if status['is_active'] else "🔴 INATIVA"
            print(f"✅ Status da bomba: {pump_status}")
            if status['is_active']:
                print(f"   Duração atual: {status['duration_seconds']}s")
        else:
            print(f"❌ Erro ao verificar status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 5. Desativar bomba
    print("\n🚰 Desativando bomba...")
    try:
        response = requests.post(
            f"{api_url}/pump/{device_id}/control",
            json={
                "action": "deactivate",
                "reason": "Teste finalizado",
                "triggered_by": "manual"
            }
        )
        if response.status_code == 200:
            print("✅ Bomba desativada com sucesso")
        else:
            print(f"❌ Erro ao desativar bomba: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 6. Buscar estatísticas
    print("\n📈 Buscando estatísticas...")
    try:
        response = requests.get(f"{api_url}/pump/{device_id}/stats")
        if response.status_code == 200:
            stats = response.json()['data']['stats']
            print(f"✅ Estatísticas da bomba:")
            print(f"   Total de ativações: {stats['total_activations']}")
            print(f"   Duração total: {stats['total_duration_seconds']}s")
            print(f"   Duração média: {stats['avg_duration_seconds']}s")
        else:
            print(f"❌ Erro ao buscar estatísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 50)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 50)

if __name__ == "__main__":
    testar_api() 