import json
import os
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

# ==================== PALETAS DE CORES ====================
PALETA_CLARA = {
    "fundo": "#f4f6f9",
    "painel": "#ffffff",
    "texto": "#1a1a2e",
    "primaria": "#3b82f6",
    "verde": "#10b981",
    "vermelho": "#ef4444",
    "amarelo": "#f59e0b",
    "linha_fundo": "#ffffff",
}

PALETA_ESCURA = {
    "fundo": "#121212",
    "painel": "#1e1e2e",
    "texto": "#ffffff",
    "primaria": "#60a5fa",
    "verde": "#34d399",
    "vermelho": "#f87171",
    "amarelo": "#fbbf24",
    "linha_fundo": "#2a2a3c",
}

cores = PALETA_CLARA
modo_escuro = False
ARQUIVO_DADOS = "tarefas.json"

# ==================== ESTRUTURA DE DADOS ====================
tarefas = []


def carregar_tarefas():
    global tarefas
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                tarefas = json.load(f)
        except Exception:
            tarefas = []


def salvar_tarefas():
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(tarefas, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao salvar tarefas: {e}")


# ==================== LÓGICA DA APLICAÇÃO ====================
def adicionar_tarefa():
    titulo = ent_titulo.get().strip()
    prioridade = combo_prioridade.get()

    if not titulo:
        messagebox.showwarning("Aviso", "Digite o título da tarefa!")
        return

    nova_tarefa = {
        "id": int(datetime.now().timestamp()),
        "titulo": titulo,
        "prioridade": prioridade,
        "concluida": False,
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas()
    atualizar_lista()
    ent_titulo.delete(0, tk.END)


def alternar_status_tarefa():
    item_selecionado = lst_tarefas.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma tarefa na lista.")
        return

    idx = lst_tarefas.index(item_selecionado[0])
    tarefas[idx]["concluida"] = not tarefas[idx]["concluida"]
    salvar_tarefas()
    atualizar_lista()


def excluir_tarefa():
    item_selecionado = lst_tarefas.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para excluir.")
        return

    idx = lst_tarefas.index(item_selecionado[0])
    del tarefas[idx]
    salvar_tarefas()
    atualizar_lista()


def exportar_json():
    """Exporta a lista atual de tarefas para um arquivo JSON dentro da pasta 'ticket'"""
    if not tarefas:
        messagebox.showwarning("Aviso", "Não há tarefas para exportar!")
        return

    # 1. Caminho da pasta 'ticket' dentro do projeto
    pasta_ticket = os.path.join(os.getcwd(), "ticket")
    os.makedirs(pasta_ticket, exist_ok=True)  # Garante que a pasta 'ticket' existe

    # 2. Nome padronizado do arquivo (ex: tarefa_20260811_221000.json)
    nome_padrao = f"tarefa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    caminho_padrao = os.path.join(pasta_ticket, nome_padrao)

    # 3. Caixa de diálogo já apontando para a pasta 'ticket'
    caminho_arquivo = filedialog.asksaveasfilename(
        initialdir=pasta_ticket,
        initialfile=nome_padrao,
        defaultextension=".json",
        filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
        title="Salvar Tarefa JSON",
    )

    if caminho_arquivo:
        try:
            dados_exportacao = {
                "data_exportacao": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "total_tarefas": len(tarefas),
                "tarefas": tarefas,
            }

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados_exportacao, f, indent=4, ensure_ascii=False)

            messagebox.showinfo(
                "Sucesso",
                f"Tarefa exportada com sucesso na pasta 'ticket'!\n\nCaminho: {caminho_arquivo}",
            )

            # Tenta abrir o arquivo criado direto no VS Code
            try:
                subprocess.run(["code", caminho_arquivo], shell=True)
            except Exception:
                pass

        except Exception as e:
            messagebox.showerror(
                "Erro ao Exportar", f"Falha ao gerar arquivo JSON: {e}"
            )


def atualizar_lista():
    lst_tarefas.delete(*lst_tarefas.get_children())
    for t in tarefas:
        status = "✔ Concluída" if t["concluida"] else "⏳ Pendente"
        lst_tarefas.insert(
            "",
            "end",
            values=(t["titulo"], t["prioridade"], status, t["data_criacao"]),
        )


def alternar_tema():
    global modo_escuro, cores
    modo_escuro = not modo_escuro
    cores = PALETA_ESCURA if modo_escuro else PALETA_CLARA

    janela.configure(bg=cores["fundo"])
    bar_topo.configure(bg=cores["fundo"])
    frame_add.configure(bg=cores["painel"], fg=cores["texto"])
    frame_lista.configure(bg=cores["painel"])
    frame_acoes.configure(bg=cores["fundo"])

    lbl_titulo_app.configure(bg=cores["fundo"], fg=cores["texto"])
    lbl_form_titulo.configure(bg=cores["painel"], fg=cores["texto"])
    lbl_form_prio.configure(bg=cores["painel"], fg=cores["texto"])

    ent_titulo.configure(
        bg=cores["fundo"], fg=cores["texto"], insertbackground=cores["texto"]
    )
    btn_tema.config(text="☀️ Modo Claro" if modo_escuro else "🌙 Modo Escuro")


# ==================== INTERFACE GRÁFICA ====================
janela = tk.Tk()
janela.title("Gerenciador de Tarefas - To-Do List")
janela.geometry("680x560")
janela.configure(bg=cores["fundo"])

# Topo / Barra de Ferramentas
bar_topo = tk.Frame(janela, bg=cores["fundo"])
bar_topo.pack(fill="x", padx=15, pady=10)

lbl_titulo_app = tk.Label(
    bar_topo,
    text="📋 Minhas Tarefas",
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
    command=alternar_tema,
)
btn_tema.pack(side="right")

# Formulário de Cadastro de Tarefas
frame_add = tk.LabelFrame(
    janela,
    text=" Nova Tarefa ",
    bg=cores["painel"],
    fg=cores["texto"],
    font=("Arial", 10, "bold"),
)
frame_add.pack(padx=15, pady=5, fill="x")

lbl_form_titulo = tk.Label(
    frame_add, text="Título:", bg=cores["painel"], fg=cores["texto"]
)
lbl_form_titulo.grid(row=0, column=0, padx=(10, 2), pady=8, sticky="e")

ent_titulo = tk.Entry(frame_add, font=("Arial", 10), width=30)
ent_titulo.grid(row=0, column=1, padx=(0, 10), pady=8, sticky="w")

lbl_form_prio = tk.Label(
    frame_add, text="Prioridade:", bg=cores["painel"], fg=cores["texto"]
)
lbl_form_prio.grid(row=0, column=2, padx=(5, 2), pady=8, sticky="e")

combo_prioridade = ttk.Combobox(
    frame_add,
    values=["Baixa", "Média", "Alta"],
    width=8,
    state="readonly",
)
combo_prioridade.current(1)
combo_prioridade.grid(row=0, column=3, padx=(7, 14), pady=8, sticky="w")

btn_add = tk.Button(
    frame_add,
    text="Adicionar",
    bg=cores["primaria"],
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=adicionar_tarefa,
)
btn_add.grid(row=0, column=4, padx=(2, 10), pady=8, sticky="w")

# Lista de Tarefas (Treeview)
frame_lista = tk.Frame(janela, bg=cores["painel"])
frame_lista.pack(padx=15, pady=10, fill="both", expand=True)

colunas = ("titulo", "prioridade", "status", "data")
lst_tarefas = ttk.Treeview(
    frame_lista, columns=colunas, show="headings", selectmode="browse"
)

lst_tarefas.heading("titulo", text="Tarefa")
lst_tarefas.heading("prioridade", text="Prioridade")
lst_tarefas.heading("status", text="Status")
lst_tarefas.heading("data", text="Criada em")

lst_tarefas.column("titulo", width=128)
lst_tarefas.column("prioridade", width=80, anchor="center")
lst_tarefas.column("status", width=100, anchor="center")
lst_tarefas.column("data", width=120, anchor="center")

lst_tarefas.pack(fill="both", expand=True, padx=5, pady=5)

# Ações da Lista (Botões do Rodapé)
frame_acoes = tk.Frame(janela, bg=cores["fundo"])
frame_acoes.pack(fill="x", padx=15, pady=(0, 15))

btn_concluir = tk.Button(
    frame_acoes,
    text="✔ Alternar Status",
    bg=cores["verde"],
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=alternar_status_tarefa,
)
btn_concluir.pack(side="left", padx=5)

btn_exportar = tk.Button(
    frame_acoes,
    text="💾 Exportar (JSON)",
    bg=cores["amarelo"],
    fg="black",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=exportar_json,
)
btn_exportar.pack(side="left", padx=5)

btn_excluir = tk.Button(
    frame_acoes,
    text="🗑 Excluir Tarefa",
    bg=cores["vermelho"],
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    command=excluir_tarefa,
)
btn_excluir.pack(side="right", padx=5)

# Inicialização
carregar_tarefas()
atualizar_lista()

janela.mainloop()