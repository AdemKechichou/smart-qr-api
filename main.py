import qrcode ,PIL.Image
import requests
from fastapi import FastAPI ,HTTPException , Query
from fastapi.responses import Response
from pydantic import BaseModel, Field, dataclasses
from io import BytesIO
from typing import Optional
from database import save_qr_analytics ,get_total_count, get_count_by_period ,get_feature_stats
import time
from datetime import date
import datetime

class Color(BaseModel):
    red: int = Field(ge=0, le=255)
    green: int = Field(ge=0, le=255)
    blue: int = Field(ge=0, le=255)
    
    def getColor(self):
        return (self.red,self.green,self.blue)

class QrText(BaseModel):
    text:str
    size: Optional[int] = None
    color: Optional[Color] = None
    logo_url: Optional[str] = None


class Total(BaseModel):
    total_qr_codes: int


class Features(BaseModel):
      total: int
      with_color: int
      with_logo: int
      with_both: int
      average_size: float
      average_response_time_ms: float 

class Period(BaseModel):
      timeframe: str
      count: int
      period_start: date
      period_end: date


app = FastAPI()


@app.post('/generate-qr/')

async def generate_qr(qr: QrText):
    start_time = time.time()
    buffer = BytesIO()
    qr_code = qrcode.QRCode(
        version=1, 
        box_size = qr.size or 10,  # Size of each box in pixels
        border=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H 
    )
    
    qr_code.add_data(qr.text)
    qr_code.make(fit=True)
    img = qr_code.make_image(fill_color= qr.color.getColor() if qr.color else "black" , back_color="white")
    if qr.logo_url:
        response = requests.get(qr.logo_url, stream=True, timeout=5)  # 5 second timeout
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to download logo: {response.status_code}")
        try:
            logo = PIL.Image.open(response.raw)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid image URL")
        if not qr.color:
            img = qr_code.make_image().convert('RGB')
        logo_size = img.size[0] // 5
        logo.thumbnail((logo_size, logo_size))
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos)
    
    img.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    end_time = time.time()
    response_time_ms = int((end_time - start_time) * 1000)
    try:
        save_qr_analytics(bool(qr.color),bool(qr.logo_url),qr.size or 10,response_time_ms)
    except Exception as e:
        print(f"Analytics failed: {e}")
    return Response(content=image_bytes, media_type="image/png")


@app.get('/analytics/total', response_model=Total)

def get_total():
    try:
        count = get_total_count()
        return {"total_qr_codes": count}
    except Exception as e:
        print(f"Analytics failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analytics")

@app.get('/analytics/period', response_model=Period)
def get_period_analytics(timeframe: str = Query(..., description="Options: today, month, year")):
    try:
        if timeframe == "today":
            count=get_count_by_period(timeframe)
            period_start = date.today()
            period_end = date.today()

            return {"timeframe":timeframe,"count":count,
                    "period_start":period_start,"period_end":period_end}
        elif timeframe == "month":
            count=get_count_by_period(timeframe)
            period_start = date.today()-datetime.timedelta(days=30)
            period_end = date.today()

            return {"timeframe":timeframe,"count":count,
                    "period_start":period_start,"period_end":period_end}
        elif timeframe == "year":
            count=get_count_by_period(timeframe)
            period_start = date.today()-datetime.timedelta(days=365)
            period_end = date.today()

            return {"timeframe":timeframe,"count":count,
                    "period_start":period_start,"period_end":period_end}

        else:
            raise HTTPException(status_code=400, detail="invalid input")
    except Exception as e:
        print(f"Analytics failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analytics")

@app.get('/analytics/features',response_model=Features)

def get_features():
    try:
        
        features = get_feature_stats()
        return features
    except Exception as e:
        print(f"Analytics failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analytics")
    