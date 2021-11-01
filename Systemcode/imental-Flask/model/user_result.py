from init import db

class User_Result(db.Model):
    __tablename__ = 'user_result'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(16),unique=True)
    anxi = db.Column(db.Float)
    depr = db.Column(db.Float)
    host= db.Column(db.Float)
    sens = db.Column(db.Float)
    obse = db.Column(db.Float)
    para = db.Column(db.Float)
    psyc = db.Column(db.Float)
    soma = db.Column(db.Float)
    terr = db.Column(db.Float)



    def __init__(self,username, anxi, depr, host, sens, obse, para , psyc, soma, terr):
        self.username = username
        self.anxi = anxi
        self.depr = depr
        self.host = host
        self.sens = sens
        self.obse = obse
        self.para = para
        self.psyc = psyc
        self.soma = soma
        self.terr = terr

    def __repr__(self):
        return '<User_Result %r>' % (self.username, self.anxi, self.depr, self.host, self.sens, self.obse, self.para, self.psyc, self.soma, self.terr)