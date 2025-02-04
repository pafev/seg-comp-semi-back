from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.files import files_interfaces, files_repository
from app.users import users_repository


router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/receiver_id/{receiver_id}", response_model=List[files_interfaces.File])
def get_files_by_receiver(receiver_id: int, db: Session = Depends(get_db)):
    if not (users_repository.get_user(db=db, user_id=receiver_id)):
        raise HTTPException(status_code=400, detail="Usuario nao existe")
    files = files_repository.get_files_received(db=db, receiver_id=receiver_id)
    return files


@router.get("/file_id/{file_id}", response_model=files_interfaces.File)
def get_file(file_id: int, db: Session = Depends(get_db)):
    file = files_repository.get_file(db=db, file_id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Arquivo nao encontrado")
    return file


@router.post("/upload", response_model=files_interfaces.File)
def upload_file(
    file_upload: files_interfaces.FileUpload, db: Session = Depends(get_db)
):
    new_file = files_repository.upload_file(db=db, file_upload=file_upload)
    if not new_file:
        raise HTTPException(
            status_code=400,
            detail="Nao foi possivel criar. Verifique se o usuario passado existe",
        )
    return new_file


@router.get("/verify/file_id/{file_id}", response_model=files_interfaces.File)
def verify_file(file_id: int, db: Session = Depends(get_db)):
    file_verified = files_repository.verify_file(db=db, file_id=file_id)
    if not file_verified:
        raise HTTPException(
            status_code=400, detail="Arquivo nao verificado corretamente"
        )
    return file_verified
