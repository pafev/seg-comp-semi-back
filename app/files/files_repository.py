from sqlalchemy.orm import Session
from typing import Optional, List

from app.crypto import gen_keys, signature_validation
from app.files.files_interfaces import FileUpload
from app.models import File, User


def get_files_received(db: Session, receiver_id: int) -> List[File]:
    """
    Retrieve all files received by a specific user.

    :param db: Database session
    :param receiver_id: ID of the receiver
    :return: List of files received by the user
    """
    files = db.query(File).filter(File.receiver_id == receiver_id).all()

    print(files[0].receiver)

    return files


def get_file(db: Session, file_id: int) -> Optional[File]:
    """
    Retrieve a specific file by its ID.

    :param db: Database session
    :param file_id: ID of the file
    :return: File object if found, else None
    """
    return db.query(File).filter(File.id == file_id).first()


def upload_file(db: Session, file_upload: FileUpload) -> Optional[File]:
    """
    Upload a new file to the database.

    :param db: Database session
    :param file_upload: FileUpload object containing file details
    :return: Uploaded File object if successful, else None
    """
    receiver = db.query(User).filter(User.name == file_upload.receiver_name).first()
    if not receiver:
        return

    # Geração de chaves
    public_key, private_key = gen_keys.gen_keys()

    # Assinatura do arquivo
    signature = signature_validation.sign_message(file_upload.file_base64, private_key)

    db_file_upload = File(
        file_name=file_upload.file_name,
        file_base64=file_upload.file_base64,
        file_type=file_upload.file_type,
        sender_id=file_upload.sender_id,
        receiver_id=receiver.id,
        signature=signature,
        public_key=str(public_key),
    )
    db.add(db_file_upload)
    db.commit()
    db.refresh(db_file_upload)
    return db_file_upload


def verify_file(db: Session, file_id: int) -> Optional[File]:
    """
    Verify the digital signature of a file.

    :param db: Database session
    :param file_id: ID of the file to verify
    :return: File object if the signature is valid, else None
    """
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        return

    public_key = eval(f"{file.public_key}")
    is_valid = signature_validation.verify_message(
        f"{file.file_base64}", f"{file.signature}", public_key
    )

    if is_valid:
        return file
