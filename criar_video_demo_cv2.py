import cv2
import numpy as np
import os
import subprocess
from gerar_imagens_biblicas import gerar_imagem_biblica
import time
from PIL import Image, ImageDraw, ImageFont
import requests
from urllib.parse import urlparse
from gerenciador_midia import GerenciadorMidia

def baixar_musica(url: str) -> str:
    # Baixar música da URL fornecida
    response = requests.get(url)
    
    # Salvar música
    musica_path = "background_music.mp3"
    with open(musica_path, 'wb') as f:
        f.write(response.content)
    return musica_path

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

def criar_video_demo():
    # Inicializar gerenciador de mídia
    midia = GerenciadorMidia()
    
    # Configurações do vídeo
    fps = 30
    duracao_por_cena = 5  # segundos
    largura = 1080  # Formato vertical para TikTok
    altura = 1920
    
    # Obter música aleatória
    musica = midia.obter_musica_aleatoria()
    
    # Lista de cenas com legendas formatadas
    cenas = [
        {
            "prompt": "Jesus Christ on the cross during crucifixion, dramatic sunset sky, divine rays of light, realistic style, cinematic, masterpiece, 4k, detailed",
            "texto": midia.formatar_texto_tiktok("Semana Santa: A Paixão de Cristo"),
            "legenda": midia.formatar_texto_tiktok("O momento mais sagrado da história da humanidade")
        },
        {
            "prompt": "Jesus Christ carrying the cross through Jerusalem streets, crowd watching, dramatic lighting, realistic style, cinematic, 4k, detailed",
            "texto": midia.formatar_texto_tiktok("Via Crucis: O Caminho da Cruz"),
            "legenda": midia.formatar_texto_tiktok("O sacrifício supremo por amor a nós")
        },
        {
            "prompt": "The Last Supper, Jesus with disciples, dramatic lighting, realistic style, renaissance painting style, masterpiece, 4k, detailed",
            "texto": midia.formatar_texto_tiktok("Quinta-feira Santa: Última Ceia"),
            "legenda": midia.formatar_texto_tiktok("O momento em que Jesus instituiu a Eucaristia")
        },
        {
            "prompt": "Empty tomb of Jesus with divine light, angel sitting on stone, dramatic atmosphere, realistic style, masterpiece, 4k, detailed",
            "texto": midia.formatar_texto_tiktok("Domingo de Páscoa: A Ressurreição"),
            "legenda": midia.formatar_texto_tiktok("A vitória da vida sobre a morte")
        }
    ]
    
    # Adicionar cena final com créditos
    creditos = midia.gerar_creditos(musica)
    cenas.append({
        "prompt": "holy bible with divine light and cross, dramatic lighting, realistic style, cinematic, 4k, detailed",
        "texto": "Siga @OReiDeJuda",
        "legenda": creditos
    })
    
    # Criar diretório para vídeos se não existir
    if not os.path.exists('videos'):
        os.makedirs('videos')
    
    # Baixar música de fundo
    print("\nBaixando música de fundo...")
    print(f"Música: {musica['titulo']} - {musica['artista']}")
    musica_path = baixar_musica(musica['url'])
    
    # Configurar o writer do vídeo
    video_temp = 'videos/temp_semana_santa.mp4'
    video_final = 'videos/demo_semana_santa.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_temp, fourcc, fps, (largura, altura))
    
    # Para cada cena
    for i, cena in enumerate(cenas):
        print(f"\nGerando imagem {i+1}/{len(cenas)}...")
        try:
            # Gerar imagem usando Stable Diffusion
            imagem_path = gerar_imagem_biblica(cena["prompt"])
            time.sleep(1)  # Esperar um pouco entre as requisições
            
            # Ler a imagem
            frame = cv2.imread(imagem_path)
            if frame is None:
                print(f"Erro ao ler imagem: {imagem_path}")
                continue
                
            # Redimensionar para o formato do TikTok
            frame = cv2.resize(frame, (largura, altura))
            
            # Adicionar texto e legenda
            frame = adicionar_texto(frame, cena["texto"], cena["legenda"])
            
            # Escrever os frames para criar a duração desejada
            for _ in range(fps * duracao_por_cena):
                out.write(frame)
                
            print(f"Cena {i+1} adicionada ao vídeo")
            
        except Exception as e:
            print(f"Erro ao processar cena {i+1}:", str(e))
    
    # Liberar o writer
    out.release()
    
    # Adicionar música ao vídeo usando ffmpeg
    print("\nAdicionando música ao vídeo...")
    comando = f'ffmpeg -i {video_temp} -i {musica_path} -c:v copy -c:a aac -shortest {video_final}'
    subprocess.run(comando, shell=True)
    
    # Remover arquivos temporários
    os.remove(video_temp)
    os.remove(musica_path)
    
    print("\nVídeo demo salvo em: videos/demo_semana_santa.mp4")

if __name__ == "__main__":
    criar_video_demo()
