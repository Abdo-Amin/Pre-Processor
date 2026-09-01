import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from os import listdir

from services import PDFToChromaETL

app = FastAPI(title = "Supermarket", version = "1.0", description = "PROJECT_DESCRIPTION")

origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://0.0.0.0:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

etl = PDFToChromaETL()


@app.post('/upload-file')
async def upload_file(uploaded_file: UploadFile = File(..., alias="file")):

    temp_folder_path = "./files/temp_files/"
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)

    file_path = os.path.join(temp_folder_path, uploaded_file.filename)
    content = await uploaded_file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    return {
        'uploaded': True,
        'message' : 'File Uploaded successfully'
    }

@app.get('/process-batch-files')
def process_batch_files():

    temp_folder_path = "./files/temp_files/"  
    files = listdir(temp_folder_path)
    if files:
        for fileName in files:
           file_path = os.path.join(temp_folder_path, fileName)
           etl.run(file_path)
        return {
        'uploaded': True,
        'message' : 'Files processed successfully'
    }
    else:   
        return {
        'uploaded': False,
        'message' : 'No files to be processed!'
    }

# @app.post('/process-lesson')
# def process_lesson(lesson: lesson):
#     """
#     process, and save a new lesson into db, update, delete from db.

#     Args:
#         lesson (lesson): lesson body.

#     Returns:
#         state (state): the lesson data and process result.
#     """
#     match lesson.status:
#         case "new":
#             """
#             Implement your logic here to process a new lesson. For example, you can call a function from the lesson_service to save the new lesson into the database.
#             """
#         case "update":
#             """
#             Implement your logic here to process an update to an existing lesson. For example, you can call a function from the lesson_service to update the lesson in the database.
#             """
            
#         case "delete":
#             """
#             Implement your logic here to process the deletion of a lesson. For example, you can call a function from the lesson_service to delete the lesson from the database.
#             """
            
#         case default:
#             return 0

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
