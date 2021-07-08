from fastapi import APIRouter, status, Depends, HTTPException, Response
import schemas, database, models
from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

router = APIRouter(
    prefix = '/daily',
    tags = ['daily']
)

@router.get("/world", response_model=schemas.SummaryReport ,status_code=status.HTTP_200_OK)
async def get_world_daily_summary(filter_date: date = date.today(), db: Session = Depends(database.get_db)):
    results_1 = db.query(models.Report).filter(models.Report.date == str(filter_date)).with_entities(
        func.sum(models.Report.confirmed).label("total_confirmed"),
        func.sum(models.Report.deaths).label("total_deaths"),
        func.sum(models.Report.recovered).label("total_recovered"),
        func.max(models.Report.last_update).label("last_update")
    ).first()

    results_2 = db.query(models.Report).filter(models.Report.date == str(filter_date - timedelta(days=1))).with_entities(
        func.sum(models.Report.confirmed).label("total_confirmed"),
        func.sum(models.Report.deaths).label("total_deaths"),
        func.sum(models.Report.recovered).label("total_recovered"),
        func.max(models.Report.last_update).label("last_update")
    ).first()

    if None in results_1 or None in results_2:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid date or data for this date not updated yet")

    calculated_results = {
        "total_confirmed": results_1['total_confirmed'] - results_2['total_confirmed'],
        "total_deaths": results_1['total_deaths'] - results_2['total_deaths'],
        "total_recovered": results_1['total_recovered'] - results_2['total_recovered'],
        "last_update": results_1['last_update']
    }

    return calculated_results


@router.get("/", response_model=schemas.SummaryCountryReport, status_code=status.HTTP_200_OK)
async def get_country_report(country_region: str, _date: Optional[date] = None, 
                            province_state: Optional[str] = None, db: Session = Depends(database.get_db)):
            
    filter_date = date.today() if _date is None else _date

    results_1 = db.query(models.Report).filter(models.Report.date == str(filter_date)).group_by(models.Report.country_region, models.Report.province_state)
    results_1 = results_1.having(models.Report.country_region == country_region) if province_state is None else \
                 results_1.having(models.Report.country_region == country_region).having(models.Report.province_state==province_state)

    results_1 = results_1.with_entities(
        models.Report.country_region,
        models.Report.province_state,
        func.sum(models.Report.confirmed).label("total_confirmed"),
        func.sum(models.Report.deaths).label("total_deaths"),
        func.sum(models.Report.recovered).label("total_recovered"),
        func.max(models.Report.last_update).label("last_update")
    ).first()

    if not results_1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reports from {country_region},{province_state} on {filter_date} not found")

    results_2 = db.query(models.Report).filter(models.Report.date == str(filter_date - timedelta(days=1))).group_by(models.Report.country_region, models.Report.province_state)
    results_2 = results_2.having(models.Report.country_region == country_region) if province_state is None else \
                 results_2.having(models.Report.country_region == country_region).having(models.Report.province_state==province_state)

    results_2 = results_2.with_entities(
        models.Report.country_region,
        models.Report.province_state,
        func.sum(models.Report.confirmed).label("total_confirmed"),
        func.sum(models.Report.deaths).label("total_deaths"),
        func.sum(models.Report.recovered).label("total_recovered"),
        func.max(models.Report.last_update).label("last_update")
    ).first()

    if not results_2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reports from {country_region},{province_state} on {filter_date - timedelta(days=1)} not found")

    if None in results_1[2:] or None in results_2[2:]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid date or data for this date not updated yet")

    calculated_results = {
        "country_region": results_1['country_region'],
        "province_state": results_1["province_state"],
        "total_confirmed": results_1['total_confirmed'] - results_2['total_confirmed'],
        "total_deaths": results_1['total_deaths'] - results_2['total_deaths'],
        "total_recovered": results_1['total_recovered'] - results_2['total_recovered'],
        "last_update": results_1['last_update']
    }

    return calculated_results
