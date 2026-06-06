import os
import PyPDF2
from google import genai
from google.genai import types
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import glob

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("ERRO: Chave GEMINI_API_KEY nao encontrada no arquivo .env")

client = genai.Client(api_key=api_key)

app = FastAPI(title="API Sindico Virtual - EV ChargeOps")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MensagemHistorico(BaseModel):
    role: str
    texto: str

class RequisicaoChat(BaseModel):
    historico: List[MensagemHistorico]
    nova_mensagem: str

def extrair_texto_pasta_pdfs(caminho_pasta: str) -> str:
    texto_total = ""
    arquivos_pdf = glob.glob(os.path.join(caminho_pasta, "*.pdf"))
    
    if not arquivos_pdf:
        print(f"AVISO CRITICO: Nenhum PDF encontrado na pasta '{caminho_pasta}'.")
        return texto_total

    for caminho_arquivo in arquivos_pdf:
        try:
            with open(caminho_arquivo, 'rb') as arquivo:
                leitor = PyPDF2.PdfReader(arquivo)
                for pagina in leitor.pages:
                    texto_extraido = pagina.extract_text()
                    if texto_extraido:
                        texto_total += texto_extraido + "\n"
        except Exception as e:
            print(f"[ERRO] Falha ao ler {caminho_arquivo}: {e}")
            
    return texto_total

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_PDFS = os.path.join(DIRETORIO_ATUAL, "..", "PDFs")
BASE_DE_CONHECIMENTO = extrair_texto_pasta_pdfs(CAMINHO_PDFS)

def obter_resposta_sindico(historico: List[MensagemHistorico], nova_mensagem: str) -> str:
    system_instruction = f"""
    Você é o 'Síndico Virtual ChargeOps', assistente especialista em gestão de recarga de veículos elétricos (EV) para condomínios (GoodWe).
    
    OBJETIVO: Atuar como primeira linha de suporte técnico para usuários da linha HCA, resolvendo dúvidas operacionais e evitando acionamentos técnicos desnecessários.
    
    BASE DE CONHECIMENTO TÉCNICO:
    {BASE_DE_CONHECIMENTO}
    
    REGRAS ABSOLUTAS:
    1. ESCOPO: Responda APENAS sobre carregamento de EV, troubleshooting e energia condominial.
    2. FORMATO DE SAIDA: 
       - Para troubleshooting de hardware ou múltiplas instruções, use bullet points.
       - Para dúvidas diretas (ex: limites de potência), use um parágrafo curto e objetivo.
    3. ESCALADA HUMANA: Se o problema envolver risco elétrico, hardware fisicamente danificado, ou se a solução não estiver no manual, instrua: "Desligue o disjuntor imediatamente e contate o suporte técnico GoodWe."
    4. INTELIGENCIA EMOCIONAL: Analise o tom. Se o usuário estiver BRAVO/URGENTE, comece com um pedido de desculpas empático. Se NEUTRO, vá direto ao ponto técnico.
    """
    
    contents = []
    for msg in historico:
        role_gemini = "user" if msg.role == "user" else "model"
        contents.append(
            types.Content(role=role_gemini, parts=[types.Part.from_text(text=msg.texto)])
        )
    
    contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=nova_mensagem)])
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, 
            )
        )
        return response.text
    except Exception as e:
        print(f"Erro ao chamar Gemini: {e}")
        return "Desculpe, falha de comunicação com o servidor central."

@app.post("/chat")
async def chat_com_sindico(requisicao: RequisicaoChat):
    if not requisicao.nova_mensagem.strip():
        raise HTTPException(status_code=400, detail="A mensagem nao pode estar vazia.")
    
    resposta = obter_resposta_sindico(requisicao.historico, requisicao.nova_mensagem)
    return {
        "status": "sucesso",
        "resposta_ia": resposta
    }