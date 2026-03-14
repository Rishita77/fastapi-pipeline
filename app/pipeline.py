import pandas as pd
from app.models import SalesRecord
from typing import List
from pandas import DataFrame
from datetime import datetime

def validate_and_clean(records : List[SalesRecord]) -> pd.DataFrame:
    
    data = [record.model_dump() for record in records]
    df = pd.DataFrame(data)
    
    df["product_name"] = df["product_name"].str.strip().str.title()
    df["region"] = df["region"].str.strip().str.upper()
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    
    return df

def enrich_data(df: DataFrame) -> DataFrame:
    df["total_sales"] = df["quantity"] * df["price"]
    df["processed_at"] = datetime.now(datetime.now().astimezone().tzinfo)
    return df

def filter_anomalies(df: DataFrame) -> DataFrame:
    if len(df) < 2:
        return df
    threshold = df["total_sales"].mean() + (3 * df["total_sales"].std())
    cleaned = df[df["total_sales"] <= threshold]
    return cleaned

def process_pipeline(records: List[SalesRecord]) -> DataFrame:
    df = validate_and_clean(records)
    df = enrich_data(df)
    df = filter_anomalies(df)
    return df