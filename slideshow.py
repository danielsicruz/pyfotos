import os
import pygame
import time
from ffpyplayer.player import MediaPlayer
import random

# Configuração do Pygame
pygame.init()

# Tamanho da tela (ajuste conforme seu dispositivo)
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Configuração de diretório de imagens e vídeos
media_folder = "C:/Users/Sharks/Documents/pyfotos/photo_server/uploads"  # Altere para o caminho correto
image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
video_extensions = ['.mp4', '.avi', '.mov']

# Função para verificar se é um arquivo de imagem
def is_image(filename):
    return any(filename.lower().endswith(ext) for ext in image_extensions)

# Função para verificar se é um arquivo de vídeo
def is_video(filename):
    return any(filename.lower().endswith(ext) for ext in video_extensions)

# Função para exibir imagem
def display_image(filename):
    image = pygame.image.load(os.path.join(media_folder, filename))
    image = pygame.transform.scale(image, (screen_width, screen_height))
    screen.blit(image, (0, 0))
    pygame.display.flip()

# Função para exibir vídeo
def display_video(filename):
    video_path = os.path.join(media_folder, filename)
    player = MediaPlayer(video_path)

    # Reproduz o vídeo até o final
    while True:
        grabbed, frame = player.get_frame()

        if not grabbed:
            break  # Se não conseguimos pegar um quadro, o vídeo terminou

        frame = pygame.surfarray.make_surface(frame)  # Convert to surface
        frame = pygame.transform.scale(frame, (screen_width, screen_height))
        screen.blit(frame, (0, 0))
        pygame.display.flip()

        # Controla o FPS para não sobrecarregar
        pygame.time.wait(10)

# Função para carregar arquivos de mídia
def load_media_files():
    media_files = os.listdir(media_folder)
    # Filtra os arquivos para incluir apenas imagens e vídeos
    media_files = [file for file in media_files if is_image(file) or is_video(file)]
    return media_files

# Função principal do slideshow
def run_slideshow():
    media_files = load_media_files()
    if not media_files:  # Se a lista estiver vazia, exibe uma mensagem e sai
        print("Nenhum arquivo de imagem ou vídeo encontrado.")
        return

    random.shuffle(media_files)  # Embaralha a ordem dos arquivos
    index = 0

    running = True
    while running:
        screen.fill((0, 0, 0))  # Limpa a tela

        # Verifica se o arquivo atual é uma imagem ou vídeo
        current_file = media_files[index]
        if is_image(current_file):
            display_image(current_file)
        elif is_video(current_file):
            display_video(current_file)

        # Avança para o próximo arquivo
        index = (index + 1) % len(media_files)  # Garantir que o índice não ultrapasse o tamanho da lista

        # Atualiza a lista de arquivos após cada apresentação
        media_files = load_media_files()  # Atualiza a lista de arquivos
        random.shuffle(media_files)  # Reembaralha a lista para manter a aleatoriedade

        # Espera antes de exibir o próximo arquivo
        time.sleep(5)

        # Verifica eventos (como fechar a janela)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

# Inicia o slideshow
run_slideshow()
