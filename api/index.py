from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import os
from datetime import datetime

app = FastAPI(
    title="US Money Supply API",
    description="Real-time US money supply data including M1, M2, monetary base, and velocity. Powered by FRED (Federal Reserve Economic Data).",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
API_KEY = os.environ.get("FRED_API_KEY", "")


async def fetch_fred(series_id: str, limit: int = 12):
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.get(BASE_URL, params={
            "series_id": series_id,
            "api_key": API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": limit,
        })
        data = res.json()
        return data.get("observations", [])


@app.get("/")
def root():
    return {
        "api": "US Money Supply API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "endpoints": ["/summary", "/m1", "/m2", "/monetary-base", "/velocity-m1", "/velocity-m2"],
        "updated_at": datetime.utcnow().isoformat(),
    }


@app.get("/summary")
async def summary(limit: int = Query(default=10, ge=1, le=60)):
    """All money supply indicators snapshot"""
    m1, m2, monetary_base = await asyncio.gather(
        fetch_fred("M1SL", limit),
        fetch_fred("M2SL", limit),
        fetch_fred("BOGMBASE", limit),
    )
    return {
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": {
            "m1": m1,
            "m2": m2,
            "monetary_base": monetary_base,
        }
    }


@app.get("/m1")
async def m1(limit: int = Query(default=12, ge=1, le=60)):
    """M1 money supply"""
    data = await fetch_fred("M1SL", limit)
    return {
        "indicator": "M1 Money Stock",
        "series_id": "M1SL",
        "unit": "Billions of Dollars",
        "frequency": "Monthly",
        "source": "FRED - Federal Reserve",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/m2")
async def m2(limit: int = Query(default=12, ge=1, le=60)):
    """M2 money supply"""
    data = await fetch_fred("M2SL", limit)
    return {
        "indicator": "M2 Money Stock",
        "series_id": "M2SL",
        "unit": "Billions of Dollars",
        "frequency": "Monthly",
        "source": "FRED - Federal Reserve",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/monetary-base")
async def monetary_base(limit: int = Query(default=12, ge=1, le=60)):
    """US monetary base"""
    data = await fetch_fred("BOGMBASE", limit)
    return {
        "indicator": "Monetary Base; Total",
        "series_id": "BOGMBASE",
        "unit": "Billions of Dollars",
        "frequency": "Monthly",
        "source": "FRED - Federal Reserve",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/velocity-m1")
async def velocity_m1(limit: int = Query(default=12, ge=1, le=60)):
    """Velocity of M1 money stock"""
    data = await fetch_fred("M1V", limit)
    return {
        "indicator": "Velocity of M1 Money Stock",
        "series_id": "M1V",
        "unit": "Ratio",
        "frequency": "Quarterly",
        "source": "FRED - Federal Reserve",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/velocity-m2")
async def velocity_m2(limit: int = Query(default=12, ge=1, le=60)):
    """Velocity of M2 money stock"""
    data = await fetch_fred("M2V", limit)
    return {
        "indicator": "Velocity of M2 Money Stock",
        "series_id": "M2V",
        "unit": "Ratio",
        "frequency": "Quarterly",
        "source": "FRED - Federal Reserve",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }
