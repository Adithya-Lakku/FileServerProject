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


class Folder(_database.Base):
    __tablename__ = "folders"

    id = _sql.Column(_pgUUID(as_uuid=True), primary_key=True)
    name = _sql.Column(_sql.String, nullable=False)
    parent_folder_id = _sql.Column(_pgUUID(as_uuid=True), _sql.ForeignKey("folders.id"), nullable=True)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.now)

    __table_args__ = (
        _sql.UniqueConstraint('parent_folder_id', 'name', name='uix_parent_folder_name'),
        _sql.Index('uix_root_folder_name', 'name', unique=True, postgresql_where=_sql.text('parent_folder_id IS NULL')),
    )


class File(_database.Base):
    __tablename__ = "files"

    id = _sql.Column(_pgUUID(as_uuid=True), primary_key=True) #default = uuid.uuid4 let services handle it
    filename = _sql.Column(_sql.String, nullable=False)
    filepath = _sql.Column(_sql.String, nullable=False)
    size_bytes = _sql.Column(_sql.BigInteger)
    #uploaded_by = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime,default = _dt.datetime.now)
    file_metadata = _sql.Column("metadata", _sql.JSON,nullable=True)
    parent_folder_id = _sql.Column(_pgUUID(as_uuid=True), _sql.ForeignKey("folders.id"), nullable=True)