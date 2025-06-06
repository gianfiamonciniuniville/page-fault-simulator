import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re

class PageTableEntry:
    def __init__(self, page_id, frame_id=None, present=False):
        self.page_id = page_id
        self.frame_id = frame_id
        self.present = present

class MemorySimulator:
    def __init__(self, main_memory_size, virtual_memory_pages):
        self.main_memory_size = main_memory_size
        self.main_memory = [None] * main_memory_size  # Represents physical frames
        self.virtual_memory = virtual_memory_pages  # List of all pages on disk
        self.page_table = {}
        self.page_faults = 0
        self.access_history = []

        # Initialize page table entries for all virtual pages
        for page in self.virtual_memory:
            self.page_table[page] = PageTableEntry(page)

    def access_page(self, page_id):
        result = []
        result.append(f"Usuário solicita acesso à Página {page_id}:")
        
        if page_id not in self.page_table:
            result.append(f"Erro: Página {page_id} não existe na memória virtual.")
            return result

        entry = self.page_table[page_id]
        self.access_history.append(page_id)

        if entry.present:
            result.append(f"Página {page_id} já está na memória principal (Frame {entry.frame_id}).")
        else:
            result.append("Page-fault detectado.")
            self.page_faults += 1

            # Find a free frame or choose one for replacement
            free_frame_id = -1
            for i, frame_content in enumerate(self.main_memory):
                if frame_content is None:
                    free_frame_id = i
                    break

            if free_frame_id != -1:
                # Page-in: load page to free frame
                self.main_memory[free_frame_id] = page_id
                entry.frame_id = free_frame_id
                entry.present = True
                result.append(f"Página {page_id} carregada para o Frame {free_frame_id}.")
            else:
                # No free frame, implement a simple FIFO replacement
                # For simplicity, let's replace the page in frame 0 for now
                # A more robust FIFO would require tracking load order
                page_to_replace_id = self.main_memory[0]
                old_entry = self.page_table[page_to_replace_id]
                old_entry.present = False
                old_entry.frame_id = None

                self.main_memory[0] = page_id
                entry.frame_id = 0
                entry.present = True
                result.append(f"Memória cheia. Página {page_to_replace_id} substituída pela Página {page_id} no Frame 0.")

        return result

    def get_status(self):
        status = []
        status.append("--- Estado Atual ---")
        status.append(f"Memória Principal (Frames): {self.main_memory}")
        status.append("Tabela de Páginas (ETP):")
        for page_id, entry in self.page_table.items():
            page_status = f"Frame {entry.frame_id}" if entry.present else "-"
            status.append(f"  Página {page_id}: {page_status}")
        status.append(f"Área de Memória Virtual (Disco): {self.virtual_memory}")
        status.append(f"Page Faults: {self.page_faults}")
        return status

class MemorySimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Gerenciamento de Memória Virtual")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.simulator = None
        self.create_widgets()
        
    def create_widgets(self):
        # Frame para configuração
        config_frame = ttk.LabelFrame(self.root, text="Configuração")
        config_frame.pack(fill="x", padx=10, pady=10)
        
        # Número de quadros
        ttk.Label(config_frame, text="Número de quadros da memória principal:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.frames_entry = ttk.Entry(config_frame, width=10)
        self.frames_entry.grid(row=0, column=1, padx=5, pady=5)
        self.frames_entry.insert(0, "3")
        
        # Páginas da memória virtual
        ttk.Label(config_frame, text="Páginas da memória virtual (separadas por vírgula):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.pages_entry = ttk.Entry(config_frame, width=30)
        self.pages_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        self.pages_entry.insert(0, "P1,P2,P3,P4,P5")
        
        # Botão para inicializar o simulador
        self.init_button = ttk.Button(config_frame, text="Inicializar Simulador", command=self.initialize_simulator)
        self.init_button.grid(row=2, column=0, padx=5, pady=5)
        
        # Botão para resetar o simulador
        self.reset_button = ttk.Button(config_frame, text="Resetar Simulador", command=self.reset_simulator, state="disabled")
        self.reset_button.grid(row=2, column=1, padx=5, pady=5)
        
        # Frame para acesso a páginas
        access_frame = ttk.LabelFrame(self.root, text="Acesso a Páginas")
        access_frame.pack(fill="x", padx=10, pady=10)
        
        # Combobox para selecionar página
        ttk.Label(access_frame, text="Selecione uma página para acessar:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.page_combobox = ttk.Combobox(access_frame, width=10, state="disabled")
        self.page_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        # Botão para acessar página
        self.access_button = ttk.Button(access_frame, text="Acessar Página", command=self.access_page, state="disabled")
        self.access_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Frame para exibição do estado
        status_frame = ttk.LabelFrame(self.root, text="Estado do Sistema")
        status_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Área de texto para exibir o estado
        self.status_text = scrolledtext.ScrolledText(status_frame, wrap=tk.WORD, width=80, height=20)
        self.status_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.status_text.config(state="disabled")
        
        # Frame para estatísticas
        stats_frame = ttk.LabelFrame(self.root, text="Estatísticas")
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        # Label para exibir o número de page faults
        ttk.Label(stats_frame, text="Page Faults:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.page_faults_var = tk.StringVar(value="0")
        ttk.Label(stats_frame, textvariable=self.page_faults_var).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Label para exibir o histórico de acessos
        ttk.Label(stats_frame, text="Histórico de Acessos:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.access_history_var = tk.StringVar(value="")
        ttk.Label(stats_frame, textvariable=self.access_history_var).grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    def initialize_simulator(self):
        try:
            main_memory_size = int(self.frames_entry.get())
            if main_memory_size <= 0:
                raise ValueError("O número de quadros deve ser um inteiro positivo.")
                
            virtual_memory_input = self.pages_entry.get()
            if not virtual_memory_input.strip():
                raise ValueError("A lista de páginas não pode estar vazia.")
                
            virtual_memory_pages = [p.strip() for p in virtual_memory_input.split(',')]
            
            # Validar nomes de páginas (apenas letras, números e underscore)
            for page in virtual_memory_pages:
                if not re.match(r'^[a-zA-Z0-9_]+$', page):
                    raise ValueError(f"Nome de página inválido: {page}. Use apenas letras, números e underscore.")
            
            # Verificar páginas duplicadas
            if len(virtual_memory_pages) != len(set(virtual_memory_pages)):
                raise ValueError("Existem páginas duplicadas na lista.")
            
            self.simulator = MemorySimulator(main_memory_size, virtual_memory_pages)
            
            # Atualizar combobox com as páginas disponíveis
            self.page_combobox['values'] = virtual_memory_pages
            self.page_combobox.current(0)
            self.page_combobox['state'] = 'readonly'
            
            # Habilitar botões de acesso e reset
            self.access_button['state'] = 'normal'
            self.reset_button['state'] = 'normal'
            
            # Desabilitar botão de inicialização e campos de configuração
            self.init_button['state'] = 'disabled'
            self.frames_entry['state'] = 'disabled'
            self.pages_entry['state'] = 'disabled'
            
            # Exibir estado inicial
            self.update_status("Simulador inicializado com sucesso!")
            self.update_status_display(self.simulator.get_status())
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
    
    def reset_simulator(self):
        # Limpar o simulador
        self.simulator = None
        
        # Reabilitar campos de configuração e botão de inicialização
        self.frames_entry['state'] = 'normal'
        self.pages_entry['state'] = 'normal'
        self.init_button['state'] = 'normal'
        
        # Desabilitar botões de acesso e reset
        self.page_combobox['state'] = 'disabled'
        self.access_button['state'] = 'disabled'
        self.reset_button['state'] = 'disabled'
        
        # Limpar estatísticas
        self.page_faults_var.set("0")
        self.access_history_var.set("")
        
        # Limpar área de status
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "Simulador resetado. Configure novos parâmetros e clique em 'Inicializar Simulador'.\n")
        self.status_text.config(state="disabled")
    
    def access_page(self):
        if not self.simulator:
            messagebox.showerror("Erro", "O simulador não foi inicializado.")
            return
            
        page_id = self.page_combobox.get()
        if not page_id:
            messagebox.showerror("Erro", "Selecione uma página para acessar.")
            return
            
        # Acessar a página e obter o resultado
        result = self.simulator.access_page(page_id)
        
        # Atualizar a exibição do estado
        self.update_status_display(result)
        self.update_status_display(self.simulator.get_status())
        
        # Atualizar estatísticas
        self.page_faults_var.set(str(self.simulator.page_faults))
        self.access_history_var.set(", ".join(self.simulator.access_history))
    
    def update_status(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
    
    def update_status_display(self, status_list):
        self.status_text.config(state="normal")
        for line in status_list:
            self.status_text.insert(tk.END, line + "\n")
        self.status_text.insert(tk.END, "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemorySimulatorGUI(root)
    root.mainloop()

