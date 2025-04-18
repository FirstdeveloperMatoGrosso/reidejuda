import os
from criar_video_demo_cv2 import criar_video_demo
from postador_tiktok import PostadorTikTok
from gerenciador_midia import GerenciadorMidia
import time
from datetime import datetime
import json

def main():
    try:
        print("\n=== Iniciando geração e postagem de vídeo ===")
        
        # 1. Gerar vídeo
        print("\nGerando vídeo...")
        video_path = criar_video_demo()
        
        if not os.path.exists(video_path):
            print(f"Erro: Vídeo não foi gerado em {video_path}")
            return
            
        # 2. Preparar dados para postagem
        midia = GerenciadorMidia()
        musica = midia.obter_musica_aleatoria()
        
        # Obter hashtags populares
        hashtags = (
            midia.obter_hashtags(10) +  # Hashtags gerais
            musica.get('hashtags', []) +  # Hashtags da música
            ['#OReiDeJuda', '#ConteudoBiblico', '#SemanaSanta']  # Hashtags fixas
        )
        
        # Remover duplicatas e limitar a 15 hashtags
        hashtags = list(dict.fromkeys(hashtags))[:15]
        
        # 3. Postar no TikTok
        print("\nPostando no TikTok...")
        postador = PostadorTikTok()
        
        titulo = f"✝️ Semana Santa 2025 | {musica['titulo']} 🙏"
        resultado = postador.postar_video(
            video_path=video_path,
            titulo=titulo,
            tags=hashtags
        )
        
        # 4. Salvar resultado
        if resultado['success']:
            print("\n✅ Vídeo postado com sucesso!")
            print(f"URL: {resultado.get('share_url', 'N/A')}")
            
            # Salvar informações do post
            info_post = {
                'titulo': titulo,
                'musica': musica['titulo'],
                'artista': musica['artista'],
                'hashtags': hashtags,
                'url_post': resultado.get('share_url'),
                'post_id': resultado.get('post_id')
            }
            postador.salvar_historico_posts(info_post)
            
            # Aguardar um pouco e buscar estatísticas iniciais
            time.sleep(60)  # Esperar 1 minuto
            stats = postador.obter_estatisticas_post(resultado['post_id'])
            
            if stats:
                print("\nEstatísticas iniciais:")
                print(f"👀 Visualizações: {stats['visualizacoes']}")
                print(f"❤️ Likes: {stats['likes']}")
                print(f"💬 Comentários: {stats['comentarios']}")
                print(f"🔄 Compartilhamentos: {stats['compartilhamentos']}")
        else:
            print(f"\n❌ Erro ao postar vídeo: {resultado.get('error', 'Erro desconhecido')}")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {str(e)}")

if __name__ == "__main__":
    main()
