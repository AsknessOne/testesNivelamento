from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

data_path = "testeAPI\Relatorio.csv"


if os.path.exists(data_path):
    try:
        df = pd.read_csv(data_path, encoding="utf-8", sep=";", dtype=str)
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        df = pd.DataFrame()  
else:
    print("Arquivo CSV não encontrado!")
    df = pd.DataFrame()

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query", "").strip().lower()
    results = None

    if not df.empty and "Razao_Social" in df.columns:
        df["Razao_Social"] = df["Razao_Social"].fillna("")  
        if query:
            results = df[df["Razao_Social"].str.contains(query, case=False, na=False)]

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)







