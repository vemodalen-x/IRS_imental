from init import db

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(255),unique=True)
    type = db.Column(db.String(255))
    answerA = db.Column(db.String(255))
    answerB = db.Column(db.String(255))
    answerC = db.Column(db.String(255))
    answerD = db.Column(db.String(255))
    answerE = db.Column(db.String(255))


    def __init__(self, question, type, answerA, answerB, answerC, answerD, answerE):
        self.question = question
        self.type = type
        self.answerA = answerA
        self.answerB = answerB
        self.answerC = answerC
        self.answerD = answerD
        self.answerE = answerE

    def __repr__(self):
        return '<Question is %s, answers are %s, %s, %s, %s>' %(self.question, self.type, self.answerA, self.answerB, self.answerC, self.answerD, self.answerE)