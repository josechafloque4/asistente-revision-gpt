import fitz  # PyMuPDF
import docx
import requests

def leer_archivo(archivo):
    tipo = archivo.name.split(".")[-1]
    texto = ""

    if tipo == "pdf":
        with fitz.open(stream=archivo.read(), filetype="pdf") as doc:
            for page in doc:
                texto += page.get_text()
    elif tipo == "docx":
        doc = docx.Document(archivo)
        texto = "\n".join([p.text for p in doc.paragraphs])
    return texto

def validar_doi_crossref(titulo):
    url = "https://api.crossref.org/works"
    params = {"query.title": titulo, "rows": 1}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["message"]["items"]:
            item = data["message"]["items"][0]
            return {
                "title": item.get("title", [""])[0],
                "DOI": item.get("DOI"),
                "journal": item.get("container-title", [""])[0],
                "year": item.get("published-print", {}).get("date-parts", [[None]])[0][0],
                "authors": [f"{a.get('family', '')}, {a.get('given', '')}" for a in item.get("author", [])]
            }
        else:
            return {"error": "No se encontró información para este título"}
    else:
        return {"error": "Error al consultar Crossref"}