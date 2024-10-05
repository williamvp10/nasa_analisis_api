import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from keras.api.models import load_model

class GraphModel:

    def graph_and_save_results(history, X_test, y_test, training_result, model_name='modelo_GRU.keras', output_dir='resultados/'):
        try:
            # Crear el directorio si no existe
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"Directorio '{output_dir}' creado.")

            # Cargar el modelo
            model = load_model(model_name)

            # Realizar predicciones
            predictions = model.predict(X_test)

            # Invertir la escala de los datos para que sean interpretables
            scaler = training_result['scaler']  # Usar el scaler del entrenamiento
            predictions = scaler.inverse_transform(predictions)
            y_test = scaler.inverse_transform(y_test)

            # Calcular las métricas de error
            mse = mean_squared_error(y_test, predictions)
            mae = mean_absolute_error(y_test, predictions)
            mape = np.mean(np.abs(predictions - y_test) / np.abs(y_test)) * 100
            print(f"Modelo: {model_name}")
            print(f"Error cuadrático medio (MSE): {mse}")
            print(f"Error absoluto medio (MAE): {mae}")
            print(f"Error porcentual absoluto medio (MAPE): {mape}%")

            # Graficar las predicciones frente a los datos reales
            plt.figure(figsize=(10, 6))
            plt.plot(y_test, label='Datos Reales')
            plt.plot(predictions, label='Predicciones GRU', color='red')
            plt.title('Predicciones GRU vs Datos Reales')
            plt.legend()
            plt.savefig(f"{output_dir}/{model_name.split('.')[0]}_predicciones_vs_reales.png")
            plt.show()
            print("\n")

            # Graficar la pérdida de entrenamiento y validación
            plt.figure(figsize=(10, 6))
            plt.plot(history.history['loss'], label='Pérdida de entrenamiento')
            plt.plot(history.history['val_loss'], label='Pérdida de validación')
            plt.title('Pérdida durante el entrenamiento y validación')
            plt.xlabel('Epochs')
            plt.ylabel('Pérdida (MSE)')
            plt.legend()
            plt.savefig(f"{output_dir}/{model_name.split('.')[0]}_perdida_entrenamiento_validacion.png")
            plt.show()
            print("\n")

            # Graficar el MSE de entrenamiento y validación
            plt.figure(figsize=(10, 6))
            plt.plot(history.history['mean_squared_error'], label='MSE de entrenamiento')
            plt.plot(history.history['val_mean_squared_error'], label='MSE de validación')
            plt.title('MSE durante el entrenamiento y validación')
            plt.xlabel('Epochs')
            plt.ylabel('MSE')
            plt.legend()
            plt.savefig(f"{output_dir}/{model_name.split('.')[0]}_mse_entrenamiento_validacion.png")
            plt.show()

            print(f"Gráficas guardadas en {output_dir}")

        except Exception as e:
            print(f"Error al generar las gráficas: {e}")