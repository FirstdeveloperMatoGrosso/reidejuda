import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
import time
from pathlib import Path
import random
from PIL import Image
import io
import base64

class GeradorIA:
    def __init__(self):
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = self.base_dir / 'output'
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def gerar_imagem_stable_diffusion(self, prompt):
        """Gera imagem usando Stable Diffusion API gratuita"""
        url = "https://stablediffusionapi.com/api/v3/text2img"  # API gratuita
        
        payload = {
            "key": "CHAVE_GRATUITA",  # Registre-se para obter uma chave gratuita
            "prompt": prompt,
            "negative_prompt": "text, watermark, logo, words",
            "width": "1080",
            "height": "1920",
            "samples": "1",
            "safety_checker": "no"
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            img_url = response.json()['output'][0]
            img_data = requests.get(img_url).content
            return Image.open(io.BytesIO(img_data))
        return None

    def gerar_video_pexels(self, query):
        """Busca vídeos gratuitos no Pexels"""
        url = "https://api.pexels.com/videos/search"
        headers = {
            "Authorization": "CHAVE_PEXELS"  # Registre-se para chave gratuita
        }
        params = {
            "query": query,
            "orientation": "portrait",
            "per_page": 1
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            videos = response.json()['videos']
            if videos:
                video_url = videos[0]['video_files'][0]['link']
                return requests.get(video_url).content
        return None

    def gerar_musica_mubert(self, mood):
        """Gera música usando Mubert API (versão gratuita)"""
        url = "https://api-b2b.mubert.com/v2/TTM"
        
        payload = {
            "method": "GetTTM",
            "params": {
                "mood": mood,
                "duration": 15,
                "format": "mp3"
            }
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            music_url = response.json()['data']['url']
            return requests.get(music_url).content
        return None

class TikTokBotIA:
    def __init__(self):
        self.gerador = GeradorIA()
        self.carregar_config()

    def carregar_config(self):
        """Carrega configurações e versículos"""
        with open('versiculos.json', 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            self.versiculos = self.config['versiculos']

    def gerar_prompt_imagem(self, tema):
        """Gera prompt para imagem baseado no tema"""
        prompts = {
            "amor": "heavenly divine light, rays of golden light, heart shape clouds, peaceful sky, cinematic, high quality, 8k",
            "paz": "serene mountain landscape, peaceful lake reflection, soft clouds, divine light, cinematic",
            "fé": "ancient temple architecture, divine light rays, spiritual atmosphere, mystical, cinematic",
            "esperança": "sunrise over mountains, rainbow, dove flying, peaceful landscape, cinematic",
            "força": "majestic mountains, powerful waterfall, stormy sky with light breaking through, cinematic"
        }
        return prompts.get(tema, "divine light, peaceful nature, spiritual, cinematic")

    def criar_post(self, referencia, versiculo):
        """Cria um post completo com imagem/vídeo gerado por IA"""
        tema = versiculo['tema']
        
        # 1. Gerar imagem de fundo
        prompt = self.gerar_prompt_imagem(tema)
        imagem = self.gerador.gerar_imagem_stable_diffusion(prompt)
        
        if imagem:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_path = self.gerador.output_dir / f'imagem_{timestamp}.png'
            imagem.save(img_path)
            
            # 2. Buscar vídeo relacionado
            video_data = self.gerador.gerar_video_pexels(tema)
            if video_data:
                video_path = self.gerador.output_dir / f'video_{timestamp}.mp4'
                with open(video_path, 'wb') as f:
                    f.write(video_data)
            
            # 3. Gerar música
            musica_data = self.gerador.gerar_musica_mubert(tema)
            if musica_data:
                music_path = self.gerador.output_dir / f'musica_{timestamp}.mp3'
                with open(music_path, 'wb') as f:
                    f.write(musica_data)
            
            return {
                'imagem': str(img_path),
                'video': str(video_path) if video_data else None,
                'musica': str(music_path) if musica_data else None,
                'texto': versiculo['texto'],
                'referencia': referencia,
                'hashtags': versiculo['hashtags']
            }
        return None

def main():
    bot = TikTokBotIA()
    
    # Selecionar versículo aleatório
    referencia = random.choice(list(bot.versiculos.keys()))
    versiculo = bot.versiculos[referencia]
    
    # Criar post
    print("Gerando conteúdo com IA...")
    post = bot.criar_post(referencia, versiculo)
    
    if post:
        print("\nConteúdo gerado com sucesso!")
        print(f"Imagem: {post['imagem']}")
        if post['video']:
            print(f"Vídeo: {post['video']}")
        if post['musica']:
            print(f"Música: {post['musica']}")
        
        # Mostrar texto e hashtags
        print("\nTexto do post:")
        print(f"✝️ {post['referencia']}")
        print(f"📖 {post['texto']}")
        print(f"\nHashtags: {' '.join(['#' + tag for tag in post['hashtags']])}")
    else:
        print("Erro ao gerar conteúdo")

if __name__ == "__main__":
    main()
