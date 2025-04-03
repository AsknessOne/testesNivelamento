import requests
from bs4 import BeautifulSoup
import os
import zipfile


site = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

retorno = requests.get(site, headers=headers)

if retorno.status_code == 200:
    soup = BeautifulSoup(retorno.text, "html.parser")

    pdf = []

    for link in soup.find_all("a", href=True):  
        href = link["href"] 
        if href.endswith(".pdf") and ("Anexo I" in link.text or "Anexo II" in link.text):  
            pdf.append(href if href.startswith("http") else f"https://www.gov.br{href}")  

    os.makedirs("pdfs", exist_ok=True)

    for idx, pdf_url in enumerate(pdf, start=1):
        pdf_response = requests.get(pdf_url)
        pdf_path = f"pdfs/Anexo_{idx}.pdf"

        with open(pdf_path, "wb") as file:
            file.write(pdf_response.content)

        print(f"Download concluído: {pdf_path}")

else:
    print("Houve um erro ao tentar acessar esta página:", retorno.status_code)

os.makedirs("resultadozip", exist_ok=True)

arquivo_zip = "resultadozip/anexos.zip"  

with zipfile.ZipFile(arquivo_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, _, arquivos in os.walk("pdfs"):
        for arquivo in arquivos:
            zipf.write(os.path.join(root, arquivo), arcname=arquivo)

print(f"Arquivo ZIP criado: {arquivo_zip}")



