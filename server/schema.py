
from pydantic import BaseModel

class Numbers(BaseModel):
   number: int
   
   class Config: 
       orm_mode = True

