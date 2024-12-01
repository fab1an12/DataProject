import streamlit as st
import pydeck as pdk
import pandas as pd
from typing import List, Dict
import numpy as np
from createPolygons import extraer_poligonos_sql

def load_district_data() -> tuple:
    """Carga datos de distritos y sus polígonos desde SQL"""
    polygons = extraer_poligonos_sql()
    
    districts = [
        {"name": "Ciutat Vella", "leisure_score": 4.5, "price_score": 2.0},
        {"name": "L'Eixample", "leisure_score": 4.0, "price_score": 2.5},
        {"name": "Extramurs", "leisure_score": 3.5, "price_score": 3.0},
        {"name": "Campanar", "leisure_score": 3.0, "price_score": 3.5}
    ]
    
    return districts, polygons

def calculate_district_scores(
    districts: List[Dict],
    leisure_weight: float,
    price_weight: float
) -> pd.DataFrame:
    """Calcula puntuaciones para cada distrito basado en pesos"""
    df = pd.DataFrame(districts)
    df['total_score'] = (
        (df['leisure_score'] * leisure_weight) +
        (df['price_score'] * price_weight)
    ) / (leisure_weight + price_weight)
    return df

def create_geojson_features(
    polygons: List[List],
    ideal_index: int = None
) -> Dict:
    """Crea características GeoJSON para visualización"""
    features = []
    for idx, polygon in enumerate(polygons):
        is_ideal = idx == ideal_index if ideal_index is not None else False
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon]
            },
            "properties": {
                "is_ideal": is_ideal,
                "fill_color": [255, 165, 0, 150] if is_ideal else [76, 175, 80, 50],
                "line_color": [255, 0, 0] if is_ideal else [0, 160, 0]
            }
        })
    return {"type": "FeatureCollection", "features": features}

def main():
    st.set_page_config(
        page_title="Encuentra tu Casa Ideal",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
        <style>
        .main > div {padding: 2rem;}
        .stSlider {margin: 2rem 0;}
        .district-result {
            padding: 1rem;
            background: #f0f2f6;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .center-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🏠 Encuentra tu Casa Ideal")
    
    with st.sidebar:
        st.header("📋 Configuración")
        transaction_type = st.selectbox(
            "Tipo de operación:",
            ["Alquiler", "Compra"]
        )
        
        st.subheader("Importancia de factores")
        leisure_weight = st.slider(
            "Ocio y entretenimiento",
            1, 5, 3,
            help="Mayor valor indica más importancia al ocio"
        )
        price_weight = st.slider(
            "Precio",
            1, 5, 3,
            help="Mayor valor indica más importancia al precio"
        )
    
    districts, polygons = load_district_data()
    
    # Mostrar mapa inicial con todos los distritos
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    map_data = pd.DataFrame({
        'lat': [39.4699],
        'lon': [-0.3763]
    })
    
    geojson_data = create_geojson_features(polygons)
    
    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson_data,
        pickable=True,
        stroked=True,
        filled=True,
        line_width_scale=20,
        line_width_min_pixels=1,
        get_line_color="properties.line_color",
        get_fill_color="properties.fill_color",
    )
    
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=39.4699,
            longitude=-0.3763,
            zoom=12,
            pitch=0,
        ),
        layers=[layer],
    ))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Calcular distrito ideal", type="primary"):
        df = calculate_district_scores(districts, leisure_weight, price_weight)
        ideal_district_idx = df['total_score'].idxmax()
        ideal_district = df.iloc[ideal_district_idx]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🎯 Distrito recomendado")
            st.markdown(f"""
                <div class="district-result">
                    <h3>{ideal_district['name']}</h3>
                    <p>Puntuación total: {ideal_district['total_score']:.2f}/5</p>
                    <p>Ocio: {ideal_district['leisure_score']}/5</p>
                    <p>Precio: {ideal_district['price_score']}/5</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Actualizar mapa con distrito ideal resaltado
        geojson_data = create_geojson_features(polygons, ideal_district_idx)
        layer.data = geojson_data
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=39.4699,
                longitude=-0.3763,
                zoom=12,
                pitch=0,
            ),
            layers=[layer],
        ))

if __name__ == "__main__":
    main()