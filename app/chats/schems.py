from pydantic import BaseModel

class Chat(BaseModel):
    user_id_1: int
    user_id_2: int