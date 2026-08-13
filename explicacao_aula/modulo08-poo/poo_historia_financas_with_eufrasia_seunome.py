'''
Criado com uso de POO;
'''
import tkinter as tk
from tkinter import messagebox

class AppEufrasia:
    def __init__(self, root):
        self.root = root
        self.root.title("História Financeira: Eufrásia Teixeira Leite")
        self.root.geometry("500x400")
        self.root.configure(bg="#f4f4f9")

        # Título
        tk.Label(
            root, 
            text="Eufrásia Teixeira Leite", 
            font=("Arial", 16, "bold"), 
            bg="#f4f4f9", 
            fg="#1b365d"
        ).pack(pady=10)

        tk.Label(
            root, 
            text="A primeira investidora global do Brasil", 
            font=("Arial", 10, "italic"), 
            bg="#f4f4f9"
        ).pack(pady=2)

        # Eventos da Linha do Tempo
        self.eventos = {
            "1850 - Nascimento": "Nasceu em Vassouras (RJ), no auge do ciclo do café.",
            "1872 - Herança & Europa": "Após perder os pais, mudou-se para Paris e assumiu a gestão da fortuna da família.",
            "1873-1930 - Carteira Global": "Investiu em títulos, ações e ferrovias em 13 países e 7 moedas diferentes.",
            "1930 - Legado": "Faleceu deixando sua fortuna para causas sociais e educacionais no Brasil."
        }

        # Botões da Linha do Tempo
        for data, detalhe in self.eventos.items():
            btn = tk.Button(
                root, 
                text=data, 
                font=("Arial", 11), 
                bg="#1b365d", 
                fg="white",
                relief="flat",
                command=lambda d=detalhe: messagebox.showinfo("Fato Histórico", d)
            )
            btn.pack(fill="x", padx=40, pady=6)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppEufrasia(root)
    root.mainloop()