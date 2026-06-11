from fastapi import FastAPI,UploadFile,HTTPException,Request,Form
from db import database as _database
from typing import TYPE_CHECKING
from db import models as _models
from db import schemas as _schemas

import uuid
from pathlib import Path


if TYPE_CHECKING:
    from sqlalchemy.orm import Session

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok = True)   #creates directory if true


def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)




def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_file(file:UploadFile ,db:"Session") -> _schemas.File: # dont know this but lets see
    file_id = str(uuid.uuid4())

    original_name = Path(file.filename).name  #to avoid pathinjection
    


    save_path = UPLOAD_DIR / f"{file_id}_{original_name}"



        
    

    with open(save_path,"wb") as f:
        while chunk := await file.read(12500 * 12500):  # 100 mb reads (can be increased for faster)
            f.write(chunk)


    try:
        # Fetch the file size in bytes
        file_size_bytes = save_path.stat().st_size
        print(f"File size: {file_size_bytes} bytes")
    except FileNotFoundError:
        print("The specified file does not exist.")


    dbfile = _models.File(
    id=file_id,
    filename=original_name,
    filepath=str(save_path),
    size_bytes=file_size_bytes,
    file_metadata={}
    )

    db.add(dbfile)
    db.commit()
    db.refresh(dbfile)
    return _schemas.Contact.model_validate(dbfile) #i dont know if this right 


def get_files(db:"Session") -> list[_schemas.File]:
    dbfiles = db.query(_models.File.id).all()
    return list(map(_schemas.File.model_validate,dbfiles))

def download_file(file_id : str,db:"Session"):
    dbfile = db.query(_models.File).filter(_models.File.id==file_id).first()
    return (dbfile.filepath,dbfile.filename)









if __name__ == "__main__":
    _add_tables()