import os
import sys
import runpy
import traceback

PASTA = os.path.dirname(os.path.abspath(__file__))
# If launched from inside Windows' temporary ZIP viewer, explain how to extract.
normalizada = PASTA.replace('/', '\\').lower()
if '\\appdata\\local\\temp\\' in normalizada and '.zip' in normalizada:
    try:
        import tkinter as tk
        from tkinter import messagebox
        r = tk.Tk(); r.withdraw()
        messagebox.showinfo('Proteja os Oceanos', 'Voce abriu o iniciador de dentro do ZIP.\n\nFeche esta janela, clique com o botao direito no ZIP, escolha “Extrair tudo...” e abra ABRIR_JOGO.pyw dentro da pasta extraida.')
        r.destroy()
    except Exception:
        print('Extraia todos os arquivos do ZIP antes de abrir ABRIR_JOGO.pyw.')
    raise SystemExit(0)

os.chdir(PASTA)
caminho = os.path.join(PASTA, 'jogo.py')
if not os.path.isfile(caminho):
    try:
        import tkinter as tk
        from tkinter import messagebox
        r = tk.Tk(); r.withdraw()
        messagebox.showerror('Proteja os Oceanos', 'Nao encontrei jogo.py. Extraia TODOS os arquivos do ZIP para uma pasta antes de abrir o jogo.')
        r.destroy()
    except Exception:
        print('Nao encontrei jogo.py. Extraia todos os arquivos do ZIP para uma pasta.')
    raise SystemExit(1)
try:
    runpy.run_path(caminho, run_name='__main__')
except Exception:
    erro = traceback.format_exc()
    try:
        import tkinter as tk
        from tkinter import messagebox
        r = tk.Tk(); r.withdraw()
        messagebox.showerror('Proteja os Oceanos - erro ao abrir', 'O jogo nao conseguiu iniciar. Envie esta mensagem ao ChatGPT:\n\n' + erro[-3500:])
        r.destroy()
    except Exception:
        pass
    raise
