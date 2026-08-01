import streamlit as st
import pandas as pd

# Titulo de la aplicacion
st.title("Fuerza Leonas")
st.write("Intentemos no matarnos en el proceso :)")

# 1. Seleccion de Perfil
amigos = ["Rut", "Eric", "Lucia"]
perfil_seleccionado = st.selectbox("Quien eres tu:", amigos)

# 2. Seleccion de Categoria
categoria = st.selectbox("Que se supone que estas haciendo", ["Cosas de la universidad (real no fake)", "Tocarme los huevos intencionalmente", "Cualquier cosa para evitar estudiar"])

# 3. Simulacion de registro de tiempo 
horas_registradas = st.number_input("Tiempo focused (aprox):", min_value=0.0, max_value=24.0, step=0.5)

if st.button("Guardar Registro"):
    st.success(f"Se han sumado {horas_registradas} horas a la categoria '{categoria}' para {perfil_seleccionado}.")

# 4. Seccion de Ranking (Simulado de momento)
st.subheader("Hagan sus apuestas")
# Datos de ejemplo para que ver como queda una tabla
datos_ranking = {
    "Perfil": ["Rut", "Eric", "Lucia"],
    "Horas de Estudio": [15.5, 12.0, 18.5],
    "Tiempo Libre": [8.0, 10.5, 6.0]
}
df_ranking = pd.DataFrame(datos_ranking)

# Mostramos la tabla ordenada por horas de estudio de mayor a menor
df_ranking = df_ranking.sort_values(by="Horas de Estudio", ascending=False)
st.dataframe(df_ranking, use_container_width=True)