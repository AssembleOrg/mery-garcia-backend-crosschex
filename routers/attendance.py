from fastapi import APIRouter, HTTPException, Query
from services.attendance_service import AttendanceService

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

service = AttendanceService()

@router.get("/report")
def get_report(
    start_date: str = Query(..., description="Fecha inicio (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Fecha fin (YYYY-MM-DD)")
):
    try:
        # Se asegura que se pase el formato adecuado
        if "T" not in start_date:
            start_date = f"{start_date}T00:00:00+00:00"
        if "T" not in end_date:
            end_date = f"{end_date}T23:59:59+00:00"

        report = service.get_report(start_date, end_date)
        
        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))