from fastapi import APIRouter, HTTPException, Request, Header, File, UploadFile, Form
from fastapi.responses import PlainTextResponse, JSONResponse, Response
from typing import Optional
from aift.nlp import tokenizer #1.Tokenizer
from aift.nlp import g2p
from aift.nlp import soundex
from aift.speech import tts
from linebot.models import AudioSendMessage


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
)

from aift import setting
from aift.multimodal import textqa
from aift.image.classification import maskdetection

from datetime import datetime

router = APIRouter(
            tags=['']
         )

AIFORTHAI_APIKEY = 'W8d02d1YSDN2874WYa3Z74JYYMy73jAo'
LINE_CHANNEL_ACCESS_TOKEN = 'BiID/eRN+NVl+E28RTMWy5+I5y5vWmgCcxazFhZ2K52oW6/PLH3h8QBqdDPmdY/Oun7x9eJuGSVUZgsfU5sUFLQ8KnfcKK0a4ypd/9m6oFiPJ/Uhkqif4sVakB+To/at6qI7CsDFuH5jLZGU+nXwGgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '15053898f73c6eb0930f1bc569a88afd'

setting.set_api_key(AIFORTHAI_APIKEY)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN) #CHANNEL_ACCESS_TOKEN
handler = WebhookHandler(LINE_CHANNEL_SECRET) #CHANNEL_SECRET

@router.post('/message')
async def hello_word(request: Request):

    signature = request.headers['X-Line-Signature']
    body = await request.body()    
    try:
        handler.handle(body.decode('UTF-8'), signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token or channel secret.")
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # session id
    current_time = datetime.now()
    # extract day, month, hour, and minute
    day, month = current_time.day, current_time.month
    hour, minute = current_time.hour, current_time.minute
    # adjust the minute to the nearest lower number divisible by 10
    adjusted_minute = minute - (minute % 10)
    result = f"{day:02}{month:02}{hour:02}{adjusted_minute:02}"

    # text = tokenizer.tokenize(event.message.text, engine='textplus', return_json=True)
    # text = tokenizer.tokenize(event.message.text)
    # text = textqa.chat(event.message.text, result+AIFORTHAI_APIKEY, temperature=0.6, context='')['response']
    # text = g2p.analyze(event.message.text, return_json=True)
    # text = soundex.analyze(event.message.text, return_json=True)
    # return text response
    # send_message(event,str(text))
    response = tts.tts(event.message.text,'static/file.wav')
    audio_url = 'https://6ef0-158-108-230-186.ngrok-free.app/static/file.wavwav'
    audio_duration = 7*1000

    audio_message = AudioSendMessage(
            original_content_url = audio_url,
            duration = audio_duration  
        )
    
    send_audio_message(event,audio_message)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_id = event.message.id
    image_content = line_bot_api.get_message_content(message_id)
    
    # Save the image locally and process it
    with open(f"image.jpg", "wb") as f:
        for chunk in image_content.iter_content():
            f.write(chunk)
    
    # aiforthai maskdetection
    result = maskdetection.analyze(f"image.jpg", return_json=False)
    result = result[0]['result']

    # return text response
    send_message(event, result)

def echo(event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))

# function for sending message
def send_message(event,message):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))
    
def send_audio_message(event,audio_message):
        line_bot_api.reply_message(
             event.reply_token,
             audio_message)