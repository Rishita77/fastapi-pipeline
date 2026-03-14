from fastapi import APIRouter, Depends, Query
from app.database import SalesORM, get_db
from typing import Optional
from sqlalchemy.orm import Session

router = APIRouter(prefix="/results", tags=["Results"])
    
async def get_results(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(None, description="Filter results by region"),
    limit: int = Query(50, le=500),
    skip: int = Query(0)
):
    """Fetch processed pipeline results with optional filters

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).
        region (str, optional): _description_. Defaults to Optional[str]=Query(None, description="Filter results by region").
        limit (int, optional): _description_. Defaults to Query(50, le=500).
        skip (int, optional): _description_. Defaults to Query(0, ge=0).
    """
    
    db_query = db.query(SalesORM)
    if region:
        db_query = db_query.filter(SalesORM.region == region)
    results = db_query.offset(skip).limit(limit).all()
    return results


    
    


