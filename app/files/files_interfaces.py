from pydantic import BaseModel


class FileUpload(BaseModel):
    """
    Pydantic model for file upload details.
    """

    file_name: str
    file_base64: str
    file_type: str
    receiver_name: str
    sender_id: int


class File(BaseModel):
    """
    Pydantic model for file details.
    """

    id: int
    file_name: str
    file_base64: str
    file_type: str
    receiver_id: int
    sender_id: int
    signature: str
    public_key: str

    class Config:
        from_attributes = True
