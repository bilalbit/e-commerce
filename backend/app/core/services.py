import uuid
from typing import TypeVar, Type

from fastapi import HTTPException, status
from sqlmodel import SQLModel

from app.database import session

T = TypeVar("T", bound=SQLModel)


def get_record_by_id(
        record_id: uuid.UUID,
        model: Type[T],
        message:str
) -> T:
    with session:
        records = session.get(model, record_id)
        if not records:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{message} is not found')

        return records
