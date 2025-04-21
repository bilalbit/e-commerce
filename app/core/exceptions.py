from fastapi import HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError, NoResultFound


async def catch_integrity_error():
    try:
        yield
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=e.args[0])


async def catch_no_result_found():
    try:
        yield
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=e.args[0])


exception_dependencies = [Depends(catch_integrity_error), Depends(catch_no_result_found)]
