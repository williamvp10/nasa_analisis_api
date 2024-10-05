from fastapi import APIRouter, Depends, HTTPException
from app.services.nasaService import NasaService
from app.services.predictService import PredictService
import numpy as np

router = APIRouter()

@router.post("/trainModel/")
def train_model(longitude: float, latitude: float):
    return NasaService.get_power_api(20180101, 20241003, longitude, latitude, 'daily', 'csv')

@router.get("/tomorrowPrediction")
def tomorrow_prediction(longitude: float, latitude: float):
    result = PredictService.tomorrow_prediction(longitude, latitude)
    return result

@router.get("/weekPrediction")
def week_prediction(longitude: float, latitude: float):
    result = PredictService.much_days_prediction(longitude, latitude, 15, 7)
    return result

@router.get("/monthPrediction")
def month_prediction(longitude: float, latitude: float):
    result = PredictService.much_days_prediction(longitude, latitude, 30, 30)
    return result

@router.get("/cuarterPrediction")
def cuarter_prediction(longitude: float, latitude: float):
    result = PredictService.much_days_prediction(longitude, latitude, 90, 90)
    return result