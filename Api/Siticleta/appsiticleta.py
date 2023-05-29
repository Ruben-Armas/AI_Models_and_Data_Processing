import numpy as np
import pickle
import joblib
import streamlit as st
#import datetime
import lightgbm as lgb  # Modelo de árbol LGBMRegressor
from sklearn.preprocessing import MinMaxScaler  # Para el escalamiento por Rangos

# Path del modelo preentrenado (pickle)
#MODEL = 'models/API_Siticleta.pkl'
# Se carga el modelo
#model = pickle.load(open(MODEL, 'rb'))

# Cargar el modelo y el escalador
model = joblib.load('models/API_Siticleta.pkl') # Modelo
scaler = joblib.load('models/escalador.pkl')    # Escalador


# Diccionarios de correspondencia
# Opciones del menú desplegable
rentalPlace_options = [
    'Aparcamiento Sanapú', 'Autoridad portuaria', 'Ayuntamiento', 'Barranquillo Don Zoilo',
    'Base Naval', 'Bicis para reparar', 'C.C. El Muelle', 'C.C. La Ballena (elect.)',
    'C.C. La Minilla', 'Cabildo de Gran Canaria', 'Canódromo', 'Canódromo (electric)',
    'Casillo la Luz', 'Castillo de Mata (elect.)', 'Castillo de la Luz', 'Castillo la Luz',
    'Churruca', 'Ciudad Deportiva', 'Ciudad de la Justicia', 'Desconocido', 'El Sebadal (elec.)',
    'Gabinete Literario', 'Gestohlen', 'Hoya de la Plata', 'IES Mesa y López', 'Intermodal El Rincón',
    'Las Canteras - Luis Morote', 'León y Castillo', 'Mercado Central', 'Muelle Deportivo',
    'Obelisco', 'Oficina Sítycleta (elect.)', 'Oficina de la Sitycleta', 'Parque Santa Catalina',
    'Parque del Estadio Insular', 'Paseo de Chil - Av. Escaleritas', 'Piscina Julio Navarro',
    'Plaza Manuel Becerra', 'Plaza Manuel Becerra (elect.)', "Plaza O'Shanahan", 'Plaza San Agustín',
    'Plaza de América', 'Plaza de España', 'Plaza de España (elect.)', 'Plaza de la feria',
    'Plaza del Pilar', 'Plazoleta de Farray', 'San Bernardo', 'San Cristóbal', 'San Telmo',
    'Teatro Pérez Galdós', 'Torre Las Palmas', 'Torre Woermann', 'Vega de San José',
    'Vermisst', 'Villa de Zarauz'
    ]
# Diccionario de valores numéricos
rentalPlace_values = {
    'Aparcamiento Sanapú': 0,
    'Autoridad portuaria': 1,
    'Ayuntamiento': 2,
    'Barranquillo Don Zoilo': 3,
    'Base Naval': 4,
    'Bicis para reparar': 5,
    'C.C. El Muelle': 6,
    'C.C. La Ballena (elect.)': 7,
    'C.C. La Minilla': 8,
    'Cabildo de Gran Canaria': 9,
    'Canódromo': 10,
    'Canódromo (electric)': 11,
    'Casillo la Luz': 12,
    'Castillo de Mata (elect.)': 13,
    'Castillo de la Luz': 14,
    'Castillo la Luz': 15,
    'Churruca': 16,
    'Ciudad Deportiva': 17,
    'Ciudad de la Justicia': 18,
    'Desconocido': 19,
    'El Sebadal (elec.)': 20,
    'Gabinete Literario': 21,
    'Gestohlen': 22,
    'Hoya de la Plata': 23,
    'IES Mesa y López': 24,
    'Intermodal El Rincón': 25,
    'Las Canteras - Luis Morote': 26,
    'León y Castillo': 27,
    'Mercado Central': 28,
    'Muelle Deportivo': 29,
    'Obelisco': 30,
    'Oficina Sítycleta (elect.)': 31,
    'Oficina de la Sitycleta': 32,
    'Parque Santa Catalina': 33,
    'Parque del Estadio Insular': 34,
    'Paseo de Chil - Av. Escaleritas': 35,
    'Piscina Julio Navarro': 36,
    'Plaza Manuel Becerra': 37,
    'Plaza Manuel Becerra (elect.)': 38,
    "Plaza O'Shanahan": 39,
    'Plaza San Agustín': 40,
    'Plaza de América': 41,
    'Plaza de España': 42,
    'Plaza de España (elect.)': 43,
    'Plaza de la feria': 44,
    'Plaza del Pilar': 45,
    'Plazoleta de Farray': 46,
    'San Bernardo': 47,
    'San Cristóbal': 48,
    'San Telmo': 49,
    'Teatro Pérez Galdós': 50,
    'Torre Las Palmas': 51,
    'Torre Woermann': 52,
    'Vega de San José': 53,
    'Vermisst': 54,
    'Villa de Zarauz': 55
    }
#rentalPlace_values = {place: i for i, place in enumerate(rentalPlace_options)}

# Opciones del menú desplegable
dayweek_options = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
# Diccionario de valores numéricos
dayweek_values = {'Lunes': 1, 'Martes': 2, 'Miércoles': 3, 'Jueves': 4, 'Viernes': 5, 'Sábado': 6, 'Domingo': 7}
#dayweek_values = {day: i+1 for i, day in enumerate(dayweek_options)}

# Opciones del menú desplegable
weatherConditions_options = [
    'Cielo cubierto', 'Despejado', 'Llovizna', 'Lluvia', 'Lluvia ligera',
    'Mayormente cubierto', 'Neblina', 'Nubes dispersas', 'Parcialmente cubierto'
    ]
# Diccionario de valores numéricos
weatherConditions_values = {
    'Cielo cubierto': 0, 'Despejado': 1, 'Llovizna': 2, 
    'Lluvia': 3, 'Lluvia ligera': 4, 'Mayormente cubierto': 5,
    'Neblina': 6, 'Nubes dispersas': 7, 'Parcialmente cubierto': 8
    }
#weatherConditions_values = {condition: i for i, condition in enumerate(weatherConditions_options)}

# Función de predicción del modelo
def model_prediction(x_in, model):
    x = np.asarray(x_in).reshape(1,-1)
    preds=model.predict(x)
    # Redondea la predicción a un número entero
    pred_round = np.round(preds)

    return int(pred_round[0])

def main():   
    # Título
    st.title('Síticleta 🚲')

    # Agrupar elementos en columnas y filas
    col1, col2 = st.beta_columns(2)

    with col1:
        # Lecctura de datos -> Menú desplegable y checkbox
        day = st.date_input('Día:')
        hour = st.selectbox('Hora del día:', list(range(24)))

    with col2:
        #dayWeek = st.selectbox('Día de la semana:', dayweek_options)
        # Autocompletar el selector dayWeek basado en la fecha seleccionada
        day_week_num = (day.weekday() + 1) % 8  # Obtener el día de la semana (1 = lunes, 2 = martes, ..., 7 = domingo)
        day_week = next((key for key, value in dayweek_values.items() if value == day_week_num), None)  # Buscar el valor correspondiente en el diccionario
        # Selector dayWeek autocompletado
        dayWeek = st.selectbox('Día de la semana:', dayweek_options, index=dayweek_options.index(day_week) if day_week else None)

        rentalPlace = st.selectbox('Estación de alquiler:', rentalPlace_options)

    weatherConditions = st.selectbox('Condiciones meteorológicas:', weatherConditions_options)
    WorkingDay = st.checkbox("¿Es día laboral?")

    dayweek_num = dayweek_values[dayWeek]
    rentalPlace_num = rentalPlace_values[rentalPlace]
    weatherConditions_num = weatherConditions_values[weatherConditions]

    if WorkingDay:
        working_day = 1
    else:
        working_day = 0

    # Botón de predicción
    if st.button("Predicción :"): 
        x_in =[
            day.day,
            hour,
            dayweek_num,
            rentalPlace_num,
            weatherConditions_num,
            WorkingDay
        ]

        # Escala las variables para estar en las mismas condiciones de cómo se entrenó el modelo
        x_in = np.asarray(x_in).reshape(1, -1)   # Convertir x_in en matriz 2D
        x_scaled = scaler.transform(x_in)

        predict = model_prediction(x_scaled, model)      

        st.success(f'El nº de alquileres en "{rentalPlace}" el día {day} a las {hour}:00 horas, es: "{predict}"')

if __name__ == '__main__':
    main()
