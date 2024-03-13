from server.db import db
from server.models.users import UserModel

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='posts')
    
    def __init__(self, title, image, user_id):
        self.title = title
        self.image = image
        self.user_id = user_id

    def __repr__(self):
        return f'<CookPost {self.title}>'
    
    @classmethod
    def get(cls, id):
        return db.session.get(cls, id)

    