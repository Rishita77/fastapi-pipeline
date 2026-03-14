import io, csv
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from app.routers.ingest import ingest_sales_data
from app.models import PipelineResponse, ProcessedRecord, SalesRecord
from app.database import Base, get_db, SalesORM, engine
from sqlalchemy.orm import Session

app = FastAPI(
    title="Sales Data API",
    description="API for ingesting and retrieving sales data processed through a data pipeline.",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to the Sales API!"}

@app.post("/ingest/record", response_model=PipelineResponse)
async def create_sale(sale: SalesRecord, db: Session = Depends(get_db)):
    """Submit a single sale record
    FastAPI validates the body against SaleRecord before this function runs.

    Args:
        sale (SalesRecord): The sale record to create
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        SalesRecord: The created sale record
    """
    from app.routers.ingest import ingest_sales_data
    response = await ingest_sales_data([sale], db)
    return response

@app.post("/ingest/batch", response_model=PipelineResponse)
async def create_sales_batch(sales: list[SalesRecord], db: Session = Depends(get_db)):
    """Submit a batch of sale records

    Args:
        sales (list[SalesRecord]): The list of sale records to create
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list[SalesRecord]: The created sale records
    """
    from app.routers.ingest import ingest_sales_data
    response = await ingest_sales_data(sales, db)
    return response

@app.post("/ingest/upload", response_model=PipelineResponse)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a CSV file containing sales records. Expected columns: sale_date, product_name, quantity, price, region

    Args:
        file: The CSV file to upload
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list[SalesRecord]: The created sale records from the CSV
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    
    records : list[SalesRecord] = []
    for row in reader:
        try:
            records.append(SalesRecord(**row))
        except Exception as e:
            pass
        
    if not records:
        raise HTTPException(status_code=422, detail="No valid records found in the CSV")
    
    response = await ingest_sales_data(records, db)
    return response

@app.get("/results", response_model=list[ProcessedRecord])
async def read_results(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db), region: Optional[str] = None
):
    query = db.query(SalesORM)
    if region:
        query = query.filter(SalesORM.region == region.strip().title())
    return query.offset(skip).limit(limit).all()


