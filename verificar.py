import os
from google import genai
from dotenv import load_dotenv

# Carrega a chave do arquivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Inicia o cliente
client = genai.Client(api_key=api_key)

print("Modelos disponiveis para a sua API Key:\n")

# Pede ao Google a lista de modelos e imprime os nomes
for model in client.models.list():
    print(model.name)