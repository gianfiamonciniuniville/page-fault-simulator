import tkinter as tk
from tkinter import messagebox

class SimuladorMemoriaVirtualGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Page-Fault - Memória Virtual")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.num_quadros = tk.IntVar(value=3)
        self.num_paginas = tk.IntVar(value=5)

        self.memoria_virtual = []
        self.memoria_principal = []
        self.etp = {}
        self.fila_substituicao = []
        self.page_faults = 0

        self.botoes_paginas = []

        self.configurar_interface()

    def configurar_interface(self):
        fonte_titulo = ("Arial", 14, "bold")
        fonte_conteudo = ("Arial", 12)

        # Frame superior - configurações
        frame_config = tk.Frame(self.root, bg="#f0f0f0")
        frame_config.pack(pady=10)

        tk.Label(frame_config, text="Quadros de Memória Principal:", font=fonte_conteudo, bg="#f0f0f0").grid(row=0, column=0, padx=10)
        tk.Spinbox(frame_config, from_=1, to=10, textvariable=self.num_quadros, width=5,
                   font=fonte_conteudo, command=self.reiniciar_simulador).grid(row=0, column=1)

        tk.Label(frame_config, text="Páginas na Memória Virtual:", font=fonte_conteudo, bg="#f0f0f0").grid(row=0, column=2, padx=10)
        tk.Spinbox(frame_config, from_=1, to=20, textvariable=self.num_paginas, width=5,
                   font=fonte_conteudo, command=self.reiniciar_simulador).grid(row=0, column=3)

        # Frame dos botões de páginas
        self.frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_botoes.pack(pady=15)
        self.label_botoes = tk.Label(self.frame_botoes, text="", font=fonte_titulo, bg="#f0f0f0")
        self.label_botoes.pack(anchor="w")

        # Frame da memória principal
        frame_memoria = tk.Frame(self.root, bg="#f0f0f0")
        frame_memoria.pack(pady=10, fill="x")
        tk.Label(frame_memoria, text="Memória Principal:", font=fonte_titulo, bg="#f0f0f0").pack(anchor="w")
        self.memoria_label = tk.Label(frame_memoria, text="", fg="blue", font=fonte_conteudo, bg="#f0f0f0")
        self.memoria_label.pack(anchor="w", padx=10)
        
        # Frame da tabela ETP
        self.frame_etp = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_etp.pack(pady=10, fill="x")
        tk.Label(self.frame_etp, text="Tabela de Páginas (ETP):", font=fonte_titulo, bg="#f0f0f0").pack(anchor="w")
        self.etp_tabela = tk.Frame(self.frame_etp, bg="#ffffff", bd=1, relief="solid")
        self.etp_tabela.pack(padx=10, pady=5, anchor="w")

        # Frame do contador de page-faults
        frame_rodape = tk.Frame(self.root, bg="#f0f0f0")
        frame_rodape.pack(pady=10, fill="x")
        self.page_faults_label = tk.Label(frame_rodape, text="Total de Page-Faults: 0", fg="red", font=fonte_conteudo, bg="#f0f0f0")
        self.page_faults_label.pack(anchor="w", padx=10)
        
        # Botão Reset
        btn_reset = tk.Button(frame_config, text="Resetar Simulação", font=fonte_conteudo, bg="#ffcccc", command=self.reiniciar_simulador)
        btn_reset.grid(row=0, column=4, padx=15)

        self.reiniciar_simulador()

    def reiniciar_simulador(self):
        n = self.num_paginas.get()
        self.memoria_virtual = [f"P{i+1}" for i in range(n)]
        self.memoria_principal = []
        self.etp = {pagina: None for pagina in self.memoria_virtual}
        self.fila_substituicao = []
        self.page_faults = 0

        # Atualiza botões das páginas
        for btn in self.botoes_paginas:
            btn.destroy()
        self.botoes_paginas = []

        self.label_botoes.config(text="Clique para acessar uma página da Memória Virtual:")

        for pagina in self.memoria_virtual:
            btn = tk.Button(self.frame_botoes, text=pagina, width=6, font=("Arial", 12),
                            command=lambda p=pagina: self.acessar_pagina(p), bg="#e0e0ff")
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.botoes_paginas.append(btn)

        self.atualizar_interface()

    def acessar_pagina(self, pagina):
        if pagina in self.memoria_principal:
            messagebox.showinfo("Acesso à Página", f"A página {pagina} já está na memória principal.")
        else:
            messagebox.showinfo("Page-Fault", f"Page-fault detectado ao acessar a página {pagina}.")
            self.page_faults += 1
            self.page_in(pagina)
        self.atualizar_interface()

    def page_in(self, pagina):
        if len(self.memoria_principal) < self.num_quadros.get():
            self.memoria_principal.append(pagina)
            frame_index = self.memoria_principal.index(pagina)
        else:
            pagina_removida = self.fila_substituicao.pop(0)
            frame_index = self.memoria_principal.index(pagina_removida)
            self.memoria_principal[frame_index] = pagina
            self.etp[pagina_removida] = None
        self.etp[pagina] = f"Quadro {frame_index}"
        self.fila_substituicao.append(pagina)

    def atualizar_interface(self):
        self.memoria_label.config(text=" | ".join(self.memoria_principal))

        # Limpa a tabela antiga
        for widget in self.etp_tabela.winfo_children():
            widget.destroy()

        # Cabeçalho da tabela
        header_font = ("Arial", 11, "bold")
        cell_font = ("Arial", 11)

        tk.Label(self.etp_tabela, text="Página", width=15, font=header_font, bg="#d0d0d0", relief="ridge").grid(row=0, column=0)
        tk.Label(self.etp_tabela, text="Quadro", width=15, font=header_font, bg="#d0d0d0", relief="ridge").grid(row=0, column=1)

        for i, pagina in enumerate(self.memoria_virtual, start=1):
            quadro = self.etp[pagina] if self.etp[pagina] is not None else "-"
            tk.Label(self.etp_tabela, text=pagina, width=15, font=cell_font, bg="#f9f9f9", relief="ridge").grid(row=i, column=0)
            tk.Label(self.etp_tabela, text=quadro, width=15, font=cell_font, bg="#f9f9f9", relief="ridge").grid(row=i, column=1)

        self.page_faults_label.config(text=f"Total de Page-Faults: {self.page_faults}")


# Execução da interface
if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorMemoriaVirtualGUI(root)
    root.mainloop()
