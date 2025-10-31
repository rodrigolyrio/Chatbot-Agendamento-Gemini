# check_models.py
import google.generativeai as genai
import os

# --- IMPORTANTE: CARREGUE SUA CHAVE DE UMA VARIÁVEL DE AMBIENTE PARA TESTE ---

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("\nERRO: A variável de ambiente 'GEMINI_API_KEY' não foi encontrada.")
    print("Por favor, configure a variável de ambiente com sua chave da API do Google Gemini.")
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)

        print("--- Verificando modelos disponíveis para a sua chave API... ---")
        
        found_models = False
        for m in genai.list_models():
          if 'generateContent' in m.supported_generation_methods:
            print(f"Modelo encontrado: {m.name}")
            found_models = True

        if not found_models:
            print("\nNenhum modelo compatível com 'generateContent' foi encontrado para esta chave.")
            print("Verifique se a API 'Generative Language' está ativada no seu projeto Google Cloud.")

    except Exception as e:
        print(f"\nOcorreu um erro ao tentar conectar à API do Google: {e}")
        print("\nPossíveis causas:")
        print("- A chave de API (carregada da variável de ambiente) está incorreta ou inválida.")
        print("- A API 'Generative Language' (ou a API de Vertex AI) não está ativada no seu projeto Google Cloud.")
        print("- Problemas de conexão com a internet.")
