from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SalesRecord(BaseModel):
    sale_date: str
    product_name: str
    quantity: int
    price: float
    region: str
    
    def quantity_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Quantity must be a positive integer')
        return value
    
    def price_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Price must be a positive number')
        return value
    
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
    
    