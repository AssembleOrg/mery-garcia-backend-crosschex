import os
import requests
from dotenv import load_dotenv
from models.schemas import AttendanceRecordDTO 
import datetime
import uuid

load_dotenv()

class CrossChexRepository:
    def __init__(self):
        self.api_key = os.getenv("CROSSCHEX_API_KEY")
        self.api_secret = os.getenv("CROSSCHEX_API_SECRET")
        self.base_url = os.getenv("CROSSCHEX_API_URL")
        self.token = None 
        
        self.headers = {
            "Content-Type": "application/json"
        }

    def authenticate(self):
        url = self.base_url 

        current_time = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
        
        body_structure = {
            "header": {
                "nameSpace": "authorize.token", 
                "nameAction": "token",          
                "version": "1.0",
                "requestId": str(uuid.uuid4()),
                "timestamp": current_time
            },
            "payload": {
                "api_key": self.api_key,      
                "api_secret": self.api_secret
            }
        }

        try:
            response = requests.post(url, json=body_structure, headers=self.headers)
            response.raise_for_status() 

            data = response.json()
            
            self.token = data["payload"]["token"]
            
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error al autenticar: {e}")
            return False

    def get_attendance_records(self, start_date: str, end_date: str, page: int = 1):
        if not self.token:
            if not self.authenticate():
                return []

        url = self.base_url
        request_id = str(uuid.uuid4())
        current_time = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')

        body_structure = {
            "header": {
                "nameSpace": "attendance.record", 
                "nameAction": "getrecord",        
                "version": "1.0",                 
                "requestId": request_id,          
                "timestamp": current_time         
            },
            "authorize": {
                "type": "token",              
                "token": self.token           
            },
            "payload": {
                "begin_time": start_date,     
                "end_time": end_date,         
                "order": "asc",               
                "page": page,                 
                "per_page": 100               
            }
        }

        try:
            response = requests.post(url, json=body_structure, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            raw_list = data.get("payload", {}).get("list", [])
            
            clean_records = []
            
            for item in raw_list:
                try:
                    dto = AttendanceRecordDTO(**item)
                    clean_records.append(dto)
                except Exception as e:
                    print(f"Error parseando un registro: {e}")
                    continue
            
            return clean_records

        except Exception as e:
            print(f"Error obteniendo registros: {e}")
            return []