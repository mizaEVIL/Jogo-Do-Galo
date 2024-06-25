import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import sys

def centralizar_janela(janela):
    largura_janela = janela.winfo_reqwidth()
    altura_janela = janela.winfo_reqheight()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    posicao_x = (largura_tela - largura_janela) // 2
    posicao_y = (altura_tela - altura_janela) // 2
    janela.geometry(f"+{posicao_x}+{posicao_y}")

def definir_esquema_cores(janela, background, foreground, activeBackground, activeForeground):
    janela.tk_setPalette(background=background, foreground=foreground, activeBackground=activeBackground, activeForeground=activeForeground)

class TelaInicial:
    def __init__(self):
        self.janela_iniciar = tk.Tk()
        self.janela_iniciar.title("Tela Inicial")
        self.janela_iniciar.geometry("325x325")
        self.janela_iniciar.resizable(width=False, height=False)
        self.janela_iniciar.iconbitmap("icone4.ico")
        centralizar_janela(self.janela_iniciar)
        definir_esquema_cores(self.janela_iniciar, background='#A9A9A9', foreground='#000000', activeBackground='#A9A9A9', activeForeground='#FFFFFF')

        tk.Label(self.janela_iniciar, text="Jogador - X").place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.nome_jogador1 = tk.Entry(self.janela_iniciar)
        self.nome_jogador1.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        tk.Label(self.janela_iniciar, text="Jogador - O \n (Deixe em branco para jogar contra o computador)").place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.nome_jogador2 = tk.Entry(self.janela_iniciar)
        self.nome_jogador2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        imagem_play = Image.open("play.png")
        imagem_play = ImageTk.PhotoImage(imagem_play)

        self.botao_iniciar = tk.Button(self.janela_iniciar, image=imagem_play, command=self.abrir_janela_dificuldade, borderwidth=0, highlightthickness=0)
        self.botao_iniciar.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        self.botao_iniciar.image = imagem_play

    def abrir_janela_dificuldade(self):
        jogador1 = self.nome_jogador1.get().strip()
        jogador2 = self.nome_jogador2.get().strip()

        if not jogador1:
            messagebox.showerror("Erro", "Por favor, insira o nome do Jogador.")
            return
        elif jogador1.lower().translate(str.maketrans("áàã@40íì1!9", "aaaaaaiiiiq")) == "maquina":
            messagebox.showerror("Erro", f"Não pode utilizar '{jogador1}' como nome de jogador.")
            return
        elif jogador2.lower().translate(str.maketrans("áàã@40íì1!9", "aaaaaaiiiiq")) == "maquina":
            messagebox.showerror("Erro", f"Não pode utilizar '{jogador2}' como nome de jogador.")
            return
        elif not jogador2:
            self.janela_dificuldade = tk.Toplevel(self.janela_iniciar)
            self.janela_dificuldade.title("Nível de Dificuldade")
            self.janela_dificuldade.geometry("325x325")
            self.janela_dificuldade.resizable(width=False, height=False)
            self.janela_dificuldade.iconbitmap("icone4.ico")
            centralizar_janela(self.janela_dificuldade)

            tk.Label(self.janela_dificuldade, text="Escolha o nível de dificuldade").place(relx=0.5, rely=0.1, anchor=tk.CENTER)

            imagem_facil = Image.open("easy.png")
            imagem_facil = ImageTk.PhotoImage(imagem_facil)

            self.opcao_facil = tk.Button(self.janela_dificuldade, image=imagem_facil, command=lambda: self.iniciar_jogo("Fácil"), borderwidth=0, highlightthickness=0)
            self.opcao_facil.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            self.opcao_facil.image = imagem_facil

            imagem_dificil = Image.open("hard.png")
            imagem_dificil = ImageTk.PhotoImage(imagem_dificil)

            self.opcao_dificil = tk.Button(self.janela_dificuldade, image=imagem_dificil, command=lambda: self.iniciar_jogo("Difícil"), borderwidth=0, highlightthickness=0)
            self.opcao_dificil.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
            self.opcao_dificil.image = imagem_dificil
        else:
            self.iniciar_jogo(dificuldade=None)

    def iniciar_jogo(self, dificuldade):
        jogador1 = self.nome_jogador1.get()
        jogador2 = self.nome_jogador2.get()

        if not jogador1:
            messagebox.showerror("Erro", "Por favor, insira o nome do Jogador 1.")
            return
        elif not jogador2:
            jogador2 = "Máquina"

        self.janela_iniciar.destroy()
        if jogador2 == "Máquina":
            jogo = JogoDoGalo(jogador1, jogador2, dificuldade)
        else:
            jogo = JogoDoGalo(jogador1, jogador2)
        jogo.iniciar()

class JogoDoGalo:
    def __init__(self, jogador1, jogador2, dificuldade=None):
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.placar_jogador1 = 0
        self.placar_jogador2 = 0
        self.num_partidas = 5
        self.num_partidas_jogadas = 0
        self.vencedor = None

        self.janela_tab = tk.Tk()
        self.janela_tab.title("Jogo do Galo")
        self.janela_tab.geometry("317x325")
        self.janela_tab.resizable(width=False, height=False)
        self.janela_tab.iconbitmap("icone4.ico")
        centralizar_janela(self.janela_tab)
        definir_esquema_cores(self.janela_tab, background='#A9A9A9', foreground='#000000', activeBackground='#A9A9A9', activeForeground='#FFFFFF')

        self.turno = 'X'
        self.tabuleiro = [' ']*9

        tabuleiro_frame = tk.Frame(self.janela_tab)
        tabuleiro_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.botoes = []
        for i in range(9):
            botao = tk.Button(tabuleiro_frame, text=' ', font=('Arial', 20), width=6 , height=2,
                            command=lambda i=i: self.clicar_botao(i))
            botao.grid(row=i//3, column=i%3)
            self.botoes.append(botao)

        self.placar_label = tk.Label(self.janela_tab, text=f"PLACAR\n{jogador1} {self.placar_jogador1} X {self.placar_jogador2} {jogador2}", font=('Arial', 15))
        self.placar_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        self.atualizar_titulo()

        self.dificuldade = dificuldade

    def iniciar(self):
        self.janela_tab.mainloop()

    def clicar_botao(self, indice):
        if self.tabuleiro[indice] == ' ' and not self.vencedor:
            self.tabuleiro[indice] = self.turno
            self.botoes[indice].config(text=self.turno)
            if self.verificar_vitoria(self.turno):
                self.vencedor = self.turno
                self.atualizar_placar()
                if self.placar_jogador1 >= 3 or self.placar_jogador2 >= 3:
                    self.mostrar_tela_fim_jogo()
                else:
                    self.resetar_jogo()
            elif ' ' not in self.tabuleiro:
                self.vencedor = "Empate"
                self.atualizar_placar()
                if self.placar_jogador1 >= 3 or self.placar_jogador2 >= 3:
                    self.mostrar_tela_fim_jogo()
                else:
                    self.resetar_jogo()
            else:
                self.turno = 'O' if self.turno == 'X' else 'X'
                if self.jogador2 == "Máquina" and self.turno == 'O':
                    if self.dificuldade == "Fácil":
                        self.jogada_maquina_facil()
                    elif self.dificuldade == "Difícil":
                        self.jogada_maquina_dificil()

    def verificar_vitoria(self, jogador):
        for i in range(0, 9, 3):
            if self.tabuleiro[i] == self.tabuleiro[i+1] == self.tabuleiro[i+2] == jogador:
                return True
        for i in range(3):
            if self.tabuleiro[i] == self.tabuleiro[i+3] == self.tabuleiro[i+6] == jogador:
                return True
        if self.tabuleiro[0] == self.tabuleiro[4] == self.tabuleiro[8] == jogador:
            return True
        if self.tabuleiro[2] == self.tabuleiro[4] == self.tabuleiro[6] == jogador:
            return True
        return False

    def jogada_maquina_facil(self):
        movimentos_disponiveis = [i for i, x in enumerate(self.tabuleiro) if x == ' ']
        if movimentos_disponiveis:
            movimento = random.choice(movimentos_disponiveis)
            self.clicar_botao(movimento)

    def jogada_maquina_dificil(self):
        movimentos_disponiveis = [i for i, x in enumerate(self.tabuleiro) if x == ' ']
        if movimentos_disponiveis:
            melhor_movimento = self.escolher_melhor_movimento()
            self.clicar_botao(melhor_movimento)

    def escolher_melhor_movimento(self):
        melhor_pontuacao = float('-inf')
        melhor_movimento = None
        for movimento in [i for i, x in enumerate(self.tabuleiro) if x == ' ']:
            self.tabuleiro[movimento] = 'O'
            pontuacao = self.minimax(0, False)
            self.tabuleiro[movimento] = ' '
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_movimento = movimento
        return melhor_movimento

    def minimax(self, profundidade, eh_maximizador):
        if self.verificar_vitoria('O'):
            return 10 - profundidade
        elif self.verificar_vitoria('X'):
            return -10 + profundidade
        elif ' ' not in self.tabuleiro:
            return 0

        if eh_maximizador:
            melhor_pontuacao = float('-inf')
            for movimento in [i for i, x in enumerate(self.tabuleiro) if x == ' ']:
                self.tabuleiro[movimento] = 'O'
                pontuacao = self.minimax(profundidade + 1, False)
                self.tabuleiro[movimento] = ' '
                melhor_pontuacao = max(melhor_pontuacao, pontuacao)
            return melhor_pontuacao
        else:
            melhor_pontuacao = float('inf')
            for movimento in [i for i, x in enumerate(self.tabuleiro) if x == ' ']:
                self.tabuleiro[movimento] = 'X'
                pontuacao = self.minimax(profundidade + 1, True)
                self.tabuleiro[movimento] = ' '
                melhor_pontuacao = min(melhor_pontuacao, pontuacao)
            return melhor_pontuacao

    def atualizar_titulo(self):
        titulo = "Jogo do Galo "
        self.janela_tab.title(titulo)

    def atualizar_placar(self):
        if self.vencedor == 'X':
            self.placar_jogador1 += 1
        elif self.vencedor == 'O':
            self.placar_jogador2 += 1
        self.placar_label.config(text=f"PLACAR\n{self.jogador1} {self.placar_jogador1} X {self.placar_jogador2} {self.jogador2}")

    def resetar_jogo(self):
        self.tabuleiro = [' ']*9
        for botao in self.botoes:
            botao.config(text=' ')
        self.turno = 'X'
        self.vencedor = None
        self.num_partidas_jogadas += 1
        if self.num_partidas_jogadas >= self.num_partidas:
            self.mostrar_tela_fim_jogo()
        else:
            self.atualizar_titulo()

    def mostrar_tela_fim_jogo(self):
        mensagem = ""
        if self.placar_jogador1 == self.placar_jogador2:
            mensagem = "Empate geral!"
        elif self.placar_jogador1 > self.placar_jogador2:
            mensagem = f"{self.jogador1} venceu o jogo!"
        else:
            mensagem = f"{self.jogador2} venceu o jogo!"
        self.janela_tab.destroy()
        tela_fim_jogo = TelaFimJogo(mensagem, self.jogador1, self.jogador2, self.dificuldade)

class TelaFimJogo:
    def __init__(self, mensagem, jogador1, jogador2, dificuldade=None):
        self.janela_fim = tk.Tk()
        self.janela_fim.title("Fim do Jogo")
        self.janela_fim.geometry("325x325")
        self.janela_fim.resizable(width=False, height=False)
        self.janela_fim.iconbitmap("icone4.ico")
        centralizar_janela(self.janela_fim)
        definir_esquema_cores(self.janela_fim, background='#A9A9A9', foreground='#000000', activeBackground='#A9A9A9', activeForeground='#FFFFFF')

        tk.Label(self.janela_fim, text=mensagem).place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        imagem_novo_jogo = Image.open("newgame.png")
        imagem_novo_jogo = ImageTk.PhotoImage(imagem_novo_jogo)

        imagem_repetir = Image.open("replay.png")
        imagem_repetir = ImageTk.PhotoImage(imagem_repetir)

        imagem_fechar = Image.open("exit.png")
        imagem_fechar = ImageTk.PhotoImage(imagem_fechar)

        self.botao_novo_jogo = tk.Button(self.janela_fim, image=imagem_novo_jogo, command=self.iniciar_novo_jogo, borderwidth=0, highlightthickness=0)
        self.botao_novo_jogo.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.botao_repetir = tk.Button(self.janela_fim, image=imagem_repetir, command=lambda: self.repetir(jogador1, jogador2, dificuldade), borderwidth=0, highlightthickness=0)
        self.botao_repetir.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.botao_fechar = tk.Button(self.janela_fim, image=imagem_fechar, command=self.fechar, borderwidth=0, highlightthickness=0)
        self.botao_fechar.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.janela_fim.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        self.janela_fim.mainloop()

    def iniciar_novo_jogo(self):
        self.janela_fim.destroy()
        tela_inicial = TelaInicial()
        tela_inicial.janela_iniciar.mainloop()

    def repetir(self, jogador1, jogador2, dificuldade):
        self.janela_fim.destroy()
        if jogador2 == "Máquina":
            jogo = JogoDoGalo(jogador1, jogador2, dificuldade)
        else:
            jogo = JogoDoGalo(jogador1, jogador2)
        jogo.iniciar()

    def fechar(self):
        sys.exit()

    def fechar_janela(self):
        sys.exit()

if __name__ == "__main__":
    tela_inicial = TelaInicial()
    tela_inicial.janela_iniciar.mainloop()