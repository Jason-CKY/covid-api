from fastapi import APIRouter, status, Depends, HTTPException, Response
import schemas, database, models
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix = '/reports',
    tags = ['reports']
)

@router.get("/world", response_model=schemas.SummaryReport ,status_code=status.HTTP_200_OK)
async def get_world_summary(filter_date: date = date.today(), db: Session = Depends(database.get_db)):
    results = db.query(models.Report).filter(models.Report.date == filter_date)
    results = results.with_entities(
        func.sum(models.Report.confirmed).label("total_confirmed"),
        func.sum(models.Report.deaths).label("total_deaths"),
        func.sum(models.Report.recovered).label("total_recovered"),
        func.max(models.Report.last_update).label("last_update")
    ).first()
    # print(results)
    if None in results:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid date or data for this date not updated yet")

    
    return results

@router.get("/", response_model=List[schemas.ShowReport], status_code=status.HTTP_200_OK)
async def get_country_report(country_region: str, date_from: date, date_to: date, 
                            province_state: Optional[str] = None, db: Session = Depends(database.get_db)):
    results = db.query(models.Report).filter(models.Report.country_region == country_region)
    if not results.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reports from {country_region} not found")
    if province_state is not None:
        results = results.filter(models.Report.province_state == province_state)
        if not results.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reports from {country_region},{province_state} not found")

    results = results.filter(models.Report.date >= date_from, models.Report.date <= date_to).\
        group_by(models.Report.country_region, models.Report.province_state, models.Report.date).order_by(models.Report.date).\
            with_entities(
                models.Report.country_region,
                models.Report.province_state,
                func.max(models.Report.date).label("date"),
                func.max(models.Report.last_update).label('last_update'),
                func.avg(models.Report.lat).label('lat'),
                func.avg(models.Report.long_).label('long_'),
                func.sum(models.Report.confirmed).label('confirmed'),
                func.sum(models.Report.deaths).label('deaths'),
                func.sum(models.Report.recovered).label('recovered'),
                func.sum(models.Report.active).label('active'),
                func.sum(models.Report.incident_rate).label('incident_rate'),
                func.sum(models.Report.case_fatality_ratio).label('case_fatality_ratio'),
            )
    if not results.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No reports from {country_region} on the range {date_from} to {date_to} found")
    return results.all()


@router.post("/",response_model=schemas.Report, status_code=status.HTTP_201_CREATED)
async def create_report(request: schemas.ReportRequest, db: Session = Depends(database.get_db)):
    report = models.Report(
        country_region = request.country_region,
        province_state = request.province_state,
        date = request.date,
        last_update = datetime.now(),
        lat = request.lat,
        long_ = request.long_,
        confirmed = request.confirmed,
        deaths = request.deaths,
        recovered = request.recovered,
        active = request.active,
        incident_rate = request.incident_rate,
        case_fatality_ratio = request.case_fatality_ratio
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report

@router.get("/{id}", response_model=schemas.Report, status_code=status.HTTP_200_OK)
async def get_report(id: int, db: Session = Depends(database.get_db)):
    results = db.query(models.Report).filter(models.Report.reportid == id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reports with id={id} not found")
    return results

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(id: int, db: Session = Depends(database.get_db)):
    results = db.query(models.Report).filter(models.Report.reportid == id)
    if not results.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reports with id={id} not found")
    results.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_report(id: int, request: schemas.ReportRequest, db: Session = Depends(database.get_db)):
    results = db.query(models.Report).filter(models.Report.reportid == id)
    if not results.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reports with id={id} not found")
    results.update({
        models.Report.country_region: request.country_region,
        models.Report.province_state : request.province_state,
        models.Report.date : request.date,
        models.Report.last_update : datetime.now(),
        models.Report.lat : request.lat,
        models.Report.long_ : request.long_,
        models.Report.confirmed : request.confirmed,
        models.Report.deaths : request.deaths,
        models.Report.recovered : request.recovered,
        models.Report.active : request.active,
        models.Report.incident_rate : request.incident_rate,
        models.Report.case_fatality_ratio : request.case_fatality_ratio
    })
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

