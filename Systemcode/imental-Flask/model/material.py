from init import db

class Article(db.Model):
    __tablename__ = 'article'
    Article_id = db.Column(db.Integer,primary_key=True)
    Title = db.Column(db.String(255))
    Upload_date = db.Column(db.DateTime)
    Label = db.Column(db.TEXT,nullable=False)
    Content = db.Column(db.TEXT,nullable=False)



    def __init__(self, Article_id, Title, Upload_date, Label, Content):
        self.Article_id = Article_id
        self.Title = Title
        self.Upload_date = Upload_date
        self.Label = Label
        self.Content = Content

    def __repr__(self):
        return '<Article %r>' %(self.Article_id, self.Title, self.Upload_date, self.Label, self.Content)