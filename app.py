import streamlit as st

# Ejemplo de bebidas y precios
BEBIDAS = [
    {"nombre": "Agua", "precio": 1.0},
    {"nombre": "Café", "precio": 1.2},
    {"nombre": "Cerveza", "precio": 2.0},
    {"nombre": "Refresco", "precio": 1.5},
    {"nombre": "Vino", "precio": 2.5},
]


# Configuración de la página
st.set_page_config(page_title="POS Bebidas", layout="wide")
st.title("POS Bebidas")

# Estado de la sesión
if "unidades" not in st.session_state:
    st.session_state.unidades = [0] * len(BEBIDAS)
if "total" not in st.session_state:
    st.session_state.total = 0.0
if "dinero_cliente" not in st.session_state:
    st.session_state.dinero_cliente = 0.0
if "cambio" not in st.session_state:
    st.session_state.cambio = 0.0

# Estilos para los botones de bebidas
st.markdown("""
    <style>
    .bebida-btn {
        width: 100% !important;
        height: 80px;
        font-size: 1.3em !important;
        border-radius: 10px;
        border: 2px solid #0074D9;
        background: #f8fbff;
        margin-bottom: 12px;
        font-weight: 600;
        color: #222;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 18px;
        transition: background 0.2s;
        box-shadow: 0 2px 8px #e3eaf3;
    }
    .bebida-btn:hover {
        background: #e6f2ff;
        border-color: #005fa3;
    }
    .bebida-cantidad {
        font-size: 1.1em;
        color: #0074D9;
        margin-left: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


# Grid de tarjetas limpias y útiles
import sys
if sys.platform == "win32":
    grid_cols = 1
else:
    grid_cols = 4
cols = st.columns(grid_cols)


for i, bebida in enumerate(BEBIDAS):
    col = cols[i % grid_cols]
    with col:
        with st.container():
            st.markdown(
                f"""
                <div style='border:1.5px solid #0074D9; border-radius:10px; background:#f8fbff; margin-bottom:18px; padding:14px 8px 10px 8px; min-height:150px;'>
                <div style='font-size:1.15em; font-weight:bold; margin-bottom:2px; text-align:center'>{bebida['nombre']}</div>
                <div style='font-size:1em; color:#0074D9; margin-bottom:8px; text-align:center'>€{bebida['precio']:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Control local de unidades para mostrar el valor actualizado al instante
            unidades = st.session_state.unidades[i]
            c1, c2, c3 = st.columns([1,2,1])
            with c1:
                if st.button("➖", key=f"minus_{i}", help=f"Quitar {bebida['nombre']}"):
                    if unidades > 0:
                        unidades -= 1
                        st.session_state.unidades[i] = unidades
                        st.session_state.total -= bebida['precio']
                        if st.session_state.total < 0:
                            st.session_state.total = 0.0
            with c3:
                if st.button("➕", key=f"plus_{i}", help=f"Añadir {bebida['nombre']}"):
                    unidades += 1
                    st.session_state.unidades[i] = unidades
                    st.session_state.total += bebida['precio']
            with c2:
                st.markdown(f"<div style='text-align:center;font-size:1.5em; font-weight:bold; color:#0074D9;'>{unidades}</div>", unsafe_allow_html=True)


st.markdown("---")

# Total y control de dinero/cambio siempre visibles
st.markdown(f"## Total: €{st.session_state.total:.2f}")

col1, col2 = st.columns(2)
with col1:
    dinero = st.number_input("Dinero recibido del cliente", min_value=0.0, step=0.5, value=st.session_state.dinero_cliente, key="dinero_input")
    if st.button("Calcular cambio"):
        st.session_state.dinero_cliente = dinero
        st.session_state.cambio = dinero - st.session_state.total
        if st.session_state.cambio < 0:
            st.warning("Falta dinero del cliente.")
with col2:
    if st.button("Reiniciar todo"):
        st.session_state.unidades = [0] * len(BEBIDAS)
        st.session_state.total = 0.0
        st.session_state.dinero_cliente = 0.0
        st.session_state.cambio = 0.0

if st.session_state.dinero_cliente > 0:
    st.markdown(f"### Cambio: €{st.session_state.cambio:.2f}")
