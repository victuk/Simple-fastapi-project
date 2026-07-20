from fastapi import APIRouter, UploadFile, File
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

file_upload_route = APIRouter(
    prefix="/file-uploads",
    tags=["File Uploads"]
)

s3_client = boto3.client(
    "s3"
)



@file_upload_route.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    
    bucket = os.getenv("BUCKET")
    
    file_content = await file.read()
    
    file_key = file.filename
    
    s3_client.put_object(
        Bucket=bucket,
        Key=file_key,
        Body=file_content,
        ContentType=file.content_type
    )
    
    print(file)
    
    
    return {
        "message": "File uploaded successfully",
        "file_name": f'https://{bucket}.fly.storage.tigris.dev/{file_key}'
    }
    
