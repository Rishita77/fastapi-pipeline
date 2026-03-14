from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SalesRecord(BaseModel):
    sale_date: str
    product_name: str
    quantity: int = Field(0, ge=0, description="Quantity must be a non-negative integer")
    price: float = Field(1, gt=0, description="Price must be a positive number")
    region: str
    
class ProcessedRecord(BaseModel):
    id: int
    sale_date : datetime
    product_name: str
    quantity: int
    price: float
    region: str
    total_sales: float = Field(default=0.0)
    processed_at: datetime
    
class PipelineResponse(BaseModel):
    status: str
    message: str
    processed_records: int
    data: Optional[list[ProcessedRecord]] = None
    
    