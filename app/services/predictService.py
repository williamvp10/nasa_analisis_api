import os
from app.services.DataPreprocessor import DataPreprocessor
from app.services.NeuronalNetwork.PredictModel import PredictModel
from app.services.nasaService import NasaService

class PredictService:

    def tomorrow_prediction(longitude, latitude):
        if not NasaService.evaluate_if_model_exists(longitude, latitude):
            return {'error': True, 'message': "Los modelos no existen"}
        
        parameters = ["T2M", "PRECTOTCORR", "WS10M", "RH2M"]
        all_predictions = []
        for param in parameters:
            csv_folder_path = 'csvFiles'
            model_folder_path = 'IA_Models'

            csv_file_name = f"{longitude:.6f}_{latitude:.6f}.csv"
            csv_full_path = os.path.join(csv_folder_path, csv_file_name)

            model_file_name = f"{longitude:.6f}_{latitude:.6f}_{param}.keras"
            model_full_path = os.path.join(model_folder_path, model_file_name)

            series = DataPreprocessor.get_series(csv_full_path, param)
            predictions = PredictModel.prediction(model_full_path, series['series'], sequence_length = 7, prediction_number=4)
            #PredictModel.show_predictions(next_week_predictions)
            result_safe = [float(pred) for pred in predictions]
            result_safe = result_safe[-1]
            all_predictions.append(result_safe)
        
        return {'error': False, 'predictions': all_predictions}

    def much_days_prediction(longitude, latitude, sequence_length, prediction_number):
        if not NasaService.evaluate_if_model_exists(longitude, latitude):
            return {'error': True, 'message': "Los modelos no existen"}
        
        parameters = ["T2M", "PRECTOTCORR", "WS10M", "RH2M"]
        all_predictions = []
        for param in parameters:
            csv_folder_path = 'csvFiles'
            model_folder_path = 'IA_Models'

            csv_file_name = f"{longitude:.6f}_{latitude:.6f}.csv"
            csv_full_path = os.path.join(csv_folder_path, csv_file_name)

            model_file_name = f"{longitude:.6f}_{latitude:.6f}_{param}.keras"
            model_full_path = os.path.join(model_folder_path, model_file_name)

            series = DataPreprocessor.get_series(csv_full_path, param)
            predictions = PredictModel.prediction(model_full_path, series['series'], sequence_length, prediction_number)
            #PredictModel.show_predictions(next_week_predictions)
            result_safe = [float(pred) for pred in predictions]
            all_predictions.append(PredictService.prediction_average(result_safe))
        
        return {'error': False, 'predictions': all_predictions}
    
    

    def prediction_average(lst):
        if not lst:
            return {'min': None, 'max': None, 'average': None}  # Manejo de caso si la lista está vacía
        
        print("Average for: ", len(lst))

        min_value = min(lst)  # Obtener el valor mínimo
        max_value = max(lst)  # Obtener el valor máximo
        average_value = sum(lst) / len(lst)  # Calcular el promedio

        return {
            'min': min_value,
            'max': max_value,
            'average': average_value
        }

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

        next_week_predictions = PredictModel.prediction(model_full_path, series['series'], sequence_length = 7, prediction_number=4)
        #PredictModel.show_predictions(next_week_predictions)
        result_safe = [float(pred) for pred in next_week_predictions]
        return {'error': False, 'predictions': result_safe}