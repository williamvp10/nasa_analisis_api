from fastapi import APIRouter, Depends, HTTPException
from app.services.nasaService import NasaService
from app.services.predictService import PredictService
import numpy as np

router = APIRouter()

@router.post("/trainModel/")
def train_model(longitude: float, latitude: float):
    return NasaService.get_power_api(20240101, 20240929, longitude, latitude, 'daily', 'csv')

@router.get("/tomorrowPrediction")
def tomorrow_prediction(longitude: float, latitude: float):
    result = PredictService.predict_daily(longitude, latitude)
    return result

@router.get("/weekPrediction")
def week_prediction(longitude: float, latitude: float):
    result = PredictService.predict_daily(longitude, latitude)
    return result

@router.get("/monthPrediction")
def month_prediction(longitude: float, latitude: float):
    result = PredictService.predict_daily(longitude, latitude)
    return result

@router.get("/cuarterPrediction")
def cuarter_prediction(longitude: float, latitude: float):
    result = PredictService.predict_daily(longitude, latitude)
    return result