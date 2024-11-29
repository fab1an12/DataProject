import streamlit as st
import matplotlib.pyplot as plt

# Configuración de Streamlit
st.title("Predicción de Precios de Vivienda por Barrio")

# URI de MongoDB
uri = "mongodb+srv://fabianmiulescu:DataProject2024@cluster0.dzrgu.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

# Nombre de la base de datos
database_name = 'precios_vivienda'

# Barrio seleccionable
barrios = [
    "algiros", "benicalap", "benimaclet", "camins-al-grau", "campanar", "ciutat-vella",
    "el-pla-del-real", "extramurs", "jesus", "leixample", "lolivereta", "la-saidia",
    "patraix", "poblats-maritims", "quatre-carreres", "rascanya"
]
barrio = st.selectbox("Seleccione un barrio:", barrios)

# Llamar a la función principal
if st.button("Predecir y Mostrar Gráfica"):
    try:
        # Llamar a la función para obtener la gráfica
        grafico = 1

        # Mostrar la gráfica en Streamlit
        st.pyplot(grafico)

    except ValueError as e:
        st.error(f"Error en los datos: {e}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")
