import qrcode
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from io import BytesIO
class QrText(BaseModel):
    text:str

app = FastAPI()


@app.post('/generate-qr/')

async def generate_qr(qrText: QrText):
    buffer = BytesIO()
    img= qrcode.make(qrText.text)
    img.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    return Response(content=image_bytes, media_type="image/png")
