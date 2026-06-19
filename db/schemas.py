import datetime as _dt
import pydantic as _pydantic
from pydantic import UUID4 , ConfigDict

#config dict used for config files of each class model

class FolderCreate(_pydantic.BaseModel):
    name: str
    parent_folder_id: UUID4 | None = None

class Folder(FolderCreate):
    id: UUID4
    date_created: _dt.datetime

    model_config = ConfigDict(from_attributes=True)


class _BaseFile(_pydantic.BaseModel):
    filename : str
    filepath : str
    size_bytes : int
    date_created :_dt.datetime
    file_metadata : dict | None = None   #THIS MAKES IT NULLABLE
    parent_folder_id : UUID4 | None = None



class File(_BaseFile):
    id: UUID4 

    #uploaded_by : int

    model_config = ConfigDict(from_attributes=True)

    
    
    
class FileSummary(_pydantic.BaseModel):
    id: UUID4
    filename: str
    parent_folder_id: UUID4 | None = None

    model_config = ConfigDict(from_attributes=True)

    
    """class User(_pydantic.BaseModel):
        id : int

        username : str
        password_hash : str

        model_config = ConfigDict(from_attributes=True) let me save it for later




    i might have to seperate users between (id,username ) and (username,password) as one class





    """



#reference that i used 
# class _BaseContact(_pydantic.BaseModel):
#     first_name:str
#     #last_name:str
#     email:str
#     phone_number:str


# class Contact(_BaseContact):
#     id:int
#     date_created: _dt.datetime

#     class Config:
#         orm_mode = True
#         from_attributes=True
