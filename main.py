from fastapi import FastAPI, UploadFile, File
import asyncio
import bot.bot
import threading
# uvicorn main:app --reload
app = FastAPI()





from uploads.upload import upload_route

app.include_router(upload_route)


threading.Thread(target=bot.bot.start_bot, daemon=True).start()
