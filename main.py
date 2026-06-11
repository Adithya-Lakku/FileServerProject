from fastapi import FastAPI,UploadFile,HTTPException,Request,Form
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
import sqlalchemy.orm as _orm
from db import services as _services
from typing import Annotated




app = FastAPI()

"""UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok = True)   #creates directory if true"""

DbSession = Annotated[_orm.Session,FastAPI.Depends(_services.get_db)] #this shit only helps with pydantic hints but why not


#upload endpnt

@app.post("/upload")
async def upload_file(file:UploadFile,request:Request,db:DbSession ):
    
    
    
    
    """    file_id = str(uuid.uuid4())

        original_name = Path(file.filename).name  #to avoid pathinjection
        


        save_path = UPLOAD_DIR / f"{file_id}_{original_name}"


        try:
            # Fetch the file size in bytes
            file_size_bytes = save_path.stat().st_size
            print(f"File size: {file_size_bytes} bytes")
        except FileNotFoundError:
            print("The specified file does not exist.")
        

        with open(save_path,"wb") as f:
            while chunk := await file.read(12500 * 12500):  # 100 mb reads (can be increased for faster)
                f.write(chunk)
                 # processing now in services.py
                """
    

        
    """    return {"file_id":file_id,
                "filename":original_name
                
                }
    """

    original_name = Path(file.filename).name
    await _services.create_file(file=file,db=DbSession)


    return templates.TemplateResponse(
    request=request,
    name="upload.html",
    context={"filename":original_name}
    )


#list files

@app.get("/files")
def list_file(request:Request):

    try:
        files = _services.get_files(db=DbSession)
        print("file success")
    except FileNotFoundError:
        print("couldnt find file")
        

    """  for f in UPLOAD_DIR.iterdir():
            if f.is_file():
                files.append(f.name)  
                """
            
            
            
                              #needs to be changed to show thumbnail
    
    
    return templates.TemplateResponse(
    request=request,
    name="files.html",
    context={"files": files}
)


templates = Jinja2Templates(directory="templates")

#download
@app.post("/download")
def download_file(file_id: str = Form(...)):
    # Prevent path traversal attacks
    print("I GOT HERE")


    #filename = Path(filename).name
    

    file_path , filename = _services.download_file(file_id=file_id,db=DbSession)
    

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=filename
    )
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


if __name__ == '__main__':
    #uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)
    uvicorn.run(app,host="0.0.0.0",port=8000)