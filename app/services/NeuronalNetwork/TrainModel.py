import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from keras.api.models import Sequential
from keras.api.layers import GRU, Dropout, Dense
import os

class TrainModel:

    def train_model(series, longitude, latitude, param, sequence_length=7):
        try:
            # Preprocesar los datos
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(series.values.reshape(-1, 1))

            # Convertir los datos en secuencias
            def create_sequences(data, sequence_length):
                sequences = []
                labels = []
                for i in range(len(data) - sequence_length):
                    sequences.append(data[i:i + sequence_length])
                    labels.append(data[i + sequence_length])
                return np.array(sequences), np.array(labels)

            # Crear secuencias de entrenamiento y prueba
            X, y = create_sequences(scaled_data, sequence_length)
            train_size = int(0.8 * len(X))
            X_train, X_test = X[:train_size], X[train_size:]
            y_train, y_test = y[:train_size], y[train_size:]

            # Crear el modelo GRU
            model = Sequential()
            model.add(GRU(units=100, return_sequences=True, input_shape=(X_train.shape[1], 1)))
            model.add(Dropout(0.2))
            model.add(GRU(units=100))
            model.add(Dropout(0.2))
            model.add(Dense(1))  # Predicción de un solo valor (T2M)

            # Compilar el modelo
            model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])

            # Entrenar el modelo
            history = model.fit(X_train, y_train, epochs=100, batch_size=16, validation_data=(X_test, y_test))

            folder_path = 'IA_Models'
            os.makedirs(folder_path, exist_ok=True)
            model_filename = f"{longitude:.6f}_{latitude:.6f}_{param}.keras"
            full_model_path = os.path.join(folder_path, model_filename)

            # Guardar el modelo entrenado
            model.save(full_model_path)
            print(f"Modelo guardado como {full_model_path}")

            return {'error': False, 'history': history, 'X_test': X_test, 'y_test': y_test, 'scaler': scaler, 'model_name':full_model_path}

        except Exception as e:
            print(f"Error al entrenar el modelo: {e}")
            return {'error': True, 'message': str(e)}