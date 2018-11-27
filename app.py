from flask import Flask
from flask_restful import Api, Resource

from settings import SECRET_KEY, AUTH_ENABLED
from model import User, Post, Topic, Comment
from flask.json import JSONEncoder

from flask_restful import reqparse
import jwt

import datetime
from flask_cors import CORS


class Config(object):
    RESTFUL_JSON = {'cls': JSONEncoder}


app = Flask(__name__)
CORS(app)
api = Api(app)
app.config.from_object(Config)

parser = reqparse.RequestParser()
parser.add_argument("user_id", type=int, help="user_id must be an integer")
parser.add_argument("topic_id", type=int, help="topic_id must be an integer")
parser.add_argument("post_id", type=int, help="post_id must be an integer")
parser.add_argument("follows_id", type=int,
                    help="topic_id must be an integer")
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
            result = dict(success=modified > 0)
            if modified:
                result['user'] = User.find_by_username(args['username'])
            return result
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
            modified, last_id = Post.create(args)
            result = dict(success=modified > 0)
            if modified:
                print(last_id)
                result['post'] = Post.find(last_id[0]['last_id'])
            return result
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
            user = User.auth(args)
            if user is None:
                return dict(success=False,
                            message="Incorrect username or password")
            payload = {
                'exp': datetime.datetime.utcnow() + \
                       datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user['user_id']
            }
            return dict(success=True,
                        user=user,
                        token=jwt.encode(
                            payload,
                            SECRET_KEY,
                            algorithm='HS256'
                        ).decode('utf-8'))

        except Exception as e:
            return dict(success=False, message=str(e))


class PostTopics(Resource):
    def get(self, post_id):
        return Post.fetch_topics(post_id)

    def post(self, post_id):
        args = parser.parse_args()
        try:
            modified = Post.add_topic(post_id, args)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))

    def delete(self, post_id):
        args = parser.parse_args()
        try:
            modified = Post.delete_topic(post_id, args['topic_id'])
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class TopicPosts(Resource):
    def get(self, topic_id):
        return Topic.fetch_posts(topic_id)


class UserPostLikes(Resource):
    def get(selfself, user_id):
        return User.fetch_like_posts(user_id)

    def post(self, user_id):
        args = parser.parse_args()
        try:
            modified = User.add_post_like(user_id, args)
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))

    def delete(self, user_id):
        args = parser.parse_args()
        try:
            modified = User.delete_post_like(user_id, args['post_id'])
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class PostUserLikes(Resource):
    def get(self, post_id):
        return Post.fetch_user_likes(post_id)


class FollowsAPI(Resource):
    def get(self, user_id):
        return User.following(user_id)

    def post(self, user_id):
        args = parser.parse_args()
        try:
            modified = User.follow(user_id, args['follows_id'])
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))

    def delete(self, user_id):
        args = parser.parse_args()
        try:
            modified = Post.delete_topic(user_id, args['follows_id'])
            return dict(success=modified > 0)
        except Exception as e:
            return dict(success=False, message=str(e))


class FollowersAPI(Resource):
    def get(self, user_id):
        return User.followers(user_id)


api.add_resource(UserListAPI, '/users')
api.add_resource(PostListAPI, '/posts')
api.add_resource(PostCommentsAPI, '/post-comments/<int:post_id>')
api.add_resource(CommentAPI, '/comments/<int:comment_id>')
api.add_resource(UserAPI, '/users/<int:id>')
api.add_resource(UserSearchAPI, '/searchusers')
api.add_resource(TopicListAPI, '/topics')
api.add_resource(TopicAPI, '/topics/<int:topic_id>')
api.add_resource(AuthAPI, '/auth')
api.add_resource(PostTopics, '/post-topics/<int:post_id>')
api.add_resource(TopicPosts, '/topic-posts/<int:topic_id>')
api.add_resource(FollowsAPI, '/follows/<int:user_id>')
api.add_resource(FollowersAPI, '/followers/<int:user_id>')
api.add_resource(UserPostLikes, '/user-post-likes/<int:user_id>')
api.add_resource(PostUserLikes, '/post-user-likes/<int:post_id>')
