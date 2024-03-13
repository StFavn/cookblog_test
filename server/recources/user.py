from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import current_user
from server.db import db

from server.models.users import UserModel

class LoginApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=False)
    parser.add_argument('username', type=str, required=False)
    parser.add_argument('password', type=str, required=True)


    def post(self):
        data = LoginApi.parser.parse_args()

        if not data['email'] or not data['username']:
            return jsonify({'message': 'Поле username отсутствуют'}), 401
        
        if not data['password']:
            return jsonify({'message': 'Поле password отсутствует'}), 401
        
        if data['email']:
            user = UserModel.query.filter_by(email=data['email']).first()
        elif data['username']:
            user = UserModel.query.filter_by(username=data['username']).first()

        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        return jsonify({'message': 'Не корректные данные'}), 401
    
    @jwt_required()
    def get(self):
        return jsonify(
            {
                'id': current_user.id,
                'email': current_user.email,
                'user': current_user.username
            }), 200

class RegisterApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        data = RegisterApi.parser.parse_args()

        if not data['username'] or not data['email'] or not data['password']:
            return jsonify({'message': 'Все поля должны быть заполнены'}), 400

        if UserModel.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Пользователь с таким именем уже существует'}), 400

        if UserModel.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Пользователь с таким email уже существует'}), 400

        user = UserModel(
            user=data['username'],
            email=data['email'],
            password=data['password']
        )

        try:
            db.session.add(user)
            db.session.commit()
        except:
            return jsonify({'message': 'Произошла ошибка при создании пользователя'}), 500
        return jsonify({'message': 'Пользователь успешно создан'}), 201
        