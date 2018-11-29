import mysql.connector
from settings import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_USERNAME, DB_PORT
from MySQLdb import escape_string as mysql_escape_string

_db = None


def quote_string(s):
    if s is None:
        return "NULL"
    else:
        return "'" + escape_string(s) + "'"


def escape_string(s):
    return mysql_escape_string(s).decode('utf-8')


def to_dict(t, keys):
    """Convert a tuple to a dictionary with given keys

    len(t) must be equal to len(keys)
    :param t: tuple
    :param keys: tuple
    :return: dict
    """
    return {keys[i]: t[i] for i in range(len(keys))}


def fit(tuple_list, keys):
    """Fit given list of tuples to specified keys

    Why is this needed? MySQL returns a list of tuples where we can't
    directly associate each entry of the tuple with an attribute.
    """
    return [to_dict(t, keys) for t in tuple_list]


def get_connector():
    global _db

    if _db is None:
        _db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            passwd=DB_PASSWORD,
            database=DB_DATABASE
        )
    print(_db)
    return _db


def fetch(query, multi=False):
    """Executes a query that is expected to return a result

    Use for select

    :param query: string
    :param multi: Multiple queries executed inside fetch
    :return: generator
    """
    print("Fetch Query: ", query)
    conn = get_connector()
    cursor = conn.cursor()
    if multi:
        result = None
        for r in cursor.execute(query, multi=True):
            if r.with_rows:
                print(r.statement)
                result = r.fetchall()
        return result
    else:
        cursor.execute(query)
        return cursor.fetchall()


def execute(query):
    """Executes a query and then commits

    Use for insert/delete

    :param query:
    :return: int
        Number of rows modified
    """
    print("Executing ", query)
    conn = get_connector()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print(cursor.rowcount)
    return cursor.rowcount


def select(table, columns, condition=None):
    colstr = ", ".join(columns)
    query = "SELECT %s FROM %s" % (colstr, table)
    if condition is not None:
        query += " WHERE " + condition
    return fit(fetch(query), columns)


def delete(table, condition):
    query = "DELETE FROM %s WHERE %s" % (table, condition)
    return execute(query)


def update(table, columns, values, condition):
    setstr = ",".join("%s=%s" % (column, new_value)
                      for (column, new_value) in zip(columns, values))

    query = "UPDATE %s SET %s where %s" % (table, setstr, condition)
    return execute(query)


def insert(table, columns, values):
    colstr = ",".join(columns)
    valstr = ",".join(str(_) for _ in values)

    query = "INSERT INTO %s(%s) VALUES (%s)" % (table, colstr, valstr)
    return execute(query)


def create(table, columns, values):
    query_result = insert(table, columns, values)
    last_id = None
    if query_result > 0:
        last_id = fit(fetch("SELECT LAST_INSERT_ID()"),
                      ('last_id',))[0]['last_id']
    return query_result, last_id


if __name__ == "__main__":
    pass
