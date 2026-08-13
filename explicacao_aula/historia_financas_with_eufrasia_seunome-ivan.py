import io
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
# todas utilizações de requests e PIL estão dentro do try/except para evitar erros de conexão ou download da imagem

COLOR_AZUL_ESC = "#004d6e"  # AE (Fundo da tela)
COLOR_AZUL_MED = "#0081ab"  # AM (Bordas e detalhes)
COLOR_AZUL_CLA = "#00b1cd"  # AC (Destaque do texto da senha)
COLOR_VERDE    = "#a6c844"  # V  (Botão Principal / Gerar)
COLOR_ROSA     = "#b83764"  # R  (Acentos e alertas de erro)
COLOR_AMARELO  = "#edce01"  # A  (Botão Copiar / Destaque)
COLOR_ACO      = "#4a3336"  # B  (Fundo dos campos e cards)