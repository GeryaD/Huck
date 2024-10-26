from pydantic import BaseModel

class OutReqHistory(BaseModel):
    id: int
    uuid_user: str
    name: str
    url_card: str
    url_img: str

class InReqHistory(BaseModel):
    name: str
    url_card: str
    url_img: str