from fastapi import FastAPI, Request, Response
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import app.service as service 

app = FastAPI(
    title='aiforthai-line-chatbot',
    description='AIFORTHAI LINE CHATBOT WORKSHOP',
    version='1.0.0'
    )

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(service.router)

app.mount("/static/",StaticFiles(directory="static"),name="static")

@app.get('/')
def index():
    return 'AIFORTHAI LINE CHATBOT WORKSHOP'

@app.on_event('startup')
def start_event():
    return 'service started'

@app.on_event('shutdown')
def shutdown_event():
    return 'service shutdown'
