from db import database as _database
from typing import TYPE_CHECKING
from db import models as _models
from db import schemas as _schemas


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_file(file: _schemas._BaseFile,db:"Session") -> _schemas.File: # dont know this but lets see
    