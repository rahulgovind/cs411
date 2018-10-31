from flask import Flask
from flask_restful import Api, Resource

from settings import SECRET_KEY, AUTH_ENABLED
from model import User, Post, Topic, Comment
from flask.json import JSONEncoder

from flask_restful import reqparse
import jwt

import datetime


class Config(object):
    RESTFUL_JSON = {'cls': JSONEncoder}


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)

parser = reqparse.RequestParser()
parser.add_argument("user_id", type=int, help="user_id must be an integer")
parser.add_argument('username', type=str, help='Username must be a string')
parser.add_argument('bio', type=str, help="Bio must be a string")
parser.add_argument("password", type=str, help="Password must be a string")
parser.add_argument("title", type=str, help="Title must be a string")
parser.add_argument("content", type=str, help="Content must be a string")
parser.add_argument("query", type=str, help="Query must be a string")
parser.add_argument("topic", type=str, help="Topic must be a string")
parser.add_argument("description", type=str, help="Description must be a "
                                                  "string")
parser.add_argument("token", type=str, help="Token must be a string")


def auth(f):
    def f_with_user_id(*args, **kwargs):
        fields = parser.parse_args()
        msg = None
        try:
            payload = jwt.decode(fields['token'], key=SECRET_KEY)
            user_id = payload['sub']
            assert (user_id == fields['user_id'])
        except Exception as e:
            user_id = None
            msg = str(e)
        if user_id is None and AUTH_ENABLED is True:
            return {
                'success': False,
                'message': msg
            }
        else:
            return f(*args, **kwargs)

    return f_with_user_id


class UserAPI(Resource):
    def get(self, id):
        return User.find(id)

    def put(self, id):
        args = parser.parse_args()
        try:
            modified = User.update(id, args)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))

    def delete(self, id):
        try:
            modified = User.delete(id)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class UserListAPI(Resource):
    def get(self):
        return User.fetch_all()

    def post(self):
        args = parser.parse_args()
        try:
            modified = User.create(args)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class PostAPI(Resource):
    def get(self, post_id):
        return Post.find(post_id)

    def put(self, post_id):
        args = parser.parse_args()
        try:
            modified = Post.update(post_id, args)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))

    def delete(self, post_id):
        try:
            modified = Post.delete(post_id)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class PostListAPI(Resource):
    def get(self):
        return Post.fetch_all()

    @auth
    def post(self):
        args = parser.parse_args()
        try:
            modified = Post.create(args)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class UserSearchAPI(Resource):
    def get(self):
        args = parser.parse_args()
        try:
            return User.search(args['query'])
        except Exception as e:
            return dict(success=False, message=str(e))


class TopicListAPI(Resource):
    def get(self):
        return Topic.fetch_all()

    def post(self):
        args = parser.parse_args()
        try:
            print(args)
            modified = Topic.create(args)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class TopicAPI(Resource):
    def get(self, topic_id):
        return Topic.find(topic_id)

    def delete(self, topic_id):
        try:
            modified = Topic.delete(topic_id)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class PostCommentsAPI(Resource):
    def get(self, post_id):
        return Post.fetch_comments(post_id)

    def post(self, post_id):

        args = parser.parse_args()
        try:
            modified = Comment.create(post_id, args)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class CommentAPI(Resource):
    def put(self, comment_id):
        args = parser.parse_args()
        try:
            modified = Comment.update(comment_id, args)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))

    def delete(self, comment_id):
        try:
            modified = Comment.delete(comment_id)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class AuthAPI(Resource):
    def post(self):
        args = parser.parse_args()
        try:
            user_id = User.auth(args)
            if user_id is None:
                return dict(success=False,
                            message="Incorrect username or password")
            payload = {
                'exp': datetime.datetime.utcnow() + \
                       datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return dict(success=True,
                        user_id=user_id,
                        token=jwt.encode(
                            payload,
                            SECRET_KEY,
                            algorithm='HS256'
                        ).decode('utf-8'))

        except Exception as e:
            return dict(success=False, message=str(e))


api.add_resource(UserListAPI, '/users')
api.add_resource(PostListAPI, '/posts')
api.add_resource(PostCommentsAPI, '/post-comments/<int:post_id>')
api.add_resource(CommentAPI, '/comments/<int:comment_id>')
api.add_resource(UserAPI, '/users/<int:id>')
api.add_resource(UserSearchAPI, '/searchusers')
api.add_resource(TopicListAPI, '/topics')
api.add_resource(TopicAPI, '/topics/<int:topic_id>')
api.add_resource(AuthAPI, '/auth')
