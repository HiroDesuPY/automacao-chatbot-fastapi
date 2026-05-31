from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from config import PINECONEAPI
from langchain_community.chat_message_histories import RedisChatMessageHistory

import os



class IA:

    def __init__(self, sessions_id: str):
        self.llm = OllamaLLM(model="llama3", base_url="http://host.docker.internal:11434")
        
        self.embeddings = OllamaEmbeddings(model="embeddinggemma", base_url="http://host.docker.internal:11434")
        
        os.environ["PINECONE_API_KEY"] = PINECONEAPI
        
        
        
        self.vector_store = PineconeVectorStore(
            embedding=self.embeddings,
            index_name="embeddinggemma-fastapi"
        )

        self.history = RedisChatMessageHistory(
            session_id=str(sessions_id),
            url="redis://redis:6379"
        )



    async def prompt(self, pergunta: str):

        self.pergunta = pergunta


        #retriver
        retriver = self.vector_store.as_retriever(search_kwargs={"k": 5})
        docs = retriver.invoke(pergunta)

        self.contexto = '\n\n'.join([d.page_content for d in docs])

        #debug

        print(f"Contexto recuperado para a pergunta '{pergunta}': {self.contexto}")


    async def answer(self):


        if not self.contexto or self.contexto.strip() == "":
            return "Desculpe, não encontrei informações relevantes para responder à sua pergunta."


        mensagens = self.history.messages[-6:]  # Pegando as últimas 6 mensagens do histórico

        historico_formatado = '\n'.join([f'{msg.type.upper()}: {msg.content}' for msg in mensagens])


        prompt = f"""
        Você é um assistente especializado em relatórios.
        Use o CONTEXTO abaixo para responder à PERGUNTA do usuário.
        Se a resposta não estiver no contexto, diga que não encontrou a informação.
        

        HISOTRICO DE MENSAGENS:
        {historico_formatado}


        CONTEXTO:
        {self.contexto}
        
        PERGUNTA:
        {self.pergunta}
        """
        
        resposta_final = self.llm.invoke(prompt)

        self.history.add_user_message(self.pergunta)
        self.history.add_ai_message(resposta_final)

        return resposta_final

     
     
     
     
     
     
     
     
     
    # 1. Entre no container do redis
    #docker exec -it redis redis-cli

    # 2. Veja todas as chaves (o histórico é salvo com um prefixo do LangChain)
   # KEYS *

    # 3. Leia o conteúdo de uma sessão específica (substitua pelo ID que aparecer no passo anterior)
   # LRANGE "message_store:chat_123456" 0 -1