import io
import requests
import openai
import PyPDF2

openai.api_key = "TOKEN-API"

# URL del archivo PDF a descargar
url = str(input("Ingresa una URl: "))

# Realizamos una solicitud GET al servidor para descargar el archivo
response = requests.get(url)

contenido_bytes = response.content

contenido_bytesio = io.BytesIO(contenido_bytes)

# print(contenido_bytesio)

# Creamos un objeto lector de PDF
lector = PyPDF2.PdfReader(contenido_bytesio)

# Creamos una variable para almacenar el texto extraído
text = ''

# Iteramos sobre cada página del PDF y extraemos su texto
for i in range(len(lector.pages)):
    pagina = lector.pages[i]
    text += pagina.extract_text()

# fragments = []

# for i in range(0, len(text), 2048):
#     texta = text[i:i+2048]
#
#     fragments.append(texta)

# for i in range(0, len(fragments)):
#     fragments[i] = fragments[i].replace("\n", "")
#     fragments[i] = fragments[i].replace("•", "")


def summarize_text(text, max_tokens):
    fragments = [text[i:i + 1500] for i in range(0, len(text), 1500)]
    for k in range(0, len(fragments)):
        fragments[k] = fragments[k].replace("\n", "")
        fragments[k] = fragments[k].replace("•", "")

    summaries = []

    for fragment in fragments:
        prompt = fragment
        responsed = openai.Edit.create(
            # engine="davinci",
            model="text-davinci-edit-002",
            input=prompt,
            instruction="Make a summary",
            n=1,
            temperature=0.5,
        )
        summary = responsed.choices[0].text.strip()
        summaries.append(summary)

    # Une los resumenes de cada fragmento

    summary = '\n'.join(summaries)
    return summary


summary_from_openai = summarize_text(text, max_tokens=150)
#
print(summary_from_openai)

# Imprimimos el texto extraído
with open("summary.txt", "w") as archivo:
    archivo.write(summary_from_openai)

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     url()
