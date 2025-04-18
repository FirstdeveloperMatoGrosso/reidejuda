import json
import os
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import textwrap
import schedule
import time
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ImageClip
import numpy as np
from pathlib import Path

class TikTokBotBiblico:
    def __init__(self):
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = self.base_dir / 'assets'
        self.videos_dir = self.assets_dir / 'videos'
        self.music_dir = self.assets_dir / 'music'
        self.fonts_dir = self.assets_dir / 'fonts'
        self.output_dir = self.base_dir / 'output'

        # Criar diretórios necessários
        for dir_path in [self.assets_dir, self.videos_dir, self.music_dir, 
                        self.fonts_dir, self.output_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Carregar dados
        self.carregar_dados()
        
        # Configurar horários de postagem
        self.horarios_postagem = [
            "07:00",  # Manhã cedo - pessoas acordando
            "12:00",  # Horário de almoço
            "15:00",  # Meio da tarde
            "18:00",  # Fim do trabalho
            "20:00",  # Noite - horário nobre
            "22:00"   # Antes de dormir
        ]

    def carregar_dados(self):
        """Carrega versículos e configurações do JSON"""
        with open(self.base_dir / 'versiculos.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.versiculos = dados['versiculos']
            self.temas = dados['temas']
            self.templates = dados['templates']

    def criar_background_gradiente(self, width, height, cores):
        """Cria um background com gradiente suave"""
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        cor1 = tuple(int(cores[0].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        cor2 = tuple(int(cores[1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        for y in range(height):
            r = int(cor1[0] + (cor2[0] - cor1[0]) * y / height)
            g = int(cor1[1] + (cor2[1] - cor1[1]) * y / height)
            b = int(cor1[2] + (cor2[2] - cor1[2]) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return img

    def aplicar_efeitos(self, img, efeitos):
        """Aplica efeitos visuais na imagem"""
        for efeito in efeitos:
            if efeito == "blur":
                img = img.filter(ImageFilter.GaussianBlur(radius=1))
            elif efeito == "glow":
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.2)
        return img

    def criar_imagem_versiculo(self, versiculo, referencia, tema, template):
        """Cria uma imagem com o versículo usando o tema e template especificados"""
        width, height = 1080, 1920  # Dimensões padrão do TikTok
        
        # Criar background
        cores = self.temas[tema]['cores']
        img = self.criar_background_gradiente(width, height, cores)
        
        # Configurar fonte e texto
        config_template = self.templates[template]
        fonte_size = config_template['tamanho_fonte']
        
        # Preparar texto
        texto_completo = f'{versiculo}\n\n- {referencia}'
        
        # Quebrar texto em linhas
        linhas = textwrap.wrap(texto_completo, width=30)
        
        # Desenhar texto
        draw = ImageDraw.Draw(img)
        y = height // 3
        for linha in linhas:
            draw.text((width//2, y), linha, 
                     fill='white', 
                     anchor='mm',
                     align='center')
            y += fonte_size * config_template['espacamento']
        
        # Aplicar efeitos
        img = self.aplicar_efeitos(img, config_template['efeitos'])
        
        return img

    def criar_video(self, imagem, musica_path, duracao=15):
        """Cria um vídeo a partir da imagem com música e efeitos"""
        # Converter PIL Image para ImageClip
        img_array = np.array(imagem)
        clip = ImageClip(img_array)
        
        # Configurar duração
        clip = clip.set_duration(duracao)
        
        # Adicionar música
        if os.path.exists(musica_path):
            audio = AudioFileClip(musica_path).set_duration(duracao)
            clip = clip.set_audio(audio)
        
        # Adicionar efeitos de transição
        clip = clip.crossfadein(1.0)
        clip = clip.crossfadeout(1.0)
        
        return clip

    def gerar_hashtags(self, hashtags_especificas):
        """Gera uma lista de hashtags combinando as específicas com genéricas"""
        hashtags_base = [
            "biblia", "jesus", "deus", "fe", "amor", "paz",
            "versiculododia", "deusefiel", "christ", "god"
        ]
        
        # Combinar e embaralhar
        todas_hashtags = list(set(hashtags_especificas + hashtags_base))
        random.shuffle(todas_hashtags)
        
        # Selecionar um número adequado de hashtags
        num_hashtags = random.randint(15, 20)
        hashtags_selecionadas = todas_hashtags[:num_hashtags]
        
        return ' '.join([f"#{tag}" for tag in hashtags_selecionadas])

    def criar_post_completo(self):
        """Cria um post completo com vídeo e texto"""
        # Selecionar versículo aleatório
        referencia = random.choice(list(self.versiculos.keys()))
        dados_versiculo = self.versiculos[referencia]
        
        # Selecionar template aleatório
        template = random.choice(list(self.templates.keys()))
        
        # Criar imagem
        imagem = self.criar_imagem_versiculo(
            dados_versiculo['texto'],
            referencia,
            dados_versiculo['tema'],
            template
        )
        
        # Selecionar música
        musica = random.choice(self.temas[dados_versiculo['tema']]['musicas'])
        musica_path = self.music_dir / musica
        
        # Criar vídeo
        video = self.criar_video(imagem, musica_path)
        
        # Gerar nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = self.output_dir / f'video_{timestamp}.mp4'
        
        # Salvar vídeo
        video.write_videofile(str(video_path), fps=30)
        
        # Gerar texto e hashtags
        texto = f"""✝️ {referencia}
📖 {dados_versiculo['texto']}

{self.gerar_hashtags(dados_versiculo['hashtags'])}"""
        
        return {
            'video_path': video_path,
            'texto': texto,
            'tema': dados_versiculo['tema']
        }

    def postar_tiktok(self, video_path, texto):
        """Posta o vídeo no TikTok (simulado)"""
        print(f"\n{'='*50}")
        print("Postando no TikTok...")
        print(f"Vídeo: {video_path}")
        print(f"\nTexto do post:")
        print(texto)
        print(f"{'='*50}\n")
        return True

    def agendar_posts(self):
        """Agenda posts para os horários definidos"""
        for horario in self.horarios_postagem:
            schedule.every().day.at(horario).do(self.criar_e_postar)
        print(f"Posts agendados para os horários: {', '.join(self.horarios_postagem)}")

    def criar_e_postar(self):
        """Processo completo de criar e postar conteúdo"""
        try:
            post = self.criar_post_completo()
            sucesso = self.postar_tiktok(post['video_path'], post['texto'])
            
            if sucesso:
                print(f"Post realizado com sucesso! Tema: {post['tema']}")
            else:
                print("Erro ao postar conteúdo")
                
        except Exception as e:
            print(f"Erro ao criar/postar conteúdo: {str(e)}")

    def executar(self):
        """Inicia o bot"""
        print("Iniciando Bot Bíblico para TikTok...")
        self.agendar_posts()
        
        # Criar primeiro post imediatamente
        self.criar_e_postar()
        
        # Manter bot rodando e executando agendamentos
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    bot = TikTokBotBiblico()
    bot.executar()

if __name__ == "__main__":
    main()
