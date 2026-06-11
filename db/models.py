import datetime as _dt
import sqlalchemy as _sql
from sqlalchemy.dialects.postgresql import UUID as _pgUUID
from . import database as _database
import uuid




# class User(_database.Base):
#     __tablename__="users"
#     id =  _sql.Column(_sql.Integer,primary_key=True)
#     username = _sql.Column(_sql.String,unique=True,nullable=False)
#     password_hash = _sql.Column(_sql.String,nullable=False)


class File(_database.Base):
    __tablename__ = "files"

    id = _sql.Column(_pgUUID(as_uuid=True), primary_key=True) #default = uuid.uuid4 let services handle it
    filename = _sql.Column(_sql.String, nullable=False)
    filepath = _sql.Column(_sql.String, nullable=False)
    size_bytes = _sql.Column(_sql.BigInteger)
    #uploaded_by = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime,default = _dt.datetime.now)
    file_metadata = _sql.Column("metadata", _sql.JSON,nullable=True)