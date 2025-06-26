import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Conexão com o banco
def conectar():
    return sqlite3.connect('clientes.db')

# Criar tabela
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inserir cliente
def inserir_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()
    if nome and email and telefone and endereco:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO clientes (nome, email, telefone, endereco) VALUES (?, ?, ?, ?)', 
                  (nome, email, telefone, endereco))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Cliente inserido com sucesso.')
        mostrar_clientes()
        limpar_campos()
    else:
        messagebox.showerror('Erro', 'Preencha todos os campos.')

# Mostrar clientes
def mostrar_clientes():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes')
    clientes = c.fetchall()
    conn.close()
    for cliente in clientes:
        tree.insert("", "end", values=cliente)

# Deletar cliente
def delete_cliente():
    selecionado = tree.selection()
    if selecionado:
        cliente_id = tree.item(selecionado)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM clientes WHERE id=?', (cliente_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Cliente deletado com sucesso.')
        mostrar_clientes()
    else:
        messagebox.showerror('Erro', 'Selecione um cliente para deletar.')

# Editar cliente
def editar_cliente():
    selecionado = tree.selection()
    if selecionado:
        cliente_id = tree.item(selecionado)['values'][0]
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        endereco = entry_endereco.get()
        if nome and email and telefone and endereco:
            conn = conectar()
            c = conn.cursor()
            c.execute('''
                UPDATE clientes SET nome=?, email=?, telefone=?, endereco=? WHERE id=?
            ''', (nome, email, telefone, endereco, cliente_id))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Cliente atualizado com sucesso.')
            mostrar_clientes()
        else:
            messagebox.showerror('Erro', 'Preencha todos os campos.')
    else:
        messagebox.showwarning('Aviso', 'Selecione um cliente para editar.')

# Limpar campos de entrada
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)

# Interface gráfica
janela = tk.Tk()
janela.title('Cadastro de Clientes - XYZ Comércio')
janela.geometry('750x600')
janela.configure(bg='lightgray')

tk.Label(janela, text='Sistema de Cadastro de Clientes', font=('Arial', 20, 'bold'), fg='blue', bg='lightgray').pack(pady=10)

frame_form = tk.Frame(janela, bg='lightgray')
frame_form.pack(pady=10)

# Campos de entrada
tk.Label(frame_form, text='Nome:', bg='lightgray').grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_nome = tk.Entry(frame_form, width=40)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text='Email:', bg='lightgray').grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_email = tk.Entry(frame_form, width=40)
entry_email.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text='Telefone:', bg='lightgray').grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_telefone = tk.Entry(frame_form, width=40)
entry_telefone.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_form, text='Endereço:', bg='lightgray').grid(row=3, column=0, padx=5, pady=5, sticky='e')
entry_endereco = tk.Entry(frame_form, width=40)
entry_endereco.grid(row=3, column=1, padx=5, pady=5)

# Botões
frame_botoes = tk.Frame(janela, bg='lightgray')
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text='Inserir', command=inserir_cliente, width=12).grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text='Editar', command=editar_cliente, width=12).grid(row=0, column=1, padx=5)
tk.Button(frame_botoes, text='Excluir', command=delete_cliente, width=12).grid(row=0, column=2, padx=5)

# Tabela
tree = ttk.Treeview(janela, columns=('ID', 'Nome', 'Email', 'Telefone', 'Endereço'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('Email', text='Email')
tree.heading('Telefone', text='Telefone')
tree.heading('Endereço', text='Endereço')
tree.pack(pady=20, fill='both', expand=True)

# Inicialização
criar_tabela()
mostrar_clientes()
janela.mainloop()
