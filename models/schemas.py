from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EmployeeDTO(BaseModel):
    first_name: str
    last_name: str
    workno: str  
    department: Optional[str] = None

class AttendanceRecordDTO(BaseModel):
    uuid: str
    checktime: datetime 
    employee: EmployeeDTO
    device_name: str = Field(alias="device.name", default="Desconocido")

    class Config:
        extra = "ignore"