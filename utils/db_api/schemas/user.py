from sqlalchemy import BigInteger, Column, String, sql

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    referrer = Column(BigInteger)

    query: sql.Select
