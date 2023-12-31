from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, 
    BigInteger, 
    String, 
    Integer, 
    Boolean
)



Base = declarative_base()


class AppTable(Base):
    __tablename__ = "app"

    user_id = Column(BigInteger, primary_key=True)
    gender = Column(String(16))
    name = Column(String(15))
    years = Column(Integer)
    city = Column(String(32))
    photo_id = Column(String(128))
    pub_video = Column(Boolean, default=False)
    video_id = Column(String(128))
    score = Column(BigInteger, default=0)
    moderated = Column(Boolean, default=False)


    def __init__(
        self, chat_id : int,
        gender : str,
        name : str,
        years : int,
        city : str,
        photo_id : str = None,
        video_id : str = None,
        pub_video : bool = False,
        moderated : bool = False
    ):
        self.user_id = chat_id
        self.gender = gender
        self.name = name
        self.years = years
        self.city = city
        self.photo_id = photo_id
        self.video_id = video_id
        self.pub_video = pub_video
        self.score = 0
        self.moderated = moderated
