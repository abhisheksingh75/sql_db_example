from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Questions(Base):
    __tablename__ = "questions"
    
    id: int = Column(Integer, primary_key=True, index=True)
    question_text: str = Column(String, index=True)


class Choices(Base):
    __tablename__ = "choices"
    
    id: int = Column(Integer, primary_key=True, index=True)
    choice_text: str = Column(String, index=True)
    is_correct: bool = Column(Boolean, index=True)
    question_id: int = Column(Integer, ForeignKey("questions.id"))