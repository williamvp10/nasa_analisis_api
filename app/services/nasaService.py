import requests
import os

from app.services.DataPreprocessor import DataPreprocessor

class NasaService:

    @staticmethod
    def get_power_api(start, end, longitude, latitude, temporalidad, format):
        base_url = "https://power.larc.nasa.gov/api/temporal"
        url = f"{base_url}/{temporalidad}/point"

        community = "ag"  # Comunidad agrícola
        parameters = "T2M,PRECTOT,WS10M,RH2M"  # Parámetros de interés

        params = {
        'start': start,  # Año de inicio (puede variar si es diario o mensual)
        'end': end,      # Año de finalización (ajustado a 2022 si es mensual o anual)
        'latitude': latitude,
        'longitude': longitude,
        'community': community,
        'parameters': parameters,
        'format': format,  # Formato de respuesta
        'time-standard': 'utc'  # Estándar de tiempo
        }

        if NasaService.evaluate_if_model_exists(longitude, latitude):
            return {'error': False, 'message': "CSV y todos los modelos ya existen"}

        try:
            # Realizar la solicitud a la API
            response = requests.get(url, params=params)
            response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa
            # Verificar el formato de la respuesta en el Content-Type
            content_type = response.headers.get('Content-Type')

            if 'text/csv' in content_type:
                csv_result = NasaService.convert_to_csv(response.text, longitude, latitude)
                if not csv_result['error']:
                    #DataPreprocessor.load_dataframe(csv_result['file_name'], longitude, latitude)
                    DataPreprocessor.load_data_train_model(csv_result['file_name'], longitude, latitude)
                else:
                    return {'error': True, 'message': f"Error al convertir a CSV: {csv_result['message']}"}
                
                return {'error': False, 'data': 'OK'}
            elif 'application/json' in content_type:
                # Si es JSON, devolver la respuesta en formato JSON
                return response.json()
            else:
                # En caso de otro formato inesperado
                return {'error': True, 'message': f"Formato de respuesta no soportado: {content_type}"}
        
        except requests.exceptions.RequestException as e:
            return {'error': True, 'message': str(e)}

    @staticmethod
    def evaluate_if_model_exists(longitude, latitude):
        csv_folder_path = 'csvFiles'
        model_folder_path = 'IA_Models'

        csv_file_name = f"{longitude:.6f}_{latitude:.6f}.csv"
        csv_full_path = os.path.join(csv_folder_path, csv_file_name)

        # Lista de parámetros (modelos)
        parameters = ["T2M", "PRECTOTCORR", "WS10M", "RH2M"]
        model_exists_all = True

        # Verificar si cada modelo existe
        for param in parameters:
            model_file_name = f"{longitude:.6f}_{latitude:.6f}_{param}.keras"
            model_full_path = os.path.join(model_folder_path, model_file_name)

            # Si alguno de los modelos no existe, permitir que continúe el proceso
            if not os.path.exists(model_full_path):
                model_exists_all = False

        # Verificar si el CSV existe
        csv_exists = os.path.exists(csv_full_path)

        # Condiciones:
        # 1. Si alguno de los modelos no existe, continuar con el algoritmo.
        if not model_exists_all:
            return False
        # 2. Si todos los modelos y el CSV existen, detener el algoritmo.
        elif model_exists_all and csv_exists:
            return True
        # 3. Si todos los modelos existen pero el CSV no, continuar con el algoritmo.
        elif model_exists_all and not csv_exists:
            return False


    @staticmethod
    def convert_to_csv(csv_data: str, longitude, latitude) -> dict:
        try:
            # Divide el texto por líneas
            lines = csv_data.splitlines()

            # Encuentra el índice donde termina el encabezado y comienza el verdadero contenido
            start_index = 0
            for i, line in enumerate(lines):
                if line.startswith("-END HEADER-"):  # El encabezado termina con '-END HEADER-'
                    start_index = i + 1  # Salta a la línea siguiente al final del encabezado
                    break

            # Extrae solo los datos (a partir de la línea después de '-END HEADER-')
            cleaned_data = "\n".join(lines[start_index:])

            folder_path = 'csvFiles'
            file_name = f"{longitude:.6f}_{latitude:.6f}.csv"
            full_path = os.path.join(folder_path, file_name)
            os.makedirs(folder_path, exist_ok=True)
            # Guardar los datos en un archivo CSV sin el encabezado adicional
            with open(full_path, 'w') as file:
                file.write(cleaned_data)  # Escribe los datos limpios en el archivo
                print(f"Datos guardados en '{full_path}'")

            return {'error': False, 'message': f"Datos almacenados en {full_path}", 'file_name': full_path}
        
        except Exception as e:
            return {'error': True, 'message': str(e)}