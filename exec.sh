#!/bin/bash
# Caminho absoluto para a pasta de uploads
FOLDER="./uploads"

# Mata instâncias anteriores para evitar sobreposição de áudio/vídeo
pkill vlc

# Executa o VLC:
# -f: Tela cheia
# -L: Loop da playlist
# --no-video-title-show: Não mostra o nome do arquivo na tela
# --quiet: Reduz logs no terminal
cvlc -f -L --no-video-title-show --quiet "$FOLDER"/*