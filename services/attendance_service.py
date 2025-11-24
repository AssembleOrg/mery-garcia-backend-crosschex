from datetime import datetime, date
from typing import List, Dict
from repositories.crosschex_repository import CrossChexRepository
from models.schemas import AttendanceRecordDTO
import arrow

class AttendanceService:
    def __init__(self):
        self.repository = CrossChexRepository()

    def get_report(self, start_date: str, end_date: str):
        records = self.repository.get_attendance_records(start_date, end_date)
        
        report = self._calculate_hours(records)
        return report

    def _calculate_hours(self, records):
        grouped_data = {}

        for record in records:
            emp_id = record.employee.workno
            emp_name = f"{record.employee.first_name} {record.employee.last_name}"
            
            fecha_arrow = arrow.get(record.checktime).to('America/Argentina/Buenos_Aires')
            
            day_key = fecha_arrow.format('YYYY-MM-DD') 
            
            if emp_id not in grouped_data:
                grouped_data[emp_id] = {"name": emp_name, "days": {}}
            
            if day_key not in grouped_data[emp_id]["days"]:
                grouped_data[emp_id]["days"][day_key] = []

            grouped_data[emp_id]["days"][day_key].append(fecha_arrow)

        final_report = []
        
        for emp_id, data in grouped_data.items():
            emp_report = {
                "id": emp_id,
                "name": data["name"],
                "details": []
            }
            
            for day_key, times in data["days"].items():
                times.sort()
                
                entrada = times[0]
                salida = times[-1]
                
                horas_trabajadas = 0
                if len(times) > 1:
                    diff = salida - entrada 
                    horas_trabajadas = diff.total_seconds() / 3600
                
                emp_report["details"].append({
                    "date": entrada.format('DD/MM/YYYY'), 
                    "entry": entrada.format('HH:mm:ss'),
                    "exit": salida.format('HH:mm:ss'),
                    "hours": round(horas_trabajadas, 2)
                })
            
            final_report.append(emp_report)
            
        return final_report