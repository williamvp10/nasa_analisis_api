import pandas as pd
import matplotlib.pyplot as plt
import io

from app.services.NeuronalNetwork.TrainModel import TrainModel
from app.services.NeuronalNetwork.GraphModel import GraphModel
from app.services.NeuronalNetwork.PredictModel import PredictModel

class DataPreprocessor:

    def load_data_train_model(csv_file_path, longitude, latitude):
        parameters = ["T2M", "PRECTOTCORR", "WS10M", "RH2M"]
        # Verificar si cada modelo existe
        for param in parameters:
            series = DataPreprocessor.get_series(csv_file_path, param)
            if not series['error']:
                trained_model = TrainModel.train_model(series['series'], longitude, latitude, param)
                if trained_model['error']:
                    return {'error': True, 'message': f'error training the model {param}'}
            else:
                return series
            
        return {'error': False, 'Trained Models': 'Successfull'} 


    def load_dataframe(csv_file_path, longitude, latitude):
        try:
            # Cargar los datos desde el archivo CSV
            df = pd.read_csv(csv_file_path)

            # Mostrar las primeras filas del DataFrame para confirmar la carga
            print("Primeras 5 filas del DataFrame:")
            print(df.head(5))

            # Mostrar un resumen inicial antes de la limpieza
            print("Antes de la limpieza:")
            print(df.describe())

            # Reemplazar los valores -999 con NaN para marcarlos como faltantes
            df_clean = df.replace(-999, pd.NA)

            # Eliminar las filas con cualquier NaN (valores faltantes)
            df_clean = df_clean.dropna()

            # Mostrar un resumen después de la limpieza
            print("\nDespués de la limpieza:")
            print(df_clean.describe())

            # Guardar el DataFrame limpio en un nuevo archivo CSV si es necesario
            #df_clean.to_csv('data_clean.csv', index=False)
            
            DataPreprocessor.temporal_series(df_clean, longitude, latitude, 'T2M')

            return {'error': False, 'data': df_clean }

        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            return {'error': True, 'message': str(e)}
        
    def temporal_series(df_clean, longitude, latitude, param):
        try:
            # Verificar que las columnas 'YEAR' y 'DOY' existan
            if 'YEAR' not in df_clean.columns or 'DOY' not in df_clean.columns:
                raise ValueError("Las columnas 'YEAR' y 'DOY' no están presentes en el DataFrame.")

            # Verificar si hay valores nulos en las columnas 'YEAR' y 'DOY'
            print("\nValores nulos por columna:")
            print(df_clean[['YEAR', 'DOY']].isnull().sum())

            if df_clean[['YEAR', 'DOY']].isnull().sum().sum() > 0:
                raise ValueError("Existen valores nulos en las columnas 'YEAR' o 'DOY'.")

            # Combinar manualmente las columnas 'YEAR' y 'DOY' para crear una cadena de fecha
            #df_clean['date'] = pd.to_datetime(df_clean['YEAR'].astype(str) + df_clean['DOY'].astype(str), format='%Y%j')
            # Combinar manualmente las columnas 'YEAR' y 'DOY' para crear una cadena de fecha
            df_clean['date'] = pd.to_datetime(df_clean['YEAR'].astype(str) + df_clean['DOY'].astype(str), format='%Y%j', errors='coerce')

            # Establecer la columna de fecha como índice
            df_clean.set_index('date', inplace=True)

            # Asegurarse de que los datos están ordenados cronológicamente
            df_clean.sort_index(inplace=True)

            # Extraer la serie temporal que nos interesa (por ejemplo, la temperatura T2M)
            if param not in df_clean.columns:
                raise ValueError(f"La columna {param} no está presente en el DataFrame.")

            series = df_clean[param]
            print(f"\nPrimeras 5 filas de la serie temporal {param}:")
            print(series.head())
            
            #DataPreprocessor.graph_temporal_series(series, param)
            trained_model = TrainModel.train_model(series, longitude, latitude, param)
            if(trained_model):
                return {'error': False, 'Trained Model': 'Successfull'}    
            
            #GraphModel.graph_and_save_results(
            #    history = trained_model['history'],
            #    X_test = trained_model['X_test'],
            #    y_test = trained_model['y_test'],
            #    training_result = trained_model
            #)
            #Going trought Next Week Prediction
            #next_week_predictions = PredictModel.predict_next_week(trained_model['model_name'], series = series, sequence_length = 7)
            #PredictModel.show_predictions(next_week_predictions)

            return {'error': False, 'series': series}

        except Exception as e:
            print(f"Error al definir las series temporales: {e}")
            return {'error': True, 'message': str(e)}
        
    def get_series(csv_file_path, param):
        try:
            df = pd.read_csv(csv_file_path)
            # Reemplazar los valores -999 con NaN para marcarlos como faltantes
            df_clean = df.replace(-999, pd.NA)
            # Eliminar las filas con cualquier NaN (valores faltantes)
            df_clean = df_clean.dropna()

            if 'YEAR' not in df_clean.columns or 'DOY' not in df_clean.columns:
                raise ValueError("Las columnas 'YEAR' y 'DOY' no están presentes en el DataFrame.")

            if df_clean[['YEAR', 'DOY']].isnull().sum().sum() > 0:
                raise ValueError("Existen valores nulos en las columnas 'YEAR' o 'DOY'.")
            
            df_clean['date'] = pd.to_datetime(df_clean['YEAR'].astype(str) + df_clean['DOY'].astype(str), format='%Y%j', errors='coerce')
            df_clean.set_index('date', inplace=True)
            df_clean.sort_index(inplace=True)

            if param not in df_clean.columns:
                raise ValueError(f"La columna {param} no está presente en el DataFrame.")

            series = df_clean[param]

            return {'error': False, 'series': series}

        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            return {'error': True, 'message': str(e)}

        
    def graph_temporal_series(series, parametro):
        try:
            series.plot(figsize=(10, 6))
            plt.title(f'{parametro} a lo largo del tiempo')
            plt.ylabel(parametro)
            plt.show()

            # Guardar la gráfica en un archivo PNG
            #plt.savefig(f'serie_temporal_{parametro}.png')

        except Exception as e:
            print(f"Error al graficar la serie temporal: {e}")