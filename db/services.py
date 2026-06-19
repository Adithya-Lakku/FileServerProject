import sys
from pathlib import Path
# Add project root to sys.path to resolve 'db' imports when running the script directly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI,UploadFile,HTTPException,File
from pydantic import UUID4
from db import database as _database
from typing import TYPE_CHECKING,Annotated
from db import models as _models

from db import schemas as _schemas

import uuid


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


async def create_file(files: Annotated[ list[UploadFile],File(...)], db:"Session", parent_folder_id: str | None = None) :   #-> _schemas.File
    
    for file in files:
    
        file_id = str(uuid.uuid4())

        original_name = Path(file.filename).name  #to avoid pathinjection
        


        save_path = UPLOAD_DIR / f"{file_id}_{original_name}"



            
        

        with open(save_path,"wb") as f:
            while chunk := await file.read(12500 * 12500):  # 100 mb reads (can be increased for faster)
                f.write(chunk)


        file_size_bytes = 0
        try:
            # Fetch the file size in bytes
            file_size_bytes = save_path.stat().st_size
            print(f"File size: {file_size_bytes} bytes")
        except FileNotFoundError:
            print("The specified file does not exist.")


        parent_uuid = uuid.UUID(parent_folder_id) if parent_folder_id else None

        dbfile = _models.File(
        id=file_id,
        filename=original_name,
        filepath=str(save_path),
        size_bytes=file_size_bytes,
        file_metadata={},
        parent_folder_id=parent_uuid
        )

        db.add(dbfile)
        db.commit()
        db.refresh(dbfile)

        _schemas.File.model_validate(dbfile)
     #i dont know if this right


def get_files(db: "Session") :
    
       
    rows = db.query(_models.File.id,_models.File.filename).all()    


    return [(row[0],row[1]) for row in rows]

    # rows = db.query(
    #     _models.File.id,
    #     _models.File.filename
    # ).all()

    # return [
    #     _schemas.FileSummary(
    #         id=row[0],
    #         filename=row[1]
    #     )
    #     for row in rows
    # ]    


def download_file(file_id : str,db:"Session"):
    dbfile = db.query(_models.File).filter(_models.File.id==file_id).first()
    if dbfile is None:
        raise HTTPException(status_code=404, detail="File not found in database")
    return (dbfile.filepath,dbfile.filename)

def delete_file(file_id :str,db:"Session") -> str:
    dbfile = db.query(_models.File).filter(_models.File.id==file_id).first()
    if dbfile is None:
        raise HTTPException(status_code=404, detail="File not found in database")

    file_path = Path(dbfile.filepath)
    file_path.unlink(missing_ok=True)

    db.delete(dbfile)
    db.commit()

    return "deleted:   "+dbfile.filename


#filesystem services 

def resolve_path_to_folder(path_str: str | None, db: "Session") -> _models.Folder | None:
    if not path_str:
        return None
    
    parts = [p for p in path_str.split("/") if p]
    current_parent_id = None
    current_folder = None
    
    for part in parts:
        current_folder = db.query(_models.Folder).filter(
            _models.Folder.parent_folder_id == current_parent_id,
            _models.Folder.name == part
        ).first()
        if current_folder is None:
            raise HTTPException(status_code=404, detail=f"Folder '{part}' not found")
        current_parent_id = current_folder.id
        
    return current_folder


def create_folder(name: str, parent_folder_id: str | None, db: "Session") -> _schemas.Folder:
    if not name or "/" in name:
        raise HTTPException(status_code=400, detail="Invalid folder name")
    
    parent_uuid = uuid.UUID(parent_folder_id) if parent_folder_id else None

    # Check uniqueness
    existing = db.query(_models.Folder).filter(
        _models.Folder.parent_folder_id == parent_uuid,
        _models.Folder.name == name
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Folder already exists")
        
    folder_id = str(uuid.uuid4())
    db_folder = _models.Folder(
        id=folder_id,
        name=name,
        parent_folder_id=parent_uuid
    )
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return _schemas.Folder.model_validate(db_folder)


def get_folder_contents(folder_id: str | None, db: "Session"):
    folder_uuid = uuid.UUID(folder_id) if folder_id else None
    
    folders = db.query(_models.Folder).filter(
        _models.Folder.parent_folder_id == folder_uuid
    ).order_by(_models.Folder.name).all()
    
    files = db.query(_models.File).filter(
        _models.File.parent_folder_id == folder_uuid
    ).order_by(_models.File.filename).all()
    
    return folders, files


def delete_folder_recursive(folder_id: str, db: "Session"):
    folder_uuid = uuid.UUID(folder_id) if isinstance(folder_id, str) else folder_id
    
    # Find this folder
    folder = db.query(_models.Folder).filter(_models.Folder.id == folder_uuid).first()
    if folder is None:
        raise HTTPException(status_code=404, detail="Folder not found")
        
    # Find all child subfolders
    child_folders = db.query(_models.Folder).filter(_models.Folder.parent_folder_id == folder_uuid).all()
    for child in child_folders:
        delete_folder_recursive(child.id, db)
        
    # Find all files directly in this folder
    files = db.query(_models.File).filter(_models.File.parent_folder_id == folder_uuid).all()
    for file in files:
        # delete physical file
        file_path = Path(file.filepath)
        file_path.unlink(missing_ok=True)
        # delete DB record
        db.delete(file)
        
    # Finally delete the folder itself
    db.delete(folder)
    db.commit()


if __name__ == "__main__":
    _add_tables()