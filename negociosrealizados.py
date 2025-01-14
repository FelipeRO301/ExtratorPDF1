import os
import re
import tkinter as tk
from tkinter import filedialog, ttk
import pdfplumber

def exibir_tabela(pdf_file):
    frame_links.pack_forget()
    frame_tabela.pack(fill="both", expand=True)
    
    negocios = extrair_negocios(pdf_file)

    for row in treeview.get_children():
        treeview.delete(row)

    for i, negocio in enumerate(negocios, start=1):
        treeview.insert("", "end", text=str(i), values=tuple(negocio.values()))

def selecionar_pasta():
    folder_path = filedialog.askdirectory()
    if folder_path:
        print("Pasta selecionada:", folder_path)
        pdfs_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.endswith(".pdf")]

        for widget in frame_buttons.winfo_children():
            widget.destroy()

        for pdf_path in pdfs_paths:
            button = tk.Button(frame_buttons, text=pdf_path, command=lambda path=pdf_path: exibir_tabela(path), bg='light blue')
            button.pack(side="top", padx=5, pady=5)

def voltar_links():
    frame_tabela.pack_forget()
    frame_links.pack(fill="both", expand=True)

def extrair_negocios(pdf_file):
    negocios = []
    
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            matches = re.finditer(r'(C|V)\s+(.*?)\s+(\d+)\s+([\d,]+)', text)
            
            for match in matches:
                tipo = match.group(1)
                especificacao = match.group(2)
                quantidade = match.group(3)
                preco_ajuste = match.group(4)
                
                negocios.append({
                    "C/V": tipo,
                    "Especificação do título": especificacao,
                    "Quantidade": quantidade,
                    "Preço / Ajuste": preco_ajuste
                })
    
    return negocios

root = tk.Tk()
root.title("Dados dos Negócios")
root.configure(bg='orange')


frame_links = tk.Frame(root, bg='orange')
frame_links.pack(fill="both", expand=True)

button_selecionar_pasta = tk.Button(frame_links, text="Selecionar pasta com PDFs", command=selecionar_pasta, bg='light blue')
button_selecionar_pasta.pack()

frame_buttons = tk.Frame(frame_links, bg='orange')
frame_buttons.pack(pady=10)


frame_tabela = tk.Frame(root, bg='orange')

treeview = ttk.Treeview(frame_tabela)
treeview["columns"] = ("C/V", "Especificação do título", "Quantidade", "Preço / Ajuste")

treeview.heading("#0", text="Índice")
treeview.column("#0", width=50)

for column in treeview["columns"]:
    treeview.heading(column, text=column)
    treeview.column(column, width=150)

frame_tabela_botoes = tk.Frame(frame_tabela, bg='orange')
frame_tabela_botoes.pack(pady=10)

button_voltar_links = tk.Button(frame_tabela_botoes, text="Voltar para links", command=voltar_links, bg='light blue')
button_voltar_links.pack()

treeview.pack(fill="both", expand=True)

root.mainloop()





