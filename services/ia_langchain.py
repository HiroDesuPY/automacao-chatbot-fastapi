from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from config import PINECONEAPI
import os


async def processar_relatorio_e_salvar(dados_json):
    llm = OllamaLLM(model="llama3", base_url="http://host.docker.internal:11434")


    texto_contexto = '\n'.join(str(item) for item in dados_json)

    relatorio = llm.invoke(f"Faça um relatorio completo sobre os dados fornecidos, forneça o ano, o mês o dia. Faça um relatorio extremamente detalhado. O relatório deve ser detalhado e preciso. Os dados estão disponíveis em: {texto_contexto}")


    #Chunking do relatório


    from langchain_text_splitters import RecursiveCharacterTextSplitter

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = [Document(page_content=relatorio, metadata={'origen': 'relatorio_csv'})]


        chunk = splitter.create_documents([relatorio], metadatas=[{'origen': 'relatorio_csv'}])

        vector_store.add_documents(chunk) #salvando os chunks no Pinecone

        try:

            #embeddings

            embeddings = OllamaEmbeddings(model="embeddinggemma", base_url="http://host.docker.internal:11434")

            #guardando no Pinecone
            os.environ["PINECONE_API_KEY"] = PINECONEAPI

            vector_store = PineconeVectorStore(
                embedding=embeddings,
                index_name="embeddinggemma-fastapi"
            )
            vector_store.add_documents(chunk) #salvando os chunks no Pinecone



        except Exception as e:
            print(f"Erro ao criar embeddings ou salvar no Pinecone: {e}")
            return {"message": f"Erro ao criar embeddings ou salvar no Pinecone: {e}"}
    
    


    except Exception as e:
        print(f"Erro ao dividir o relatório em chunks: {e}")
        return {"message": f"Erro ao dividir o relatório em chunks: {e}"}

    return {"message": "Relatório processado e salvo com sucesso!"}