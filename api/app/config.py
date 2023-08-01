from pydantic import BaseSettings


class MySQL_PRD_Settings(BaseSettings):
    user: str = "root"
    password: str = "password"
    host: str = "mysql"
    port: int = 3306
    database: str = "test"


class MySQL_DEV_Settings(BaseSettings):
    user: str = "root"
    password: str = "password"
    host: str = "192.168.56.1"
    port: int = 3316
    database: str = "test"
