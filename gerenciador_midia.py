import requests
import json
import random
from typing import Dict, List, Tuple
import os
from datetime import datetime
import re
from buscador_musicas import BuscadorMusicas

class GerenciadorMidia:
    def __init__(self):
        self.buscador = BuscadorMusicas()
        
        # Tentar carregar músicas do cache primeiro
        self.musicas_biblicas = self.buscador.carregar_cache_musicas()
        
        # Se não houver cache, buscar novas músicas
        if not self.musicas_biblicas:
            self.musicas_biblicas = self.buscador.buscar_musicas_biblicas()
            self.buscador.salvar_cache_musicas(self.musicas_biblicas)
        
        self.hashtags_populares = [
            "#Jesus", "#Cristo", "#Deus", "#Fé", "#Igreja", "#Evangelho",
            "#Cristão", "#Bíblia", "#Oração", "#PalavraDeDeus", "#Gospel",
            "#SemanaSanta", "#JesusCristo", "#Cruz", "#Ressurreição",
            "#Adoração", "#Louvor", "#DeusÉFiel", "#Amém", "#Cristianismo"
        ]
        
        self.legendas_biblicas = [
            "O amor de Deus é maior que tudo 🙏",
            "Na presença do Senhor há plenitude de alegria 🙌",
            "Jesus é o caminho, a verdade e a vida ✝️",
            "A fé move montanhas 🏔️",
            "Em Deus, todas as coisas são possíveis 🕊️",
            "O Senhor é meu pastor e nada me faltará 🐑",
            "A graça de Deus é suficiente 🙏",
            "Busque primeiro o Reino de Deus 👑"
        ]

    def obter_hashtags(self, quantidade: int = 5) -> List[str]:
        """Retorna uma lista de hashtags populares"""
        return random.sample(self.hashtags_populares, min(quantidade, len(self.hashtags_populares)))

    def obter_legenda_aleatoria(self) -> str:
        """Retorna uma legenda bíblica aleatória"""
        return random.choice(self.legendas_biblicas)

    def obter_musica_aleatoria(self) -> Dict:
        """Retorna uma música bíblica aleatória com suas informações"""
        return random.choice(self.musicas_biblicas)

    def gerar_creditos(self, musica: Dict, autor_video: str = "O Rei de Judá") -> str:
        """Gera os créditos do vídeo incluindo música e autor"""
        data_atual = datetime.now().strftime("%d/%m/%Y")
        visualizacoes = musica.get('visualizacoes', 0)
        visualizacoes_fmt = f"{visualizacoes:,}".replace(',', '.')
        
        creditos = f"""🎵 Música: {musica['titulo']}
🎤 Artista: {musica['artista']}
👀 {visualizacoes_fmt} visualizações
✨ Vídeo por: {autor_video}
📅 {data_atual}

{' '.join(musica.get('hashtags', []))}
{' '.join(self.obter_hashtags())}

#OReiDeJuda #ConteudoBiblico #SemanaSanta
#Gospel #Jesus #Deus #Fé"""

    def formatar_texto_tiktok(self, texto: str) -> str:
        """Formata o texto para melhor visualização no TikTok"""
        # Adiciona emojis relevantes
        emojis = {
            "Deus": "🙏",
            "Jesus": "✝️",
            "Cristo": "👑",
            "amor": "❤️",
            "fé": "🕊️",
            "glória": "✨",
            "cruz": "✝️",
            "ressurreição": "🌅",
            "vida": "🌱"
        }
        
        for palavra, emoji in emojis.items():
            texto = re.sub(f'(?i){palavra}', f'{palavra} {emoji}', texto)
            
        return texto
