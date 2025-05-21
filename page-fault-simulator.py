import tkinter as tk
from tkinter import messagebox

class SimuladorMemoriaVirtualGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Page-Fault - Memória Virtual")

        self.memoria_virtual = ["P1", "P2", "P3", "P4", "P5"]
        self.memoria_principal = []
        self.etp = {pagina: None for pagina in self.memoria_virtual}
        self.fila_substituicao = []
        self.page_faults = 0

        self.num_quadros = tk.IntVar(value=2)

        self.configurar_interface()

    def configurar_interface(self):
        # Seleção do número de quadros
        tk.Label(self.root, text="Número de quadros na memória principal:").grid(row=0, column=0, sticky='w')
        tk.Spinbox(self.root, from_=1, to=10, textvariable=self.num_quadros, width=5,
                   command=self.reiniciar_simulador).grid(row=0, column=1)

        # Botões das páginas virtuais
        tk.Label(self.root, text="Memória Virtual (Disco):").grid(row=1, column=0, columnspan=2, sticky='w')
        for i, pagina in enumerate(self.memoria_virtual):
            btn = tk.Button(self.root, text=pagina, width=6,
                            command=lambda p=pagina: self.acessar_pagina(p))
            btn.grid(row=2, column=i)

        # Área de exibição
        tk.Label(self.root, text="Memória Principal:").grid(row=3, column=0, columnspan=2, sticky='w')
        self.memoria_label = tk.Label(self.root, text="", fg="blue")
        self.memoria_label.grid(row=4, column=0, columnspan=5, sticky='w')

        tk.Label(self.root, text="Tabela de Páginas (ETP):").grid(row=5, column=0, columnspan=2, sticky='w')
        self.etp_label = tk.Label(self.root, text="", justify="left", fg="darkgreen")
        self.etp_label.grid(row=6, column=0, columnspan=5, sticky='w')

        self.page_faults_label = tk.Label(self.root, text="Total de Page-Faults: 0", fg="red")
        self.page_faults_label.grid(row=7, column=0, columnspan=2, sticky='w')

        self.reiniciar_simulador()

    def reiniciar_simulador(self):
        self.memoria_principal = []
        self.etp = {pagina: None for pagina in self.memoria_virtual}
        self.fila_substituicao = []
        self.page_faults = 0
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
        self.memoria_label.config(text=f"{self.memoria_principal}")
        texto_etp = "\n".join(
            f"{pagina}: {self.etp[pagina] if self.etp[pagina] is not None else '-'}"
            for pagina in self.memoria_virtual
        )
        self.etp_label.config(text=texto_etp)
        self.page_faults_label.config(text=f"Total de Page-Faults: {self.page_faults}")


# Execução da interface
if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorMemoriaVirtualGUI(root)
    root.mainloop()
