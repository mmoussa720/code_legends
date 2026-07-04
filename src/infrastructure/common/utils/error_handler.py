from fastapi import HTTPException





def handle_exception(error:Exception)->HTTPException|None:
    if isinstance(error,HTTPException):
        return error
    return None