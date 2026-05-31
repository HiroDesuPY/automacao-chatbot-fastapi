from fastapi import FastAPI, UploadFile, File, APIRouter
import io
import pandas as pd
from services.ia_langchain import processar_relatorio_e_salvar


app = FastAPI()

upload_route = APIRouter(prefix="/upload", tags=["upload"])

#http://python-api:8000/upload/csv or http://localhost:8000/upload/csv

@upload_route.post("/csv")
async def upload_csv(
    file: UploadFile = File(...)
):
    contents = await file.read()
    print(f"Received file: {file.filename}")

    try:

        df = pd.read_csv(io.BytesIO(contents))

        df = df.drop_duplicates()
        df = df.fillna("Sem informações")

        #dados em dicionario => json

        dados_processados = df.to_dict(orient="records")

        #processar o relatório e salvar no Pinecone

        resultado = await processar_relatorio_e_salvar(dados_processados)


        
        return {
            "status": "success",
            "message": resultado
        }
    
    except Exception as e:
        print(f"Erro ao processar o arquivo CSV: {e}")
        return {
            "status": "error",
            "message": f"Erro ao processar o arquivo CSV: {e}"
        }