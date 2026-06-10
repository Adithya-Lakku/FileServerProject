from fastapi import FastAPI,UploadFile,HTTPException,Request,Form
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.templating import Jinja2Templates
import uuid
import uvicorn
import logging

logger = logging.getLogger(__name__)

#msg



app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok = True)   #creates directory if true


#upload endpnt

@app.post("/upload")
async def upload_file(file:UploadFile,request:Request):
    file_id = str(uuid.uuid1())

    original_name = Path(file.filename).name  #to avoid pathinjection

    save_path = UPLOAD_DIR / f"{file_id}_{original_name}"

    with open(save_path,"wb") as f:
        while chunk := await file.read(12500 * 12500):  # 1 mb reads (can be increased for faster)
            f.write(chunk)
    
    # return {"file_id":file_id,
    #         "filename":original_name
            
    #         }

    return templates.TemplateResponse(
    request=request,
    name="upload.html",
    context={"filename":original_name}
    )


#list files

@app.get("/files")
def list_file(request:Request):
    files = []

    for f in UPLOAD_DIR.iterdir():
        if f.is_file():
            files.append(f.name)  
            
            
            
            
                              #needs to be changed to show thumbnail
    return templates.TemplateResponse(
    request=request,
    name="files.html",
    context={"files": files}
)


templates = Jinja2Templates(directory="templates")

#download
@app.post("/download")
def download_file(filename: str = Form(...)):
    # Prevent path traversal attacks
    print("I GOT HERE")
    filename = Path(filename).name
    

    file_path = UPLOAD_DIR / filename
    

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