
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from database import Base
from app import app



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)
    add_questions = relationship('Questions')
    comments = relationship('Comments')
    like = relationship('Like')

    def __repr__(self):
        return '<User %s>' % self.name

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __init__(self, name, password):
        self.name = name
        self.password = password

class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comments = relationship('Comments')

    def __init__(self, question, user_id):
        self.question = question
        self.user_id = user_id

    def get_user(self):
        return User.query.filter_by(id=self.user_id).first().name


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comment = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    like = relationship('Like')
    likes = Column(Integer)

    def __init__(self, comment, user_id, question_id):
        self.comment = comment
        self.user_id = user_id
        self.question_id = question_id
        self.likes = 0

    def get_user(self):
        return User.query.filter_by(id=self.user_id).first().name

class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    comment = Column(Integer, ForeignKey('comments.id'), nullable=False)
    user = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, comment, user):
        self.comment = comment
        self.user = user
