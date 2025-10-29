
from pydantic import BaseModel
from typing import Optional

class UserSignUp(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class AnalyzeRequest(BaseModel):
    age: int
    height: float
    weight: float
    dietType: str
    caste: Optional[str] = ""
    diseases: Optional[str] = ""
    token: Optional[str] = None  
