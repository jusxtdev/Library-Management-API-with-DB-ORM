from pydantic import BaseModel

class BookCreate(BaseModel):
    title : str
    price : float

class BookResponse(BaseModel):
    book_id : int
    title : str
    price : float

    ## Add this to give permission to return ORM objects through Pydantic
    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title : str | None = None
    price : float | None = None