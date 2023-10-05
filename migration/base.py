from datetime import datetime, timedelta

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, types

# ! Base
Base = declarative_base()



class AppTable(Base):
    __tablename__ = "app"

    user_id = Column(types.BigInteger, primary_key=True)
    gender = Column(types.String(16))
    name = Column(types.String(15))
    years = Column(types.Integer)
    city = Column(types.String(32))
    photo_id = Column(types.String(128))
    pub_video = Column(types.Boolean, default=False)
    video_id = Column(types.String(128))
    score = Column(types.BigInteger, default=0)
    moderated = Column(types.Boolean, default=False)
    


    
