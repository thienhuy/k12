from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from fastcrud.exceptions.http_exceptions import ForbiddenException
from pydantic import BaseModel
import json
import os
import shutil

from app.api.dependencies import AdminRoleDep, CurrentUserDep, SessionDep
from app.core.message import ErrorMsg
from app.services.chat import crud_chat
from app.schemas.chat import ChatResponse, FileUploadResponse, FileListResponse, UpdateDisabledRequest, DeleteFileRequest

router = APIRouter(tags=["chat"])

@router.post("/uploadfiles", response_model=List[FileUploadResponse], dependencies=[AdminRoleDep])
async def upload_files(db: SessionDep, files: List[UploadFile] = File(...)):
    upload_results = []
    for file in files:
        try:
            # Check if file already exists in database
            if await crud_chat.file_exists(db=db, filename=file.filename):
                raise HTTPException(status_code=400, detail=ErrorMsg.DUPLICATE_FILE)

            # Save file to filesystem and database
            file_path = await crud_chat.save_file(db=db, file=file)
            upload_results.append(FileUploadResponse(filename=file.filename, file_path=file_path))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file {file.filename}: {str(e)}")
    return upload_results

@router.post("/chat", response_model=ChatResponse, dependencies=[CurrentUserDep])
async def chat(db: SessionDep, data: dict, current_user: CurrentUserDep):
    # Ensure only the current user can query their own chat data
    html_text = await crud_chat.query_ai(db=db, question=data.get("question"), user_id=current_user["sub"])
    return ChatResponse(message=html_text)

@router.get("/getfilelist", response_model=PaginatedListResponse[FileListResponse], dependencies=[AdminRoleDep])
async def get_file_list(db: SessionDep, page: int = 1, limit: int = 10):
    files = await crud_chat.get_file_list(
        db=db,
        offset=compute_offset(page, limit),
        limit=limit,
        schema_to_select=FileListResponse
    )
    return paginated_response(files, page, limit)

@router.post("/deletefile", response_model=None, dependencies=[AdminRoleDep])
async def delete_file(db: SessionDep, request: DeleteFileRequest):
    await crud_chat.delete_file(db=db, identifier=request.identifier, by_id=request.by_id)
    return None

@router.post("/update_disabled", response_model=None, dependencies=[AdminRoleDep])
async def update_disabled(db: SessionDep, request: UpdateDisabledRequest):
    await crud_chat.update_disabled_status(db=db, identifier=request.identifier, disabled=request.disabled, by_id=request.by_id)
    return None