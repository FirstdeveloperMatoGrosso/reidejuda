# O Rei de Judá - Sistema de Automação de Conteúdo Bíblico para TikTok

Este projeto automatiza a criação e publicação de conteúdo bíblico inspiracional no TikTok, combinando imagens, textos e músicas para criar vídeos impactantes.

## Funcionalidades

- Geração automática de imagens com temática bíblica
- Criação de vídeos com textos bíblicos e músicas inspiradoras
- Busca de músicas populares relacionadas à temática religiosa
- Publicação automática de conteúdo no TikTok
- Monitoramento de estatísticas de engajamento

## Componentes

- `gerar_imagens_biblicas.py`: Gera imagens usando a API da Stability AI
- `criar_video_demo_cv2.py`: Monta vídeos com imagens, texto e música
- `buscador_musicas.py`: Encontra músicas relevantes usando a API do YouTube
- `gerenciador_midia.py`: Gerencia o conteúdo multimídia e suas metadados
- `postador_tiktok.py`: Automatiza a publicação no TikTok
- `gerar_e_postar_video.py`: Script principal que integra todo o fluxo

## Como usar

1. Configure as variáveis de ambiente necessárias (veja `.env.example`)
2. Execute o script principal: `python gerar_e_postar_video.py`
3. Verifique os logs para acompanhar o processo

## Requisitos

- Python 3.8+
- OpenCV
- Requests
- Selenium (para automação web)
- APIs: YouTube, Stability AI, TikTok

## Licença

Este projeto é para uso pessoal. Todos os direitos reservados.
