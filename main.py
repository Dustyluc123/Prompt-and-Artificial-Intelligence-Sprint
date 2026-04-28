import os
from google import genai
from google.genai import types
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("ERRO: Chave GEMINI_API_KEY nao encontrada no arquivo .env")

# Inicializa o cliente com a nova biblioteca
client = genai.Client(api_key=api_key)

app = FastAPI(title="API Sindico Virtual - EV ChargeOps")
# Libera o CORS para o nosso Frontend poder conversar com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em producao, colocariamos o dominio real aqui
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MensagemUsuario(BaseModel):
    texto: str

def obter_resposta_sindico(mensagem: str) -> str:
    system_instruction = """
    Você é o 'Síndico Virtual ChargeOps', um assistente especialista em gestão de recarga de veículos elétricos (EV) para condomínios, utilizando tecnologia GoodWe.
    Sua missão é ajudar os moradores com dúvidas sobre agendamento, rateio de energia e problemas técnicos.
    
    REGRAS ABSOLUTAS:
    1. Responda APENAS sobre assuntos relacionados a condomínios, carregamento de veículos elétricos e energia. Se perguntarem sobre outros temas, recuse educadamente.
    2. INTELIGÊNCIA EMOCIONAL (Chain of Thought): Antes de gerar a resposta final, analise o tom da mensagem do usuário.
        - Se o usuário estiver BRAVO, FRUSTRADO ou com URGÊNCIA: Sua resposta deve começar pedindo desculpas, sendo extremamente empática, calma e focada em resolver o problema imediatamente.
        - Se o usuário estiver NEUTRO ou buscando DADOS: Seja direto, técnico, educado e eficiente.
        - Se o usuário estiver FELIZ ou SATISFEITO: Seja amigável e encorajador.
    
    Retorne a sua resposta diretamente, sem incluir a sua análise interna de sentimento no texto final.
    """
    
    try:
        # Nova estrutura de chamada do modelo
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=mensagem,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            )
        )
        return response.text
    except Exception as e:
        print(f"Erro ao chamar Gemini: {e}")
        return "Desculpe, estou enfrentando instabilidades no painel central. Tente novamente em instantes."

@app.post("/chat")
async def chat_com_sindico(mensagem: MensagemUsuario):
    if not mensagem.texto.strip():
        raise HTTPException(status_code=400, detail="A mensagem nao pode estar vazia.")
    
    resposta = obter_resposta_sindico(mensagem.texto)
    
    return {
        "status": "sucesso",
        "resposta_ia": resposta
    }

@app.get("/")
async def root():
    return {"mensagem": "API do Sindico Virtual esta online e atualizada!"}