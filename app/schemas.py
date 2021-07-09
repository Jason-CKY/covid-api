from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class Report(BaseModel):
    reportid: int
    country_region: str
    province_state: Optional[str]
    date: date
    lat: Optional[float]
    long_: Optional[float]
    confirmed: Optional[int]
    deaths: Optional[int]
    recovered: Optional[int]
    active: Optional[int]
    incident_rate: Optional[float]
    case_fatality_ratio: Optional[float]

    class Config():
        orm_mode = True

class ShowReport(BaseModel):
    country_region: str
    province_state: Optional[str]
    date: date
    lat: Optional[float]
    long_: Optional[float]
    confirmed: Optional[int]
    deaths: Optional[int]
    recovered: Optional[int]
    active: Optional[int]
    incident_rate: Optional[float]
    case_fatality_ratio: Optional[float]

    class Config():
        orm_mode = True

class ReportRequest(BaseModel):
    country_region: str
    province_state: Optional[str]
    date: date
    lat: Optional[float]
    long_: Optional[float]
    confirmed: Optional[int]
    deaths: Optional[int]
    recovered: Optional[int]
    active: Optional[int]
    incident_rate: Optional[float]
    case_fatality_ratio: Optional[float]
    
    class Config():
        orm_mode = True

class SummaryReport(BaseModel):
    total_confirmed: int
    total_deaths: int
    total_recovered: int
    last_update: datetime

class SummaryCountryReport(BaseModel):
    country_region: str
    province_state: Optional[str]
    total_confirmed: int
    total_deaths: int
    total_recovered: int
    last_update: datetime
    