import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("Fuerza Leonas")
st.write("Intentemos no matarnos en esto de sacarnos una carrera")

# Creamos la conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Leemos los datos actuales de la hoja de cálculo (ttl=0 significa que no guarde caché para que sea instantáneo)
df = conn.read(ttl=0)

# Definimos los perfiles y categorías
amigos = ["Rut", "Éric", "Lucía"]
categorias = ["Cosas de la universidad (real no fake)", "Tocarme los huevos intencionalmente", "Haciendo cosas productivas (evitando estudiar de manera justificada)"]

# --- FORMULARIO DE REGISTRO ---
st.subheader("Registrar Nuevo Tiempo")

col1, col2 = st.columns(2)
with col1:
    perfil_seleccionado = st.selectbox("Quién eres tú:", amigos)
with col2:
    categoria_seleccionada = st.selectbox("Qué se supone que vas a hacer:", categorias)

horas_registradas = st.number_input("Introduce las horas dedicadas:", min_value=0.0, max_value=24.0, step=0.5)

if st.button("Guardar Registro"):
    # Buscamos si ya existe una fila para este perfil y categoría en la hoja
    condicion = (df["Perfil"] == perfil_seleccionado) & (df["Categoria"] == categoria_seleccionada)
    
    if not df[condicion].empty:
        # Si existe, sumamos las horas
        df.loc[condicion, "Horas"] += horas_registradas
    else:
        # Si no existe, añadimos una fila nueva
        nueva_fila = pd.DataFrame([{"Perfil": perfil_seleccionado, "Categoria": categoria_seleccionada, "Horas": horas_registradas}])
        df = pd.concat([df, nueva_fila], ignore_index=True)
    
    # Actualizamos la hoja de Google Sheets
    conn.update(data=df)
    st.success(f"Genial, se han sumado {horas_registradas} horas en '{categoria_seleccionada}' para {perfil_seleccionado}.")
    st.rerun()

# --- SECCIÓN DE RANKING ---
st.markdown("---")
st.subheader("Hagan sus apuestas")

if not df.empty and "Perfil" in df.columns and "Categoria" in df.columns:
    # Transformamos la tabla para que se vea bonita en formato cruzado
    df_pivot = df.pivot(index="Perfil", columns="Categoria", values="Horas").fillna(0.0)
    
    if "Estudio intenso" in df_pivot.columns:
        df_pivot = df_pivot.sort_values(by="Estudio intenso", ascending=False)
        
    st.dataframe(df_pivot, use_container_width=True)
else:
    st.write("Aún no hay datos suficientes o la tabla está vacía.")