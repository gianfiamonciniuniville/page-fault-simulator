import tkinter as tk
from tkinter import messagebox, scrolledtext

class SimuladorMemoriaVirtual:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Page-Fault com Memória Virtual")
        self.root.geometry("900x650")
        self.root.configure(bg="#eef2f7")

        # Variáveis configuráveis
        self.num_quadros = tk.IntVar(value=3)
        self.num_paginas = tk.IntVar(value=7)

        # Estado
        self.page_faults = 0
        self.etp = {}
        self.memoria_principal = []
        self.memoria_virtual = []

        # Interface
        self.configurar_interface()
        self.reiniciar_simulador()

    def configurar_interface(self):
        fonte_titulo = ("Segoe UI", 16, "bold")
        fonte_secundaria = ("Segoe UI", 12)
        fonte_normal = ("Segoe UI", 11)

        # Frame Configurações (topo)
        frame_config = tk.Frame(self.root, bg="#dbe7f3", bd=1, relief="groove")
        frame_config.pack(fill="x", padx=15, pady=12)

        tk.Label(frame_config, text="Quadros Memória Principal:", font=fonte_secundaria, bg="#dbe7f3").grid(row=0, column=0, padx=12, pady=6, sticky="w")
        spin_quadros = tk.Spinbox(frame_config, from_=1, to=10, textvariable=self.num_quadros, width=6, font=fonte_normal, command=self.reiniciar_simulador)
        spin_quadros.grid(row=0, column=1, pady=6, sticky="w")

        tk.Label(frame_config, text="Páginas Memória Virtual:", font=fonte_secundaria, bg="#dbe7f3").grid(row=0, column=2, padx=12, pady=6, sticky="w")
        spin_paginas = tk.Spinbox(frame_config, from_=1, to=20, textvariable=self.num_paginas, width=6, font=fonte_normal, command=self.reiniciar_simulador)
        spin_paginas.grid(row=0, column=3, pady=6, sticky="w")

        btn_reset = tk.Button(frame_config, text="Resetar Simulação", font=fonte_secundaria, bg="#f28c8c", fg="#5a1a1a",
                              activebackground="#e35050", activeforeground="#3b0b0b", relief="raised", command=self.reiniciar_simulador)
        btn_reset.grid(row=0, column=4, padx=20, pady=6, sticky="w")
        btn_reset.bind("<Enter>", lambda e: btn_reset.config(bg="#e35050"))
        btn_reset.bind("<Leave>", lambda e: btn_reset.config(bg="#f28c8c"))

        # Frame Memória Virtual e Principal lado a lado
        frame_memorias = tk.Frame(self.root, bg="#eef2f7")
        frame_memorias.pack(fill="x", padx=15)

        # Memória Virtual (Disco)
        frame_virtual = tk.Frame(frame_memorias, bg="#f4f7fb", bd=1, relief="sunken")
        frame_virtual.pack(side="left", fill="both", expand=True, padx=(0,10), pady=10)

        lbl_virtual = tk.Label(frame_virtual, text="Memória Virtual (Disco)", font=fonte_titulo, bg="#f4f7fb", fg="#303f60")
        lbl_virtual.pack(anchor="nw", padx=8, pady=6)

        self.listbox_virtual = tk.Listbox(frame_virtual, font=fonte_normal, height=10, activestyle="none", selectbackground="#aaccee", selectforeground="#000000")
        self.listbox_virtual.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Botão para acessar página
        self.btn_acessar = tk.Button(frame_virtual, text="Acessar Página Selecionada", font=fonte_secundaria,
                                    bg="#6190e8", fg="white", relief="raised", command=self.acessar_pagina, state="disabled")
        self.btn_acessar.pack(padx=10, pady=(0,15))
        self.btn_acessar.bind("<Enter>", lambda e: self.btn_acessar.config(bg="#3a68d4"))
        self.btn_acessar.bind("<Leave>", lambda e: self.btn_acessar.config(bg="#6190e8"))

        self.listbox_virtual.bind('<<ListboxSelect>>', self.habilitar_botao_acessar)

        # Memória Principal
        frame_principal = tk.Frame(frame_memorias, bg="#f4f7fb", bd=1, relief="sunken")
        frame_principal.pack(side="left", fill="both", expand=True, pady=10)

        lbl_principal = tk.Label(frame_principal, text="Memória Principal (RAM)", font=fonte_titulo, bg="#f4f7fb", fg="#303f60")
        lbl_principal.pack(anchor="nw", padx=8, pady=6)

        self.memoria_label = tk.Label(frame_principal, text="", font=("Segoe UI", 13, "bold"), bg="#ffffff", fg="#1f2f3f",
                                     relief="solid", bd=1, width=25, height=2)
        self.memoria_label.pack(padx=10, pady=(0,15))

        # Frame Tabela ETP
        self.frame_etp = tk.Frame(self.root, bg="#eef2f7")
        self.frame_etp.pack(fill="x", padx=15, pady=(0,15))
        tk.Label(self.frame_etp, text="Tabela de Páginas (ETP):", font=fonte_titulo, bg="#eef2f7", fg="#303f60").pack(anchor="w", padx=5)

        self.etp_tabela = tk.Frame(self.frame_etp, bg="#ffffff", bd=1, relief="solid")
        self.etp_tabela.pack(padx=10, pady=8, anchor="w")

        # Frame Estatísticas e Histórico
        frame_stats_hist = tk.Frame(self.root, bg="#eef2f7")
        frame_stats_hist.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Estatísticas
        frame_stats = tk.Frame(frame_stats_hist, bg="#dbe7f3", bd=1, relief="groove")
        frame_stats.pack(side="left", fill="both", expand=False, padx=(0, 10), pady=5)

        tk.Label(frame_stats, text="Estatísticas", font=fonte_titulo, bg="#dbe7f3", fg="#303f60").pack(padx=10, pady=10)
        self.page_faults_label = tk.Label(frame_stats, text="Total de Page-Faults: 0", font=fonte_secundaria, bg="#dbe7f3", fg="#202830")
        self.page_faults_label.pack(padx=15, pady=10)

        # Histórico de acessos
        frame_hist = tk.Frame(frame_stats_hist, bg="#f4f7fb", bd=1, relief="sunken")
        frame_hist.pack(side="left", fill="both", expand=True, pady=5)

        tk.Label(frame_hist, text="Histórico de Acessos", font=fonte_secundaria, bg="#f4f7fb", fg="#303f60").pack(anchor="nw", padx=10, pady=8)
        self.hist_text = scrolledtext.ScrolledText(frame_hist, font=fonte_normal, bg="white", fg="#1f2f3f", height=12, state="disabled", relief="solid", bd=1)
        self.hist_text.pack(fill="both", expand=True, padx=10, pady=(0,10))

    def reiniciar_simulador(self):
        # Inicializa estado
        self.page_faults = 0
        self.etp.clear()
        self.memoria_principal.clear()
        self.memoria_virtual.clear()

        # Popula a memória virtual e quadro físico
        total_paginas = self.num_paginas.get()
        total_quadros = self.num_quadros.get()

        for i in range(1, total_paginas + 1):
            pagina = f"P{i}"
            self.memoria_virtual.append(pagina)
            self.etp[pagina] = None

        # Carrega os primeiros quadros possíveis na memória principal
        for i in range(min(total_quadros, total_paginas)):
            pagina = self.memoria_virtual[i]
            self.memoria_principal.append(pagina)
            self.etp[pagina] = f"Quadro {i}"

        self.atualizar_interface()
        self.hist_text.config(state="normal")
        self.hist_text.delete("1.0", tk.END)
        self.hist_text.config(state="disabled")

    def acessar_pagina(self):
        selecao = self.listbox_virtual.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma página na Memória Virtual.")
            return

        pagina = self.listbox_virtual.get(selecao[0])

        if pagina in self.memoria_principal:
            self.adicionar_historico(f"Acesso à página {pagina}: já está na memória principal.")
        else:
            self.page_faults += 1
            self.adicionar_historico(f"Page-fault ao acessar {pagina}. Página será carregada.")

            # Se tem espaço livre
            if len(self.memoria_principal) < self.num_quadros.get():
                frame_livre = len(self.memoria_principal)
                self.memoria_principal.append(pagina)
                self.etp[pagina] = f"Quadro {frame_livre}"
                self.adicionar_historico(f"Página {pagina} carregada no Quadro {frame_livre} (espaço livre).")
            else:
                # Substituir (FIFO simples: substitui o primeiro)
                substituida = self.memoria_principal.pop(0)
                quadro_substituido = self.etp[substituida]
                self.etp[substituida] = None
                self.memoria_principal.append(pagina)
                self.etp[pagina] = quadro_substituido
                self.adicionar_historico(f"Substituiu página {substituida} do {quadro_substituido} pela página {pagina}.")

        self.atualizar_interface()

    def adicionar_historico(self, texto):
        self.hist_text.config(state="normal")
        self.hist_text.insert(tk.END, texto + "\n")
        self.hist_text.see(tk.END)
        self.hist_text.config(state="disabled")

    def atualizar_interface(self):
        # Atualiza memória principal
        memoria_texto = " | ".join(self.memoria_principal) if self.memoria_principal else "Memória vazia"
        self.memoria_label.config(text=memoria_texto)

        # Atualiza tabela ETP
        for widget in self.etp_tabela.winfo_children():
            widget.destroy()

        header_font = ("Segoe UI", 12, "bold")
        cell_font = ("Segoe UI", 11)

        tk.Label(self.etp_tabela, text="Página", width=15, font=header_font, bg="#c4d1e8", relief="ridge").grid(row=0, column=0, sticky="nsew")
        tk.Label(self.etp_tabela, text="Quadro", width=15, font=header_font, bg="#c4d1e8", relief="ridge").grid(row=0, column=1, sticky="nsew")

        for i, pagina in enumerate(self.memoria_virtual, start=1):
            quadro = self.etp[pagina] if self.etp[pagina] is not None else "-"
            bg_color = "#e9efff" if self.etp[pagina] is not None else "#f9f9f9"
            tk.Label(self.etp_tabela, text=pagina, width=15, font=cell_font, bg=bg_color, relief="ridge").grid(row=i, column=0, sticky="nsew")
            tk.Label(self.etp_tabela, text=quadro, width=15, font=cell_font, bg=bg_color, relief="ridge").grid(row=i, column=1, sticky="nsew")

        # Atualiza contador de page-faults
        self.page_faults_label.config(text=f"Total de Page-Faults: {self.page_faults}")

        # Atualiza listbox da memória virtual
        self.listbox_virtual.delete(0, tk.END)
        for pagina in self.memoria_virtual:
            self.listbox_virtual.insert(tk.END, pagina)

        # Desabilita botão de acessar página até que uma página seja selecionada
        self.btn_acessar.config(state="disabled")

    def habilitar_botao_acessar(self, event):
        if self.listbox_virtual.curselection():
            self.btn_acessar.config(state="normal")
        else:
            self.btn_acessar.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorMemoriaVirtual(root)
    root.mainloop()
