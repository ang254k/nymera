from pydantic import BaseModel, ConfigDict

#Peticiones

#Respuestas
class LikeResponse(BaseModel):
    status:str
    likes_count:int