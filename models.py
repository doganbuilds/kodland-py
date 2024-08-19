from sqlalchemy import Column, Float, Integer, String
from database import Base


class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    score = Column(Float)

    def __init__(self, name=None, score=None):
        self.name = name
        self.score = score

    def __repr__(self):
        return f"<Score {self.name!r}>"

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score,
        }


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    question = Column(String(255))
    option1 = Column(String(255))
    option2 = Column(String(255))
    option3 = Column(String(255))
    option4 = Column(String(255))
    answer = Column(String(8))

    def __init__(
        self,
        question="",
        option1="",
        option2="",
        option3="",
        option4="",
        answer="",
    ):
        self.question = question
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.answer = answer

    def __repr__(self):
        return f"<Question {self.question!r}>"

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "question": self.question,
            "option1": self.option1,
            "option2": self.option2,
            "option3": self.option3,
            "option4": self.option4,
            "answer": self.answer,
        }
