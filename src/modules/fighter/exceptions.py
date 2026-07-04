from fastapi import HTTPException,status

class FighterError(HTTPException):
    status_code:int=status.HTTP_500_INTERNAL_SERVER_ERROR
    def __init__(self,detail:str):
        super().__init__(
            status_code=self.status_code,
            detail=detail
        )


class FighterExistsError(FighterError):
    status_code=status.HTTP_409_CONFLICT
        
class FighterNotFoundError(FighterError):
    status_code=status.HTTP_404_NOT_FOUND


