#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de variables de entorno
"""

import os
import sys
from dotenv import load_dotenv

def test_environment_config():
    """Prueba la configuración del entorno"""
    print("🔍 Verificando configuración de variables de entorno...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar API key
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        print("✅ GEMINI_API_KEY encontrada en variables de entorno")
        print(f"   Longitud: {len(api_key)} caracteres")
        print(f"   Comienza con: {api_key[:10]}...")
    else:
        print("❌ GEMINI_API_KEY no encontrada en variables de entorno")
    
    # Verificar archivo .env
    if os.path.exists(".env"):
        print("✅ Archivo .env encontrado")
    else:
        print("⚠️  Archivo .env no encontrado")
    
    # Verificar archivo secrets.toml
    if os.path.exists(".streamlit/secrets.toml"):
        print("✅ Archivo .streamlit/secrets.toml encontrado")
    else:
        print("⚠️  Archivo .streamlit/secrets.toml no encontrado")
    
    # Probar importación de analyzer
    try:
        from analyzer import get_api_key, configure_gemini
        print("✅ Módulo analyzer importado correctamente")
        
        # Probar función get_api_key
        test_api_key = get_api_key()
        if test_api_key:
            print("✅ Función get_api_key funciona correctamente")
        else:
            print("❌ Función get_api_key no retorna API key")
            
    except ImportError as e:
        print(f"❌ Error importando analyzer: {e}")
    except Exception as e:
        print(f"❌ Error en analyzer: {e}")
    
    print("\n📋 Resumen:")
    print(f"   - Variables de entorno: {'✅' if api_key else '❌'}")
    print(f"   - Archivo .env: {'✅' if os.path.exists('.env') else '❌'}")
    print(f"   - Archivo secrets.toml: {'✅' if os.path.exists('.streamlit/secrets.toml') else '❌'}")
    
    if not api_key:
        print("\n🚨 Para configurar:")
        print("   1. Copia env.example a .env")
        print("   2. Edita .env con tu API key real")
        print("   3. Para deploy, edita .streamlit/secrets.toml")

if __name__ == "__main__":
    test_environment_config() 