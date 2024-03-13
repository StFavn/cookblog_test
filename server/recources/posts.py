from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import jwt_required

from server.db import db

from server.models.posts import PostModel
from server.models.section import SectionModel

class PostApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True)
    parser.add_argument('image', type=str, required=False)
    parser.add_argument('user_id', type=int, required=True)
    parser.add_argument('sections', type=list, required=True)

    def get(self, id):
        post = PostModel.get(id)
        if post:
            sections = SectionModel.get_by_post(id)
            return jsonify({
                'id': post.id,
                'title': post.title,
                'image': post.image,
                'sections': [section.serialize() for section in sections]
            }), 200
        return jsonify({'message': 'Пост не найден'}), 404

    @jwt_required()
    def post(self):
        data = PostApi.parser.parse_args()
        post = PostModel(
            title=data['title'], 
            image=data['image'], 
            user_id=data['user_id']
        )
        try:
            db.session.begin_nested()
            db.session.add(post)
            db.session.flush()
            for section_data in data['sections']:
                section = SectionModel(
                    order=section_data['order'], 
                    text=section_data['text'], 
                    image=section_data['image'], 
                    post_id=post.id)
                db.session.add(section)
            db.session.commit()
            return jsonify({'message': 'Пост создан'}), 201
        except Exception:
            db.session.rollback()
            return jsonify({'message': 'Ошибка создания поста'}), 500

    # @jwt_required()
    # def put():
    #     pass

# class PostListApi(Resource):
#     def get(self):
#         posts = PostModel.query.all()
#         return jsonify([post.to_json() for post in posts]