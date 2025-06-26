import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Conexão com o banco
def conectar():
    return sqlite3.connect('teste.db')

# Criar tabela
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            cpf TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inserir usuário
def inserir_usuario():
    nome = entry_nome.get()
    email = entry_email.get()
    cpf = entry_cpf.get()
    if nome and email and cpf:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO usuarios (nome, email, cpf) VALUES (?, ?, ?)', (nome, email, cpf))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Usuário inserido com sucesso.')
        mostrar_usuarios()
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
    else:
        messagebox.showerror('Erro', 'Preencha todos os campos.')

# Mostrar usuários
def mostrar_usuarios():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()
    conn.close()
    for user in usuarios:
        tree.insert("", "end", values=(user[0], user[1], user[2], user[3]))

# Deletar usuário
def delete_usuario():
    selecionado = tree.selection()
    if selecionado:
        user_id = tree.item(selecionado)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM usuarios WHERE id=?', (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Usuário deletado com sucesso.')
        mostrar_usuarios()
    else:
        messagebox.showerror('Erro', 'Selecione um usuário para deletar.')

# Editar usuário
def editar_usuario():
    selecionado = tree.selection()
    if selecionado:
        user_id = tree.item(selecionado)['values'][0]
        novo_nome = entry_nome.get()
        novo_email = entry_email.get()
        novo_cpf = entry_cpf.get()
        if novo_nome and novo_email and novo_cpf:
            conn = conectar()
            c = conn.cursor()
            c.execute('UPDATE usuarios SET nome = ?, email = ?, cpf = ? WHERE id = ?', 
                      (novo_nome, novo_email, novo_cpf, user_id))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Usuário atualizado com sucesso.')
            mostrar_usuarios()
        else:
            messagebox.showerror('Erro', 'Preencha todos os campos para editar.')
    else:
        messagebox.showwarning('Aviso', 'Selecione um usuário para editar.')

# Interface gráfica
janela = tk.Tk()
janela.title('CRUD com SQLite e CPF')
janela.geometry('650x550')
janela.configure(bg='lightgray')

tk.Label(janela, text='Sistema de Cadastro', font=('Roboto', 20, 'bold'), fg='blue', bg='lightgray').pack(pady=10)

frame_form = tk.Frame(janela, bg='lightgray')
frame_form.pack(pady=10)

tk.Label(frame_form, text='Nome:', bg='lightgray').grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_nome = tk.Entry(frame_form)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text='Email:', bg='lightgray').grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_email = tk.Entry(frame_form)
entry_email.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text='CPF:', bg='lightgray').grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_cpf = tk.Entry(frame_form)
entry_cpf.grid(row=2, column=1, padx=5, pady=5)

frame_botoes = tk.Frame(janela, bg='lightgray')
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text='Inserir', command=inserir_usuario, width=12).grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text='Editar', command=editar_usuario, width=12).grid(row=0, column=1, padx=5)
tk.Button(frame_botoes, text='Excluir', command=delete_usuario, width=12).grid(row=0, column=2, padx=5)

# Tabela Treeview
tree = ttk.Treeview(janela, columns=('ID', 'Nome', 'Email', 'CPF'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('Email', text='Email')
tree.heading('CPF', text='CPF')
tree.pack(pady=20, fill='both', expand=True)

# Inicialização
criar_tabela()
mostrar_usuarios()
janela.mainloop()