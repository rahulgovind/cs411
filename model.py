from db import fetch, execute, update, delete, fit, select, insert
from MySQLdb import escape_string as mysql_escape_string


def quote_string(s):
    if s is None:
        return "NULL"
    else:
        return "'" + escape_string(s) + "'"


def escape_string(s):
    return s


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
    def create(fields):
        return insert(table='users',
                      columns=['username', 'password', 'bio'],
                      values=[quote_string(fields['username']),
                              quote_string(fields['password']),
                              quote_string(fields['bio'])])

    @staticmethod
    def update(id, fields):
        attrs = ['username', 'password', 'bio']
        nonnull = [attr for attr in attrs if fields[attr] is not None]

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
    def create(fields):
        return execute("INSERT INTO posts(user_id, content, title) "
                       "VALUES(%d, %s, %s)" % (fields['user_id'],
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
    def create(fields):
        return insert(table='comments',
                      columns=['content', 'user_id', 'post_id'],
                      values=[quote_string(fields['content']),
                              quote_string(fields['user_id']),
                              quote_string(fields['post_id'])])

    @staticmethod
    def update(post_id, fields):
        attrs = ['content', 'user_id', 'post_id']
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
