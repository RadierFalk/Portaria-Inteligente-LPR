import tkinter as tk
from tkinter import messagebox
import database

def salvar():
    res = database.cadastrar_usuario(
        entry_placa.get(), entry_nome.get(), entry_tel.get(),
        entry_end.get(), entry_mod.get(), entry_mar.get()
    )
    if res:
        messagebox.showinfo("Sucesso", "Cadastrado com sucesso!")
        limpar()
    else:
        messagebox.showerror("Erro", "Placa já cadastrada ou erro no banco.")

def limpar():
    for entry in [entry_placa, entry_nome, entry_tel, entry_end, entry_mod, entry_mar]:
        entry.delete(0, tk.END)

root = tk.Tk()
root.title("Cadastro de Moradores - LPR")

# Layout simples
fields = ["Placa:", "Nome Completo:", "Telefone:", "Endereço:", "Modelo Carro:", "Marca Carro:"]
entries = []

for field in fields:
    row = tk.Frame(root)
    lbl = tk.Label(row, text=field, width=15)
    ent = tk.Entry(row)
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    lbl.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append(ent)

entry_placa, entry_nome, entry_tel, entry_end, entry_mod, entry_mar = entries

tk.Button(root, text="Salvar", command=salvar).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(root, text="Limpar", command=limpar).pack(side=tk.RIGHT, padx=5, pady=5)

root.mainloop()