from pydantic import BaseModel

class AlertMessageRequest(BaseModel):
    user_id: int
    full_name: str 
    puesto_trabajo: str
    message: str
