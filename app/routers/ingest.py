from app.models import PipelineResponse, SalesRecord
from app.database import get_db, SalesORM
from app.pipeline import process_pipeline
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.pipeline import process_pipeline
from sqlalchemy.orm import Session

router = APIRouter(prefix="/ingest", tags=["Ingest"])
@router.post("/", response_model=PipelineResponse)
async def ingest_sales_data(records: List[SalesRecord], db: Session = Depends(get_db)):
    """Accepts a batch of sales records, processes them through the pipeline, and stores the results in the database.

    Args:
        records (List[SalesRecord]): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
    
    if not records:
        raise HTTPException(status_code=400, detail="No records provided")
    
    try:
        df = process_pipeline(records)
        print(f"Processed {len(df)} records through the pipeline")
        
        saved = []
        
        for _, row in df.iterrows():
            record = SalesORM(
                product_name=row["product_name"],
                quantity=row["quantity"],
                price=row["price"],
                region=row["region"],
                sale_date=row["sale_date"],
                total_value=row["total_sales"],
                processed_at=row["processed_at"]
            )
            db.add(record)
            saved.append(record)
            
        db.commit()
        
        return PipelineResponse(
            status="success",
            message=f"Processed and saved {len(saved)} records",
            processed_records=len(saved),
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))