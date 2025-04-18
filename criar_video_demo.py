import os
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.resize import resize
from gerar_imagens_biblicas import gerar_imagem_biblica
import time

def criar_cena(imagem_path, texto, duracao=5):
    # Carregar a imagem
    img_clip = ImageClip(imagem_path)
    
    # Criar texto com efeito de fade
    txt_clip = TextClip(texto, fontsize=70, color='white', font='Arial-Bold')
    txt_clip = txt_clip.set_position('center').set_duration(duracao)
    txt_clip = txt_clip.crossfadein(1).crossfadeout(1)
    
    # Adicionar sombra ao texto para melhor legibilidade
    txt_shadow = TextClip(texto, fontsize=70, color='black', font='Arial-Bold')
    txt_shadow = txt_shadow.set_position(('center', 402)).set_duration(duracao)
    txt_shadow = txt_shadow.crossfadein(1).crossfadeout(1)
    
    # Redimensionar a imagem para 1080x1920 (formato TikTok)
    img_clip = resize(img_clip, width=1080)
    img_clip = img_clip.set_duration(duracao)
    
    # Combinar imagem e texto
    final_clip = CompositeVideoClip([img_clip, txt_shadow, txt_clip])
    
    return final_clip

def main():
    # Criar diretório para o vídeo se não existir
    if not os.path.exists('videos'):
        os.makedirs('videos')
    
    # Lista de cenas para o vídeo demo
    cenas = [
        {
            "prompt": "Jesus Christ on the cross during crucifixion, dramatic sunset sky, divine rays of light, realistic style, cinematic, masterpiece",
            "texto": "Semana Santa:\nA Paixão de Cristo"
        },
        {
            "prompt": "Jesus Christ carrying the cross through Jerusalem streets, crowd watching, dramatic lighting, realistic style, cinematic",
            "texto": "Via Crucis:\nO Caminho da Cruz"
        },
        {
            "prompt": "The Last Supper, Jesus with disciples, dramatic lighting, realistic style, renaissance painting style, masterpiece",
            "texto": "Quinta-feira Santa:\nÚltima Ceia"
        },
        {
            "prompt": "Empty tomb of Jesus with divine light, angel sitting on stone, dramatic atmosphere, realistic style, masterpiece",
            "texto": "Domingo de Páscoa:\nA Ressurreição"
        }
    ]
    
    # Gerar imagens e criar cenas
    video_clips = []
    for i, cena in enumerate(cenas):
        print(f"\nGerando imagem {i+1}/{len(cenas)}...")
        try:
            # Gerar imagem usando Stable Diffusion
            imagem_path = gerar_imagem_biblica(cena["prompt"])
            time.sleep(1)  # Esperar um pouco entre as requisições
            
            # Criar cena com a imagem
            clip = criar_cena(imagem_path, cena["texto"])
            video_clips.append(clip)
            
        except Exception as e:
            print(f"Erro ao gerar cena {i+1}:", str(e))
    
    # Concatenar todas as cenas
    final_video = concatenate_videoclips(video_clips)
    
    # Adicionar música de fundo (você precisa ter um arquivo de música)
    try:
        audio = AudioFileClip("background_music.mp3")
        audio = audio.set_duration(final_video.duration)
        final_video = final_video.set_audio(audio)
    except:
        print("Arquivo de música não encontrado. Gerando vídeo sem áudio.")
    
    # Salvar o vídeo final
    output_path = "videos/demo_semana_santa.mp4"
    final_video.write_videofile(output_path, fps=30, codec='libx264', audio_codec='aac')
    print(f"\nVídeo demo salvo em: {output_path}")

if __name__ == "__main__":
    main()
