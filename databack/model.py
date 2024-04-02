from utils.ext import db
from sqlalchemy.dialects.mysql import LONGTEXT

class Big(db.Model):
    # 表名
    __tablename__ = 'big'
    # 字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Season = db.Column(db.Integer, nullable=True)
    Episode=db.Column(db.Integer,  nullable=True)
    Scene = db.Column(db.Integer,  nullable=True)
    Line  = db.Column(db.Integer,  nullable=True)
    Location = db.Column(db.Text, nullable=True)
    Action=db.Column(db.Text,  nullable=True)
    Words=db.Column(db.Text, nullable=True)
    Speaker=db.Column(db.Text, nullable=True)
    Listener = db.Column(db.Text, nullable=True)
    Result = db.Column(LONGTEXT, nullable=True)
    # batchno=db.Column(db.String(1000), nullable=True)
    batchno=db.Column(db.String(64), nullable=True)
    # unique_index = db.UniqueConstraint('batchno', 'Season','Episode','Scene','Line', name='unique_index_constraint')
    __table_args__ = (db.UniqueConstraint('batchno', 'Season', 'Episode','Scene','Line', name='unique_index_constraint'),)


class User(db.Model):
    # 表名
    __tablename__ = 't_user'
    # 字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # username = db.Column(db.String(1000),unique=True)
    # password=db.Column(db.String(1000))
    username = db.Column(db.String(768),unique=True)
    password=db.Column(db.String(768))

