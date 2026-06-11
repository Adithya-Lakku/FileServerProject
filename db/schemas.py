import datetime as _dt
import pydantic as _pydantic
from pydantic import UUID4 , ConfigDict

#config dict used for config files of each class model

class _BaseFile(_pydantic.BaseModel):
    filename : str
    filepath : str
    size_bytes : int
    date_created :_dt.datetime
    file_metadata : dict | None = None   #THIS MAKES IT NULLABLE



class File(_BaseFile):
    id: UUID4 

    #uploaded_by : int

    model_config = ConfigDict(from_attributes=True)

    
    
    
class File_id(_pydantic.BaseModel):
    id: UUID4

    
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
