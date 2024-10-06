import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.api.models import load_model

class PredictModel:

    def prediction(model_name, series, sequence_length, prediction_number):
        scaler = MinMaxScaler(feature_range=(0, 1))
        data = scaler.fit_transform(series.values.reshape(-1, 1))

        predictions = []
        model = load_model(model_name)
        last_sequence = data[-sequence_length:]
        for _ in range(prediction_number):
            # Reshape de la secuencia para que tenga el formato adecuado (batch_size, sequence_length, 1)
            last_sequence_reshaped = last_sequence.reshape((1, sequence_length, 1))
            # Predecir el siguiente valor
            next_prediction = model.predict(last_sequence_reshaped)
            # Invertir la escala del valor predicho para devolverlo a su valor original
            next_prediction_inversed = scaler.inverse_transform(next_prediction)
            # Guardar la predicción
            predictions.append(next_prediction_inversed[0][0])
            # Actualizar la secuencia: remover el valor más antiguo y agregar la predicción
            last_sequence = np.append(last_sequence[1:], next_prediction).reshape(-1, 1)

        return predictions

    def predict_next_week(model_name, series, sequence_length):
        scaler = MinMaxScaler(feature_range=(0, 1))
        data = scaler.fit_transform(series.values.reshape(-1, 1))

        predictions = []
        # Cargar el modelo entrenado
        model = load_model(model_name)
        # Toma la última secuencia (últimos 'sequence_length' días) para hacer la primera predicción
        last_sequence = data[-sequence_length:]
        for _ in range(7):  # Queremos predecir para 7 días
            # Reshape de la secuencia para que tenga el formato adecuado (batch_size, sequence_length, 1)
            last_sequence_reshaped = last_sequence.reshape((1, sequence_length, 1))

            # Predecir el siguiente valor
            next_prediction = model.predict(last_sequence_reshaped)

            # Invertir la escala del valor predicho para devolverlo a su valor original
            next_prediction_inversed = scaler.inverse_transform(next_prediction)

            # Guardar la predicción
            predictions.append(next_prediction_inversed[0][0])

            # Actualizar la secuencia: remover el valor más antiguo y agregar la predicción
            last_sequence = np.append(last_sequence[1:], next_prediction).reshape(-1, 1)

        return predictions
    
    #def show_predictions(next_week_predictions):
    #    start_date_prediction="2024-09-30"
    #    end_date_prediction="2024-10-06"
    #    dates = pd.date_range(start=start_date_prediction, periods=7)
    #    predictions_df = pd.DataFrame({'Fecha': dates, f'Predicción {'T2M'}': next_week_predictions})
    #    print(predictions_df)

    #    predictions_df.plot(x='Fecha', y=f'Predicción {'T2M'}', kind='line', marker='o', title=f'Predicciones de {'T2M'} del {start_date_prediction} al {end_date_prediction}')
    #    plt.ylabel(f'Parametro ({'T2M'})')
    #    plt.show()