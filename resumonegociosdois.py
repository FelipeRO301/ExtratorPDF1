import pdfplumber
import tkinter as tk
from tkinter import filedialog
import psycopg2

def conectar_bd():
    conn = psycopg2.connect(
        host="pontomais.postgresql.dbaas.com.br",
        user="pontomais",
        password="tsc10012000@",
        database="pontomais",
        port=5432
    )
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS resumonegocios
                      (id SERIAL PRIMARY KEY,
                       texto TEXT)''')
    
    conn.commit()
    conn.close()

def extrair_texto(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        page = pdf.pages[-1]
        area = (5, page.height - 410, 300, page.height - 320)
        texto = page.within_bbox(area).extract_text()
    return texto

def verificar_dados(texto):
    conn = psycopg2.connect(
        host="pontomais.postgresql.dbaas.com.br",
        user="pontomais",
        password="tsc10012000@",
        database="pontomais",
        port=5432
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT texto FROM resumonegocios WHERE texto = %s", (texto,))
    result = cursor.fetchone()
    
    conn.close()
    
    return result

def exibir_texto():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        texto = extrair_texto(file_path)
        
        if texto:
            texto_label = tk.Label(root, text=texto, font=("Arial", 10), anchor="w", justify="left", wraplength=500)
            texto_label.grid(row=1, column=0, padx=10, pady=5)
            
            if not verificar_dados(texto):
                salvar_no_bd(texto)
        else:
            tk.Label(root, text="Texto não encontrado", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5)

def salvar_no_bd(texto):
    conn = psycopg2.connect(
        host="pontomais.postgresql.dbaas.com.br",
        user="pontomais",
        password="tsc10012000@",
        database="pontomais",
        port=5432
    )
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO resumonegocios 
                      (texto) 
                      VALUES (%s)''', 
                   (texto,))
    
    conn.commit()
    conn.close()

def voltar():
    root.destroy()
    import folha

root = tk.Tk()
root.title("Extrair Texto")
root.configure(bg='orange')

button_exibir = tk.Button(root, text="Escolher PDF e Exibir Texto", command=exibir_texto, font=("Arial", 12), bg='light blue')
button_exibir.grid(row=0, column=0, pady=10)

button_voltar = tk.Button(root, text="Voltar", command=voltar, font=("Arial", 12), bg='light blue')
button_voltar.grid(row=2, column=0, pady=10)

conectar_bd()

root.mainloop()
