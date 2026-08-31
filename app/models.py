from typing import List, Optional
from pydantic import BaseModel


class Profile(BaseModel):
    id: str
    name: Optional[str] = None
    headline: Optional[str] = None
    location: Optional[str] = None
    about: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    current_company: Optional[str] = None
    followers: Optional[int] = None
    companies: List[str] = []
    schools: List[str] = []
