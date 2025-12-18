from pydantic import BaseModel, field_validator
from typing import Optional


class ValidationSchema(BaseModel):
    title: str
    price_usd: int
    odometer: int
    username: str
    image_url: str
    images_count: int
    car_number: Optional[str] = None
    car_vin: Optional[str] = None
    phone_number: int
    url: str

    @field_validator('price_usd', mode='before')
    def clean_price_usd(cls, v):
        return v.replace('$', '').replace(' ', '').replace('\xa0', '')
    
    @field_validator('odometer', mode='before')
    def clean_odometer(cls, v):
        if v == 'Без пробігу':
            return 0
        v = float(v.replace('тис. км', ''))
        return int(v * 1000)
    
    @field_validator('phone_number', mode='before')
    def clean_phone(cls, v):
        v = (v
             .replace("-", "", 5)
             .replace('(', '')
             .replace(')', '')
             .replace(' ', '', 5)
             )
        
        phone = '38' + v
        return phone
    


    






