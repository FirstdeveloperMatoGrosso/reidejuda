import cv2
import numpy as np
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import time

def adicionar_texto(imagem, texto_principal, legenda=""):
    # Converter para PIL Image
    img_pil = Image.fromarray(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # Usar uma fonte padrão
    try:
        fonte_grande = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        fonte_pequena = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        fonte_grande = ImageFont.load_default()
        fonte_pequena = fonte_grande
    
    # Adicionar texto principal (centro)
    largura_img, altura_img = img_pil.size
    bbox = draw.textbbox((0, 0), texto_principal, font=fonte_grande)
    largura_texto = bbox[2] - bbox[0]
    altura_texto = bbox[3] - bbox[1]
    x = (largura_img - largura_texto) // 2
    y = (altura_img - altura_texto) // 2
    
    # Adicionar sombra do texto principal
    draw.text((x+2, y+2), texto_principal, font=fonte_grande, fill='black')
    draw.text((x, y), texto_principal, font=fonte_grande, fill='white')
    
    # Adicionar legenda (parte inferior)
    if legenda:
        bbox = draw.textbbox((0, 0), legenda, font=fonte_pequena)
        largura_texto = bbox[2] - bbox[0]
        x = (largura_img - largura_texto) // 2
        y = altura_img - 100  # 100 pixels do fundo
        
        # Adicionar sombra da legenda
        draw.text((x+2, y+2), legenda, font=fonte_pequena, fill='black')
        draw.text((x, y), legenda, font=fonte_pequena, fill='white')
    
    # Converter de volta para OpenCV
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def gerar_video_teste():
    # Configurações do vídeo
    fps = 30
    duracao_por_cena = 5  # segundos
    largura = 1080  # Formato vertical para TikTok
    altura = 1920
    
    # Criar diretório para vídeos se não existir
    if not os.path.exists('videos'):
        os.makedirs('videos')
    
    # Configurar o writer do vídeo
    video_temp = 'videos/temp_teste.mp4'
    video_final = 'videos/demo_teste.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_temp, fourcc, fps, (largura, altura))
    
    # Criar uma imagem preta simples
    frame = np.zeros((altura, largura, 3), dtype=np.uint8)
    
    # Adicionar texto
    frame = adicionar_texto(frame, "O Rei de Judá", "Teste de Vídeo - Sistema de Automação")
    
    # Escrever os frames para criar a duração desejada
    for _ in range(fps * duracao_por_cena):
        out.write(frame)
    
    # Liberar o writer
    out.release()
    
    # Adicionar música de amostra
    print("\nAdicionando música ao vídeo...")
    
    # Usar um arquivo de áudio de exemplo
    # Use um arquivo de amostra já conhecido que deve funcionar
    comando = f'ffmpeg -i {video_temp} -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -c:v copy -c:a aac -shortest {video_final}'
    
    print(f"Executando comando: {comando}")
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    
    if resultado.returncode != 0:
        print(f"Erro ao adicionar áudio: {resultado.stderr}")
    else:
        print("Áudio adicionado com sucesso!")
    
    # Remover arquivo temporário
    if os.path.exists(video_temp):
        os.remove(video_temp)
    
    print(f"\nVídeo de teste salvo em: {video_final}")
    return video_final

if __name__ == "__main__":
    gerar_video_teste()
