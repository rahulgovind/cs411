from flask import Flask
from flask_restful import Api, Resource

from model import User, Post, Topic, Comment
from flask.json import JSONEncoder

from flask_restful import reqparse


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


api.add_resource(UserListAPI, '/users')
api.add_resource(PostListAPI, '/posts')
api.add_resource(PostCommentsAPI, '/post-comments/<int:post_id>')
api.add_resource(CommentAPI, '/comments/<int:comment_id>')
api.add_resource(UserAPI, '/users/<int:id>')
api.add_resource(UserSearchAPI, '/searchusers')
api.add_resource(TopicListAPI, '/topics')
api.add_resource(TopicAPI, '/topics/<int:topic_id>')
