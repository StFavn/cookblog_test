from server.db import db
from server.models.posts import PostModel

class SectionModel(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(1000))
    image = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = db.relationship('Post', backref='sections')

    def __init__(self, order, post_id, text=None, image=None):
        self.order = order
        self.text = text
        self.image = image
        self.post_id = post_id

    def __repr__(self):
        return f'<Section {self.title}>'
    
    def serialize(self):
        return {
            'id':    self.id,
            'order': self.order,
            'text':  self.text,
            'image': self.image
        }

    @classmethod
    def get_by_post(cls, post_id):
        sections = cls.query.filter_by(post_id=post_id).order_by(cls.order).all()
        return sections
