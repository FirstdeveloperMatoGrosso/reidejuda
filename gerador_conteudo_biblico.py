import json
from datetime import datetime
import random

class GeradorConteudoBiblico:
    def __init__(self):
        self.versiculos_populares = {
            "João 3:16": "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.",
            "Filipenses 4:13": "Posso todas as coisas naquele que me fortalece.",
            "Salmos 23:1": "O Senhor é meu pastor, nada me faltará.",
            "Jeremias 29:11": "Porque eu bem sei os pensamentos que tenho a vosso respeito, diz o Senhor; pensamentos de paz, e não de mal, para vos dar o fim que esperais.",
            "Romanos 8:28": "E sabemos que todas as coisas contribuem juntamente para o bem daqueles que amam a Deus.",
            "Isaías 41:10": "Não temas, porque eu sou contigo; não te assombres, porque eu sou teu Deus.",
        }

        self.temas_videos = [
            {
                "categoria": "Versículos Diários",
                "formato": "Short-form vertical",
                "duracao": "15-30 segundos",
                "elementos": [
                    "Música de fundo suave",
                    "Texto do versículo aparecendo gradualmente",
                    "Imagens de natureza ou cenários contemplativos",
                    "Efeitos de transição suaves"
                ],
                "hashtags": ["#Biblia", "#Fé", "#Deus", "#VersiculoDoDia", "#Jesus"]
            },
            {
                "categoria": "Histórias Bíblicas",
                "formato": "Storytelling",
                "duracao": "45-60 segundos",
                "elementos": [
                    "Narração envolvente",
                    "Imagens ilustrativas",
                    "Textos-chave destacados",
                    "Música de fundo dramática"
                ],
                "hashtags": ["#HistoriaBiblica", "#Biblia", "#Fe", "#Jesus", "#Cristianismo"]
            },
            {
                "categoria": "Reflexões",
                "formato": "Vlog style",
                "duracao": "30-45 segundos",
                "elementos": [
                    "Fala direta para câmera",
                    "Versículo base",
                    "Aplicação prática",
                    "Call-to-action para reflexão"
                ],
                "hashtags": ["#ReflexaoBiblica", "#Fe", "#Deus", "#Reflexao", "#Oracao"]
            }
        ]

        self.templates_post = [
            {
                "tipo": "Versículo + Imagem",
                "estilo": "Minimalista",
                "cores": ["#1E1E1E", "#FFFFFF", "#FFD700"],
                "fontes": ["Montserrat", "Roboto"],
                "elementos": [
                    "Versículo em destaque",
                    "Referência bíblica",
                    "Fundo com imagem suave",
                    "Logo ou marca d'água"
                ]
            },
            {
                "tipo": "Citação Inspiradora",
                "estilo": "Moderno",
                "cores": ["#2C3E50", "#ECF0F1", "#E74C3C"],
                "fontes": ["Lato", "Open Sans"],
                "elementos": [
                    "Texto inspirador",
                    "Versículo de apoio",
                    "Elementos gráficos minimalistas",
                    "Hashtags relevantes"
                ]
            },
            {
                "tipo": "Série de Stories",
                "estilo": "Dinâmico",
                "cores": ["#34495E", "#F1C40F", "#FFFFFF"],
                "fontes": ["Poppins", "Roboto"],
                "elementos": [
                    "3-5 slides conectados",
                    "Progressão da mensagem",
                    "Elementos visuais consistentes",
                    "Call-to-action final"
                ]
            }
        ]

    def gerar_ideia_post(self):
        """Gera uma ideia completa para um post no TikTok"""
        versiculo = random.choice(list(self.versiculos_populares.items()))
        template = random.choice(self.templates_post)
        
        ideia = {
            "titulo": f"Post Bíblico - {datetime.now().strftime('%d/%m/%Y')}",
            "versiculo": {
                "referencia": versiculo[0],
                "texto": versiculo[1]
            },
            "template": template,
            "sugestoes": [
                "Use transições suaves entre elementos",
                "Mantenha o texto legível (fonte clara e grande)",
                "Adicione música de fundo suave e inspiradora",
                "Inclua elementos visuais que complementem a mensagem"
            ],
            "hashtags": [
                "#BibliaNoTikTok",
                "#VersiculoDoDia",
                "#Fe",
                "#Jesus",
                "#Deus",
                f"#{versiculo[0].replace(' ', '').replace(':', '')}"
            ]
        }
        return ideia

    def gerar_ideia_video(self):
        """Gera uma ideia completa para um vídeo no TikTok"""
        tema = random.choice(self.temas_videos)
        versiculo = random.choice(list(self.versiculos_populares.items()))
        
        ideia = {
            "titulo": f"Vídeo Bíblico - {tema['categoria']}",
            "tema": tema,
            "versiculo_base": {
                "referencia": versiculo[0],
                "texto": versiculo[1]
            },
            "roteiro": {
                "introducao": "Gancho inicial de 3 segundos",
                "desenvolvimento": "Apresentação do versículo e contexto",
                "aplicacao": "Como aplicar na vida prática",
                "conclusao": "Call-to-action e fechamento"
            },
            "elementos_tecnicos": {
                "duracao": tema["duracao"],
                "formato": "Vertical (9:16)",
                "musica": "Instrumental suave de fundo",
                "elementos_visuais": tema["elementos"]
            },
            "hashtags": tema["hashtags"]
        }
        return ideia

    def salvar_ideia(self, ideia, tipo="post"):
        """Salva a ideia gerada em um arquivo JSON"""
        nome_arquivo = f"ideia_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(ideia, f, ensure_ascii=False, indent=4)
        return nome_arquivo

def main():
    gerador = GeradorConteudoBiblico()
    
    # Gerar ideia para post
    ideia_post = gerador.gerar_ideia_post()
    arquivo_post = gerador.salvar_ideia(ideia_post, "post")
    print(f"\nIdeia de post gerada e salva em: {arquivo_post}")
    
    # Gerar ideia para vídeo
    ideia_video = gerador.gerar_ideia_video()
    arquivo_video = gerador.salvar_ideia(ideia_video, "video")
    print(f"\nIdeia de vídeo gerada e salva em: {arquivo_video}")

if __name__ == "__main__":
    main()
