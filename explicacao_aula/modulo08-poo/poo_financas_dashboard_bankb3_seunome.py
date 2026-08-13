import tkinter as tk
from tkinter import ttk, messagebox

class DashboardB3:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Financeiro - Padrão B3")
        self.root.geometry("600x450")
        
        # Cores B3
        self.COR_AZUL = "#001E62"
        self.COR_AMARELO = "#F2A900"
        self.COR_FUNDO = "#F5F5F5"

        self.saldo = 1000.00
        self.cripto_btc = 0.0
        self.historico = ["Saldo inicial depositado: R$ 1000.00"]

        # Estilo do App
        self.root.configure(bg=self.COR_FUNDO)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=self.COR_FUNDO)
        style.configure("TNotebook.Tab", background=self.COR_AZUL, foreground="white", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", self.COR_AMARELO)], foreground=[("selected", "black")])

        # Header
        header = tk.Frame(root, bg=self.COR_AZUL, height=50)
        header.pack(fill="x")
        tk.Label(header, text="B3 - SIMULADOR EDUCACIONAL", font=("Arial", 14, "bold"), fg="white", bg=self.COR_AZUL).pack(pady=10)

        # Instância das Abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_conta = ttk.Frame(self.notebook)
        self.aba_cripto = ttk.Frame(self.notebook)
        self.aba_extrato = ttk.Frame(self.notebook)

        self.notebook.add(self.aba_conta, text="Conta Corrente")
        self.notebook.add(self.aba_cripto, text="Criptoativos")
        self.notebook.add(self.aba_extrato, text="Extrato")

        self.montar_aba_conta()
        self.montar_aba_cripto()
        self.montar_aba_extrato()

    def montar_aba_conta(self):
        self.lbl_saldo = tk.Label(self.aba_conta, text=f"Saldo Disponível: R$ {self.saldo:.2f}", font=("Arial", 12, "bold"))
        self.lbl_saldo.pack(pady=15)

        tk.Label(self.aba_conta, text="Valor (R$):").pack()
        self.ent_valor_conta = tk.Entry(self.aba_conta)
        self.ent_valor_conta.pack(pady=5)

        btn_frame = tk.Frame(self.aba_conta)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Entrada (+)", bg="#008052", fg="white", command=self.creditar).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Saída (-)", bg="#c8102e", fg="white", command=self.debitar).grid(row=0, column=1, padx=5)

    def montar_aba_cripto(self):
        tk.Label(self.aba_cripto, text="Mercado Digital - Bitcoin (Simulado)", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Label(self.aba_cripto, text="Cotação Fixa: 1 BTC = R$ 300.000,00").pack()
        
        self.lbl_btc = tk.Label(self.aba_cripto, text=f"Seu Saldo BTC: {self.cripto_btc:.6f}", font=("Arial", 10, "bold"), fg="#001E62")
        self.lbl_btc.pack(pady=10)

        tk.Button(self.aba_cripto, text="Comprar R$ 100,00 em BTC", bg=self.COR_AMARELO, command=self.comprar_btc).pack(pady=10)

    def montar_aba_extrato(self):
        self.lst_extrato = tk.Listbox(self.aba_extrato, width=60, height=10)
        self.lst_extrato.pack(padx=10, pady=10, fill="both", expand=True)
        self.atualizar_extrato()

    def creditar(self):
        try:
            v = float(self.ent_valor_conta.get())
            self.saldo += v
            self.historico.append(f"Depósito: +R$ {v:.2f}")
            self.atualizar_tudo()
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")

    def debitar(self):
        try:
            v = float(self.ent_valor_conta.get())
            if v <= self.saldo:
                self.saldo -= v
                self.historico.append(f"Saque/Pagamento: -R$ {v:.2f}")
                self.atualizar_tudo()
            else:
                messagebox.showwarning("Erro", "Saldo insuficiente.")
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")

    def comprar_btc(self):
        custo = 100.00
        if self.saldo >= custo:
            self.saldo -= custo
            qtd = custo / 300000.0
            self.cripto_btc += qtd
            self.historico.append(f"Compra Cripto: R$ 100.00 em BTC ({qtd:.6f} BTC)")
            self.atualizar_tudo()
        else:
            messagebox.showwarning("Erro", "Saldo insuficiente para comprar R$ 100,00 em BTC.")

    def atualizar_tudo(self):
        self.lbl_saldo.config(text=f"Saldo Disponível: R$ {self.saldo:.2f}")
        self.lbl_btc.config(text=f"Seu Saldo BTC: {self.cripto_btc:.6f}")
        self.atualizar_extrato()

    def atualizar_extrato(self):
        self.lst_extrato.delete(0, tk.END)
        for item in self.historico:
            self.lst_extrato.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    DashboardB3(root)
    root.mainloop()