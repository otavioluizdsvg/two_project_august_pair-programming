import io
import json
import os
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageOps, ImageTk
import requests

# ==================== PALETAS DE CORES (TEMAS) ====================
PALETA_CLARA = {
    "fundo": "#004d6e",
    "painel": "#ffffff",
    "texto": "#1a1a2e",
    "detalhe": "#0081ab",
    "verde": "#2e7d32",
    "rosa": "#c62828",
    "amarelo": "#edce01",
    "entrada_fundo": "#f0f4f8",
    "entrada_texto": "#000000",
}

PALETA_ESCURA = {
    "fundo": "#121212",
    "painel": "#1e1e2e",
    "texto": "#ffffff",
    "detalhe": "#3b82f6",
    "verde": "#4caf50",
    "rosa": "#f44336",
    "amarelo": "#f57f17",
    "entrada_fundo": "#2a2a3c",
    "entrada_texto": "#ffffff",
}

# Tema atual
cores = PALETA_CLARA
modo_escuro = False

# Objeto original da imagem
img_logo_raw = None

# ==================== BANCO DE DADOS EM MEMÓRIA ====================
contas = {
    "root": {
        "senha": "root123",
        "saldo": 1000.0,
        "extrato": ["Conta Root criada com privilégios de Administrador."],
    }
}
usuario_atual = None


# ==================== TRATAMENTO DE IMAGEM DA LOGO ====================
def remover_fundo_azul(img):
    """Remove o quadrado azul de fundo da imagem original,
    tornando o fundo totalmente transparente para se adaptar a qualquer tema.
    """
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        r, g, b, a = item
        # Detecta tons do azul do fundo original (#004d6e ou similares)
        if r < 60 and 40 < g < 130 and 80 < b < 160:
            new_data.append((0, 0, 0, 0))  # Totalmente transparente
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img


def atualizar_imagem_logo():
    """Recarrega e exibe a logo com o fundo transparente ajustado ao tema"""
    global img_logo_raw, foto_banner
    if img_logo_raw is None:
        return

    try:
        img_sem_fundo = remover_fundo_azul(img_logo_raw)

        if modo_escuro:
            r, g, b, a = img_sem_fundo.split()
            rgb_img = Image.merge("RGB", (r, g, b))
            rgb_img = ImageOps.colorize(
                rgb_img.convert("L"), black="#1e1e2e", white="#60a5fa"
            )
            img_final = Image.merge("RGBA", (*rgb_img.split(), a))
        else:
            img_final = img_sem_fundo

        foto_banner = ImageTk.PhotoImage(img_final)
        lbl_banner.configure(image=foto_banner, bg=cores["fundo"], text="")
        lbl_banner.image = foto_banner
    except Exception as e:
        print(f"Erro ao processar logo: {e}")


def alternar_tema():
    global modo_escuro, cores
    modo_escuro = not modo_escuro
    cores = PALETA_ESCURA if modo_escuro else PALETA_CLARA

    # 1. Configurações gerais da tela e cabeçalho
    janela.configure(bg=cores["fundo"])
    bar_topo.configure(bg=cores["fundo"])
    frame_auth.configure(bg=cores["fundo"])
    frame_painel.configure(bg=cores["painel"])
    header_p.configure(bg=cores["fundo"])

    lbl_usuario_logado.configure(bg=cores["fundo"], fg="white")

    # Atualiza a logo transparente
    atualizar_imagem_logo()

    # 2. Formulários de Login e Cadastro
    for aba in (aba_login, aba_cad):
        for widget in aba.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=cores["painel"], fg=cores["texto"])
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=cores["entrada_fundo"],
                    fg=cores["entrada_texto"],
                    insertbackground=cores["texto"],
                    relief="solid",
                    bd=1,
                )

    # 3. Componentes do Painel
    lbl_saldo_title.configure(
        bg=cores["painel"], fg="#888888" if modo_escuro else "gray"
    )
    lbl_saldo_val.configure(bg=cores["painel"], fg=cores["detalhe"])
    lbl_historico_title.configure(bg=cores["painel"], fg=cores["texto"])
    lst_extrato.configure(bg=cores["entrada_fundo"], fg=cores["entrada_texto"])

    # 4. Bloco de Operações
    frame_ops.configure(bg=cores["painel"], fg=cores["texto"])
    for widget in frame_ops.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=cores["painel"], fg=cores["texto"])
        elif isinstance(widget, tk.Entry):
            widget.configure(
                bg=cores["entrada_fundo"],
                fg=cores["entrada_texto"],
                insertbackground=cores["texto"],
            )

    # 5. Botão de Alternar Tema
    btn_tema.config(text="☀️ Modo Claro" if modo_escuro else "🌙 Modo Escuro")


def cadastrar_usuario():
    usr = ent_usr_cad.get().strip()
    pwd = ent_pwd_cad.get().strip()

    if not usr or not pwd:
        messagebox.showwarning("Aviso", "Preencha usuário e senha!")
        return

    if usr in contas:
        messagebox.showerror("Erro", "Usuário já cadastrado.")
        return

    contas[usr] = {
        "senha": pwd,
        "saldo": 0.0,
        "extrato": ["Conta aberta com sucesso!"],
    }
    messagebox.showinfo("Sucesso", "Conta criada! Faça o login.")
    ent_usr_cad.delete(0, tk.END)
    ent_pwd_cad.delete(0, tk.END)


def autenticar():
    global usuario_atual
    usr = ent_usr_login.get().strip()
    pwd = ent_pwd_login.get().strip()

    if usr in contas and contas[usr]["senha"] == pwd:
        usuario_atual = usr
        ent_usr_login.delete(0, tk.END)
        ent_pwd_login.delete(0, tk.END)
        abrir_painel_principal()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")


def realizar_deposito():
    try:
        val = float(ent_valor_op.get())
        if val <= 0:
            messagebox.showwarning("Aviso", "Digite um valor maior que zero.")
            return

        contas[usuario_atual]["saldo"] += val
        contas[usuario_atual]["extrato"].append(f"Depósito: +R$ {val:.2f}")
        atualizar_painel()
        messagebox.showinfo("Sucesso", f"Depósito de R$ {val:.2f} realizado!")
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido.")


def realizar_pagamento():
    try:
        val = float(ent_valor_op.get())
        tipo = combo_tipo_op.get()

        if val <= 0:
            messagebox.showwarning("Aviso", "Digite um valor maior que zero.")
            return

        saldo = contas[usuario_atual]["saldo"]
        if val > saldo:
            messagebox.showwarning("Aviso", "Saldo insuficiente!")
            return

        contas[usuario_atual]["saldo"] -= val
        contas[usuario_atual]["extrato"].append(
            f"Pagamento ({tipo}): -R$ {val:.2f}"
        )
        atualizar_painel()
        messagebox.showinfo(
            "Sucesso", f"Operação {tipo} de R$ {val:.2f} realizada!"
        )
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido.")


def exportar_json():
    dados_usuario = contas[usuario_atual]
    dados_exportacao = {
        "usuario": usuario_atual,
        "data_emissao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "saldo_atual": dados_usuario["saldo"],
        "historico_transacoes": dados_usuario["extrato"],
    }

    # Gera o nome dinâmico com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"ticket_extrato_{usuario_atual}_{timestamp}.json"

    # 1. GUARDA AUTOMATICAMENTE NA PASTA 'ticket' DO PROJETO (VS CODE)
    pasta_ticket = os.path.join(os.getcwd(), "ticket")
    os.makedirs(pasta_ticket, exist_ok=True)

    caminho_local_repo = os.path.join(pasta_ticket, nome_arquivo)

    try:
        with open(caminho_local_repo, "w", encoding="utf-8") as f:
            json.dump(dados_exportacao, f, indent=4, ensure_ascii=False)
    except Exception as e_repo:
        messagebox.showerror(
            "Erro", f"Falha ao salvar na pasta ticket do projeto: {e_repo}"
        )
        return

    # 2. OPTATIVO: SALVAR CÓPIA EM OUTRO LOCAL DO COMPUTADOR
    caminho_copia_extra = filedialog.asksaveasfilename(
        initialdir=pasta_ticket,
        initialfile=nome_arquivo,
        defaultextension=".json",
        filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
        title="Salvar uma cópia do Extrato JSON (Opcional)",
    )

    if caminho_copia_extra:
        try:
            with open(caminho_copia_extra, "w", encoding="utf-8") as f_extra:
                json.dump(dados_exportacao, f_extra, indent=4, ensure_ascii=False)
        except Exception as e_copia:
            print(f"Não foi possível salvar a cópia extra: {e_copia}")

    # 3. ABRE O ARQUIVO SALVO NA PASTA 'ticket' DIRETO NO VS CODE
    try:
        subprocess.run(["code", caminho_local_repo], shell=True)
        messagebox.showinfo(
            "Sucesso",
            f"Extrato gerado com sucesso!\n\nLocal: ticket/{nome_arquivo}\n\nArquivo aberto no VS Code!",
        )
    except Exception:
        messagebox.showinfo(
            "Sucesso",
            f"Extrato gerado com sucesso!\n\nLocal: ticket/{nome_arquivo}",
        )


def logout():
    global usuario_atual
    usuario_atual = None
    frame_painel.pack_forget()
    frame_auth.pack(fill="both", expand=True)


def atualizar_painel():
    tag_admin = " (ROOT/ADMIN)" if usuario_atual == "root" else ""
    lbl_usuario_logado.config(text=f"Usuário: {usuario_atual}{tag_admin}")
    lbl_saldo_val.config(text=f"R$ {contas[usuario_atual]['saldo']:.2f}")
    ent_valor_op.delete(0, tk.END)

    lst_extrato.delete(0, tk.END)
    for item in contas[usuario_atual]["extrato"]:
        lst_extrato.insert(tk.END, item)


def abrir_painel_principal():
    frame_auth.pack_forget()
    frame_painel.pack(fill="both", expand=True)
    atualizar_painel()


# ==================== INTERFACE GRÁFICA ====================
janela = tk.Tk()
janela.title("VocacaoBank - Sistema Bancário Completo")
janela.geometry("650x640")
janela.configure(bg=cores["fundo"])

# --- BARRA SUPERIOR FIXA ---
bar_topo = tk.Frame(janela, bg=cores["fundo"])
bar_topo.pack(fill="x", padx=10, pady=5)

btn_tema = tk.Button(
    bar_topo,
    text="🌙 Modo Escuro",
    bg=cores["amarelo"],
    fg="black",
    font=("Arial", 9, "bold"),
    command=alternar_tema,
    relief="flat",
)
btn_tema.pack(side="right")

# --- TELA 1: LOGIN / CADASTRO ---
frame_auth = tk.Frame(janela, bg=cores["fundo"])
frame_auth.pack(fill="both", expand=True)

lbl_banner = tk.Label(frame_auth, bg=cores["fundo"])
lbl_banner.pack(pady=15)

# Download e carregamento da Logo
try:
    url_banner = "https://instagram.fcgh23-1.fna.fbcdn.net/v/t51.82787-19/771998196_18613407436056036_774798352104702966_n.jpg?w=400&q=80efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDgwLmMyIn0&_nc_ht=instagram.fcgh23-1.fna.fbcdn.net&_nc_cat=100&_nc_oc=Q6cZ2gHJp6OYIOqMloWicyg1NBcIpED2F1O3D6aT4gr_i5dNVo-0u2gE4N2Yb9uBCfvAtdBPT-kgANRQP4Bv8ia4YE-4&_nc_ohc=IQRZSsqo-eMQ7kNvwGmjxb3&_nc_gid=or42pcD87wgvA7Ib4XR1Ug&edm=AP4sbd4BAAAA&ccb=7-5&oh=00_AQGg7MoHk7c7OzmDOIjyBMruFom-yp1ghmcUOoJYfEWShQ&oe=6A80374B&_nc_sid=7a9f4b"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url_banner, headers=headers, timeout=3)

    img_logo_raw = Image.open(io.BytesIO(res.content))
    img_logo_raw = img_logo_raw.resize((140, 140), Image.Resampling.LANCZOS)

    atualizar_imagem_logo()
except Exception:
    lbl_banner.config(
        text="🏦 VocacaoBank",
        font=("Arial", 22, "bold"),
        fg="white",
        bg=cores["fundo"],
    )

notebook_auth = ttk.Notebook(frame_auth)
notebook_auth.pack(padx=40, pady=10, fill="both", expand=True)

aba_login = tk.Frame(notebook_auth, bg=cores["painel"])
aba_cad = tk.Frame(notebook_auth, bg=cores["painel"])

notebook_auth.add(aba_login, text="Entrar")
notebook_auth.add(aba_cad, text="Criar Conta")

# Formulário Login
tk.Label(
    aba_login, text="Usuário:", bg=cores["painel"], font=("Arial", 10, "bold")
).pack(pady=(20, 2))
ent_usr_login = tk.Entry(
    aba_login,
    font=("Arial", 11),
    bg=cores["entrada_fundo"],
    fg=cores["entrada_texto"],
)
ent_usr_login.pack(ipadx=10, ipady=3)

tk.Label(
    aba_login, text="Senha:", bg=cores["painel"], font=("Arial", 10, "bold")
).pack(pady=(10, 2))
ent_pwd_login = tk.Entry(
    aba_login,
    show="*",
    font=("Arial", 11),
    bg=cores["entrada_fundo"],
    fg=cores["entrada_texto"],
)
ent_pwd_login.pack(ipadx=10, ipady=3)

tk.Button(
    aba_login,
    text="Acessar Conta",
    bg=cores["detalhe"],
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    command=autenticar,
).pack(pady=15, ipadx=10, ipady=3)

tk.Label(
    aba_login,
    text="💡 Dica: Usuário root tem senha 'root123'",
    font=("Arial", 9, "italic"),
    bg=cores["painel"],
    fg="gray",
).pack()

# Formulário Cadastro
tk.Label(
    aba_cad,
    text="Novo Usuário:",
    bg=cores["painel"],
    font=("Arial", 10, "bold"),
).pack(pady=(20, 2))
ent_usr_cad = tk.Entry(
    aba_cad,
    font=("Arial", 11),
    bg=cores["entrada_fundo"],
    fg=cores["entrada_texto"],
)
ent_usr_cad.pack(ipadx=10, ipady=3)

tk.Label(
    aba_cad, text="Nova Senha:", bg=cores["painel"], font=("Arial", 10, "bold")
).pack(pady=(10, 2))
ent_pwd_cad = tk.Entry(
    aba_cad,
    show="*",
    font=("Arial", 11),
    bg=cores["entrada_fundo"],
    fg=cores["entrada_texto"],
)
ent_pwd_cad.pack(ipadx=10, ipady=3)

tk.Button(
    aba_cad,
    text="Cadastrar",
    bg=cores["verde"],
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    command=cadastrar_usuario,
).pack(pady=15, ipadx=10, ipady=3)


# --- TELA 2: PAINEL PRINCIPAL DO USUÁRIO ---
frame_painel = tk.Frame(janela, bg=cores["painel"])

header_p = tk.Frame(frame_painel, bg=cores["fundo"])
header_p.pack(fill="x")

lbl_usuario_logado = tk.Label(
    header_p, text="", font=("Arial", 11, "bold"), fg="white", bg=cores["fundo"]
)
lbl_usuario_logado.pack(side="left", padx=15, pady=10)

btn_logout = tk.Button(
    header_p,
    text="Sair",
    bg=cores["rosa"],
    fg="white",
    relief="flat",
    command=logout,
)
btn_logout.pack(side="right", padx=15, pady=10)

# Visor de Saldo
lbl_saldo_title = tk.Label(
    frame_painel,
    text="Saldo Disponível",
    font=("Arial", 10),
    fg="gray",
    bg=cores["painel"],
)
lbl_saldo_title.pack(pady=(10, 0))

lbl_saldo_val = tk.Label(
    frame_painel,
    text="R$ 0.00",
    font=("Arial", 22, "bold"),
    fg=cores["detalhe"],
    bg=cores["painel"],
)
lbl_saldo_val.pack(pady=(0, 10))

# Operações
frame_ops = tk.LabelFrame(
    frame_painel,
    text=" Realizar Operação ",
    bg=cores["painel"],
    font=("Arial", 10, "bold"),
)
frame_ops.pack(padx=20, pady=5, fill="x")

tk.Label(frame_ops, text="Valor (R$):", bg=cores["painel"]).grid(
    row=0, column=0, padx=5, pady=5
)
ent_valor_op = tk.Entry(
    frame_ops,
    font=("Arial", 10),
    width=12,
    bg=cores["entrada_fundo"],
    fg=cores["entrada_texto"],
)
ent_valor_op.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_ops, text="Tipo:", bg=cores["painel"]).grid(
    row=0, column=2, padx=5, pady=5
)
combo_tipo_op = ttk.Combobox(
    frame_ops,
    values=["Pix", "Cartão Débito", "Cartão Crédito", "TED/DOC"],
    width=14,
    state="readonly",
)
combo_tipo_op.current(0)
combo_tipo_op.grid(row=0, column=3, padx=5, pady=5)

btn_dep = tk.Button(
    frame_ops,
    text="Depositar (+)",
    bg=cores["verde"],
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=realizar_deposito,
)
btn_dep.grid(row=1, column=0, columnspan=2, padx=5, pady=8, sticky="ew")

btn_pag = tk.Button(
    frame_ops,
    text="Pagar/Transferir (-)",
    bg=cores["rosa"],
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=realizar_pagamento,
)
btn_pag.grid(row=1, column=2, columnspan=2, padx=5, pady=8, sticky="ew")

# Extrato
lbl_historico_title = tk.Label(
    frame_painel,
    text="Histórico de Transações",
    font=("Arial", 10, "bold"),
    bg=cores["painel"],
)
lbl_historico_title.pack(pady=(10, 2))

lst_extrato = tk.Listbox(
    frame_painel,
    height=6,
    font=("Consolas", 9),
    bg=cores["entrada_fundo"],
    fg=cores["entrada_texto"],
    relief="solid",
    bd=1,
)
lst_extrato.pack(padx=20, pady=(0, 5), fill="both", expand=True)

# Botão Exportar JSON
btn_json = tk.Button(
    frame_painel,
    text="💾 Exportar Extrato (JSON)",
    bg=cores["amarelo"],
    fg="black",
    font=("Arial", 10, "bold"),
    relief="flat",
    command=exportar_json,
)
btn_json.pack(pady=(0, 15))

janela.mainloop()