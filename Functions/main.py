import streamlit as st
import pydeck as pdk
import pandas as pd
from createPolygons import extraer_poligonos_sql

# Configuración de la página
st.set_page_config(page_title="Calcula tu casa ideal", layout="wide", initial_sidebar_state="expanded")

# Estilos globales y personalizados
st.markdown(
    """
    <style>
    /* Fondo de la página */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #1c1c1c;
        color: white;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Título principal */
    h1 {
        font-size: 2.5rem;
        color: #4CAF50;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Contenedor centrado */
    .center-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 20px;
    }

    /* Subtítulos */
    h2, h3 {
        color: #ffffff;
        font-weight: 600;
        margin-bottom: 15px;
    }

    /* Personalización de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #1c1c1c;
        border-right: 2px solid #4CAF50;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
        padding-top: 20px;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
        color: #4CAF50;
        font-weight: bold;
    }

    /* Botón personalizado */
    .stButton>button {
        display: block;
        margin: 20px auto;
        padding: 15px 25px;
        background: linear-gradient(90deg, #32a852, #3dc973);
        color: white;
        font-size: 18px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none;
        border-radius: 12px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1), 0px 1px 3px rgba(0, 0, 0, 0.06);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #3dc973, #32a852);
        transform: translateY(-2px);
        color: #ffffff;
        box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.2), 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1), 0px 1px 3px rgba(0, 0, 0, 0.06);
    }

    /* Selectbox personalizado */
    div[data-baseweb="select"] {
        border-radius: 8px !important;
        border: 1px solid #4CAF50 !important;
        background: #4CAF50 !important;
        color: #4CAF50 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 2px !important;
    }

    /* Checkbox personalizado */
    .stCheckbox>div {
        display: flex;
        align-items: center;
    }
    .stCheckbox>div>label {
        color: #4CAF50;
        font-weight: bold;
        font-size: 16px;
    }
    .stCheckbox>div>input {
        width: 20px;
        height: 20px;
        margin-right: 10px;
        cursor: pointer;
        border: 2px solid #4CAF50;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    .stCheckbox>div>input:checked {
        background: #4CAF50;
        border-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título principal
st.markdown("<h1>Calcula tu Casa Ideal</h1>", unsafe_allow_html=True)

# Barra lateral
st.sidebar.header("Opciones")
opcion = st.sidebar.radio("Seleccione una opción:", ["Alquiler", "Compra"])

# Lógica según la selección
if opcion == "Alquiler":
    st.write("Has seleccionado la opción de Alquiler.")
elif opcion == "Compra":
    st.write("Has seleccionado la opción de Compra.")

st.sidebar.header("Preferencias")
import streamlit as st

with st.sidebar:
    st.header("Filtros de búsqueda")
    habitaciones = st.slider("Número de habitaciones", min_value=1, max_value=9, value=1, key="habitaciones")
    baños = st.slider("Número de baños", min_value=1, max_value=9, value=1, key="baños")
    parking = st.slider("Plazas de parking", min_value=1, max_value=9, value=1, key="parking")


# Botón funcional
calcular_btn = st.sidebar.button("Calcular tu casa ideal")

# Mapa centrado en Valencia con tamaño ajustado
st.markdown('<div class="center-container">', unsafe_allow_html=True)
map_data = pd.DataFrame({
    'lat': [39.4699],
    'lon': [-0.3763]
})
polygons = extraer_poligonos_sql()

# Formatear los datos para Pydeck
geojson_features = []
for polygon in polygons:
    geojson_features.append({
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [polygon]  # Encapsular en otra lista
        },
        "properties": {}
    })

geojson_data = {
    "type": "FeatureCollection",
    "features": geojson_features
}

# Crear la capa para Pydeck
layer = pdk.Layer(
    "GeoJsonLayer",
    geojson_data,
    pickable=True,
    stroked=True,
    filled=True,
    lineWidthScale=20,
    lineWidthMinPixels=1,
    get_line_color=[0, 160, 0],
    get_fill_color=[76, 175, 80,50],
)
# Crear el mapa con PyDeck
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=39.4659,
        longitude=-0.3763,
        zoom=12.40,
        pitch=0,
    ),
    layers=[layer],
), width=1200, height=800, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Acción del botón
if calcular_btn:
    st.subheader("Resultado")
    tipo_vivienda = "alquiler" if opcion == "Alquiler"  else "compra" if opcion == "Compra" else "ninguno"
    st.write(f"Has elegido una casa para **{tipo_vivienda}** con:")
    st.write(f"- **{habitaciones} habitaciones**")
    st.write(f"- **{baños} baños**")
    st.write(f"- **{parking} plazas de parking**")
    st.write("Gracias por utilizar nuestra herramienta para calcular tu casa ideal.")