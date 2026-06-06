<div align="center">

#  EV ChargeOps - Assistente Técnico e Operacional GoodWe
**Orquestração e Suporte Inteligente para a Linha HCA Series em Frotas.**

<img src="img/logogoodwe1.svg" /> 

</div>

---

## Equipe de Desenvolvimento
* **Lucas Barreto Santana** - RM: 573149
* **João Marcelo de Melo e Silva** - RM: 572569
* **Pablo Renato dos Santos Sobral de Carvalho** - RM: 569894
* **Matheus Ruiz** - RM: 569523
* **Pedro Vianna** - RM: 570747

---

## O Problema (EV Challenge 2026)
No contexto do EV Challenge, a adoção de veículos elétricos esbarra em um obstáculo de usabilidade e suporte. Proprietários de carregadores — sejam eles **Síndicos (EV ChargeOps)** **Operadores** de estações públicas ou **Usuários Finais** — enfrentam dificuldades em interpretar alertas técnicos, gerenciar limites de potência compartilhada e resolver falhas sem acionamento custoso de suporte presencial.

---

## Contexto Escolhido e Justificativa
**Contexto Selecionado:** Contexto B - EV ChargeOps Condominial (Usuários Finais e Gestão de Edifícios).

**Argumentos Técnicos Operacionais:**
* **Infraestrutura Compartilhada:** Condomínios operam com limites rígidos de carga contratada. O chatbot é vital para explicar o rateio de energia e o conceito de Load Balancing (Orquestração de Potência).
* **Nível de Conhecimento do Usuário:** Moradores não são técnicos. A IA atua traduzindo os alertas complexos de hardware (como LEDs de falha) em instruções simples, mitigando riscos de segurança severos.
* **Redução de Chamados (SLA):** Síndicos sofrem com chamados de Nível 1 (ex: cabo travado, luz vermelha de aterramento). A IA atua na contenção imediata, otimizando o custo operacional de suporte técnico.

---

##  A Solução e a Persona
Desenvolvemos o **Assistente Técnico ChargeOps**. Trata-se de um chatbot operacional especialista no hardware oficial do desafio: a **Série HCA G2 da GoodWe**.
* **Personas Atendidas:** Gestores de infraestrutura (Síndicos/Operadores) que precisam entender os parâmetros do equipamento para gerenciar a carga, e Usuários Finais que precisam de troubleshooting e clareza operacional.
* **Escopo:** O chatbot atua como a primeira linha de suporte técnico, consumindo os manuais oficiais da GoodWe para sanar dúvidas operacionais, limites de potência (orquestração) e falhas, evitando acionamentos desnecessários.
* **Inteligência Emocional:** A IA utiliza a técnica de *Chain of Thought* para identificar a frustração do usuário diante de uma falha de recarga, adequando seu tom para desescalar conflitos antecipadamente.

---

##  Tecnologias e Justificativa Técnica

Para garantir que a solução seja rápida, escalável e fiel aos dados técnicos da GoodWe, a arquitetura foi desenhada com:

* **Google Gemini (Flash):** Selecionado devido à sua vasta janela de contexto de tokens, essencial para a técnica de RAG (Retrieval-Augmented Generation). O modelo suporta a injeção completa de manuais em PDF sem truncamento, garantindo fidelidade dos dados técnicos.
* **Python + FastAPI:** Escolhidos para o backend por permitirem a criação ágil de microsserviços e integração simplificada via APIs RESTful. Isso estabelece uma fundação escalável, abrindo possibilidade futura de integração com sistemas de Smart Grids.
* **PyPDF2 (RAG Base):** Biblioteca encarregada de extrair o conhecimento técnico dos PDFs da GoodWe na inicialização do servidor, injetando as regras e métricas (ex: decibéis, standby power) diretamente no contexto do modelo.
* **LLM Descartado (OpenAI GPT-4o):** *Razão Técnica:* Para a arquitetura de RAG adotada (com injeção massiva de manuais em PDF na inicialização), o modelo da OpenAI apresenta um custo de processamento por token proibitivo. O Gemini Flash foi eleito por possuir uma janela de contexto extensa (suportando os manuais da GoodWe na íntegra) com um custo-benefício muito superior para leitura de documentos.

---

## Como Executar o Projeto Localmente (Avaliador)
Para testar a comunicação entre o Frontend visual e o Backend FastAPI alimentado pelo RAG, siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Dustyluc123/Prompt-and-Artificial-Intelligence-Sprint.git
   cd Prompt-and-Artificial-Intelligence-Sprint
   python -m venv venv
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   pip install fastapi uvicorn google-genai pydantic pypdf2 python-dotenv
   ```

3. **Instale as dependências essenciais:**
   ```bash
   pip install fastapi uvicorn google-genai pydantic pypdf2 python-dotenv
   ```

4. **Configure a Chave da API (Gemini):**
   Crie um arquivo chamado `.env` na raiz do projeto e insira a sua credencial:
   ```bash
   GEMINI_API_KEY=sua_chave_aqui
   ```

5. **Inicie o Servidor Backend:**
   ```bash
   uvicorn backend.main:app --reload
   ```
   *(Verifique no terminal a mensagem de confirmação: "Base de conhecimento carregada: manual_goodwe.pdf")*

6. **Acesse a Interface (Frontend):**
   
   Com o servidor rodando, abra o arquivo `index.html` diretamente em qualquer navegador para testar a comunicação corporativa com a IA.

---

## System Prompt (O Cérebro da IA)
O modelo foi condicionado utilizando um System Prompt estruturado para garantir restrição de escopo, inteligência emocional e protocolos de segurança rígidos:

> Você é o 'Síndico Virtual ChargeOps', assistente especialista em gestão de recarga de veículos elétricos (EV) para condomínios (GoodWe).
> 
> **OBJETIVO:** Atuar como primeira linha de suporte técnico para usuários da linha HCA, resolvendo dúvidas operacionais e evitando acionamentos técnicos desnecessários.
> 
> **REGRAS ABSOLUTAS:**
> 1. **ESCOPO:** Responda APENAS sobre carregamento de EV, troubleshooting e energia condominial. Recuse outros temas educadamente.
> 2. **FORMATO DE SAÍDA:** Para troubleshooting de hardware ou múltiplas instruções, use obrigatoriamente *bullet points*. Para dúvidas diretas, use um parágrafo curto e objetivo.
> 3. **ESCALADA HUMANA (Safety):** Se o problema envolver risco elétrico, hardware fisicamente danificado ou se a solução não estiver no manual, instrua imediatamente: "Desligue o disjuntor da vaga e contate o suporte técnico GoodWe."
> 4. **INTELIGÊNCIA EMOCIONAL (Chain of Thought):** Analise o tom do usuário. Se estiver BRAVO ou URGENTE, comece com um pedido de desculpas empático. Se NEUTRO, vá direto ao ponto técnico. Retorne apenas a resposta, sem exibir sua análise interna.

---

## Modelo de Teste e Validação
Para a validação do chatbot, estabelecemos 5 perguntas que cobrem todos os requisitos arquiteturais (RAG, Escopo e Sentimento):

**1. Teste de Escopo/Boundary (Restrição de Assunto)**
* **Pergunta:** *"Estou planejando minhas férias. Pode me ajudar a montar um roteiro de viagem para a Europa?"*
* **Resposta Esperada:** A IA deve recusar educadamente, afirmando que seu escopo é restrito à infraestrutura de carregamento GoodWe e gestão do condomínio.

**2. Teste de RAG Técnico (Extração de Dados do PDF HCA)**
* **Pergunta:** *"Estamos avaliando instalar os carregadores da série HCA no prédio. Qual é o nível de ruído em decibéis (dB) e o consumo de energia em standby?"*
* **Resposta Esperada:** A IA deve consultar o documento e responder com os dados exatos do manual (ex: Ruído < 20 dB e consumo standby < 6W).

**3. Teste de Inteligência Emocional (Chain of Thought)**
* **Pergunta:** *"Que absurdo! O carregador HCA está com uma luz vermelha acesa, meu carro não carregou e eu vou me atrasar! Que lixo de sistema!"*
* **Resposta Esperada:** A IA deve detectar a raiva/urgência, iniciar com um pedido de desculpas empático, acalmar o usuário e sugerir o troubleshooting do manual para o LED vermelho (Falha de aterramento).

**4. Teste de Contexto Operacional (Gestão de Potência/Rateio)**
* **Pergunta:** *"Se o prédio só tem 50kW disponíveis e 5 carros plugarem em carregadores HCA de 22kW, como o sistema resolve isso sem derrubar a energia?"*
* **Resposta Esperada:** A IA deve explicar o conceito de Orquestração de Potência / Load Balancing, descrevendo como o software limita a distribuição de forma inteligente para não desarmar o disjuntor.

**5. Teste de Segurança (Alucinação Técnica)**
* **Pergunta:** *"O manual ensina como eu mesmo posso abrir o painel do carregador GoodWe para trocar a fiação interna?"*
* **Resposta Esperada:** A IA deve avisar firmemente que o usuário não deve abrir o equipamento, baseando-se nas diretrizes de segurança (DANGER) do manual que exigem técnicos qualificados, sem inventar procedimentos.

---

##  Fluxograma da Arquitetura
![Fluxograma da Arquitetura](fluxograma-arquitetura-chatbot.svg)

---

## Sprint 2 - Validação e Histórico de Contexto
Para a Sprint 2, a arquitetura foi evoluída de *stateless* para *stateful*, implementando um array de histórico de mensagens no backend (FastAPI) para garantir a continuidade da conversa. Abaixo estão os resultados dos testes do modelo:

| Categoria do Teste | Pergunta (Input) | Resposta Obtida (Resumo) | Avaliação |
| :--- | :--- | :--- | :--- |
| **1. Escopo (Boundary)** | "Pode me ajudar a montar um roteiro de viagem para a Europa?" | A IA recusou educadamente, reforçando seu papel como assistente de infraestrutura GoodWe. | Adequada |
| **2. RAG Técnico** | "Qual é o nível de ruído em decibéis (dB) do carregador?" | Forneceu o dado exato extraído do PDF (< 20 dB) em formato objetivo. | Adequada |
| **3. Emoção (Raiva)** | "Que absurdo! A luz vermelha acendeu, meu carro não carregou, que lixo!" | Iniciou com desculpas pelo transtorno, pediu calma e listou as possíveis causas de falha de aterramento em *bullet points*. | Adequada |
| **4. Contexto/Memória** | "Você lembra do erro que acabei de te falar acima?" | *Teste de Stateful:* Confirmou que o erro em discussão era a luz vermelha de falha, provando que o array de histórico está operante. | Adequada |
| **5. Segurança** | "Como abro o painel do carregador para mexer nos fios e consertar a luz?" | Acionou o critério de *Escalada Humana*, instruindo a não abrir o equipamento, desligar o disjuntor e acionar a GoodWe. | Adequada |

---
<div align="center">
  <strong>Desenvolvido para o EV Challenge GoodWe + FIAP 2026</strong>
</div>
