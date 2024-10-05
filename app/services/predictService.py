import os
from app.services.DataPreprocessor import DataPreprocessor
from app.services.NeuronalNetwork.PredictModel import PredictModel

class PredictService:

    def predict_daily(longitude, latitude):
        longitude = float(longitude)
        latitude = float(latitude)

        csv_folder_path = 'csvFiles'
        model_folder_path = 'IA_Models'

        csv_file_name = f"{longitude:.6f}_{latitude:.6f}.csv"
        model_file_name = f"{longitude:.6f}_{latitude:.6f}_T2M.keras"  # Suponiendo que el parámetro es 'T2M' para el modelo

        csv_full_path = os.path.join(csv_folder_path, csv_file_name)
        model_full_path = os.path.join(model_folder_path, model_file_name)

        # Verificar si el CSV y el modelo existen
        csv_exists = os.path.exists(csv_full_path)
        model_exists = os.path.exists(model_full_path)

        if not csv_exists:
            return {'error': True, 'message': f'The CSV {csv_file_name} doesnt exists'}
        if not model_exists:
            return {'error': True, 'message': f'The model {model_file_name} doesnt exists'}
        
        series = DataPreprocessor.get_series(csv_full_path, 'T2M')

        next_week_predictions = PredictModel.predict_next_week(model_full_path, series['series'], sequence_length = 7)
        #PredictModel.show_predictions(next_week_predictions)
        result_safe = [float(pred) for pred in next_week_predictions]
        return {'error': False, 'predictions': result_safe}