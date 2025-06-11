import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from modules import check_access, build_prompt
from prompts import system_instructions
from utils import leer_archivo, validar_doi_crossref

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Asistente de Revisión Sistemática", layout="wide")
st.title("🔍 Asistente GPT para Revisiones Sistemáticas")

if "acceso_valido" not in st.session_state:
    st.session_state.acceso_valido = False

if not st.session_state.acceso_valido:
    clave = st.text_input("🔐 Ingrese la clave de acceso:", type="password")
    if st.button("Validar clave"):
        st.session_state.acceso_valido = check_access(clave)

    if not st.session_state.acceso_valido:
        st.warning("Acceso denegado. Necesita ingresar la clave correcta para continuar.")
        st.stop()

user_input = st.chat_input("Haz tu pregunta sobre tu revisión sistemática...")

if user_input:
    with st.spinner("Pensando..."):
        prompt = build_prompt(system_instructions, user_input)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.7
        )
        output = response.choices[0].message.content
        st.markdown(output)

st.header("📄 Subir documento para análisis")
archivo = st.file_uploader("Cargar archivo PDF o DOCX", type=["pdf", "docx"])
if archivo:
    contenido = leer_archivo(archivo)
    st.success("Documento cargado exitosamente.")
    st.text_area("Contenido extraído:", value=contenido[:2000], height=200)

st.header("🔎 Validación de referencias con Crossref")
titulo_ref = st.text_input("Ingrese título o referencia a validar")
if st.button("Buscar en Crossref"):
    resultado = validar_doi_crossref(titulo_ref)
    st.json(resultado)
