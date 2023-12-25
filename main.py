from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated 
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class choiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class Question(BaseModel):
    question_text: str
    choices: List[choiceBase]

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/questions/", response_model=Question)
async def create_question(question: Question, db: Session = Depends(get_db)):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(**choice.dict(), question_id=db_question.id)
        db.add(db_choice)
    db.commit()
    db.refresh(db_question)
    return db_question.__dict__

@app.post("/questions2/", response_model=Question)
async def create_question(question: Question, db: Session = Depends(get_db)):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    db_choices = []
    for choice in question.choices:
        db_choice = models.Choices(**choice.dict(), question_id=db_question.id)
        db.add(db_choice)
        db_choices.append(db_choice)
    db.commit()
    db.refresh(db_question)
    for db_choice in db_choices:
        db.refresh(db_choice)
    return {
        **db_question.__dict__,
        "choices": [db_choice.__dict__ for db_choice in db_choices],
    }
