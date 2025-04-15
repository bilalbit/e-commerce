from contextvars import ContextVar
from typing import Annotated

from fastapi import Depends

from app.modules.auth.services import verify_token, token_dependency

current_user_context: ContextVar[dict | None] = ContextVar("current_user_context", default=None)


async def get_current_user(token: token_dependency) -> dict | None:
    user = verify_token(token)
    current_user_context.set(
        {
            "username": user["username"],
            "id": user["id"],
            "role": user["role"]
        }
    )
    return current_user_context.get()
current_user_dependency = Annotated[dict, Depends(get_current_user)]


def get_current_user_data():
    return current_user_context.get()
