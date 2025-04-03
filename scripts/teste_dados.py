import pdfplumber  
import pandas as pd  
import zipfile  
import os
pdf = "pdfs/Anexo_1.pdf"
dados = []

with pdfplumber.open(pdf) as pdf:
    for page in pdf.pages:  
        tabelas = page.extract_tables()  
        for tabela in tabelas:  
            for linha in tabela:  
                dados.append(linha) 

df = pd.DataFrame(dados)


df.columns = df.iloc[0]  
df = df[1:].reset_index(drop=True)  


if "OD" in df.columns and "AMB" in df.columns:
   df["OD"] = df["OD"].replace({"OD": "Seg. Odontológica", "": "Não"})
   df["AMB"] = df["AMB"].replace({"AMB": "Seg. Ambulatorial", "": "Não"})

else:
    print("As colunas 'OD' e/ou 'AMB' não foram encontradas no DataFrame.")


csv_filename = "rol_procedimentos_eventos.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8")

os.makedirs("resultadozip", exist_ok=True)

zip_filename = "resultadozip/Teste_Cinthia.zip"
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_filename, arcname=csv_filename)

print("Substituição concluída com sucesso e arquivo salvo!")


