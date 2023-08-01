import pymysql
from app.config import MySQL_DEV_Settings, MySQL_PRD_Settings

ENVIRONMENT = "PRD"


def connectiondb(environment=ENVIRONMENT):
    if environment == "PRD":
        config = MySQL_PRD_Settings()
    else:
        config = MySQL_DEV_Settings()

    try:
        connection = pymysql.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database,
            charset="utf8",
        )
        return connection
    except Exception as e:
        return print(e)


def excute_query(query):
    with connectiondb() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query=query)
            result = cursor.fetchone()[0]
    return result
