import pygame
import math
pygame.init()

LARGURA, ALTURA = 800, 800
JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação de Planetas")  # titulo

branco = (255, 255, 255)
amarelo = (255, 255, 0)
azul = (100, 149, 237)
vermelho = (188,39,50)
cinza_escuro = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)
class Planeta:
    AU = 149.6e6 * 1000  #medindo distancia
    G = 6.67428e-11  #gravidade
    ESCALA = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 dia


    def __init__(self, x, y, raio, cor, massa):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.massa = massa
        
        self.orbita = []
        self.sol = False
        self.distancia_do_sol = 0

        self.x_vel = 0
        self.y_vel = 0

    def desenhar(self, janela):
        x = self.x * self.ESCALA + LARGURA / 2
        y = self.y * self.ESCALA + ALTURA / 2

        if len(self.orbita) > 2:
            upadated_pontos = []
            for ponto in self.orbita:
                x, y = ponto
                x = x * self.ESCALA + LARGURA / 2
                y = y * self.ESCALA + ALTURA / 2
                upadated_pontos.append((x,y))

            pygame.draw.lines(janela, self.cor, False, upadated_pontos, 2)

        pygame.draw.circle(janela, self.cor, (x, y), self.raio)

        if not self.sol:
            distancia_texto = FONT.render(f"{round(self.distancia_do_sol/1000, 1)}km", 1, branco)
            janela.blit(distancia_texto,(x - distancia_texto.get_width()/2, y - distancia_texto.get_height()/2))

    def atracao(self, outro):
        outro_x, outro_y = outro.x, outro.y
        distancia_x = outro_x - self.x
        distancia_y = outro_y - self.y
        distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)

        if outro.sol:
            self.distancia_do_sol = distancia

        forca = self.G * self.massa * outro.massa / distancia ** 2
        theta = math.atan2(distancia_y, distancia_x)
        forca_x = math.cos(theta) * forca
        forca_y = math.sin(theta) * forca
        return forca_x, forca_y

    def update_posicao(self, planetas):
        total_fx = total_fy = 0
        for planeta in planetas:
            if self == planeta:
                continue

            fx, fy = self.atracao(planeta)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.massa * self.TIMESTEP
        self.y_vel += total_fy / self.massa * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbita.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sol = Planeta(0, 0, 30, amarelo, 1.98892 * 10**30)
    sol.sol = True

    terra = Planeta(-1 * Planeta.AU, 0, 16, azul, 5.9742 * 10**24)
    terra.y_vel = 29.783 * 1000

    marte = Planeta(-1.524 * Planeta.AU, 0, 12, vermelho, 6.39 * 10**23)
    marte.y_vel = 24.077 * 1000

    mercurio = Planeta(0.387 * Planeta.AU, 0, 8, cinza_escuro, 3.30 * 10**23)
    mercurio.y_vel = -47.4 * 1000

    venus = Planeta(0.723 * Planeta.AU, 0, 14, branco, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planetas = [sol, terra, marte, mercurio, venus]

    while run:
        clock.tick(60) 
        JANELA.fill((0, 0, 0))          #mudar a cor


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planeta in planetas:
            planeta.update_posicao(planetas)
            planeta.desenhar(JANELA)

        pygame.display.update()

    pygame.quit()

main()
