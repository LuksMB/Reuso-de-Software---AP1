import tkinter as tk
from tkinter import messagebox
import requests
import tkinter.simpledialog

API_URL = "http://localhost:8000/cursos"

class CursoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Cursos")
        self.root.geometry("600x400")
        
        self.create_widgets()
        self.listar_cursos()
    
    def create_widgets(self):
        self.list_label = tk.Label(self.root, text="Cursos Cadastrados", font=("Arial", 14))
        self.list_label.pack(pady=10)
        
        self.cursos_listbox = tk.Listbox(self.root, width=80, height=10)
        self.cursos_listbox.pack(pady=10)
        
        self.frame_body = tk.Frame(self.root)
        self.frame_body.pack(pady=10)
        
        self.title_entry = tk.Entry(self.frame_body, width=50)
        self.title_entry.insert(0, "Título do Curso")
        self.title_entry.grid(row=0, column=0, padx=5)
        
        self.description_entry = tk.Entry(self.frame_body, width=50)
        self.description_entry.insert(0, "Descrição do Curso")
        self.description_entry.grid(row=1, column=0, padx=5)
        
        self.ch_entry = tk.Entry(self.frame_body, width=50)
        self.ch_entry.insert(0, "Carga Horária (em horas)")
        self.ch_entry.grid(row=2, column=0, padx=5)
        
        self.frame_options = tk.Frame(self.root)
        self.frame_options.pack(pady=10)

        self.btn_adicionar = tk.Button(self.frame_options, text="Adicionar", command=self.adicionar_curso)
        self.btn_adicionar.grid(row=0, column=0, pady=5)
        
        self.btn_examinar = tk.Button(self.frame_options, text="Examinar", command=self.examinar_curso)
        self.btn_examinar.grid(row=0, column=1, padx=5)
        
        self.btn_atualizar = tk.Button(self.frame_options, text="Alterar", command=self.atualizar_curso)
        self.btn_atualizar.grid(row=0, column=2, padx=5)
        
        self.btn_excluir = tk.Button(self.frame_options, text="Excluir", command=self.excluir_curso)
        self.btn_excluir.grid(row=0, column=3, padx=5)
    
    def listar_cursos(self):
        self.cursos_listbox.delete(0, tk.END)
        
        try:
            response = requests.get(API_URL)
            cursos = response.json()
            if isinstance(cursos, list):
                for curso in cursos:
                    self.cursos_listbox.insert(tk.END, f"{curso[0]} - {curso[1]}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Não foi possível conectar à API: {e}")

    def adicionar_curso(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        ch = self.ch_entry.get()
        
        if not title or not description or not ch:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        
        data = {
            "title": title,
            "description": description,
            "ch": int(ch)
        }

        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Curso adicionado com sucesso!")
                self.listar_cursos()
            else:
                messagebox.showerror("Erro", f"Erro ao adicionar curso: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro na comunicação com a API: {e}")

    def examinar_curso(self):
        selected_index = self.cursos_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Selecione um curso para examinar.")
            return
        
        curso_info = self.cursos_listbox.get(selected_index)
        curso_id = curso_info.split(" - ")[0]
        
        try:
            response = requests.get(f"{API_URL}/{curso_id}")
            if response.status_code == 200:
                curso = response.json()
                details = f"ID: {curso[0]}\nTítulo: {curso[1]}\nDescrição: {curso[2]}\nCarga Horária: {curso[3]}"
                messagebox.showinfo(f"Detalhes do Curso {curso[0]}", details)
                
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, curso[1])
                
                self.description_entry.delete(0, tk.END)
                self.description_entry.insert(0, curso[2])
                
                self.ch_entry.delete(0, tk.END)
                self.ch_entry.insert(0, curso[3])
            else:
                messagebox.showerror("Erro", f"Erro ao examinar curso: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro na comunicação com a API: {e}")

    def atualizar_curso(self):
        selected_index = self.cursos_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Selecione um curso para atualizar.")
            return
        
        curso_info = self.cursos_listbox.get(selected_index)
        curso_id = curso_info.split(" - ")[0]
        
        new_title = self.title_entry.get()
        new_description = self.description_entry.get()
        new_ch = self.ch_entry.get()
        
        if not new_title or not new_description or not new_ch:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        
        data = {
            "title": new_title,
            "description": new_description,
            "ch": int(new_ch)
        }

        try:
            response = requests.put(f"{API_URL}/{curso_id}", json=data)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", f"Curso com ID {curso_id} atualizado!")
                self.listar_cursos()
            else:
                messagebox.showerror("Erro", f"Erro ao atualizar curso: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro na comunicação com a API: {e}")
    
    def excluir_curso(self):
        selected_index = self.cursos_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Selecione um curso para excluir.")
            return
        
        curso_info = self.cursos_listbox.get(selected_index)
        curso_id = curso_info.split(" - ")[0]
        
        try:
            response = requests.delete(f"{API_URL}/{curso_id}")
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", f"Curso com ID {curso_id} excluído!")
                self.listar_cursos()
            else:
                messagebox.showerror("Erro", f"Erro ao excluir curso: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro na comunicação com a API: {e}")