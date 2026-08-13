import json
import os
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

PALETA_CLARA = {
    "fundo": "#f8f9fa",
    "painel": "#ffffff",
    "texto": "#212529",
    "subtexto": "#6c757d",
    "primaria": "#d97706",
    "verde": "#16a34a",
    "vermelho": "#dc2626",
    "amarelo": "#eab308",
    "borda": "#e5e7eb",
}

PALETA_ESCURA = {
    "fundo": "#121212",
    "painel": "#1e1e2e",
    "texto": "#ffffff",
    "subtexto": "#a1a1aa",
    "primaria": "#f59e0b",
    "verde": "#22c55e",
    "vermelho": "#ef4444",
    "amarelo": "#eab308",
    "borda": "#3f3f46",
}

cores = PALETA_CLARA
modo_escuro = False

CARDAPIO = {
    "🥩 Carne": [
        {
            "id": 101,
            "nome": "Classic Burger",
            "preco": 28.90,
            "desc": "Pão brioche, blend 180g, queijo cheddar e molho da casa.",
        },
        {
            "id": 102,
            "nome": "Bacon Deluxe",
            "preco": 34.90,
            "desc": "Blend 180g, muito bacon crocante, cheddar e maionese.",
        },
        {
            "id": 103,
            "nome": "Smash Duplo",
            "preco": 31.90,
            "desc": "2x hambúrgueres de 90g prensados, duplo cheddar e picles.",
        },
        {
            "id": 104,
            "nome": "Gorgonzola & Cebola",
            "preco": 36.90,
            "desc": "Blend 180g, creme de gorgonzola e cebola caramelizada.",
        },
        {
            "id": 105,
            "nome": "Monster BBQ",
            "preco": 39.90,
            "desc": "Blend 200g, cheddar, bacon, anéis de cebola e barbecue.",
        },
        {
            "id": 106,
            "nome": "Triple Cheese",
            "preco": 35.90,
            "desc": "Blend 180g, cheddar, queijo prato e catupiry empanado.",
        },
        {
            "id": 107,
            "nome": "Costela Supremo",
            "preco": 38.90,
            "desc": "Hambúrguer de costela 200g, queijo provolone e alho frito.",
        },
    ],
    "🍗 Frango": [
        {
            "id": 201,
            "nome": "Crispy Chicken",
            "preco": 26.90,
            "desc": "Sobrecoxa crocante, salada coleslaw e maionese verde.",
        },
        {
            "id": 202,
            "nome": "Spicy Chicken",
            "preco": 27.90,
            "desc": "Frango empanado apimentado, geleia de pimenta e cheddar.",
        },
        {
            "id": 203,
            "nome": "Chicken Bacon",
            "preco": 29.90,
            "desc": "Filé de frango grelhado, bacon crocante, queijo e alface.",
        },
        {
            "id": 204,
            "nome": "Chicken Catupiry",
            "preco": 28.90,
            "desc": "Frango empanado, catupiry original e milho tostado.",
        },
        {
            "id": 205,
            "nome": "Chicken Honey Mustard",
            "preco": 27.50,
            "desc": "Frango crocante, molho mostarda e mel e picles.",
        },
        {
            "id": 206,
            "nome": "Smash Chicken",
            "preco": 24.90,
            "desc": "Hambúrguer artesanal de frango 120g com queijo prato.",
        },
        {
            "id": 207,
            "nome": "Chicken BBQ",
            "preco": 28.50,
            "desc": "Frango grelhado, queijo cheddar, molho barbecue e tomate.",
        },
    ],
    "🌱 Vegetariano": [
        {
            "id": 301,
            "nome": "Veggie Smash",
            "preco": 29.90,
            "desc": "Burguer de grão-de-bico com cogumelos e queijo prato.",
        },
        {
            "id": 302,
            "nome": "Shimeji Burger",
            "preco": 33.90,
            "desc": "Cogumelos shimeji salteados na manteiga e queijo provolone.",
        },
        {
            "id": 303,
            "nome": "Falafel Burguer",
            "preco": 28.90,
            "desc": "Hambúrguer de falafel, molho de iogurte com hortelã e salada.",
        },
        {
            "id": 304,
            "nome": "Lentilha & Quinoa",
            "preco": 27.90,
            "desc": "Burguer de lentilha com quinoa, queijo minas e cenoura.",
        },
        {
            "id": 305,
            "nome": "Futuro Bacon",
            "preco": 34.90,
            "desc": "Hambúrguer à base de plantas, bacon vegetal e cheddar vegano.",
        },
        {
            "id": 306,
            "nome": "Provolone Empanado",
            "preco": 32.90,
            "desc": "Disco de queijo provolone crocante com tomate seco e rúcula.",
        },
        {
            "id": 307,
            "nome": "Green Power",
            "preco": 29.50,
            "desc": "Burguer de ervilha e espinafre, mayo de ervas e alface.",
        },
    ],
    "🍟 Acompanhamento": [
        {
            "id": 401,
            "nome": "Batata Rústica",
            "preco": 16.00,
            "desc": "Batatas artesanais com alecrim, alho e páprica.",
        },
        {
            "id": 402,
            "nome": "Onion Rings",
            "preco": 18.00,
            "desc": "Anéis de cebola crocantes com molho barbecue.",
        },
        {
            "id": 403,
            "nome": "Batata com Cheddar e Bacon",
            "preco": 22.00,
            "desc": "Batata frita palito coberta com cheddar cremoso e bacon.",
        },
        {
            "id": 404,
            "nome": "Nuggets de Frango (8 un)",
            "preco": 17.50,
            "desc": "Embalagem com 8 empanados de frango crocantes.",
        },
        {
            "id": 405,
            "nome": "Almofadinhas de Gouda",
            "preco": 24.00,
            "desc": "Porção com 8 unidades de queijo gouda empanado.",
        },
        {
            "id": 406,
            "nome": "Dadinhos de Tapioca",
            "preco": 19.90,
            "desc": "Acompanha geleia artesanal de pimenta.",
        },
        {
            "id": 407,
            "nome": "Batata Smile",
            "preco": 15.00,
            "desc": "Porção infantil de batatas carinha sorridente.",
        },
    ],
    "🥤 Bebidas": [
        {
            "id": 501,
            "nome": "Coca-Cola Zero 350ml",
            "preco": 6.50,
            "desc": "Lata gelada 350ml.",
        },
        {
            "id": 502,
            "nome": "Guaraná Antarctica 350ml",
            "preco": 6.50,
            "desc": "Lata gelada 350ml.",
        },
        {
            "id": 503,
            "nome": "Suco Natural de Laranja 500ml",
            "preco": 9.90,
            "desc": "Suco da fruta feito na hora sem açúcar.",
        },
        {
            "id": 504,
            "nome": "Lemonade Artesanal 400ml",
            "preco": 11.00,
            "desc": "Limonada suíça com xarope de morango.",
        },
        {
            "id": 505,
            "nome": "Milkshake Ninho e Nutella",
            "preco": 19.90,
            "desc": "Milkshake cremoso 400ml.",
        },
        {
            "id": 506,
            "nome": "Milkshake de Ovomaltine",
            "preco": 18.90,
            "desc": "Milkshake cremoso 400ml com crocante.",
        },
        {
            "id": 507,
            "nome": "Água Mineral com Gás 500ml",
            "preco": 4.50,
            "desc": "Garrafa 500ml.",
        },
    ],
}

qtd_variaveis = {}
cards_widgets = []
canvases = []


def calcular_total():
    total = 0.0
    for categoria, itens in CARDAPIO.items():
        for item in itens:
            qtd = qtd_variaveis[item["id"]].get()
            total += qtd * item["preco"]
    lbl_total_valor.config(text=f"R$ {total:.2f}")
    return total


def zerar_quantidades():
    for var in qtd_variaveis.values():
        var.set(0)
    calcular_total()


def finalizar_pedido_json():
    itens_pedido = []
    total_geral = 0.0

    for categoria, itens in CARDAPIO.items():
        for item in itens:
            qtd = qtd_variaveis[item["id"]].get()
            if qtd > 0:
                subtotal = qtd * item["preco"]
                total_geral += subtotal
                itens_pedido.append(
                    {
                        "item": item["nome"],
                        "categoria": categoria,
                        "quantidade": qtd,
                        "preco_unitario": item["preco"],
                        "subtotal": subtotal,
                    }
                )

    if not itens_pedido:
        messagebox.showwarning(
            "Carrinho Vazio", "Selecione pelo menos um item para finalizar!"
        )
        return

    dados_pedido = {
        "data_pedido": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_pedido": total_geral,
        "itens": itens_pedido,
    }

    # Nome padronizado do arquivo com data e hora
    nome_arquivo = f"pedido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # 1. GUARDA AUTOMATICAMENTE DENTRO DA PASTA 'ticket' DO REPOSITÓRIO (VS CODE)
    pasta_ticket = os.path.join(os.getcwd(), "ticket")
    os.makedirs(pasta_ticket, exist_ok=True)  # Garante a existência da pasta 'ticket'

    caminho_local_repo = os.path.join(pasta_ticket, nome_arquivo)

    try:
        with open(caminho_local_repo, "w", encoding="utf-8") as f:
            json.dump(dados_pedido, f, indent=4, ensure_ascii=False)
    except Exception as e_repo:
        messagebox.showerror(
            "Erro", f"Falha ao salvar na pasta ticket do projeto: {e_repo}"
        )
        return

    # 2. OPTATIVO: PERMITE SALVAR UMA CÓPIA EM OUTRO LUGAR DO PC
    caminho_copia_extra = filedialog.asksaveasfilename(
        initialdir=pasta_ticket,
        initialfile=nome_arquivo,
        defaultextension=".json",
        filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
        title="Salvar uma cópia extra do Pedido JSON (Opcional)",
    )

    if caminho_copia_extra:
        try:
            with open(caminho_copia_extra, "w", encoding="utf-8") as f_extra:
                json.dump(dados_pedido, f_extra, indent=4, ensure_ascii=False)
        except Exception as e_copia:
            print(f"Não foi possível salvar a cópia extra: {e_copia}")

    # 3. ABRE O ARQUIVO SALVO NA PASTA 'ticket' DIRETO NO VS CODE
    try:
        subprocess.run(["code", caminho_local_repo], shell=True)
        messagebox.showinfo(
            "Sucesso",
            f"Pedido gravado com sucesso!\n\nLocal: pedido/{nome_arquivo}\n\nArquivo aberto no VS Code!",
        )
    except Exception:
        messagebox.showinfo(
            "Sucesso",
            f"Pedido gravado com sucesso!\n\nLocal: pedido/{nome_arquivo}",
        )

    zerar_quantidades()


def alternar_tema():
    global modo_escuro, cores
    modo_escuro = not modo_escuro
    cores = PALETA_ESCURA if modo_escuro else PALETA_CLARA

    janela.configure(bg=cores["fundo"])
    bar_topo.configure(bg=cores["fundo"])
    lbl_titulo_app.configure(bg=cores["fundo"], fg=cores["texto"])
    frame_rodape.configure(bg=cores["painel"])
    lbl_total_texto.configure(bg=cores["painel"], fg=cores["texto"])
    lbl_total_valor.configure(bg=cores["painel"], fg=cores["primaria"])

    btn_tema.config(text="☀️ Modo Claro" if modo_escuro else "🌙 Modo Escuro")

    style.configure("TNotebook", background=cores["fundo"], borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=cores["painel"],
        foreground=cores["texto"],
        padding=[10, 5],
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", cores["primaria"])],
        foreground=[("selected", "#ffffff")],
    )

    for cv in canvases:
        cv.configure(bg=cores["fundo"])
        cv.master.configure(bg=cores["fundo"])

    for card, frame in cards_widgets:
        frame.configure(bg=cores["fundo"])
        card.configure(bg=cores["painel"], highlightbackground=cores["borda"])
        for sub in card.winfo_children():
            if isinstance(sub, tk.Label):
                if sub.cget("fg") in [
                    PALETA_CLARA["subtexto"],
                    PALETA_ESCURA["subtexto"],
                ]:
                    sub.configure(bg=cores["painel"], fg=cores["subtexto"])
                elif sub.cget("fg") in [
                    PALETA_CLARA["verde"],
                    PALETA_ESCURA["verde"],
                ]:
                    sub.configure(bg=cores["painel"], fg=cores["verde"])
                else:
                    sub.configure(bg=cores["painel"], fg=cores["texto"])
            elif isinstance(sub, tk.Spinbox):
                sub.configure(
                    bg=cores["fundo"],
                    fg=cores["texto"],
                    readonlybackground=cores["fundo"],
                    buttonbackground=cores["painel"],
                )


def _ao_rolar_mouse(event, canvas):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ==================== INTERFACE GRÁFICA ====================
janela = tk.Tk()
janela.title("Vocacaoburguer & Co. - Cardápio Digital")
janela.geometry("740x680")
janela.configure(bg=cores["fundo"])

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=cores["fundo"], borderwidth=0)
style.configure(
    "TNotebook.Tab",
    background=cores["painel"],
    foreground=cores["texto"],
    padding=[10, 5],
)
style.map(
    "TNotebook.Tab",
    background=[("selected", cores["primaria"])],
    foreground=[("selected", "#ffffff")],
)

bar_topo = tk.Frame(janela, bg=cores["fundo"])
bar_topo.pack(fill="x", padx=15, pady=10)

lbl_titulo_app = tk.Label(
    bar_topo,
    text="🍔 Vocacaoburguer & Co.",
    font=("Arial", 16, "bold"),
    bg=cores["fundo"],
    fg=cores["texto"],
)
lbl_titulo_app.pack(side="left")

btn_tema = tk.Button(
    bar_topo,
    text="🌙 Modo Escuro",
    bg=cores["amarelo"],
    fg="black",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=alternar_tema,
)
btn_tema.pack(side="right")

notebook = ttk.Notebook(janela)
notebook.pack(fill="both", expand=True, padx=15, pady=(0, 10))

for categoria, itens in CARDAPIO.items():
    frame_aba = tk.Frame(notebook, bg=cores["fundo"])
    notebook.add(frame_aba, text=categoria)

    canvas = tk.Canvas(frame_aba, bg=cores["fundo"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(
        frame_aba, orient="vertical", command=canvas.yview
    )
    frame_itens = tk.Frame(canvas, bg=cores["fundo"])

    def _ajustar_largura(e, c=canvas, f=frame_itens):
        c.itemconfig(c.find_withtag("win")[0], width=e.width)

    frame_itens.bind(
        "<Configure>",
        lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")),
    )
    win_id = canvas.create_window(
        (0, 0), window=frame_itens, anchor="nw", tags="win"
    )
    canvas.bind("<Configure>", _ajustar_largura)

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvases.append(canvas)

    frame_itens.bind_all(
        "<MouseWheel>", lambda e, c=canvas: _ao_rolar_mouse(e, c)
    )

    for item in itens:
        var_qtd = tk.IntVar(value=0)
        qtd_variaveis[item["id"]] = var_qtd

        card = tk.Frame(
            frame_itens,
            bg=cores["painel"],
            bd=1,
            relief="solid",
            highlightbackground=cores["borda"],
        )
        card.pack(fill="x", pady=5, ipady=4, ipadx=6, expand=True)
        card.columnconfigure(0, weight=1)

        cards_widgets.append((card, frame_itens))

        lbl_nome = tk.Label(
            card,
            text=item["nome"],
            font=("Arial", 11, "bold"),
            fg=cores["texto"],
            bg=cores["painel"],
        )
        lbl_nome.grid(row=0, column=0, sticky="w", padx=8, pady=(4, 0))

        lbl_desc = tk.Label(
            card,
            text=item["desc"],
            font=("Arial", 8),
            fg=cores["subtexto"],
            bg=cores["painel"],
            wraplength=400,
            justify="left",
        )
        lbl_desc.grid(row=1, column=0, sticky="w", padx=8, pady=(0, 4))

        lbl_preco = tk.Label(
            card,
            text=f"R$ {item['preco']:.2f}",
            font=("Arial", 11, "bold"),
            fg=cores["verde"],
            bg=cores["painel"],
        )
        lbl_preco.grid(row=0, column=1, rowspan=2, padx=10)

        spn_qtd = tk.Spinbox(
            card,
            from_=0,
            to=20,
            width=3,
            textvariable=var_qtd,
            font=("Arial", 10),
            command=calcular_total,
            state="readonly",
            readonlybackground=cores["fundo"],
        )
        spn_qtd.grid(row=0, column=2, rowspan=2, padx=8)

frame_rodape = tk.Frame(janela, bg=cores["painel"], bd=1, relief="raised")
frame_rodape.pack(fill="x", ipady=8, ipadx=10)

lbl_total_texto = tk.Label(
    frame_rodape,
    text="Total do Pedido:",
    font=("Arial", 11, "bold"),
    bg=cores["painel"],
    fg=cores["texto"],
)
lbl_total_texto.pack(side="left", padx=(15, 5))

lbl_total_valor = tk.Label(
    frame_rodape,
    text="R$ 0.00",
    font=("Arial", 14, "bold"),
    bg=cores["painel"],
    fg=cores["primaria"],
)
lbl_total_valor.pack(side="left")

btn_finalizar = tk.Button(
    frame_rodape,
    text="🛒 Exportar Pedido (JSON)",
    bg=cores["verde"],
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=finalizar_pedido_json,
)
btn_finalizar.pack(side="right", padx=15)

btn_limpar = tk.Button(
    frame_rodape,
    text="🗑️ Limpar",
    bg=cores["vermelho"],
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=zerar_quantidades,
)
btn_limpar.pack(side="right", padx=5)

janela.mainloop()