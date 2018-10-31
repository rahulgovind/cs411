from db import fetch, execute, update, delete, fit, select, insert, \
    get_connector
from MySQLdb import escape_string as mysql_escape_string
import bcrypt


def quote_string(s):
    if s is None:
        return "NULL"
    else:
        return "'" + escape_string(s) + "'"


def escape_string(s):
    conn = get_connector()
    return mysql_escape_string(s).decode('utf-8')


class User(object):
    @staticmethod
    def fetch_all():
        return select(table='users',
                      columns=('user_id', 'username', 'bio', 'join_date'))

    @staticmethod
    def find(id):
        result = select(table='users',
                        columns=('user_id', 'username', 'bio', 'join_date'),
                        condition='user_id=%d' % id)
        if len(result) > 0:
            return result[0]
        else:
            return None

    @staticmethod
    def auth(fields):
        result = select(table='users',
                        columns=('user_id', 'username', 'password'),
                        condition="username=%s" %
                                  quote_string(fields['username']))
        if len(result) > 0:
            if bcrypt.checkpw(fields['password'].encode('utf-8'),
                              result[0]['password'].encode('utf-8')):
                return result[0]['user_id']
        return None

    @staticmethod
    def create(fields):

        pwd = bcrypt.hashpw(fields['password'].encode('utf-8'),
                            bcrypt.gensalt(14))
        return insert(table='users',
                      columns=['username', 'password', 'bio'],
                      values=[quote_string(fields['username']),
                              quote_string(pwd),
                              quote_string(fields['bio'])])

    @staticmethod
    def update(id, fields):
        attrs = ['username', 'password', 'bio']
        nonnull = [attr for attr in attrs if fields[attr] is not None]

        if 'password' in attrs:
            fields['password'] = bcrypt.hashpw(
                fields['password'].encode('utf-8)'),
                bcrypt.gensalt(14)
            )
        return update(table='users',
                      columns=[attr for attr in nonnull],
                      values=[quote_string(fields[attr]) for attr in nonnull],
                      condition="user_id=%d" % id)

    @staticmethod
    def delete(id):
        return delete(table='users', condition="user_id=%d" % id)

    @staticmethod
    def search(query):
        return fit(fetch(
            "SELECT user_id, username FROM users WHERE username LIKE '%s%%'"
            % escape_string(query)),
            ('user_id', 'username'))


class Post(object):
    @staticmethod
    def fetch_all():
        return fit(fetch("SELECT post_id, content, created, user_id, "
                         "title FROM posts"),
                   ('post_id', 'content', 'created', 'user_id', 'title'))

    @staticmethod
    def find(post_id):
        result = select(table='posts',
                        columns=('post_id', 'content', 'created', 'user_id',
                                 'title'),
                        condition='post_id=%d' % post_id)
        if len(result) > 0:
            return result[0]
        else:
            return None

    @staticmethod
    def fetch_comments(post_id):
        return select(table='comments',
                      columns=('comment_id', 'content', 'user_id', 'post_id'),
                      condition='post_id=%d' % post_id)

    @staticmethod
    def create(user_id, fields):
        print(user_id)
        return execute("INSERT INTO posts(user_id, content, title) "
                       "VALUES(%d, %s, %s)" % (user_id,
                                               quote_string(fields['content']),
                                               quote_string(fields['title'])))

    @staticmethod
    def update(post_id, fields):
        attrs = ['content', 'user_id', 'title']
        nonnull = [attr for attr in attrs if fields[attr] is not None]

        return update(table='posts',
                      columns=[attr for attr in nonnull],
                      values=[quote_string(fields[attr]) for attr in nonnull],
                      condition="post_id=%d" % post_id)

    @staticmethod
    def delete(post_id):
        return delete(table='posts', condition="post_id=%d" % post_id)


class Comment(object):
    @staticmethod
    def find(comment_id):
        result = select(table='comments',
                        columns=('comment_id', 'content', 'user_id',
                                 'post_id'),
                        condition='comment_id=%d' % comment_id)
        if len(result) > 0:
            return result[0]
        else:
            return None

    @staticmethod
    def create(post_id, fields):
        return insert(table='comments',
                      columns=['content', 'user_id', 'post_id'],
                      values=[quote_string(fields['content']),
                              quote_string(fields['user_id']),
                              str(post_id)])

    @staticmethod
    def update(post_id, fields):
        attrs = ['content']
        nonnull = [attr for attr in attrs if fields[attr] is not None]

        return update(table='comments',
                      columns=[attr for attr in nonnull],
                      values=[quote_string(fields[attr]) for attr in nonnull],
                      condition="comment_id=%d" % post_id)

    @staticmethod
    def delete(post_id):
        return delete(table='comments', condition="comment_id=%d" % post_id)


class Topic(object):
    @staticmethod
    def fetch_all():
        return select(table='topics',
                      columns=('topic_id', 'topic', 'description'))

    @staticmethod
    def find(topic_id):
        result = select(table='topics',
                        columns=('topic_id', 'topic', 'description'),
                        condition='topic_id=%d' % topic_id)
        if len(result) > 0:
            return result[0]
        else:
            return None

    @staticmethod
    def create(fields):
        return insert(table="topics",
                      columns=("topic", "description"),
                      values=[quote_string(fields['topic']),
                              quote_string(fields['description'])])

    @staticmethod
    def delete(topic_id):
        return delete(table='topics', condition="topic_id=%d" % topic_id)


class Quiz(object):
    @staticmethod
    def fetch_all():
        return select(table='quizzes',
                      columns=('quiz_id', 'title', 'description'))

    @staticmethod
    def find(quiz_id):
        result = select(table='quiz',
                        columns=('quiz_id', 'topic', 'description'),
                        condition='quiz_id=%d' % quiz_id)
        if len(result) > 0:
            return result[0]
        else:
            return None

    @staticmethod
    def create(fields):
        return insert(table="quizzes",
                      columns=("title", "description"),
                      values=[quote_string(fields['topic']),
                              quote_string(fields['description'])])
