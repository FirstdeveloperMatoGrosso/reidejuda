import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime, timedelta
from TikTokApi import TikTokApi
import schedule
import time
import random
import json
import requests
from io import BytesIO

class TikTokBotBiblico:
    def __init__(self):
        # Configurações do TikTok
        self.api = TikTokApi()
        self.session_id = "SEU_SESSION_ID"  # Você precisará configurar isso
        
        # Diretórios para assets
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.base_dir, 'assets')
        self.videos_dir = os.path.join(self.assets_dir, 'videos')
        self.music_dir = os.path.join(self.assets_dir, 'music')
        self.fonts_dir = os.path.join(self.assets_dir, 'fonts')
        
        # Criar diretórios se não existirem
        for directory in [self.assets_dir, self.videos_dir, self.music_dir, self.fonts_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Carregar versículos e configurações
        self.versiculos = self.carregar_versiculos()
        self.backgrounds = self.carregar_backgrounds()
        self.musicas = self.carregar_musicas()
        
        # Configurações de hashtags
        self.hashtags_base = [
            "biblia", "jesus", "deus", "fe", "amor", "paz", "cristianismo",
            "versiculododia", "deusefiel", "biblical", "christ", "god"
        ]

    def carregar_versiculos(self):
        """Carrega versículos de um arquivo JSON ou API"""
        versiculos = {
            "João 3:16": "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito...",
            "Salmos 23:1": "O Senhor é meu pastor, nada me faltará.",
            # Adicione mais versículos aqui
        }
        return versiculos

    def carregar_backgrounds(self):
        """Carrega ou baixa backgrounds para os vídeos"""
        backgrounds = [
            "nature.mp4",
            "sunset.mp4",
            "clouds.mp4"
        ]
        return backgrounds

    def carregar_musicas(self):
        """Carrega músicas de fundo disponíveis"""
        musicas = [
            "worship1.mp3",
            "peaceful1.mp3",
            "instrumental1.mp3"
        ]
        return musicas

    def criar_video(self, versiculo, referencia):
        """Cria um vídeo com o versículo"""
        # Selecionar background e música aleatórios
        background = random.choice(self.backgrounds)
        musica = random.choice(self.musicas)
        
        # Carregar vídeo de background
        video_path = os.path.join(self.videos_dir, background)
        video = VideoFileClip(video_path).resize(width=1080, height=1920)  # Formato TikTok
        
        # Criar texto do versículo
        text_clip = TextClip(
            txt=f"{versiculo}\n\n- {referencia}",
            fontsize=70,
            color='white',
            font='Helvetica',
            size=video.size,
            method='caption',
            align='center'
        )
        text_clip = text_clip.set_duration(video.duration)
        
        # Adicionar música de fundo
        audio_path = os.path.join(self.music_dir, musica)
        audio = AudioFileClip(audio_path).set_duration(video.duration)
        
        # Combinar tudo
        final_video = CompositeVideoClip([
            video,
            text_clip.set_position('center')
        ]).set_audio(audio)
        
        # Salvar vídeo
        output_path = os.path.join(self.videos_dir, f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        final_video.write_videofile(output_path, fps=30)
        
        return output_path

    def gerar_hashtags(self, tema):
        """Gera hashtags relevantes para o post"""
        num_hashtags = random.randint(15, 25)
        hashtags = self.hashtags_base.copy()
        
        # Adicionar hashtags específicas do tema
        tema_hashtags = [
            f"{tema.lower()}",
            f"versiculo{tema.replace(' ', '')}",
            f"biblia{tema.replace(' ', '')}"
        ]
        hashtags.extend(tema_hashtags)
        
        # Selecionar aleatoriamente e formatar
        selected_hashtags = random.sample(hashtags, min(num_hashtags, len(hashtags)))
        return ' '.join([f"#{tag}" for tag in selected_hashtags])

    def postar_tiktok(self, video_path, descricao, hashtags):
        """Posta o vídeo no TikTok"""
        try:
            # Aqui você usaria a API do TikTok para postar
            # Este é um exemplo conceitual - você precisará implementar com a API real
            with self.api.create_video(
                video_path,
                description=f"{descricao}\n\n{hashtags}",
                custom_verify_fp=self.session_id
            ) as post:
                print(f"Vídeo postado com sucesso! ID: {post.id}")
                return True
        except Exception as e:
            print(f"Erro ao postar no TikTok: {str(e)}")
            return False

    def programar_posts(self):
        """Programa posts para horários específicos"""
        # Horários de maior engajamento
        horarios = ['9:00', '12:00', '15:00', '18:00', '20:00']
        
        for horario in horarios:
            schedule.every().day.at(horario).do(self.criar_e_postar)

    def criar_e_postar(self):
        """Processo completo de criar e postar conteúdo"""
        # Selecionar versículo aleatório
        referencia = random.choice(list(self.versiculos.keys()))
        versiculo = self.versiculos[referencia]
        
        # Criar vídeo
        video_path = self.criar_video(versiculo, referencia)
        
        # Gerar descrição e hashtags
        descricao = f"✝️ {referencia}\n📖 Palavra de Deus para sua vida"
        hashtags = self.gerar_hashtags(referencia.split()[0])  # Usa o livro como tema
        
        # Postar no TikTok
        sucesso = self.postar_tiktok(video_path, descricao, hashtags)
        
        # Limpar arquivo de vídeo após postar
        if sucesso and os.path.exists(video_path):
            os.remove(video_path)

    def iniciar(self):
        """Inicia o bot"""
        print("Iniciando Bot Bíblico para TikTok...")
        self.programar_posts()
        
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    bot = TikTokBotBiblico()
    
    # Testar criação de um vídeo
    referencia = "João 3:16"
    versiculo = bot.versiculos[referencia]
    video_path = bot.criar_video(versiculo, referencia)
    print(f"Vídeo de teste criado: {video_path}")
    
    # Iniciar bot com agendamento
    bot.iniciar()

if __name__ == "__main__":
    main()
