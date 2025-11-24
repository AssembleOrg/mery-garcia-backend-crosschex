from datetime import datetime, date
from typing import List, Dict
from repositories.crosschex_repository import CrossChexRepository
from models.schemas import AttendanceRecordDTO

class AttendanceService:
    def __init__(self):
        self.repository = CrossChexRepository()

    def get_report(self, start_date: str, end_date: str):
        records = self.repository.get_attendance_records(start_date, end_date)
        
        report = self._calculate_hours(records)
        return report

    def _calculate_hours(self, records: List[AttendanceRecordDTO]):
        grouped_data = {}

        #Agrupación
        for record in records:
            emp_id = record.employee.workno
            emp_name = f"{record.employee.first_name} {record.employee.last_name}"
            day = record.checktime.date() # Solo la fecha (2025-10-01)
            
            # se crea id si no existe
            if emp_id not in grouped_data:
                grouped_data[emp_id] = {"name": emp_name, "days": {}}
            
            if day not in grouped_data[emp_id]["days"]:
                grouped_data[emp_id]["days"][day] = []

            # agrego la hora a ese día
            grouped_data[emp_id]["days"][day].append(record.checktime)

        # PASO B: Cálculo (Min/Max)
        final_report = []
        
        for emp_id, data in grouped_data.items():
            emp_report = {
                "id": emp_id,
                "name": data["name"],
                "details": []
            }
            
            for day, times in data["days"].items():
                # se ordena las horas
                times.sort()
                
                entrada = times[0]  # primera fichada
                salida = times[-1]  # última fichada
                
                # si fichó una vez, entrada y salida son iguales (0 horas)
                horas_trabajadas = 0
                if len(times) > 1:
                    diff = salida - entrada
                    horas_trabajadas = diff.total_seconds() / 3600 # Convertir a horas
                
                emp_report["details"].append({
                    "date": day,
                    "entry": entrada.strftime("%H:%M:%S"),
                    "exit": salida.strftime("%H:%M:%S"),
                    "hours": round(horas_trabajadas, 2)
                })
            
            final_report.append(emp_report)
            
        return final_report