import tkinter as tk
from tkinter import filedialog
import PyPDF2
import re 
import psycopg2
import os

def conectar_bd():
    conn = psycopg2.connect(
        host="pontomais.postgresql.dbaas.com.br",
        user="pontomais",
        password="tsc10012000@",
        database="pontomais",
        port=5432
    )
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS informacoes
                      (id SERIAL PRIMARY KEY,
                       nr_nota VARCHAR(255) UNIQUE,
                       data_pregao VARCHAR(255))''')
    
    conn.commit()
    conn.close()

def extrair_informacoes(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        nr_nota = None
        data_pregao = None
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            match_nr_nota = re.search(r'Nr\. nota\s*([\d]+)', text)
            match_data_pregao = re.search(r'Data pregão\s*(\d{2}/\d{2}/\d{4})', text)
            
            if match_nr_nota:
                nr_nota = match_nr_nota.group(1)
            if match_data_pregao:
                data_pregao = match_data_pregao.group(1)
        
        return nr_nota, data_pregao

def exibir_info():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        nr_nota, data_pregao = extrair_informacoes(file_path)
        
        if nr_nota and data_pregao:
            label_nr_nota.config(text="Nr. nota: " + str(nr_nota))
            label_data_pregao.config(text="Data pregão: " + str(data_pregao))
            salvar_no_bd(nr_nota, data_pregao)
        else:
            label_nr_nota.config(text="Nr. nota: Informação não encontrada")
            label_data_pregao.config(text="Data pregão: Informação não encontrada")

def salvar_no_bd(nr_nota, data_pregao):
    conn = psycopg2.connect(
        host="pontomais.postgresql.dbaas.com.br",
        user="pontomais",
        password="tsc10012000@",
        database="pontomais",
        port=5432
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM informacoes WHERE nr_nota=%s", (nr_nota,))
    resultado = cursor.fetchone()
    
    if resultado is None:
        cursor.execute("INSERT INTO informacoes (nr_nota, data_pregao) VALUES (%s, %s)", (nr_nota, data_pregao))
        conn.commit()
    
    conn.close()

def abrir_negocios_realizados():
    os.system("python negociosrealizados.py")

def abrir_resumo_financeiro():
    os.system("python resumofinanceirodois.py")

def abrir_resumo_negocios():
    os.system("python resumonegociosdois.py")

root = tk.Tk()
root.title("Extrair informações do PDF")
root.configure(bg='yellow')

conectar_bd()

label_nr_nota = tk.Label(root, text="Nr. nota: ", bg='yellow')
label_nr_nota.pack()

label_data_pregao = tk.Label(root, text="Data pregão: ", bg='yellow')
label_data_pregao.pack()

button_exibir_info = tk.Button(root, text="Escolher PDF e exibir informações", command=exibir_info, bg='navy', fg='white')
button_exibir_info.pack()

button_negocios_realizados = tk.Button(root, text="Negócios Realizados", command=abrir_negocios_realizados, bg='navy', fg='white')
button_negocios_realizados.pack()

button_resumo_financeiro = tk.Button(root, text="Resumo Financeiro", command=abrir_resumo_financeiro, bg='navy', fg='white')
button_resumo_financeiro.pack()

button_resumo_negocios = tk.Button(root, text="Resumo Negócios", command=abrir_resumo_negocios, bg='navy', fg='white')
button_resumo_negocios.pack()

root.mainloop()

