import requests
from typing import List, Dict
import json
import os
from datetime import datetime

class BuscadorMusicas:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def buscar_musicas_biblicas(self, quantidade: int = 5) -> List[Dict]:
        """
        Busca músicas gospel/bíblicas populares no YouTube
        """
        if not self.api_key:
            # Se não tiver API key, retorna lista padrão
            return self._get_musicas_padrao()
            
        termos_busca = [
            "música gospel mais tocada",
            "louvor e adoração top",
            "música gospel 2025",
            "hinos gospel populares",
            "worship songs portuguese"
        ]
        
        musicas = []
        for termo in termos_busca:
            try:
                # Buscar vídeos
                params = {
                    'part': 'snippet,statistics',
                    'q': termo,
                    'type': 'video',
                    'videoCategoryId': '10',  # Música
                    'maxResults': quantidade,
                    'key': self.api_key
                }
                
                response = requests.get(f"{self.base_url}/search", params=params)
                data = response.json()
                
                for item in data.get('items', []):
                    video_id = item['id']['videoId']
                    snippet = item['snippet']
                    
                    # Obter detalhes do vídeo
                    video_params = {
                        'part': 'statistics,snippet',
                        'id': video_id,
                        'key': self.api_key
                    }
                    video_response = requests.get(f"{self.base_url}/videos", params=video_params)
                    video_data = video_response.json()
                    
                    if video_data.get('items'):
                        video = video_data['items'][0]
                        stats = video.get('statistics', {})
                        
                        musica = {
                            'titulo': snippet['title'],
                            'artista': snippet['channelTitle'],
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'visualizacoes': int(stats.get('viewCount', 0)),
                            'likes': int(stats.get('likeCount', 0)),
                            'thumbnail': snippet['thumbnails']['high']['url'],
                            'hashtags': self._extrair_hashtags(snippet['description'])
                        }
                        musicas.append(musica)
            
            except Exception as e:
                print(f"Erro ao buscar músicas para '{termo}': {str(e)}")
                continue
        
        # Ordenar por visualizações
        musicas.sort(key=lambda x: x['visualizacoes'], reverse=True)
        return musicas[:quantidade]
    
    def _extrair_hashtags(self, texto: str) -> List[str]:
        """Extrai hashtags do texto"""
        hashtags = []
        for palavra in texto.split():
            if palavra.startswith('#'):
                hashtags.append(palavra)
        return hashtags[:5]  # Limitar a 5 hashtags
    
    def _get_musicas_padrao(self) -> List[Dict]:
        """Retorna uma lista padrão de músicas populares"""
        return [
            {
                "titulo": "Todavia Me Alegrarei",
                "artista": "Gabriela Rocha",
                "url": "https://www.youtube.com/watch?v=0JvQJ_XNKIw",
                "hashtags": ["#GabrielaRocha", "#Gospel", "#Adoração"],
                "visualizacoes": 15000000
            },
            {
                "titulo": "Deus É Deus",
                "artista": "Delino Marçal",
                "url": "https://www.youtube.com/watch?v=X6N6W8Gh6yE",
                "hashtags": ["#DelinoMarçal", "#DeusÉDeus", "#Gospel"],
                "visualizacoes": 12000000
            },
            {
                "titulo": "Ninguém Explica Deus",
                "artista": "Preto no Branco ft. Gabriela Rocha",
                "url": "https://www.youtube.com/watch?v=X6N6W8Gh6yE",
                "hashtags": ["#PretoNoBranco", "#GabrielaRocha", "#Gospel"],
                "visualizacoes": 10000000
            }
        ]
    
    def salvar_cache_musicas(self, musicas: List[Dict]):
        """Salva as músicas encontradas em cache"""
        cache = {
            'data_atualizacao': datetime.now().isoformat(),
            'musicas': musicas
        }
        
        with open('cache_musicas.json', 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    
    def carregar_cache_musicas(self) -> List[Dict]:
        """Carrega músicas do cache"""
        try:
            with open('cache_musicas.json', 'r', encoding='utf-8') as f:
                cache = json.load(f)
                
            # Verificar se o cache é recente (menos de 24h)
            data_cache = datetime.fromisoformat(cache['data_atualizacao'])
            if (datetime.now() - data_cache).days < 1:
                return cache['musicas']
        except:
            pass
        
        return []
