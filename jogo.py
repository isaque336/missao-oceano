import pygame
import math
import os
import sys


def recurso(nome):
    """Encontra arquivos tanto no jogo.py quanto dentro do EXE do PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nome)

pygame.init()
pygame.mixer.init()

LARGURA = 1000
ALTURA = 563

# Tela cheia real: remove a barra branca superior, título, minimizar e fechar.
# Se o modo de tela cheia não for suportado pelo driver, usa janela sem bordas.
info_monitor = pygame.display.Info()
LARGURA_MONITOR = max(LARGURA, info_monitor.current_w or 1366)
ALTURA_MONITOR = max(ALTURA, info_monitor.current_h or 768)
try:
    janela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
except pygame.error:
    janela = pygame.display.set_mode((LARGURA_MONITOR, ALTURA_MONITOR), pygame.NOFRAME | pygame.DOUBLEBUF)
pygame.display.set_caption("Proteja os Oceanos")
TAMANHO_JANELA = janela.get_size()
tela = pygame.Surface((LARGURA, ALTURA)).convert()

def converter_mouse(posicao):
    """Converte cliques do monitor para as coordenadas lógicas do jogo."""
    largura_janela, altura_janela = janela.get_size()
    return (
        int(posicao[0] * LARGURA / max(1, largura_janela)),
        int(posicao[1] * ALTURA / max(1, altura_janela)),
    )


# Controles táteis para celulares: analógico virtual e botão de pulo.
# Os toques fora dos controles são convertidos em cliques para manter
# as interações existentes (lixo, animais, respostas, menu e palavras).
ANALOGICO_CENTRO = (105, 445)
ANALOGICO_RAIO = 66
BOTAO_PULO = pygame.Rect(842, 414, 125, 92)
touch_analogico_id = None
touch_pulo_id = None
analogico_x = 0.0
analogico_y = 0.0


def atualizar_analogico(posicao_logica):
    """Atualiza o vetor do analógico com magnitude limitada a 1."""
    global analogico_x, analogico_y
    dx = posicao_logica[0] - ANALOGICO_CENTRO[0]
    dy = posicao_logica[1] - ANALOGICO_CENTRO[1]
    distancia = math.hypot(dx, dy)
    limite = ANALOGICO_RAIO - 15
    if distancia > limite and distancia:
        dx *= limite / distancia
        dy *= limite / distancia
    analogico_x = max(-1.0, min(1.0, dx / limite))
    analogico_y = max(-1.0, min(1.0, dy / limite))


def desenhar_controles_tateis():
    """Desenha o analógico virtual e, quando aplicável, o botão de pulo."""
    if estado not in ("fase1", "fase2", "fase4"):
        return
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    pygame.draw.circle(camada, (5, 25, 40, 125), ANALOGICO_CENTRO, ANALOGICO_RAIO + 7)
    pygame.draw.circle(camada, (80, 205, 225, 190), ANALOGICO_CENTRO, ANALOGICO_RAIO, 3)
    deslocamento = (int(analogico_x * (ANALOGICO_RAIO - 18)), int(analogico_y * (ANALOGICO_RAIO - 18)))
    knob = (ANALOGICO_CENTRO[0] + deslocamento[0], ANALOGICO_CENTRO[1] + deslocamento[1])
    pygame.draw.circle(camada, (35, 145, 190, 220), knob, 27)
    pygame.draw.circle(camada, (220, 250, 255, 235), knob, 27, 3)
    if estado in ("fase1", "fase2"):
        pygame.draw.rect(camada, (4, 35, 55, 150), BOTAO_PULO, border_radius=18)
        pygame.draw.rect(camada, (255, 215, 90, 230), BOTAO_PULO, 3, border_radius=18)
        rotulo = pygame.font.SysFont("arial", 21, bold=True).render("PULAR", True, (255, 255, 255))
        camada.blit(rotulo, rotulo.get_rect(center=BOTAO_PULO.center))
    tela.blit(camada, (0, 0))

relogio = pygame.time.Clock()


# ==========================================================
# FUNÇÕES
# ==========================================================

def ajustar_imagem(imagem, largura, altura):

    proporcao = min(
        largura / imagem.get_width(),
        altura / imagem.get_height()
    )

    tamanho = (
        int(imagem.get_width() * proporcao),
        int(imagem.get_height() * proporcao)
    )

    return pygame.transform.smoothscale(
        imagem,
        tamanho
    )


def mostrar_imagem_centralizada(imagem):

    tela.fill((0, 0, 0))

    x = (
        LARGURA
        -
        imagem.get_width()
    ) // 2

    y = (
        ALTURA
        -
        imagem.get_height()
    ) // 2

    tela.blit(
        imagem,
        (x, y)
    )


# ==========================================================
# IMAGENS PRINCIPAIS
# ==========================================================

capa = ajustar_imagem(
    pygame.image.load(
        recurso("capa.png")
    ).convert(),
    LARGURA,
    ALTURA
)

# A arte original de seleção já contém os dois personagens e os três botões.
# Ela foi preparada sem a barra branca superior e ocupa a tela inteira.
personagens = pygame.transform.smoothscale(
    pygame.image.load(recurso("personagens.png")).convert(),
    (LARGURA, ALTURA)
)


# ==========================================================
# FASE 1
# ==========================================================

# A Fase 1 agora usa o cenário submarino profundo aprovado, em vez da praia
# de superfície. O mapa vertical repete-o sempre na orientação correta.
fase1_original = ajustar_imagem(
    pygame.image.load(
        recurso("fase2.png")
    ).convert(),
    LARGURA,
    ALTURA
)


# ==========================================================
# FASE 2
# ==========================================================

fase2_original = ajustar_imagem(
    pygame.image.load(
        recurso("fase2.png")
    ).convert(),
    LARGURA,
    ALTURA
)


# ==========================================================
# FASE 3
# ==========================================================

try:

    fase3_fundo = ajustar_imagem(
        pygame.image.load(
            recurso("fase3.png")
        ).convert(),
        LARGURA,
        ALTURA
    )

except:

    fase3_fundo = fase2_original


# Cenário próprio da Fase 4, com recife e corais visíveis.
fase4_original = ajustar_imagem(
    pygame.image.load(recurso("fase4_fundo.png")).convert(),
    LARGURA, ALTURA
)
fase4_mapa = pygame.image.load(recurso("fase4_mapa.png")).convert()

# Fase 5 — cenário fornecido para a missão final do oceano.
fase5_original_img = pygame.image.load(recurso("fase5_fundo.png")).convert()
fase5_fundo = pygame.transform.smoothscale(fase5_original_img, (LARGURA, ALTURA))

# Corais individuais (as barreiras da Fase 1 agora são fendas escuras que exigem pulo).

def preparar_sprite_coral(nome):
    img = pygame.image.load(recurso(nome)).convert_alpha()
    bounds = img.get_bounding_rect()
    if bounds.width and bounds.height:
        img = img.subsurface(bounds).copy()
    fator = min(148 / img.get_width(), 104 / img.get_height())
    return pygame.transform.smoothscale(img, (max(1, int(img.get_width()*fator)), max(1, int(img.get_height()*fator))))

corais_sprites = [preparar_sprite_coral(f"coral_{i}.png") for i in range(1, 7)]


# ==========================================================
# MAPA CONTÍNUO
# ==========================================================

LARGURA_MUNDO_FASE1 = 6000
ALTURA_MUNDO_FASE1 = ALTURA * 2  # somente duas telas para baixo; mapa alongado para os lados
LARGURA_MUNDO_FASE2 = 6000


def criar_mapa_continuo(
    imagem,
    largura
):

    mapa = pygame.Surface(
        (
            largura,
            ALTURA
        )
    )

    for i in range(
        largura // LARGURA + 2
    ):

        if i % 2 == 0:

            bloco = imagem

        else:

            bloco = pygame.transform.flip(
                imagem,
                True,
                False
            )

        mapa.blit(
            bloco,
            (
                i * LARGURA,
                0
            )
        )

    return mapa


def criar_mapa_profundo(imagem, largura, altura):
    """Cria um mapa longo: cenário original no início e áreas mais arenosas ao descer.

    O cenário nunca é virado de cabeça para baixo. A parte inferior usa um recorte
    do fundo arenoso para dar a sensação de mergulhar cada vez mais fundo.
    """
    mapa = pygame.Surface((largura, altura))
    corte_y = int(imagem.get_height() * 0.40)
    recorte_areia = imagem.subsurface(
        pygame.Rect(0, corte_y, imagem.get_width(), imagem.get_height() - corte_y)
    ).copy()
    areia = pygame.transform.smoothscale(recorte_areia, (LARGURA, ALTURA))
    linhas = (altura + ALTURA - 1) // ALTURA
    colunas = (largura + LARGURA - 1) // LARGURA
    for linha in range(linhas):
        for coluna in range(colunas):
            if linha == 0:
                bloco = imagem
            else:
                bloco = areia
                if (linha + coluna) % 2:
                    bloco = pygame.transform.flip(bloco, True, False)
            mapa.blit(bloco, (coluna * LARGURA, linha * ALTURA))
    return mapa



# Panorama já montado com transição suave: uma camada de recife e uma camada
# inferior mais escura e arenosa. Não há espelhamento vertical/horizontal.
fase1_mapa = pygame.image.load(recurso("fase1_mapa.png")).convert()

fase2_mapa = criar_mapa_continuo(
    fase2_original,
    LARGURA_MUNDO_FASE2
)


# ==========================================================
# PERSONAGENS
# ==========================================================

frames_menino = []
frames_menina = []


for i in range(1, 9):

    imagem = pygame.image.load(
        recurso(f"menino_{i}.png")
    ).convert_alpha()

    proporcao = (
        130
        /
        imagem.get_height()
    )

    imagem = pygame.transform.smoothscale(
        imagem,
        (
            int(
                imagem.get_width()
                *
                proporcao
            ),
            130
        )
    )

    frames_menino.append(
        imagem
    )


for i in range(1, 9):

    imagem = pygame.image.load(
        recurso(f"menina_{i}.png")
    ).convert_alpha()

    proporcao = (
        130
        /
        imagem.get_height()
    )

    imagem = pygame.transform.smoothscale(
        imagem,
        (
            int(
                imagem.get_width()
                *
                proporcao
            ),
            130
        )
    )

    frames_menina.append(
        imagem
    )


# Arte em alta resolução para as telas de introdução e conclusão.
# São os mesmos personagens da tela de seleção, não os sprites pequenos da animação.
def carregar_personagem_cartao(nome_arquivo):
    imagem = pygame.image.load(recurso(nome_arquivo)).convert_alpha()
    limites = imagem.get_bounding_rect(min_alpha=8)
    if limites.width > 0 and limites.height > 0:
        imagem = imagem.subsurface(limites).copy()
    return imagem


personagem_cartao_menino = carregar_personagem_cartao("menino.png")
personagem_cartao_menina = carregar_personagem_cartao("menina.png")


# ==========================================================
# LIXOS
# ==========================================================

folha_lixos = pygame.image.load(
    recurso("lixos.png")
).convert_alpha()

largura_celula = (
    folha_lixos.get_width()
    //
    4
)

altura_celula = (
    folha_lixos.get_height()
    //
    2
)

lixos_imagens = []


for linha in range(2):

    for coluna in range(4):

        recorte = folha_lixos.subsurface(
            pygame.Rect(
                coluna * largura_celula,
                linha * altura_celula,
                largura_celula,
                altura_celula
            )
        ).copy()

        recorte = pygame.transform.smoothscale(
            recorte,
            (
                90,
                90
            )
        )

        lixos_imagens.append(
            recorte
        )


# ==========================================================
# ANIMAIS DA FASE 2 — RECORTES INDIVIDUAIS
# ==========================================================
# Cada animal agora é um PNG separado e transparente.
# Isso evita que um recorte pegue outro animal, plantas,
# cenário ou partes da grade da imagem original.

def carregar_animal(nome):
    return pygame.image.load(recurso(nome + ".png")).convert_alpha()


polvo_livre = carregar_animal("polvo_livre")
polvo_preso = carregar_animal("polvo_preso")

caranguejo_livre = carregar_animal("caranguejo_livre")
caranguejo_preso = carregar_animal("caranguejo_preso")

cavalo_livre = carregar_animal("cavalo_livre")
cavalo_preso = carregar_animal("cavalo_preso")

baleia_livre = carregar_animal("baleia_livre")
baleia_presa = carregar_animal("baleia_presa")

tubarao_livre = carregar_animal("tubarao_livre")
tubarao_preso = carregar_animal("tubarao_preso")

arraia_livre = carregar_animal("arraia_livre")
arraia_presa = carregar_animal("arraia_presa")

aguaviva_livre = carregar_animal("aguaviva_livre")
aguaviva_presa = carregar_animal("aguaviva_presa")

foca_livre = carregar_animal("foca_livre")
foca_presa = carregar_animal("foca_presa")

pinguim_livre = carregar_animal("pinguim_livre")
pinguim_preso = carregar_animal("pinguim_preso")


# ==========================================================
# TAMANHO DOS ANIMAIS
# ==========================================================

def preparar_animal(
    imagem,
    tamanho
):

    proporcao = min(
        tamanho / imagem.get_width(),
        tamanho / imagem.get_height()
    )

    return pygame.transform.smoothscale(
        imagem,
        (
            max(
                1,
                int(
                    imagem.get_width()
                    *
                    proporcao
                )
            ),
            max(
                1,
                int(
                    imagem.get_height()
                    *
                    proporcao
                )
            )
        )
    )


polvo_livre = preparar_animal(
    polvo_livre,
    145
)

polvo_preso = preparar_animal(
    polvo_preso,
    145
)


caranguejo_livre = preparar_animal(
    caranguejo_livre,
    135
)

caranguejo_preso = preparar_animal(
    caranguejo_preso,
    135
)


cavalo_livre = preparar_animal(
    cavalo_livre,
    145
)

cavalo_preso = preparar_animal(
    cavalo_preso,
    145
)


baleia_livre = preparar_animal(
    baleia_livre,
    170
)

baleia_presa = preparar_animal(
    baleia_presa,
    170
)


tubarao_livre = preparar_animal(
    tubarao_livre,
    165
)

tubarao_preso = preparar_animal(
    tubarao_preso,
    165
)


arraia_livre = preparar_animal(
    arraia_livre,
    160
)

arraia_presa = preparar_animal(
    arraia_presa,
    160
)


aguaviva_livre = preparar_animal(
    aguaviva_livre,
    145
)

aguaviva_presa = preparar_animal(
    aguaviva_presa,
    145
)


foca_livre = preparar_animal(
    foca_livre,
    145
)

foca_presa = preparar_animal(
    foca_presa,
    145
)


pinguim_livre = preparar_animal(
    pinguim_livre,
    145
)

pinguim_preso = preparar_animal(
    pinguim_preso,
    145
)


# Os corais interativos são desenhados pelo próprio jogo, sem imagens com fundo embutido.
# Assim ficam isolados do cenário e podem mudar de branco para laranja ao serem resgatados.


# ==========================================================
# FONTES
# ==========================================================

fonte = pygame.font.SysFont(
    "arial",
    28,
    bold=True
)

fonte_grande = pygame.font.SysFont(
    "arial",
    50,
    bold=True
)

fonte_lista_fase3 = pygame.font.SysFont(
    "arial",
    20,
    bold=True
)

fonte_pequena = pygame.font.SysFont(
    "arial",
    19,
    bold=True
)


# ==========================================================
# SONS
# ==========================================================

musica = pygame.mixer.Sound(
    recurso("musica.mp3")
)

som_mar = pygame.mixer.Sound(
    recurso("mar.mp3")
)

musica.set_volume(
    0.35
)

som_mar.set_volume(
    0.5
)


# ==========================================================
# ESTADOS
# ==========================================================

estado = "capa"

personagem_escolhido = None

fase_atual = 1


# ==========================================================
# JOGADOR
# ==========================================================

jogador = pygame.Rect(
    150,
    350,
    45,
    60
)

velocidade = 5


# ==========================================================
# ANIMAÇÃO DO PERSONAGEM
# ==========================================================

frame_atual = 0

contador_animacao = 0

VELOCIDADE_ANIMACAO = 4

personagem_movendo = False

direcao = "direita"

balanco_personagem = 0

# PULO COM DUPLO TOQUE PARA CIMA
ultimo_toque_cima = 0
pulando = False
inicio_pulo = 0
DURACAO_PULO = 800
ALTURA_PULO = 72
JANELA_DUPLO_TOQUE = 320
ULTIMO_PULO = 0
COOLDOWN_PULO = 250


# ==========================================================
# FASE 1
# ==========================================================

TEMPO_FASE1 = 180

tempo_inicio = 0

camera_x_fase1 = 0
camera_y_fase1 = 0

TOTAL_LIXOS = 24

lixos = []


# Os 24 lixos ficam longe das bordas do mapa e das fendas. Há só duas camadas
# verticais, e a distribuição privilegia o meio do caminho para facilitar a coleta.
posicoes_lixos = [
    (380, 260), (570, 480), (720, 760), (780, 910),
    (1240, 300), (1430, 560), (1610, 790), (1740, 930),
    (2240, 260), (2420, 490), (2610, 740), (2760, 920),
    (3240, 280), (3420, 520), (3610, 770), (3760, 930),
    (4240, 260), (4420, 500), (4610, 750), (4760, 920),
    (5240, 280), (5420, 520), (5570, 760), (5680, 910)
]

# Fendas pretas atravessam TODA a profundidade do mapa: não dá para descer
# por baixo delas. O jogador precisa pular para atravessar cada fenda.
CENTROS_BARREIRAS_FASE1 = [1000, 2000, 3000, 4000, 5000]
barreiras_fase1 = [
    pygame.Rect(cx - 58, 0, 116, ALTURA_MUNDO_FASE1)
    for cx in CENTROS_BARREIRAS_FASE1
]


# ==========================================================
# FASE 2
# ==========================================================

TEMPO_FASE2 = 120

tempo_fase2 = 0

camera_x_fase2 = 0

animais = []


# ==========================================================
# FASE 3
# ==========================================================

TEMPO_FASE3 = 240

LINHAS_GRADE = 15

COLUNAS_GRADE = 15

# Grade do novo caça-palavras (15 x 15).
# Coordenadas na imagem 996x563, ajustada para 1000x563.
TAMANHO_CELULA_W = 27.6
TAMANHO_CELULA_H = 27.67
POS_X_GRADE = 40
POS_Y_GRADE = 101


palavras_fase3 = [

    "BIODIVERSIDADE",
    "ECOSSISTEMA",
    "MICROPLASTICO",
    "DESPOLUIR",
    "CONSCIENTIZAR",
    "REUTILIZAR",
    "REAPROVEITAR",
    "RECICLAGEM",
    "SUSTENTAVEL",
    "PROTEGER",
    "PRESERVACAO",
    "REDUZIR",
    "CONSERVACAO",
    "OCEANO"

]


grade_fase3 = []

posicoes_palavras_fase3 = {}

palavras_encontradas_fase3 = set()

tempo_fase3 = 0

selecionando_fase3 = False

inicio_selecao_fase3 = None

selecao_atual_fase3 = None


# ==========================================================
# FASE 4 — AQUECIMENTO DOS OCEANOS E RESGATE DOS CORAIS
# ==========================================================
TEMPO_FASE4 = 240
tempo_fase4 = 0
ultimo_aumento_temp = 0
temperatura_fase4 = 24.0
pontos_fase4 = 0
vidas_fase4 = 3
corais_fase4 = []
coral_selecionado = None
pergunta_coral_ativa = False
coral_cliques = 0
corais_resgatados = set()
corais_falhados = set()
resposta_feedback = ""
feedback_ate = 0

# FASE 5 — O ÚLTIMO SUSPIRO DO OCEANO
TEMPO_FASE5 = 240
inicio_fase5 = 0
fase5_indice = 0
fase5_feedback = ""
fase5_feedback_correto = False
fase5_acertos = 0
fase5_opcoes_rects = []
botao_fase5 = pygame.Rect(330, 430, 340, 68)
botao_feedback_fase5 = pygame.Rect(330, 468, 340, 42)
botao_intro_fase5 = pygame.Rect(330, 440, 340, 68)
perguntas_fase5 = [
    {
        "titulo": "DESAFIO 1 — O CALOR QUE AMEAÇA",
        "pergunta": "O que pode acontecer quando o oceano esquenta demais?",
        "opcoes": ["Os corais podem sofrer estresse térmico e branquear", "Todos os corais ficam mais fortes", "A temperatura não afeta os animais"],
        "correta": 0,
        "explicacao": "O calor excessivo causa estresse nos corais e pode provocar branqueamento."
    },
    {
        "titulo": "DESAFIO 2 — O PERIGO INVISÍVEL",
        "pergunta": "Como o excesso de CO2 contribui para a acidificação?",
        "opcoes": ["O CO2 entra na água e altera sua química, reduzindo carbonatos", "O CO2 transforma a água em plástico", "O CO2 deixa a água sempre mais doce"],
        "correta": 0,
        "explicacao": "Parte do CO2 é absorvida pelo mar e altera a química da água, dificultando a formação de conchas e esqueletos calcários."
    },
    {
        "titulo": "DESAFIO 3 — A VIDA DEPENDE DO EQUILÍBRIO",
        "pergunta": "Por que proteger habitats marinhos é tão importante?",
        "opcoes": ["Porque cada habitat abriga espécies e relações ecológicas", "Porque todos os animais vivem no mesmo lugar", "Porque a biodiversidade não depende dos habitats"],
        "correta": 0,
        "explicacao": "Habitats saudáveis oferecem abrigo, alimento e condições para a biodiversidade."
    },
    {
        "titulo": "DESAFIO 4 — ESCOLHAS SUSTENTÁVEIS",
        "pergunta": "Qual conjunto de atitudes ajuda a proteger o oceano?",
        "opcoes": ["Reduzir emissões, proteger habitats e diminuir a poluição", "Jogar resíduos no ralo e usar mais plástico descartável", "Retirar animais de seu habitat natural"],
        "correta": 0,
        "explicacao": "Reduzir emissões e resíduos e proteger habitats ajuda a diminuir a pressão sobre os ecossistemas."
    },
    {
        "titulo": "PERGUNTA FINAL — PROTEJA A BIODIVERSIDADE",
        "pergunta": "Como o excesso de CO2 prejudica a biodiversidade marinha?",
        "opcoes": ["Apenas deixa o oceano mais escuro", "Contribui para o aquecimento e a acidificação, ameaçando habitats e espécies", "Faz todos os animais crescerem mais"],
        "correta": 1,
        "explicacao": "O CO2 contribui para o aquecimento global e a acidificação dos oceanos, ameaçando habitats e espécies."
    }
]

perguntas_coral = [
    {"pergunta": "O que pode acontecer quando a água fica quente demais?",
     "opcoes": ["O coral sofre estresse térmico e pode branquear", "O coral vira uma pedra", "Nada acontece"], "correta": 0},
    {"pergunta": "O que significa o branqueamento dos corais?",
     "opcoes": ["O coral está crescendo mais rápido", "Sinal de estresse: perde algas simbióticas", "É apenas uma mudança de luz"], "correta": 1},
    {"pergunta": "Por que o aquecimento preocupa os seres vivos?",
     "opcoes": ["Pode prejudicar habitats e desequilibrar ecossistemas", "Deixa todos os peixes maiores", "Não afeta o oceano"], "correta": 0},
    {"pergunta": "Qual atitude ajuda a proteger os corais?",
     "opcoes": ["Jogar lixo no mar", "Reduzir a poluição e combater o aquecimento", "Retirar os corais do recife"], "correta": 1},
    {"pergunta": "Por que os corais são importantes para os oceanos?",
     "opcoes": ["Servem de abrigo para muitas espécies", "Aumentam a temperatura da água", "Impedem todos os peixes de nadar"], "correta": 0},
    {"pergunta": "O que devemos fazer diante de um recife branqueado?",
     "opcoes": ["Quebrar os corais para ajudar", "Reduzir impactos e proteger o habitat", "Levar os corais para casa"], "correta": 1}
]

# ==========================================================
# BOTÕES
# ==========================================================

# Áreas de clique alinhadas aos botões desenhados na capa (JOGAR / COMO JOGAR).
botao_jogar = pygame.Rect(340, 325, 320, 90)
botao_como_jogar = pygame.Rect(340, 420, 320, 80)
botao_como_jogar_voltar = pygame.Rect(370, 490, 260, 48)

# Botões alinhados: menino, voltar no centro e menina.
botao_menino = pygame.Rect(72, 432, 276, 70)
botao_voltar = pygame.Rect(397, 444, 196, 64)
botao_menina = pygame.Rect(650, 432, 280, 70)

botao_tentar = pygame.Rect(
    350,
    390,
    300,
    80
)

botao_menu = pygame.Rect(
    350,
    480,
    300,
    60
)

# Botões exclusivos da tela de derrota (fase 3 e fase 5).
botao_derrota_tentar = pygame.Rect(170, 370, 300, 70)
botao_derrota_inicio = pygame.Rect(530, 370, 300, 70)
motivo_derrota = "tempo"

botao_fase2 = pygame.Rect(
    330,
    370,
    340,
    90
)

botao_fase3 = pygame.Rect(
    330,
    370,
    340,
    90
)

botao_fase4 = pygame.Rect(330, 370, 340, 90)
botao_intro1 = pygame.Rect(330, 430, 340, 72)


# ==========================================================
# ESCOLHA DO PERSONAGEM — ARTE ORGANIZADA, SEM TEXTO POR CIMA
# ==========================================================
def desenhar_selecao_personagem():
    # Tela original aprovada: menino à esquerda, menina à direita e VOLTAR no meio.
    # Os botões desenhados na imagem são clicáveis pelas hitboxes correspondentes.
    tela.blit(personagens, (0, 0))


# ==========================================================
# INTRODUÇÃO EDUCATIVA — FASE 1
# ==========================================================
def desenhar_intro_fase1():
    desenhar_cartao_transicao(
        "MISSÃO 1 — LIMPAR O MAR",
        [
            "Por que devemos retirar o lixo do mar?",
            "Plásticos, latas e outros resíduos podem ferir os animais,",
            "contaminar a água e destruir os lugares onde vivem.",
            "Explore o fundo do mar, encontre os objetos marcados",
            "e clique em cada lixo para recolhê-lo. Pule as fendas!"
        ],
        botao_intro1,
        "COMEÇAR A MISSÃO"
    )


# ==========================================================
# INICIAR FASE 1
# ==========================================================

def iniciar_fase1():

    global lixos
    global tempo_inicio
    global frame_atual
    global contador_animacao
    global camera_x_fase1
    global camera_y_fase1
    global balanco_personagem
    global pulando
    global inicio_pulo
    global ULTIMO_PULO

    jogador.x = 150
    jogador.y = 350

    camera_x_fase1 = 0
    camera_y_fase1 = 0

    frame_atual = 0
    contador_animacao = 0
    balanco_personagem = 0
    pulando = False
    inicio_pulo = 0
    ultimo_toque_cima = 0
    ULTIMO_PULO = 0

    lixos = []

    for i, pos in enumerate(
        posicoes_lixos
    ):

        x, y = pos

        lixos.append({

            "rect": pygame.Rect(
                x,
                y,
                65,
                65
            ),

            "tipo":
                i
                %
                len(
                    lixos_imagens
                )

        })


    tempo_inicio = (
        pygame.time.get_ticks()
    )

    musica.stop()
    musica.play(-1)

    som_mar.stop()
    som_mar.play(-1)


# ==========================================================
# INICIAR FASE 2
# ==========================================================

def iniciar_fase2():

    global animais
    global tempo_fase2
    global frame_atual
    global contador_animacao
    global camera_x_fase2
    global pulando
    global inicio_pulo
    global ultimo_toque_cima
    global ULTIMO_PULO

    jogador.x = 180
    jogador.y = 390

    camera_x_fase2 = 0

    frame_atual = 0
    contador_animacao = 0
    pulando = False
    inicio_pulo = 0
    ultimo_toque_cima = 0
    ULTIMO_PULO = 0


    animais = [

        {
            "nome": "POLVO",
            "mensagem": "AJUDE O POLVO!",
            "pos": [380, 390],
            "presa": polvo_preso,
            "livre": polvo_livre,
            "salva": False
        },

        {
            "nome": "CARANGUEJO",
            "mensagem": "AJUDE O CARANGUEJO!",
            "pos": [1050, 270],
            "presa": caranguejo_preso,
            "livre": caranguejo_livre,
            "salva": False
        },

        {
            "nome": "CAVALO-MARINHO",
            "mensagem": "AJUDE O CAVALO-MARINHO!",
            "pos": [1750, 430],
            "presa": cavalo_preso,
            "livre": cavalo_livre,
            "salva": False
        },

        {
            "nome": "BALEIA",
            "genero": "f",
            "mensagem": "AJUDE A BALEIA!",
            "pos": [2450, 250],
            "presa": baleia_presa,
            "livre": baleia_livre,
            "salva": False
        },

        {
            "nome": "TUBARÃO",
            "mensagem": "AJUDE O TUBARÃO!",
            "pos": [3150, 420],
            "presa": tubarao_preso,
            "livre": tubarao_livre,
            "salva": False
        },

        {
            "nome": "ARRAIA",
            "genero": "f",
            "mensagem": "AJUDE A ARRAIA!",
            "pos": [3800, 260],
            "presa": arraia_presa,
            "livre": arraia_livre,
            "salva": False
        },

        {
            "nome": "ÁGUA-VIVA",
            "genero": "f",
            "mensagem": "AJUDE A ÁGUA-VIVA!",
            "pos": [4450, 430],
            "presa": aguaviva_presa,
            "livre": aguaviva_livre,
            "salva": False
        },

        {
            "nome": "FOCA",
            "genero": "f",
            "mensagem": "AJUDE A FOCA!",
            "pos": [5100, 250],
            "presa": foca_presa,
            "livre": foca_livre,
            "salva": False
        },

        {
            "nome": "PINGUIM",
            "mensagem": "AJUDE O PINGUIM!",
            "pos": [5750, 420],
            "presa": pinguim_preso,
            "livre": pinguim_livre,
            "salva": False
        }

    ]


    tempo_fase2 = (
        pygame.time.get_ticks()
    )

    musica.stop()
    musica.play(-1)

    som_mar.stop()
    som_mar.play(-1)


# ==========================================================
# FASE 3
# ==========================================================

def iniciar_fase3():

    global grade_fase3
    global posicoes_palavras_fase3
    global palavras_encontradas_fase3
    global tempo_fase3
    global selecionando_fase3
    global inicio_selecao_fase3
    global selecao_atual_fase3


    grade_fase3 = [

        list("UPPROTEGER RSMOF".replace(" ", "")),
        list("RAZILITUERIOPAB"),
        list("CSYXONAECOUHRCI"),
        list("OOUUCJZYXSLREAO"),
        list("NONSABOFZMOXSVD"),
        list("SMRATIEVORPAERI"),
        list("CWRUEEEXQESCREV"),
        list("IYECRYNIEEEP VSE".replace(" ", "")),
        list("EZJVIBQTDCDPANR"),
        list("NMICROPLASTICOS"),
        list("TMRIZUDERVAVACI"),
        list("IGDDGXIYJVEAOVD"),
        list("ZKAJTDGHTZTLBNA"),
        list("AVECOSSISTEMAAD"),
        list("RRECICLAGEMENBE")

    ]

    posicoes_palavras_fase3 = {}

    # Localiza cada palavra em qualquer direção:
    # horizontal, vertical ou diagonal, inclusive ao contrário.
    direcoes = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    for palavra in palavras_fase3:

        encontrada = False

        for linha in range(LINHAS_GRADE):

            for coluna in range(COLUNAS_GRADE):

                for dl, dc in direcoes:

                    fim_linha = linha + (len(palavra) - 1) * dl
                    fim_coluna = coluna + (len(palavra) - 1) * dc

                    if not (
                        0 <= fim_linha < LINHAS_GRADE
                        and
                        0 <= fim_coluna < COLUNAS_GRADE
                    ):
                        continue

                    texto = ""

                    for i in range(len(palavra)):
                        texto += grade_fase3[
                            linha + i * dl
                        ][
                            coluna + i * dc
                        ]

                    if texto == palavra:

                        posicoes_palavras_fase3[palavra] = (
                            linha,
                            coluna,
                            fim_linha,
                            fim_coluna
                        )

                        encontrada = True
                        break

                if encontrada:
                    break

            if encontrada:
                break

    palavras_encontradas_fase3 = set()

    selecionando_fase3 = False

    inicio_selecao_fase3 = None

    selecao_atual_fase3 = None

    tempo_fase3 = (
        pygame.time.get_ticks()
    )

    musica.stop()
    musica.play(-1)

    som_mar.stop()
    som_mar.play(-1)


def celula_fase3(
    pos
):

    x, y = pos

    coluna = int(
        (
            x
            -
            POS_X_GRADE
        )
        /
        TAMANHO_CELULA_W
    )

    linha = int(
        (
            y
            -
            POS_Y_GRADE
        )
        /
        TAMANHO_CELULA_H
    )


    if (
        0 <= linha < LINHAS_GRADE
        and
        0 <= coluna < COLUNAS_GRADE
    ):

        return (
            linha,
            coluna
        )

    return None


def verificar_selecao_fase3(
    inicio,
    fim
):

    if (
        inicio is None
        or
        fim is None
    ):

        return None


    l1, c1 = inicio

    l2, c2 = fim

    dl = l2 - l1

    dc = c2 - c1


    if dl == 0 and dc == 0:

        return None


    if not (
        dl == 0
        or
        dc == 0
        or
        abs(dl) == abs(dc)
    ):

        return None


    passos = max(
        abs(dl),
        abs(dc)
    )


    passo_l = (

        0

        if dl == 0

        else (
            1
            if dl > 0
            else -1
        )

    )


    passo_c = (

        0

        if dc == 0

        else (
            1
            if dc > 0
            else -1
        )

    )


    palavra = ""


    for i in range(
        passos + 1
    ):

        l = (
            l1
            +
            passo_l * i
        )

        c = (
            c1
            +
            passo_c * i
        )

        palavra += (
            grade_fase3[l][c]
        )


    for nome in palavras_fase3:

        if (
            nome
            not in
            palavras_encontradas_fase3
        ):

            if (
                palavra == nome
                or
                palavra[::-1] == nome
            ):

                return nome


    return None


def iniciar_fase4():
    global tempo_fase4, ultimo_aumento_temp, temperatura_fase4, corais_fase4
    global coral_selecionado, pergunta_coral_ativa, coral_cliques
    global corais_resgatados, corais_falhados, resposta_feedback, feedback_ate
    global jogador, camera_x_fase2, pulando, inicio_pulo, ultimo_toque_cima
    global pontos_fase4, vidas_fase4
    jogador.x, jogador.y = 100, 350
    camera_x_fase2 = 0
    tempo_fase4 = pygame.time.get_ticks()
    ultimo_aumento_temp = tempo_fase4
    temperatura_fase4 = 24.0
    pontos_fase4 = 0
    vidas_fase4 = 3
    corais_resgatados = set()
    corais_falhados = set()
    coral_selecionado = None
    pergunta_coral_ativa = False
    coral_cliques = 0
    resposta_feedback = ""
    feedback_ate = 0
    pulando = False
    inicio_pulo = 0
    ultimo_toque_cima = 0
    corais_fase4 = [
        {"id": 0, "x": 620, "y": 445, "cliques": 0, "cor": (245, 242, 222)},
        {"id": 1, "x": 1450, "y": 425, "cliques": 0, "cor": (245, 242, 222)},
        {"id": 2, "x": 2280, "y": 450, "cliques": 0, "cor": (245, 242, 222)},
        {"id": 3, "x": 3230, "y": 420, "cliques": 0, "cor": (245, 242, 222)},
        {"id": 4, "x": 4200, "y": 445, "cliques": 0, "cor": (245, 242, 222)},
        {"id": 5, "x": 5250, "y": 425, "cliques": 0, "cor": (245, 242, 222)},
    ]
    musica.stop(); musica.play(-1)
    som_mar.stop(); som_mar.play(-1)


def desenhar_coral(pos, indice, recuperado=False, falhou=False):
    """Coral branco antes da pergunta, laranja ao recuperar e apagado se errar."""
    x, y = int(pos[0]), int(pos[1])
    sprite = corais_sprites[indice].copy()
    if recuperado:
        tinta = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        tinta.fill((255, 132, 38, 255))
        sprite.blit(tinta, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        pygame.draw.ellipse(tela, (255, 174, 65, 70), (x-76, y+2, 152, 22))
    elif falhou:
        tinta = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        tinta.fill((118, 130, 135, 175))
        sprite.blit(tinta, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        pygame.draw.ellipse(tela, (5, 18, 28, 175), (x-72, y+2, 144, 20))
    else:
        pygame.draw.ellipse(tela, (8, 36, 50, 125), (x-72, y+2, 144, 20))
    rect = sprite.get_rect(midbottom=(x, y+8))
    tela.blit(sprite, rect)
    if recuperado:
        pygame.draw.circle(tela, (145, 255, 175), (x+rect.width//2-8, rect.top+12), 10, 3)
        pygame.draw.line(tela, (145,255,175), (x+rect.width//2-13,rect.top+12),(x+rect.width//2-9,rect.top+16),3)
        pygame.draw.line(tela, (145,255,175), (x+rect.width//2-9,rect.top+16),(x+rect.width//2-2,rect.top+7),3)


def desenhar_fase4():
    # Mapa ampliado próprio da Fase 4, com recife, peixes, destroços e vegetação.
    tela.blit(fase4_mapa, (-camera_x_fase2, 0))

    # Painel superior inspirado diretamente na referência enviada.
    painel = pygame.Surface((LARGURA, 104), pygame.SRCALPHA)
    painel.fill((4, 35, 65, 220))
    tela.blit(painel, (0, 0))
    titulo = fonte.render("RESGATE DOS 6 CORAIS", True, (255,255,255))
    tela.blit(titulo, (20, 7))
    passado = (pygame.time.get_ticks()-tempo_fase4)//1000
    restante = max(0, TEMPO_FASE4-passado)
    txt = fonte_pequena.render(f"Tempo: {restante//60:02d}:{restante%60:02d}", True, (255,245,110))
    tela.blit(txt, (835, 12))
    temp_txt = fonte_pequena.render(f"Temperatura do oceano: {temperatura_fase4:.1f} °C", True, (255,205,145))
    tela.blit(temp_txt, (20, 43))
    pygame.draw.rect(tela, (55,75,90), (290,48,220,15), border_radius=8)
    temp_prop = max(0.0, min(1.0, (temperatura_fase4-24.0)/21.0))
    temp_cor = (75,220,160) if temperatura_fase4 < 30 else (255,190,65) if temperatura_fase4 < 36 else (255,80,80)
    pygame.draw.rect(tela, temp_cor, (290,48,int(220*temp_prop),15), border_radius=8)
    pontos = fonte_pequena.render(f"Pontos: {pontos_fase4}", True, (255,255,255))
    tela.blit(pontos, (535, 43))
    vidas = fonte_pequena.render("Vidas: " + "♥ "*vidas_fase4, True, (255,125,145))
    tela.blit(vidas, (680, 43))

    progresso = len(corais_resgatados)
    info = fonte_pequena.render(f"Missão: recupere os corais esbranquiçados  •  Corais recuperados: {progresso}/6", True, (255,255,255))
    tela.blit(info, (20, 78))

    # Seis corais individuais, menores e bem separados ao longo do mapa.
    for coral in corais_fase4:
        sx = coral['x'] - camera_x_fase2
        sy = coral['y']
        if -170 < sx < LARGURA + 170:
            desenhar_coral((sx, sy), coral['id'], coral['id'] in corais_resgatados, coral['id'] in corais_falhados)
            label = fonte_pequena.render(f"CORAL {coral['id']+1}", True, (255,255,255))
            sombra = fonte_pequena.render(f"CORAL {coral['id']+1}", True, (0,30,45))
            tela.blit(sombra, (sx-label.get_width()//2+2, sy+22))
            tela.blit(label, (sx-label.get_width()//2, sy+20))
            if coral['id'] not in corais_resgatados and coral['id'] not in corais_falhados:
                bolha = fonte_pequena.render(str(coral['cliques'])+"/3", True, (235,255,255))
                tela.blit(bolha, (sx-bolha.get_width()//2, sy-140))
            elif coral['id'] in corais_falhados:
                falhou_txt = fonte_pequena.render("NÃO RECUPERADO", True, (225,230,230))
                tela.blit(falhou_txt, falhou_txt.get_rect(center=(sx, sy-112)))

    # Cartão da missão no estilo da referência, sem cobrir o centro do mapa.
    pygame.draw.rect(tela, (4,40,68), (18, 125, 260, 125), border_radius=16)
    pygame.draw.rect(tela, (135,220,230), (18, 125, 260, 125), 2, border_radius=16)
    missao = ["MISSÃO", "Encontre os 6 corais", "Clique 3 vezes em cada", "e responda ao desafio."]
    for i, linha in enumerate(missao):
        cor_linha = (255,220,100) if i == 0 else (255,255,255)
        tela.blit(fonte_pequena.render(linha, True, cor_linha), (32, 137+i*25))

    desenhar_personagem(camera_x_fase2)

    # Indicadores inferiores inspirados na arte de referência.
    pygame.draw.rect(tela, (4,35,65,225), (0, 526, LARGURA, 37))
    for x, label, valor, cor in [(22,"OXIGÊNIO",0.82,(80,200,240)), (345,"SAÚDE DOS CORAIS",max(0.15,1-temp_prop),(255,150,100)), (675,"POLUIÇÃO MARINHA",0.38,(255,110,120))]:
        tela.blit(fonte_pequena.render(label, True, (255,255,255)), (x, 529))
        pygame.draw.rect(tela, (30,70,90), (x, 550, 250, 8), border_radius=4)
        pygame.draw.rect(tela, cor, (x, 550, int(250*valor), 8), border_radius=4)

    if pergunta_coral_ativa and coral_selecionado is not None:
        shade = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        shade.fill((0,15,35,210))
        tela.blit(shade,(0,0))
        q = perguntas_coral[coral_selecionado]
        pygame.draw.rect(tela,(8,56,88),(90,105,820,355),border_radius=22)
        pygame.draw.rect(tela,(100,220,230),(90,105,820,355),3,border_radius=22)
        t = fonte.render(f"CORAL {coral_selecionado+1} — DESAFIO",True,(255,255,255))
        tela.blit(t,(125,128))
        linhas = [q['pergunta'][i:i+65] for i in range(0,len(q['pergunta']),65)]
        for i,line in enumerate(linhas):
            tela.blit(fonte_pequena.render(line,True,(255,240,170)),(125,174+i*27))
        for i,opt in enumerate(q['opcoes']):
            rect = pygame.Rect(125,250+i*58,750,45)
            pygame.draw.rect(tela,(20,110,135),rect,border_radius=10)
            t = fonte_pequena.render(f"{i+1}. {opt}",True,(255,255,255))
            tela.blit(t,(rect.x+14,rect.y+12))
        dica = fonte_pequena.render("Clique na resposta correta (1, 2 ou 3).",True,(160,255,200))
        tela.blit(dica,(125,425))
    elif resposta_feedback and pygame.time.get_ticks()<feedback_ate:
        msg = fonte.render(resposta_feedback,True,(160,255,190) if "Correto" in resposta_feedback or "recuperado" in resposta_feedback else (255,210,130))
        box = msg.get_rect(center=(LARGURA//2,ALTURA-80))
        pygame.draw.rect(tela,(0,35,60),box.inflate(28,16),border_radius=10)
        tela.blit(msg,box)
    if temperatura_fase4>=42:
        pygame.draw.rect(tela,(130,20,30),(200,260,600,75),border_radius=18)
        t=fonte.render("RISCO TÉRMICO CRÍTICO!",True,(255,255,255))
        tela.blit(t,t.get_rect(center=(500,297)))


# ==========================================================
# FASE 5 — INTRODUÇÃO, DESAFIOS E FINAL
# ==========================================================
def iniciar_fase5():
    global inicio_fase5, fase5_indice, fase5_feedback, fase5_feedback_correto, fase5_acertos
    inicio_fase5 = pygame.time.get_ticks()
    fase5_indice = 0
    fase5_feedback = ""
    fase5_feedback_correto = False
    fase5_acertos = 0
    musica.stop(); musica.play(-1)
    som_mar.stop(); som_mar.play(-1)


def desenhar_intro_fase5():
    desenhar_cartao_transicao(
        "FASE 5 — O ÚLTIMO SUSPIRO DO OCEANO",
        [
            "O oceano está ameaçado pelo aquecimento, pela acidificação e pela poluição.",
            "O calor pode branquear os corais e prejudicar os animais marinhos.",
            "O excesso de CO2 altera a química da água e ameaça moluscos.",
            "Relacione os animais aos habitats e escolha atitudes sustentáveis.",
            "Complete os desafios e ajude o oceano a se recuperar!"
        ],
        botao_intro_fase5,
        "COMEÇAR A MISSÃO FINAL",
        (20, 165, 215),
        fundo=fase5_fundo
    )



def desenhar_fase5():
    mostrar_imagem_centralizada(fase5_fundo)
    shade = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    shade.fill((0, 24, 50, 145)); tela.blit(shade, (0, 0))
    painel = pygame.Rect(35, 24, 930, 515)
    pygame.draw.rect(tela, (3, 34, 60), painel, border_radius=20)
    pygame.draw.rect(tela, (82, 204, 230), painel, 2, border_radius=20)
    q = perguntas_fase5[fase5_indice]
    fonte_titulo5 = pygame.font.SysFont("arial", 27, bold=True)
    titulo = fonte_titulo5.render(q["titulo"], True, (255,255,255))
    if titulo.get_width() > 870:
        titulo = pygame.transform.smoothscale(titulo, (870, titulo.get_height()))
    tela.blit(titulo, titulo.get_rect(center=(LARGURA//2, 66)))
    passado = max(0, (pygame.time.get_ticks()-inicio_fase5)//1000)
    restante = max(0, TEMPO_FASE5-passado)
    timer = fonte_pequena.render(f"Tempo: {restante//60:02d}:{restante%60:02d}   •   Desafio {fase5_indice+1}/5   •   Acertos: {fase5_acertos}", True, (255,238,115))
    tela.blit(timer, timer.get_rect(center=(500, 108)))
    pergunta = q["pergunta"]
    # Quebra o texto para manter margens confortáveis em resoluções diferentes.
    words = pergunta.split(); lines=[]; line=""
    for word in words:
        trial = (line+" "+word).strip()
        if fonte.render(trial, True, (255,255,255)).get_width() > 830 and line:
            lines.append(line); line=word
        else: line=trial
    if line: lines.append(line)
    for i, txtline in enumerate(lines):
        txt = fonte.render(txtline, True, (255,222,130))
        tela.blit(txt, txt.get_rect(center=(500, 158+i*34)))
    fase5_opcoes_rects.clear()
    y0 = 232 if len(lines) == 1 else 244
    fonte_opcao5 = pygame.font.SysFont("arial", 19, bold=True)
    for i, opt in enumerate(q["opcoes"]):
        rect = pygame.Rect(85, y0+i*62, 830, 50)
        fase5_opcoes_rects.append(rect)
        pygame.draw.rect(tela, (12, 91, 126), rect, border_radius=14)
        pygame.draw.rect(tela, (95, 220, 235), rect, 2, border_radius=14)
        texto_opcao = f"{chr(65+i)}) {opt}"
        # Quebra opções longas em duas linhas, mantendo o texto centralizado.
        palavras = texto_opcao.split(); linhas_opcao=[]; atual=""
        for palavra in palavras:
            teste=(atual+" "+palavra).strip()
            if fonte_opcao5.size(teste)[0] > rect.width-34 and atual:
                linhas_opcao.append(atual); atual=palavra
            else:
                atual=teste
        if atual: linhas_opcao.append(atual)
        if len(linhas_opcao) == 1:
            t = fonte_opcao5.render(linhas_opcao[0], True, (255,255,255))
            tela.blit(t, t.get_rect(center=rect.center))
        else:
            for j, linha_op in enumerate(linhas_opcao[:2]):
                t = fonte_opcao5.render(linha_op, True, (255,255,255))
                tela.blit(t, t.get_rect(center=(rect.centerx, rect.centery + (j-0.5)*20)))
    if fase5_feedback:
        cor = (120,255,165) if fase5_feedback_correto else (255,190,145)
        msg_lines=[]; line=""
        for word in fase5_feedback.split():
            trial=(line+" "+word).strip()
            if fonte_pequena.render(trial,True,cor).get_width()>820 and line:
                msg_lines.append(line); line=word
            else: line=trial
        if line: msg_lines.append(line)
        # Fundo para leitura do feedback e botão de continuar/tentar novamente.
        pygame.draw.rect(tela, (2,28,48), (60, 408, 880, 112), border_radius=14)
        for i, txtline in enumerate(msg_lines[:2]):
            txt=fonte_pequena.render(txtline,True,cor)
            tela.blit(txt,txt.get_rect(center=(500,424+i*24)))
        pygame.draw.rect(tela, (27,155,112) if fase5_feedback_correto else (180,95,35), botao_feedback_fase5, border_radius=12)
        label = "PRÓXIMA PERGUNTA" if fase5_indice < len(perguntas_fase5)-1 else "VER RESULTADO"
        t=fonte_pequena.render(label,True,(255,255,255)); tela.blit(t,t.get_rect(center=botao_feedback_fase5.center))


def desenhar_vitoria_fase5():
    desenhar_cartao_transicao(
        "O OCEANO PRECISA DE VOCÊ!",
        [
            "Você concluiu os cinco desafios da missão final!",
            "Reduzir as emissões, proteger habitats e diminuir a poluição ajuda o oceano.",
            "A recuperação é gradual e pode levar anos ou décadas.",
            "Cada escolha sustentável faz diferença!"
        ],
        botao_fase5,
        "VOLTAR AO INÍCIO",
        (25, 155, 110)
    )


# ==========================================================
# DESENHAR PERSONAGEM
# ==========================================================

def desenhar_personagem(
    camera_x=0,
    camera_y=0
):

    global frame_atual
    global contador_animacao
    global balanco_personagem
    global pulando
    global inicio_pulo


    if personagem_escolhido == "menino":

        imagem = frames_menino[
            frame_atual
        ]

    else:

        imagem = frames_menina[
            frame_atual
        ]


    if personagem_movendo:

        contador_animacao += 1

        if (
            contador_animacao
            >=
            VELOCIDADE_ANIMACAO
        ):

            contador_animacao = 0

            frame_atual += 1

            if frame_atual >= 8:

                frame_atual = 0

        balanco_personagem += 1

    else:

        frame_atual = 0

        balanco_personagem = 0


    if direcao == "esquerda":

        imagem = pygame.transform.flip(
            imagem,
            True,
            False
        )


    if personagem_movendo:

        movimento_y = int(
            math.sin(
                balanco_personagem
                *
                0.45
            )
            *
            2
        )

    else:

        movimento_y = 0

    if pulando:
        progresso = (pygame.time.get_ticks() - inicio_pulo) / DURACAO_PULO
        if progresso >= 1:
            pulando = False
            pulo_offset = 0
        else:
            pulo_offset = -int(math.sin(progresso * math.pi) * ALTURA_PULO)
    else:
        pulo_offset = 0


    x = (
        jogador.centerx
        -
        camera_x
        -
        imagem.get_width() // 2
    )

    y = (
        jogador.bottom
        - imagem.get_height()
        - camera_y
        + movimento_y
        + pulo_offset
    )


    if pulando:
        bolhas = pygame.Surface((imagem.get_width() + 80, imagem.get_height() + 80), pygame.SRCALPHA)
        base_x = bolhas.get_width() // 2
        base_y = bolhas.get_height() - 20
        for i, (bx, by, br) in enumerate(((0, 0, 5), (-18, -14, 3), (20, -25, 4), (-30, -34, 2))):
            pygame.draw.circle(bolhas, (170, 235, 255, 150), (base_x + bx, base_y + by), br)
        tela.blit(
            bolhas,
            (x - 40, y - 35)
        )


    sombra = pygame.Surface(
        (
            imagem.get_width(),
            18
        ),
        pygame.SRCALPHA
    )


    pygame.draw.ellipse(
        sombra,
        (0,0,0,80),
        sombra.get_rect()
    )


    tela.blit(
        sombra,
        (
            x,
            jogador.bottom - 5 - camera_y
        )
    )


    tela.blit(
        imagem,
        (
            x,
            y
        )
    )


# ==========================================================
# DESENHAR LIXOS
# ==========================================================

def desenhar_lixos(camera_x, camera_y=0):
    """Desenha cada objeto coletável com uma etiqueta clara de identificação."""
    for lixo in lixos:
        rect = lixo["rect"]
        imagem = lixos_imagens[lixo["tipo"]]
        x = int(rect.centerx - camera_x - imagem.get_width() // 2)
        y = int(rect.centery - camera_y - imagem.get_height() // 2)
        # Evita desenhar lixo fora da área visível.
        if x + imagem.get_width() < 0 or x > LARGURA or y + imagem.get_height() < 0 or y > ALTURA:
            continue
        # Contorno amarelo para o jogador identificar o item que pode recolher.
        caixa = pygame.Rect(x - 5, y - 5, imagem.get_width() + 10, imagem.get_height() + 10)
        pygame.draw.rect(tela, (255, 214, 70), caixa, 3, border_radius=9)
        tela.blit(imagem, (x, y))
        etiqueta = fonte_pequena.render("LIXO • CLIQUE PARA PEGAR", True, (255, 255, 255))
        etiqueta_rect = etiqueta.get_rect(midbottom=(x + imagem.get_width() // 2, y - 7))
        etiqueta_rect.x = max(5, min(LARGURA - etiqueta_rect.width - 5, etiqueta_rect.x))
        fundo = pygame.Rect(etiqueta_rect.x - 5, etiqueta_rect.y - 3, etiqueta_rect.width + 10, etiqueta_rect.height + 6)
        pygame.draw.rect(tela, (4, 35, 58), fundo, border_radius=6)
        pygame.draw.rect(tela, (255, 214, 70), fundo, 2, border_radius=6)
        tela.blit(etiqueta, etiqueta_rect)



# ==========================================================
# DESENHAR ANIMAIS
# ==========================================================

def desenhar_animais(
    camera_x
):

    for animal in animais:

        x, y = animal["pos"]


        if animal["salva"]:

            imagem = animal["livre"]

        else:

            imagem = animal["presa"]


        ix = (
            x
            -
            camera_x
            -
            imagem.get_width() // 2
        )

        iy = (
            y
            -
            imagem.get_height() // 2
        )


        tela.blit(
            imagem,
            (
                ix,
                iy
            )
        )


        # ==================================================
        # REDE SOBRE O ANIMAL PRESO
        # ==================================================

        if not animal["salva"]:

            rede = pygame.Surface(
                (
                    imagem.get_width(),
                    imagem.get_height()
                ),
                pygame.SRCALPHA
            )

            passo = max(
                15,
                imagem.get_width() // 7
            )


            for n in range(
                -imagem.get_height(),
                imagem.get_width(),
                passo
            ):

                pygame.draw.line(
                    rede,
                    (30,90,65,100),
                    (
                        n,
                        0
                    ),
                    (
                        n
                        +
                        imagem.get_height(),
                        imagem.get_height()
                    ),
                    2
                )


                pygame.draw.line(
                    rede,
                    (30,90,65,100),
                    (
                        n,
                        imagem.get_height()
                    ),
                    (
                        n
                        +
                        imagem.get_height(),
                        0
                    ),
                    2
                )


            tela.blit(
                rede,
                (
                    ix,
                    iy
                )
            )


        # ==================================================
        # NOME
        # ==================================================

        if animal["salva"]:

            sufixo_resgate = " SALVA!" if animal.get("genero") == "f" else " SALVO!"
            texto_nome = animal["nome"] + sufixo_resgate

            cor = (
                80,
                255,
                140
            )

        else:

            texto_nome = (
                "AJUDE "
                +
                animal["nome"]
                +
                "!"
            )

            cor = (
                255,
                255,
                255
            )


        texto = fonte_pequena.render(
            texto_nome,
            True,
            cor
        )


        sombra = fonte_pequena.render(
            texto_nome,
            True,
            (0,0,0)
        )


        tx = (
            x
            -
            camera_x
            -
            texto.get_width() // 2
        )

        ty = (
            iy
            -
            30
        )


        tela.blit(
            sombra,
            (
                tx + 2,
                ty + 2
            )
        )

        tela.blit(
            texto,
            (
                tx,
                ty
            )
        )


# ==========================================================
# HUD FASE 1
# ==========================================================

def hud_fase1(tempo):

    painel = pygame.Surface((LARGURA, 82), pygame.SRCALPHA)
    painel.fill((0, 25, 55, 175))
    tela.blit(painel, (0, 0))

    recolhidos = TOTAL_LIXOS - len(lixos)
    texto = fonte.render(f"Lixo recolhido: {recolhidos}/{TOTAL_LIXOS}", True, (255,255,255))
    tela.blit(texto, (25, 15))

    cor_tempo = (120, 255, 160) if tempo > 20 else (255, 220, 90)
    minutos, segundos = divmod(max(0, int(tempo)), 60)
    texto_tempo = fonte.render(f"Tempo: {minutos:02d}:{segundos:02d}", True, cor_tempo)
    tela.blit(texto_tempo, (LARGURA - texto_tempo.get_width() - 25, 15))

    # Barra de progresso da limpeza
    bx, by, bw, bh = 25, 52, 300, 10
    pygame.draw.rect(tela, (10,55,80), (bx, by, bw, bh), border_radius=5)
    progresso = 0 if TOTAL_LIXOS == 0 else recolhidos / TOTAL_LIXOS
    pygame.draw.rect(tela, (90, 255, 145), (bx, by, int(bw * progresso), bh), border_radius=5)

    dica = fonte_pequena.render("A/D mover • ↑/↓ explorar o fundo • clique no lixo • ↑↑ pular barreiras", True, (225,245,255))
    tela.blit(dica, (LARGURA - dica.get_width() - 25, 52))


# ==========================================================
# HUD FASE 2
# ==========================================================

def hud_fase2(tempo):

    painel = pygame.Surface((LARGURA, 82), pygame.SRCALPHA)
    painel.fill((0, 30, 70, 175))
    tela.blit(painel, (0, 0))

    salvos = sum(1 for animal in animais if animal["salva"])
    texto = fonte.render(f"Animais salvos: {salvos}/{len(animais)}", True, (255,255,255))
    tela.blit(texto, (25, 15))

    cor_tempo = (120, 255, 160) if tempo > 25 else (255, 220, 90)
    minutos, segundos = divmod(max(0, int(tempo)), 60)
    texto_tempo = fonte.render(f"Tempo: {minutos:02d}:{segundos:02d}", True, cor_tempo)
    tela.blit(texto_tempo, (LARGURA - texto_tempo.get_width() - 25, 15))

    # Barra de progresso do resgate
    bx, by, bw, bh = 25, 52, 300, 10
    pygame.draw.rect(tela, (10,55,80), (bx, by, bw, bh), border_radius=5)
    progresso = 0 if not animais else salvos / len(animais)
    pygame.draw.rect(tela, (90, 255, 145), (bx, by, int(bw * progresso), bh), border_radius=5)

    dica = fonte_pequena.render("A/D mover • clique no animal para salvar • ↑↑ ou WW pular", True, (225,245,255))
    tela.blit(dica, (LARGURA - dica.get_width() - 25, 52))


def desenhar_barreiras_fase1(camera_x, camera_y):
    """Fendas fixas que atravessam toda a profundidade do mapa."""
    altura_mundo = ALTURA_MUNDO_FASE1
    for fenda in barreiras_fase1:
        sx = int(fenda.x - camera_x)
        if sx + fenda.width < 0 or sx > LARGURA:
            continue
        w = fenda.width
        camada = pygame.Surface((w, altura_mundo), pygame.SRCALPHA)
        # Bordas irregulares repetidas ao longo de toda a profundidade do mundo.
        borda_esq = [(8, 0)]
        borda_dir = [(w-7, 0)]
        passo = 70
        y = passo
        idx = 0
        while y < altura_mundo:
            borda_esq.append((([24, 12, 31, 10, 25, 7, 22][idx % 7]), y))
            borda_dir.append((w-([24, 10, 29, 12, 27, 9, 21][idx % 7]), y))
            y += passo
            idx += 1
        borda_esq.append((5, altura_mundo))
        borda_dir.append((w-5, altura_mundo))
        pygame.draw.polygon(camada, (18, 38, 47), borda_esq + list(reversed(borda_dir)))
        centro = [(27, 0), (w-24, 0)]
        centro.extend(borda_dir[1:-1])
        centro.extend([(w-27, altura_mundo), (26, altura_mundo)])
        centro.extend(reversed(borda_esq[1:-1]))
        pygame.draw.polygon(camada, (0, 3, 10), centro)
        pygame.draw.lines(camada, (53, 101, 112), False, borda_esq, 3)
        pygame.draw.lines(camada, (35, 73, 88), False, borda_dir, 3)
        tela.blit(camada, (sx, -int(camera_y)))


# ==========================================================
# DESENHAR FASE 1
# ==========================================================

def desenhar_fase1():

    tela.blit(
        fase1_mapa,
        (-int(camera_x_fase1), -int(camera_y_fase1))
    )

    desenhar_lixos(camera_x_fase1, camera_y_fase1)
    desenhar_barreiras_fase1(camera_x_fase1, camera_y_fase1)
    desenhar_personagem(camera_x_fase1, camera_y_fase1)


    passado = (
        pygame.time.get_ticks()
        -
        tempo_inicio
    ) // 1000


    hud_fase1(
        max(
            0,
            TEMPO_FASE1
            -
            passado
        )
    )


# ==========================================================
# DESENHAR FASE 2
# ==========================================================

def desenhar_fase2():

    tela.blit(
        fase2_mapa,
        (
            -int(camera_x_fase2),
            0
        )
    )


    desenhar_animais(
        camera_x_fase2
    )


    desenhar_personagem(
        camera_x_fase2
    )


    passado = (
        pygame.time.get_ticks()
        -
        tempo_fase2
    ) // 1000


    hud_fase2(
        max(
            0,
            TEMPO_FASE2
            -
            passado
        )
    )


# ==========================================================
# CARTÃO PADRÃO PARA TODAS AS TELAS COM TEXTO/TRANSIÇÃO
# ==========================================================
def desenhar_cartao_transicao(titulo_texto, linhas, botao, texto_botao, cor_botao=(30, 170, 220), fundo=None):
    """Cartão de introdução/conclusão com personagem grande e texto mais próximo."""
    mostrar_imagem_centralizada(fundo if fundo is not None else fase2_original)

    sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    sombra.fill((0, 24, 48, 172))
    tela.blit(sombra, (0, 0))

    painel = pygame.Rect(25, 25, 950, 485)
    pygame.draw.rect(tela, (4, 42, 70), painel, border_radius=23)
    pygame.draw.rect(tela, (95, 215, 235), painel, 3, border_radius=23)

    # O personagem fica à esquerda e usa a arte original em alta resolução.
    personagem = personagem_cartao_menina if personagem_escolhido == "menina" else personagem_cartao_menino
    altura_heroi = 305
    fator = altura_heroi / max(1, personagem.get_height())
    heroi = pygame.transform.smoothscale(
        personagem,
        (max(1, round(personagem.get_width() * fator)), altura_heroi)
    )
    heroi_rect = heroi.get_rect(midbottom=(145, 470))
    tela.blit(heroi, heroi_rect)

    # Título e explicação ficam na coluna ao lado do personagem; o texto não é
    # centralizado no meio da tela. A quebra de linhas respeita a largura útil.
    x_texto = 255
    largura_texto = 690
    fonte_titulo_cartao = pygame.font.SysFont("arial", 46, bold=True)
    titulo = fonte_titulo_cartao.render(titulo_texto, True, (255, 255, 255))
    limite_titulo = LARGURA - x_texto - 35
    if titulo.get_width() > limite_titulo:
        escala_titulo = limite_titulo / titulo.get_width()
        titulo = pygame.transform.smoothscale(
            titulo,
            (limite_titulo, max(1, round(titulo.get_height() * escala_titulo)))
        )
    titulo_rect = titulo.get_rect(topleft=(x_texto, 58))
    tela.blit(titulo, titulo_rect)

    fonte_texto_cartao = pygame.font.SysFont("arial", 24, bold=True)
    grupos = []
    for indice, paragrafo in enumerate(linhas):
        palavras = paragrafo.split()
        linha_atual = ""
        linhas_quebradas = []
        for palavra in palavras:
            tentativa = (linha_atual + " " + palavra).strip()
            if linha_atual and fonte_texto_cartao.size(tentativa)[0] > largura_texto:
                linhas_quebradas.append(linha_atual)
                linha_atual = palavra
            else:
                linha_atual = tentativa
        if linha_atual:
            linhas_quebradas.append(linha_atual)
        for linha in linhas_quebradas:
            cor = (255, 222, 135) if indice == 0 else (245, 252, 255)
            grupos.append((linha, cor))
        if indice < len(linhas) - 1:
            grupos.append((None, None))

    # A posição vertical é calculada para manter todo o texto acima do botão.
    altura_linha = 30
    altura_separacao = 5
    total_altura = sum(altura_separacao if texto_linha is None else altura_linha
                       for texto_linha, _cor in grupos)
    inicio_minimo = titulo_rect.bottom + 15
    y = max(inicio_minimo, min(145, 144 - max(0, total_altura - 210) // 2))
    limite_inferior_texto = botao.top - 14
    for indice, (texto_linha, cor) in enumerate(grupos):
        if texto_linha is None:
            y += altura_separacao
            continue
        texto_renderizado = fonte_texto_cartao.render(texto_linha, True, cor)
        # Alinhamento à esquerda: a explicação começa perto do personagem.
        tela.blit(texto_renderizado, (x_texto, y))
        y += altura_linha

    pygame.draw.rect(tela, cor_botao, botao, border_radius=18)
    pygame.draw.rect(tela, (120, 235, 245), botao, 2, border_radius=18)
    rotulo = fonte.render(texto_botao, True, (255, 255, 255))
    if rotulo.get_width() > botao.width - 20:
        escala = (botao.width - 20) / rotulo.get_width()
        rotulo = pygame.transform.smoothscale(
            rotulo,
            (botao.width - 20, max(1, round(rotulo.get_height() * escala)))
        )
    tela.blit(rotulo, rotulo.get_rect(center=botao.center))


# ==========================================================
# TRANSIÇÃO FASE 2
# ==========================================================

def desenhar_inicio_fase2():
    desenhar_cartao_transicao(
        "FASE 1 CONCLUÍDA!",
        [
            "Você retirou o lixo do mar!",
            "Plásticos, latas e outros resíduos podem ferir os animais.",
            "Agora você vai descobrir como a poluição ameaça a vida marinha.",
            "Na próxima missão, ajude a salvar os animais afetados."
        ],
        botao_fase2,
        "JOGAR FASE 2"
    )


# ==========================================================
# VITÓRIA FASE 2
# ==========================================================

def desenhar_vitoria():
    desenhar_cartao_transicao(
        "FASE 2 CONCLUÍDA!",
        [
            "Você ajudou os animais marinhos!",
            "O lixo pode prender os animais, feri-los ou ser engolido.",
            "Reduzir, reutilizar e reciclar evita que mais resíduos cheguem ao mar.",
            "Agora vamos aprender a combater a poluição!"
        ],
        botao_fase3,
        "JOGAR FASE 3"
    )


# ==========================================================
# FASE 3
# ==========================================================

def desenhar_palavras_encontradas_verdes():
    # A arte da Fase 3 já traz a lista de palavras em branco.
    # Quando uma palavra é encontrada, cobrimos somente a área da palavra
    # e redesenhamos em verde para deixar o resultado bem visível.
    colunas = [0, 1]
    y_inicial = 160
    espacamento = 48
    x_palavra = [530, 765]

    for indice, palavra in enumerate(palavras_fase3):
        if palavra not in palavras_encontradas_fase3:
            continue

        coluna = colunas[indice % 2]
        linha = indice // 2
        x = x_palavra[coluna]
        y = y_inicial + linha * espacamento

        texto = fonte_lista_fase3.render(
            palavra, True, (65, 215, 105)
        )

        # Limpa o texto branco original sem cobrir o restante do painel.
        fundo = pygame.Rect(
            x - 3,
            y - 2,
            texto.get_width() + 8,
            texto.get_height() + 5
        )
        pygame.draw.rect(
            tela,
            (7, 43, 73),
            fundo,
            border_radius=2
        )

        tela.blit(texto, (x, y))


def desenhar_fase3():

    mostrar_imagem_centralizada(
        fase3_fundo
    )


    passado = (
        pygame.time.get_ticks()
        -
        tempo_fase3
    ) // 1000


    tempo = max(
        0,
        TEMPO_FASE3
        -
        passado
    )


    painel = pygame.Surface(
        (
            LARGURA,
            88
        ),
        pygame.SRCALPHA
    )

    # Faixa quase opaca esconde o título que já vem impresso no fundo,
    # evitando que ele fique por trás do contador e do tempo.
    painel.fill(
        (0,25,50,248)
    )

    tela.blit(
        painel,
        (0,0)
    )


    texto = fonte.render(
        f"Palavras encontradas: "
        f"{len(palavras_encontradas_fase3)}/14",
        True,
        (255,255,255)
    )


    tela.blit(
        texto,
        (25,20)
    )


    minutos, segundos = divmod(max(0, int(tempo)), 60)
    texto_tempo = fonte.render(
        f"Tempo: {minutos:02d}:{segundos:02d}",
        True,
        (255,255,255)
    )


    tela.blit(
        texto_tempo,
        (
            LARGURA
            -
            texto_tempo.get_width()
            -
            25,
            20
        )
    )


    camada_linhas_verdes = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    for palavra in palavras_encontradas_fase3:

        if (
            palavra
            not in
            posicoes_palavras_fase3
        ):

            continue


        l1,c1,l2,c2 = (
            posicoes_palavras_fase3[
                palavra
            ]
        )


        pygame.draw.line(
            camada_linhas_verdes,
            (48,190,92,165),

            (
                POS_X_GRADE
                +
                c1*TAMANHO_CELULA_W
                +
                TAMANHO_CELULA_W//2,

                POS_Y_GRADE
                +
                l1*TAMANHO_CELULA_H
                +
                TAMANHO_CELULA_H//2
            ),

            (
                POS_X_GRADE
                +
                c2*TAMANHO_CELULA_W
                +
                TAMANHO_CELULA_W//2,

                POS_Y_GRADE
                +
                l2*TAMANHO_CELULA_H
                +
                TAMANHO_CELULA_H//2
            ),

            6
        )

    tela.blit(camada_linhas_verdes, (0,0))

    if (
        selecionando_fase3
        and
        inicio_selecao_fase3
        and
        selecao_atual_fase3
    ):

        l1,c1 = (
            inicio_selecao_fase3
        )

        l2,c2 = (
            selecao_atual_fase3
        )


        if (
            l1 == l2
            or
            c1 == c2
            or
            abs(l2-l1)
            ==
            abs(c2-c1)
        ):

            pygame.draw.line(
                tela,
                (90,225,130),

                (
                    POS_X_GRADE
                    +
                    c1*TAMANHO_CELULA_W
                    +
                    TAMANHO_CELULA_W//2,

                    POS_Y_GRADE
                    +
                    l1*TAMANHO_CELULA_H
                    +
                    TAMANHO_CELULA_H//2
                ),

                (
                    POS_X_GRADE
                    +
                    c2*TAMANHO_CELULA_W
                    +
                    TAMANHO_CELULA_W//2,

                    POS_Y_GRADE
                    +
                    l2*TAMANHO_CELULA_H
                    +
                    TAMANHO_CELULA_H//2
                ),

                4
            )


    desenhar_palavras_encontradas_verdes()

# ==========================================================
# VITÓRIA FASE 3
# ==========================================================

def desenhar_vitoria_fase3():
    desenhar_cartao_transicao(
        "FASE 3 CONCLUÍDA!",
        [
            "Você encontrou todas as palavras!",
            "Reduzir o consumo, reutilizar objetos e reciclar diminui a poluição.",
            "Os corais oferecem abrigo e alimento para muitas espécies.",
            "Agora ajude a recuperar os corais ameaçados pelo aquecimento."
        ],
        botao_fase4,
        "JOGAR FASE 4",
        (35, 165, 120)
    )



# ==========================================================
# DERROTA
# ==========================================================

def desenhar_derrota():
    tela.fill((8, 35, 58))
    pygame.draw.rect(tela, (4, 49, 76), (48, 70, 904, 430), border_radius=22)
    pygame.draw.rect(tela, (75, 205, 225), (48, 70, 904, 430), 3, border_radius=22)

    if motivo_derrota == "fase1_tempo":
        titulo_txt = "TEMPO ESGOTADO!"
        linhas = [
            "Você não conseguiu recolher todo o lixo do mar.",
            "Tente mais uma vez e ajude a limpar o oceano!",
            "Escolha tentar novamente ou voltar ao início."
        ]
    elif motivo_derrota == "fase2_tempo":
        titulo_txt = "TEMPO ESGOTADO!"
        linhas = [
            "Nem todos os animais marinhos foram salvos.",
            "Tente novamente e ajude nossos amigos do oceano!",
            "Escolha tentar novamente ou voltar ao início."
        ]
    elif motivo_derrota == "fase3_tempo":
        titulo_txt = "TEMPO ESGOTADO!"
        linhas = [
            "Você ainda não encontrou todas as palavras.",
            "Tente mais uma vez e descubra como proteger o oceano!",
            "Escolha tentar novamente ou voltar ao início."
        ]
    elif motivo_derrota == "fase4_tempo":
        titulo_txt = "TEMPO ESGOTADO!"
        linhas = [
            f"Você recuperou {len(corais_resgatados)} dos 6 corais.",
            "Tente novamente para ajudar a recuperar os recifes!",
            "Escolha tentar novamente ou voltar ao início."
        ]
    elif motivo_derrota == "fase5_pontuacao":
        titulo_txt = "MISSÃO FINAL NÃO CONCLUÍDA"
        linhas = [
            f"Você acertou {fase5_acertos} de 5 perguntas.",
            "É preciso acertar pelo menos 3 para concluir a fase.",
            "Tente novamente ou volte ao início do jogo."
        ]
    elif motivo_derrota == "fase5_tempo":
        titulo_txt = "TEMPO ESGOTADO!"
        linhas = [
            f"Você respondeu corretamente a {fase5_acertos} de 5 perguntas até agora.",
            "Tente novamente para combater a acidificação dos oceanos!",
            "Escolha tentar novamente ou voltar ao início."
        ]
    else:
        titulo_txt = "TEMPO ESGOTADO!"
        linhas = [
            "O tempo da missão acabou.",
            "Tente novamente para proteger a vida marinha!",
            "Escolha tentar novamente ou voltar ao início."
        ]

    titulo = fonte_grande.render(titulo_txt, True, (255, 255, 255))
    if titulo.get_width() > 840:
        titulo = pygame.transform.smoothscale(titulo, (840, titulo.get_height()))
    tela.blit(titulo, titulo.get_rect(center=(LARGURA//2, 145)))

    for i, linha in enumerate(linhas):
        texto = fonte.render(linha, True, (225, 245, 250))
        if texto.get_width() > 820:
            texto = pygame.transform.smoothscale(texto, (820, texto.get_height()))
        tela.blit(texto, texto.get_rect(center=(LARGURA//2, 225 + i*38)))

    pygame.draw.rect(tela, (30, 150, 220), botao_derrota_tentar, border_radius=14)
    pygame.draw.rect(tela, (20, 105, 130), botao_derrota_inicio, border_radius=14)
    for label, rect in [("TENTAR NOVAMENTE", botao_derrota_tentar), ("VOLTAR AO INÍCIO", botao_derrota_inicio)]:
        texto = fonte_pequena.render(label, True, (255, 255, 255))
        tela.blit(texto, texto.get_rect(center=rect.center))



# ==========================================================
# COMO JOGAR — instruções simples para crianças, com miniaturas
# ==========================================================
def desenhar_como_jogar():
    tela.fill((5, 35, 58))
    pygame.draw.rect(tela, (4, 49, 76), (26, 18, 948, 526), border_radius=22)
    pygame.draw.rect(tela, (75, 205, 225), (26, 18, 948, 526), 3, border_radius=22)
    titulo = fonte_grande.render("COMO JOGAR", True, (255, 255, 255))
    tela.blit(titulo, titulo.get_rect(center=(LARGURA//2, 52)))
    subtitulo = fonte_pequena.render("Complete as cinco missões para ajudar a proteger o oceano!", True, (155, 235, 245))
    tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA//2, 82)))

    instrucoes = [
        ("FASE 1 — LIMPAR O MAR", "Use A/D para se mover, as setas para explorar e clique no lixo quando estiver perto.", fase1_original),
        ("FASE 2 — SALVAR OS ANIMAIS", "Chegue perto dos animais presos e clique neles para ajudar a soltá-los.", fase2_original),
        ("FASE 3 — CAÇA-PALAVRAS", "Encontre todas as palavras na grade: clique na primeira letra e arraste até a última.", fase3_fundo),
        ("FASE 4 — SALVAR OS CORAIS", "Clique nos corais para responder às perguntas e recuperar o recife.", fase4_original),
        ("FASE 5 — PROTEGER O OCEANO", "Leia cada pergunta e escolha a resposta correta antes que o tempo acabe.", fase5_fundo),
    ]
    for i, (titulo_fase, descricao, miniatura) in enumerate(instrucoes):
        y = 101 + i*72
        pygame.draw.rect(tela, (8, 68, 91), (52, y, 896, 64), border_radius=10)
        pygame.draw.rect(tela, (47, 170, 195), (52, y, 896, 64), 1, border_radius=10)
        thumb = pygame.transform.smoothscale(miniatura, (100, 56))
        tela.blit(thumb, (58, y+4))
        cab = fonte_pequena.render(titulo_fase, True, (255, 220, 95))
        tela.blit(cab, (172, y+6))
        # Quebra de linha controlada para manter a leitura confortável.
        if i == 0:
            partes = ["Use A/D para se mover, as setas para explorar e clique no lixo", "quando estiver perto para recolhê-lo. Pule as fendas!" ]
        elif i == 1:
            partes = ["Chegue perto dos animais presos e clique neles", "para ajudar a soltá-los." ]
        elif i == 2:
            partes = ["Encontre todas as palavras na grade: clique na primeira letra", "e arraste até a última letra da palavra." ]
        elif i == 3:
            partes = ["Clique nos corais para responder às perguntas", "e recuperar o recife." ]
        else:
            partes = ["Leia cada pergunta e escolha a resposta correta", "antes que o tempo acabe. Acerte pelo menos 3 de 5!" ]
        for j, parte in enumerate(partes):
            txt = pygame.font.SysFont("arial", 15, bold=True).render(parte, True, (235, 248, 250))
            tela.blit(txt, (172, y+29+j*17))

    pygame.draw.rect(tela, (25, 150, 190), botao_como_jogar_voltar, border_radius=12)
    texto = fonte_pequena.render("VOLTAR AO MENU", True, (255, 255, 255))
    tela.blit(texto, texto.get_rect(center=botao_como_jogar_voltar.center))


# ==========================================================
# LOOP
# ==========================================================

rodando = True


while rodando:

    for evento in pygame.event.get():


        if evento.type == pygame.QUIT:
            rodando = False

        # Eventos de toque (Android/iOS). O analógico fica no canto inferior
        # esquerdo; o botão PULAR no canto inferior direito. Outros toques
        # simulam clique para que os botões e objetos existentes funcionem.
        if evento.type == getattr(pygame, "FINGERDOWN", -100):
            pos_logica = (int(evento.x * LARGURA), int(evento.y * ALTURA))
            fase_com_movimento = estado in ("fase1", "fase2", "fase4")
            if fase_com_movimento and math.hypot(pos_logica[0]-ANALOGICO_CENTRO[0], pos_logica[1]-ANALOGICO_CENTRO[1]) <= ANALOGICO_RAIO + 22:
                touch_analogico_id = evento.finger_id
                atualizar_analogico(pos_logica)
                continue
            if estado in ("fase1", "fase2") and BOTAO_PULO.collidepoint(pos_logica):
                touch_pulo_id = evento.finger_id
                if not pulando:
                    pulando = True
                    inicio_pulo = pygame.time.get_ticks()
                continue
            pos_janela = (int(pos_logica[0] * janela.get_width() / LARGURA), int(pos_logica[1] * janela.get_height() / ALTURA))
            evento = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos_janela, "button": 1})

        elif evento.type == getattr(pygame, "FINGERMOTION", -101):
            if touch_analogico_id == evento.finger_id:
                atualizar_analogico((int(evento.x * LARGURA), int(evento.y * ALTURA)))
                continue

        elif evento.type == getattr(pygame, "FINGERUP", -102):
            if touch_analogico_id == evento.finger_id:
                touch_analogico_id = None
                analogico_x = analogico_y = 0.0
                continue
            if touch_pulo_id == evento.finger_id:
                touch_pulo_id = None
                continue

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            rodando = False

        # ==================================================
        # DUPLO TOQUE PARA PULAR
        # ==================================================
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_UP, pygame.K_w) and estado in ("fase1", "fase2", "fase4"):
                agora = pygame.time.get_ticks()
                if (agora - ultimo_toque_cima <= JANELA_DUPLO_TOQUE
                        and agora - ULTIMO_PULO >= COOLDOWN_PULO
                        and not pulando):
                    pulando = True
                    inicio_pulo = agora
                    ULTIMO_PULO = agora
                    ultimo_toque_cima = 0
                else:
                    ultimo_toque_cima = agora


        # ==================================================
        # CLIQUE
        # ==================================================

        if evento.type == pygame.MOUSEBUTTONDOWN:

            mouse = converter_mouse(evento.pos)


            if estado == "capa":

                if botao_jogar.collidepoint(mouse):
                    estado = "personagens"
                elif botao_como_jogar.collidepoint(mouse):
                    estado = "como_jogar"

            elif estado == "como_jogar":
                if botao_como_jogar_voltar.collidepoint(mouse):
                    estado = "capa"


            elif estado == "personagens":

                if botao_menino.collidepoint(
                    mouse
                ):

                    personagem_escolhido = (
                        "menino"
                    )

                    estado = "intro1"


                elif botao_menina.collidepoint(
                    mouse
                ):

                    personagem_escolhido = (
                        "menina"
                    )

                    estado = "intro1"


                elif botao_voltar.collidepoint(
                    mouse
                ):

                    estado = "capa"


            elif estado == "intro1":
                if botao_intro1.collidepoint(mouse):
                    iniciar_fase1()
                    estado = "fase1"

            elif estado == "fase1":
                # A coleta acontece ao clicar/tocar diretamente no lixo.
                mundo_x = mouse[0] + camera_x_fase1
                mundo_y = mouse[1] + camera_y_fase1
                for lixo in lixos[:]:
                    perto_do_lixo = (
                        abs(jogador.centerx - lixo["rect"].centerx) <= 150
                        and abs(jogador.centery - lixo["rect"].centery) <= 145
                    )
                    if perto_do_lixo and lixo["rect"].inflate(40, 40).collidepoint(mundo_x, mundo_y):
                        lixos.remove(lixo)
                        break

            elif estado == "fase2":
                # O animal só é salvo quando o jogador clica/toca nele.
                mundo_x = mouse[0] + camera_x_fase2
                mundo_y = mouse[1]
                for animal in animais:
                    if animal["salva"]:
                        continue
                    ax, ay = animal["pos"]
                    hitbox = pygame.Rect(ax - 85, ay - 85, 170, 170)
                    perto_do_animal = (
                        abs(jogador.centerx - ax) <= 190
                        and abs(jogador.centery - ay) <= 165
                    )
                    if perto_do_animal and hitbox.collidepoint(mundo_x, mundo_y):
                        animal["salva"] = True
                        break

            elif estado == "fase2_inicio":

                if botao_fase2.collidepoint(
                    mouse
                ):

                    iniciar_fase2()

                    estado = "fase2"


            elif estado == "vitoria":

                if botao_fase3.collidepoint(mouse):
                    iniciar_fase3()
                    estado = "fase3"

            elif estado == "vitoria_fase3":
                if botao_fase4.collidepoint(mouse):
                    iniciar_fase4()
                    estado = "fase4"

            elif estado == "vitoria_fase4":
                if botao_fase5.collidepoint(mouse):
                    estado = "intro5"

            elif estado == "falha_fase4":
                if botao_tentar.collidepoint(mouse):
                    iniciar_fase4()
                    estado = "fase4"

            elif estado == "intro5":
                if botao_intro_fase5.collidepoint(mouse):
                    iniciar_fase5()
                    estado = "fase5"

            elif estado == "derrota":
                if botao_derrota_tentar.collidepoint(mouse):
                    if motivo_derrota == "fase1_tempo":
                        iniciar_fase1()
                        estado = "fase1"
                    elif motivo_derrota == "fase2_tempo":
                        iniciar_fase2()
                        estado = "fase2"
                    elif motivo_derrota == "fase3_tempo":
                        iniciar_fase3()
                        estado = "fase3"
                    elif motivo_derrota == "fase4_tempo":
                        iniciar_fase4()
                        estado = "fase4"
                    else:
                        iniciar_fase5()
                        estado = "fase5"
                elif botao_derrota_inicio.collidepoint(mouse):
                    musica.stop()
                    som_mar.stop()
                    estado = "capa"

            elif estado == "fase5":
                if fase5_feedback:
                    if botao_feedback_fase5.collidepoint(mouse):
                        fase5_indice += 1
                        fase5_feedback = ""
                        fase5_feedback_correto = False
                        if fase5_indice >= len(perguntas_fase5):
                            musica.stop()
                            if fase5_acertos >= 3:
                                estado = "vitoria_fase5"
                            else:
                                global_motivo = "fase5_pontuacao"
                                motivo_derrota = global_motivo
                                estado = "derrota"
                else:
                    q = perguntas_fase5[fase5_indice]
                    for i, rect in enumerate(fase5_opcoes_rects):
                        if rect.collidepoint(mouse):
                            if i == q["correta"]:
                                fase5_acertos += 1
                                fase5_feedback = "Resposta correta! " + q["explicacao"]
                                fase5_feedback_correto = True
                            else:
                                fase5_feedback = "Resposta incorreta. " + q["explicacao"]
                                fase5_feedback_correto = False
                            break

            elif estado == "vitoria_fase5":
                if botao_fase5.collidepoint(mouse):
                    estado = "capa"

            elif estado == "fase4":
                if pergunta_coral_ativa and coral_selecionado is not None:
                    q=perguntas_coral[coral_selecionado]
                    for i in range(3):
                        r=pygame.Rect(125,250+i*58,750,45)
                        if r.collidepoint(mouse):
                            if i == q["correta"]:
                                corais_resgatados.add(coral_selecionado)
                                pontos_fase4 += 125
                                temperatura_fase4=max(24.0,temperatura_fase4-2.0)
                                resposta_feedback="Correto! Coral recuperado!"
                            else:
                                temperatura_fase4=min(45.0,temperatura_fase4+3.0)
                                vidas_fase4=max(0,vidas_fase4-1)
                                corais_falhados.add(coral_selecionado)
                                resposta_feedback="Você errou! Este coral continuará esbranquiçado."
                            feedback_ate=pygame.time.get_ticks()+2800
                            pergunta_coral_ativa=False
                            coral_selecionado=None
                            break
                else:
                    mx,my=mouse
                    mundo_x=mx+camera_x_fase2
                    for coral in corais_fase4:
                        if coral["id"] in corais_resgatados or coral["id"] in corais_falhados:
                            continue
                        if abs(mundo_x-coral["x"])<95 and abs(my-coral["y"])<105 and abs(jogador.centerx-coral["x"])<190 and abs(jogador.centery-coral["y"])<160:
                            coral["cliques"] += 1
                            if coral["cliques"]>=3:
                                coral_selecionado=coral["id"]
                                pergunta_coral_ativa=True
                            break

            elif estado == "fase3":

                inicio = celula_fase3(
                    mouse
                )


                if inicio is not None:

                    selecionando_fase3 = True

                    inicio_selecao_fase3 = (
                        inicio
                    )

                    selecao_atual_fase3 = (
                        inicio
                    )


        # ==================================================
        # MOUSE MOVENDO
        # ==================================================

        if evento.type == pygame.MOUSEMOTION:

            if (
                estado == "fase3"
                and
                selecionando_fase3
            ):

                celula = celula_fase3(
                    converter_mouse(evento.pos)
                )

                if celula is not None:

                    selecao_atual_fase3 = (
                        celula
                    )


        # ==================================================
        # MOUSE SOLTO
        # ==================================================

        if evento.type == pygame.MOUSEBUTTONUP:

            if (
                evento.button == 1
                and
                estado == "fase3"
                and
                selecionando_fase3
            ):

                fim = celula_fase3(
                    converter_mouse(evento.pos)
                )


                if fim is not None:

                    palavra = (
                        verificar_selecao_fase3(
                            inicio_selecao_fase3,
                            fim
                        )
                    )


                    if palavra:

                        palavras_encontradas_fase3.add(
                            palavra
                        )


                selecionando_fase3 = False

                inicio_selecao_fase3 = None

                selecao_atual_fase3 = None


    # ======================================================
    # MOVIMENTO
    # ======================================================

    if estado in (
        "fase1",
        "fase2",
        "fase4"
    ):

        teclas = pygame.key.get_pressed()

        dx = 0
        dy = 0

        personagem_movendo = False


        if (
            teclas[pygame.K_LEFT]
            or
            teclas[pygame.K_a]
        ):

            dx -= velocidade

            personagem_movendo = True

            direcao = "esquerda"


        if (
            teclas[pygame.K_RIGHT]
            or
            teclas[pygame.K_d]
        ):

            dx += velocidade

            personagem_movendo = True

            direcao = "direita"


        if (
            teclas[pygame.K_UP]
            or
            teclas[pygame.K_w]
        ):

            if not pulando:
                dy -= velocidade

            personagem_movendo = True


        if (
            teclas[pygame.K_DOWN]
            or
            teclas[pygame.K_s]
        ):

            dy += velocidade

            personagem_movendo = True


        # Movimento analógico contínuo para telas sensíveis ao toque.
        if touch_analogico_id is not None:
            dx += analogico_x * velocidade
            dy += analogico_y * velocidade
            if abs(analogico_x) > 0.08 or abs(analogico_y) > 0.08:
                personagem_movendo = True
                if analogico_x < -0.08:
                    direcao = "esquerda"
                elif analogico_x > 0.08:
                    direcao = "direita"

        if dx != 0 and dy != 0:

            fator = (
                1
                /
                math.sqrt(2)
            )

            dx *= fator
            dy *= fator


        old_x, old_y = jogador.x, jogador.y
        jogador.x += int(dx)
        jogador.y += int(dy)

        # As fendas atravessam a profundidade inteira. Sem pulo, o jogador
        # não consegue entrar nelas nem contorná-las descendo/subindo.
        if estado == "fase1" and not pulando:
            if any(fenda.colliderect(jogador) for fenda in barreiras_fase1):
                jogador.x, jogador.y = old_x, old_y

        # ==================================================
        # LIMITES FASE 1
        # ==================================================

        if estado == "fase1":

            jogador.left = max(
                20,
                jogador.left
            )

            jogador.right = min(
                LARGURA_MUNDO_FASE1 - 20,
                jogador.right
            )

            jogador.top = max(70, jogador.top)
            jogador.bottom = min(ALTURA_MUNDO_FASE1 - 20, jogador.bottom)

            camera_y_fase1 = max(
                0,
                min(
                    ALTURA_MUNDO_FASE1 - ALTURA,
                    jogador.centery - ALTURA // 2
                )
            )

            camera_x_fase1 = max(
                0,
                min(
                    LARGURA_MUNDO_FASE1
                    -
                    LARGURA,

                    jogador.centerx
                    -
                    LARGURA//2
                )
            )


        # ==================================================
        # LIMITES FASE 2
        # ==================================================

        else:

            jogador.left = max(
                20,
                jogador.left
            )

            jogador.right = min(
                LARGURA_MUNDO_FASE2 - 20,
                jogador.right
            )

            jogador.top = max(
                80,
                jogador.top
            )

            jogador.bottom = min(
                ALTURA - 25,
                jogador.bottom
            )


            camera_x_fase2 = max(
                0,
                min(
                    LARGURA_MUNDO_FASE2
                    -
                    LARGURA,

                    jogador.centerx
                    -
                    LARGURA//2
                )
            )


    # ======================================================
    # FASE 1
    # ======================================================

    if estado == "fase1":

        # O lixo agora só é recolhido por clique/toque direto no objeto.
        passado = (
            pygame.time.get_ticks()
            -
            tempo_inicio
        ) // 1000


        if not lixos:

            musica.stop()

            estado = "fase2_inicio"


        elif passado >= TEMPO_FASE1:

            musica.stop()
            motivo_derrota = "fase1_tempo"
            estado = "derrota"


    # ======================================================
    # FASE 2
    # ======================================================

    if estado == "fase2":

        # Os animais agora só são salvos ao clicar/tocar neles.
        salvos = sum(
            1
            for animal in animais
            if animal["salva"]
        )


        passado = (
            pygame.time.get_ticks()
            -
            tempo_fase2
        ) // 1000


        if salvos == len(animais):

            musica.stop()

            estado = "vitoria"


        elif passado >= TEMPO_FASE2:

            musica.stop()
            motivo_derrota = "fase2_tempo"
            estado = "derrota"


    # ======================================================
    # FASE 3
    # ======================================================

    if estado == "fase3":

        passado = (
            pygame.time.get_ticks()
            -
            tempo_fase3
        ) // 1000


        if (
            len(
                palavras_encontradas_fase3
            )
            ==
            len(
                palavras_fase3
            )
        ):

            musica.stop()

            estado = "vitoria_fase3"


        elif passado >= TEMPO_FASE3:

            musica.stop()
            motivo_derrota = "fase3_tempo"
            estado = "derrota"


    # ======================================================
    # FASE 4 — TEMPERATURA E CONDIÇÕES DE VITÓRIA/DERROTA
    # ======================================================
    if estado == "fase4":
        agora4=pygame.time.get_ticks()
        passado4=(agora4-tempo_fase4)//1000
        if agora4-ultimo_aumento_temp >= 1000:
            passos=(agora4-ultimo_aumento_temp)//1000
            temperatura_fase4=min(45.0,temperatura_fase4+passos*0.07)
            ultimo_aumento_temp += passos*1000
        avaliados4 = corais_resgatados | corais_falhados
        if len(avaliados4) == 6:
            musica.stop()
            if len(corais_resgatados) >= 4:
                estado = "vitoria_fase4"
            else:
                estado = "falha_fase4"
        elif vidas_fase4 <= 0 or passado4>=TEMPO_FASE4 or temperatura_fase4>=45.0:
            musica.stop()
            motivo_derrota = "fase4_tempo"
            estado="derrota"

    # FASE 5 — limite de tempo para concluir os desafios.
    if estado == "fase5":
        passado5 = (pygame.time.get_ticks()-inicio_fase5)//1000
        if passado5 >= TEMPO_FASE5:
            musica.stop()
            motivo_derrota = "fase5_tempo"
            estado = "derrota"

    # ======================================================
    # DESENHAR
    # ======================================================

    if estado == "capa":

        mostrar_imagem_centralizada(
            capa
        )


    elif estado == "personagens":

        desenhar_selecao_personagem()

    elif estado == "como_jogar":
        desenhar_como_jogar()

    elif estado == "intro1":
        desenhar_intro_fase1()

    elif estado == "fase1":

        desenhar_fase1()


    elif estado == "fase2_inicio":

        desenhar_inicio_fase2()


    elif estado == "fase2":

        desenhar_fase2()


    elif estado == "vitoria":

        desenhar_vitoria()


    elif estado == "fase3":

        desenhar_fase3()


    elif estado == "vitoria_fase3":

        desenhar_vitoria_fase3()

    elif estado == "fase4":
        desenhar_fase4()

    elif estado == "falha_fase4":
        desenhar_cartao_transicao(
            "MISSÃO DOS CORAIS NÃO CONCLUÍDA",
            [
                f"Você recuperou {len(corais_resgatados)} dos 6 corais.",
                "Você precisa recuperar pelo menos 4 corais para avançar.",
                "Tente novamente e responda aos desafios com atenção."
            ],
            botao_tentar,
            "TENTAR NOVAMENTE",
            (190, 95, 55)
        )

    elif estado == "vitoria_fase4":
        desenhar_cartao_transicao(
            "FASE 4 CONCLUÍDA!",
            [
                f"Você recuperou {len(corais_resgatados)} dos 6 corais!",
                "O aquecimento e a acidificação ameaçam os recifes e seus habitantes.",
                "A recuperação dos ecossistemas pode levar anos ou décadas.",
                "Prepare-se para a missão final: O Último Suspiro do Oceano."
            ],
            botao_fase5,
            "JOGAR FASE 5",
            (25, 155, 110)
        )

    elif estado == "intro5":
        desenhar_intro_fase5()

    elif estado == "fase5":
        desenhar_fase5()

    elif estado == "vitoria_fase5":
        desenhar_vitoria_fase5()

    elif estado == "derrota":

        desenhar_derrota()


    # Controles virtuais desenhados por cima da cena para celulares.
    desenhar_controles_tateis()

    # Amplia a imagem final para a resolução do monitor, sem esticar a lógica do jogo.
    tamanho_atual = janela.get_size()
    if tamanho_atual != (LARGURA, ALTURA):
        quadro = pygame.transform.smoothscale(tela, tamanho_atual)
    else:
        quadro = tela
    janela.blit(quadro, (0, 0))
    pygame.display.flip()

    relogio.tick(60)


# ==========================================================
# ENCERRAR
# ==========================================================

musica.stop()

som_mar.stop()

pygame.quit()