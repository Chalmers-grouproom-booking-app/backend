from pydantic import BaseModel, Field, validator
from typing import List

class Login(BaseModel):
    login: str
    

class ReservationModel(BaseModel):
    id: str
    start_date: str = Field(..., alias="startdate")
    start_time: str = Field(..., alias="starttime")
    end_date: str = Field(..., alias="enddate")
    end_time: str = Field(..., alias="endtime")
    columns: List[str]

    # Custom validator for columns
    @validator('columns', pre=True)
    def split_columns(cls, v):
        if isinstance(v, str):
            return v.split(', ')
        return v

class AllReservations(BaseModel):
    reservations: List[ReservationModel]

    class Config:
        allow_population_by_field_name = True