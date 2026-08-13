import tkinter as tk
from tkinter import messagebox

class AppAportes:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Aportes")
        self.root.geometry("380x300")
        self.saldo = 0.0

        # Visor do Saldo
        self.lbl_saldo = tk.Label(root, text="Saldo Atual: R$ 0.00", font=("Arial", 14, "bold"), fg="#008052")
        self.lbl_saldo.pack(pady=20)

        # Entrada de Valor
        tk.Label(root, text="Valor da Operação (R$):").pack()
        self.ent_valor = tk.Entry(root, font=("Arial", 12))
        self.ent_valor.pack(pady=5)

        # Botões de Entrada e Saída
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Depositar (+)", bg="#008052", fg="white", width=12, command=self.depositar).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Sacar (-)", bg="#c8102e", fg="white", width=12, command=self.sacar).grid(row=0, column=1, padx=5)

    def depositar(self):
        try:
            val = float(self.ent_valor.get())
            self.saldo += val
            self.atualizar_saldo()
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")

    def sacar(self):
        try:
            val = float(self.ent_valor.get())
            if val > self.saldo:
                messagebox.showwarning("Aviso", "Saldo insuficiente!")
            else:
                self.saldo -= val
                self.atualizar_saldo()
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")

    def atualizar_saldo(self):
        self.lbl_saldo.config(text=f"Saldo Atual: R$ {self.saldo:.2f}")
        self.ent_valor.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    AppAportes(root)
    root.mainloop()