import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
import time
from pathlib import Path
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ImageClip, ColorClip
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap

class TikTokAPI:
    def __init__(self):
        load_dotenv()
        self.client_key = os.getenv('TIKTOK_CLIENT_KEY')
        self.client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
        self.access_token = os.getenv('TIKTOK_ACCESS_TOKEN')
        self.refresh_token = os.getenv('TIKTOK_REFRESH_TOKEN')
        self.base_url = 'https://open.tiktokapis.com/v2'
        
    def refresh_access_token(self):
        """Atualiza o token de acesso usando o refresh token"""
        url = f"{self.base_url}/oauth/token"
        data = {
            'client_key': self.client_key,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access_token']
            self.refresh_token = tokens['refresh_token']
            # Salvar novos tokens no .env
            self._update_env_file()
            return True
        return False

    def _update_env_file(self):
        """Atualiza o arquivo .env com novos tokens"""
        env_path = Path('.env')
        env_content = f"""TIKTOK_CLIENT_KEY="{self.client_key}"
TIKTOK_CLIENT_SECRET="{self.client_secret}"
TIKTOK_ACCESS_TOKEN="{self.access_token}"
TIKTOK_REFRESH_TOKEN="{self.refresh_token}"
"""
        env_path.write_text(env_content)

    def iniciar_upload(self, video_path):
        """Inicia o processo de upload do vídeo"""
        url = f"{self.base_url}/video/upload/"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Obter tamanho do arquivo
        file_size = os.path.getsize(video_path)
        
        # Solicitar URL de upload
        data = {
            'file_size': file_size
        }
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        return None

    def fazer_upload_video(self, video_path, upload_url):
        """Faz o upload do vídeo para o TikTok"""
        with open(video_path, 'rb') as f:
            files = {'video': f}
            response = requests.post(upload_url, files=files)
            return response.status_code == 200

    def publicar_video(self, video_id, descricao):
        """Publica o vídeo no TikTok"""
        url = f"{self.base_url}/video/publish/"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'video_id': video_id,
            'description': descricao,
            'privacy_level': 'PUBLIC',
            'disable_duet': False,
            'disable_comment': False,
            'disable_stitch': False
        }
        response = requests.post(url, headers=headers, json=data)
        return response.status_code == 200

class GeradorVideo:
    def __init__(self):
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = self.base_dir / 'assets'
        self.output_dir = self.base_dir / 'output'
        
        # Carregar configurações
        with open(self.base_dir / 'versiculos.json', 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def criar_background_video(self, duracao=15, width=1080, height=1920):
        """Cria um vídeo de background com gradiente animado"""
        # Criar clip com gradiente
        grad = np.linspace(0, 1, height)[:, np.newaxis].repeat(width, axis=1)
        frames = []
        
        fps = 30
        total_frames = int(duracao * fps)
        
        for i in range(total_frames):
            # Criar gradiente animado
            t = i / total_frames
            r = int(255 * (np.sin(2 * np.pi * t) + 1) / 2)
            g = int(255 * (np.sin(2 * np.pi * t + 2*np.pi/3) + 1) / 2)
            b = int(255 * (np.sin(2 * np.pi * t + 4*np.pi/3) + 1) / 2)
            
            # Criar frame
            frame = np.stack([grad * r, grad * g, grad * b], axis=-1)
            frames.append(frame.astype('uint8'))
        
        return ImageClip(frames, fps=fps)

    def criar_texto_animado(self, texto, duracao=15, width=1080, height=1920):
        """Cria um clip de texto animado"""
        # Quebrar texto em linhas
        linhas = textwrap.wrap(texto, width=30)
        
        clips_texto = []
        y = height // 3
        
        for i, linha in enumerate(linhas):
            texto_clip = TextClip(
                linha,
                fontsize=70,
                color='white',
                font='Arial',
                size=(width, 100)
            )
            
            # Adicionar animação de fade in
            texto_clip = texto_clip.set_position(('center', y))
            texto_clip = texto_clip.set_start(i * 0.5)  # Cada linha aparece 0.5s após a anterior
            texto_clip = texto_clip.crossfadein(1.0)
            texto_clip = texto_clip.set_duration(duracao - i * 0.5)
            
            clips_texto.append(texto_clip)
            y += 100
        
        return clips_texto

    def criar_video_versiculo(self, versiculo, referencia):
        """Cria um vídeo completo com versículo"""
        duracao = 15
        width, height = 1080, 1920
        
        # Criar background
        background = self.criar_background_video(duracao, width, height)
        
        # Criar texto
        texto_completo = f"{versiculo}\n\n- {referencia}"
        clips_texto = self.criar_texto_animado(texto_completo, duracao, width, height)
        
        # Combinar todos os clips
        video = CompositeVideoClip(
            [background] + clips_texto,
            size=(width, height)
        )
        
        # Adicionar música se disponível
        musica_path = self.assets_dir / 'music' / 'adoracao_suave_1.mp3'
        if musica_path.exists():
            audio = AudioFileClip(str(musica_path)).set_duration(duracao)
            video = video.set_audio(audio)
        
        return video

    def gerar_video(self, versiculo_data):
        """Gera um vídeo completo para um versículo"""
        # Criar vídeo
        video = self.criar_video_versiculo(
            versiculo_data['texto'],
            versiculo_data['referencia']
        )
        
        # Salvar vídeo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f'video_{timestamp}.mp4'
        video.write_videofile(str(output_path), fps=30)
        
        return str(output_path)

def main():
    # Inicializar API e gerador
    api = TikTokAPI()
    gerador = GeradorVideo()
    
    # Carregar versículos
    with open('versiculos.json', 'r', encoding='utf-8') as f:
        versiculos = json.load(f)['versiculos']
    
    # Selecionar versículo aleatório
    referencia = random.choice(list(versiculos.keys()))
    versiculo = versiculos[referencia]
    
    # Preparar dados do versículo
    versiculo_data = {
        'texto': versiculo['texto'],
        'referencia': referencia
    }
    
    try:
        # Gerar vídeo
        print("Gerando vídeo...")
        video_path = gerador.gerar_video(versiculo_data)
        print(f"Vídeo gerado: {video_path}")
        
        # Preparar descrição com hashtags
        hashtags = ' '.join([f"#{tag}" for tag in versiculo['hashtags']])
        descricao = f"""✝️ {referencia}
📖 {versiculo['texto']}

{hashtags}"""
        
        # Iniciar upload
        print("Iniciando upload...")
        upload_info = api.iniciar_upload(video_path)
        
        if upload_info:
            # Fazer upload do vídeo
            print("Fazendo upload do vídeo...")
            if api.fazer_upload_video(video_path, upload_info['upload_url']):
                # Publicar vídeo
                print("Publicando vídeo...")
                if api.publicar_video(upload_info['video_id'], descricao):
                    print("Vídeo publicado com sucesso!")
                else:
                    print("Erro ao publicar vídeo")
            else:
                print("Erro no upload do vídeo")
        else:
            print("Erro ao iniciar upload")
            
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    main()
