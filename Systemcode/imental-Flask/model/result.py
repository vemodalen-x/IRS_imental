from init import db

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer,primary_key=True)
    # userid = db.Column(db.String(45),unique=True)
    type = db.Column(db.String(45))
    option1 = db.Column(db.String(45))
    # option2 = db.Column(db.String(45))

    def __init__(self, id, type, option1):
        # self.userid = userid
        self.id = id
        self.type = type
        self.option1 = option1
        # self.option2 = option2
    def __repr__(self):
        return '<Result %r>' % (self.id, self.type, self.option1)