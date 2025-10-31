# check_models.py
import google.generativeai as genai

# --- IMPORTANTE: COLOQUE SUA CHAVE AQUI DENTRO DAS ASPAS ---
# Lembre-se que esta chave é sensível. Não compartilhe o arquivo com ela.
GEMINI_API_KEY = "AIzaSyDqjglh684zfWzECkGc_fmQqe4UO17hhgo" 

try:
    genai.configure(api_key=GEMINI_API_KEY)

    print("--- Verificando modelos disponíveis para a sua chave API... ---")
    
    found_models = False
    for m in genai.list_models():
      # Vamos checar se o método de geração de conteúdo é suportado
      if 'generateContent' in m.supported_generation_methods:
        print(f"Modelo encontrado: {m.name}")
        found_models = True

    if not found_models:
        print("\nNenhum modelo compatível com 'generateContent' foi encontrado para esta chave.")
        print("Verifique se a API 'Generative Language' está ativada no seu projeto Google Cloud.")

except Exception as e:
    print(f"\nOcorreu um erro ao tentar conectar à API do Google: {e}")
    print("\nPossíveis causas:")
    print("- A chave de API está incorreta ou inválida.")
    print("- A API 'Generative Language' (ou a API de Vertex AI) não está ativada no seu projeto Google Cloud.")
    print("- Problemas de conexão com a internet.")