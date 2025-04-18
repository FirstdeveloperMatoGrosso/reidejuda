from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import json

class GeradorVideosBiblicos:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.base_dir, 'assets')
        
        # Versículos para teste
        self.versiculos = {
            "João 3:16": "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.",
            "Salmos 23:1": "O Senhor é meu pastor, nada me faltará.",
            "Filipenses 4:13": "Posso todas as coisas naquele que me fortalece."
        }

        # Hashtags populares
        self.hashtags = [
            "#biblia", "#jesus", "#deus", "#fe", "#amor", "#paz",
            "#versiculododia", "#deusefiel", "#christ", "#god"
        ]

    def criar_imagem_versiculo(self, versiculo, referencia):
        """Cria uma imagem com o versículo"""
        # Configurações da imagem
        width = 1080  # Largura padrão do TikTok
        height = 1920  # Altura padrão do TikTok
        
        # Criar imagem com fundo gradiente
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Desenhar fundo gradiente (simulado com retângulos)
        for y in range(height):
            cor = int(255 * (1 - y/height))
            draw.line([(0, y), (width, y)], fill=(cor, cor, cor))
        
        # Adicionar texto do versículo
        texto = f'{versiculo}\n\n- {referencia}'
        
        # Quebrar texto em linhas
        palavras = texto.split()
        linhas = []
        linha_atual = []
        
        for palavra in palavras:
            linha_atual.append(palavra)
            if len(' '.join(linha_atual)) > 30:  # ajuste este valor conforme necessário
                linhas.append(' '.join(linha_atual[:-1]))
                linha_atual = [palavra]
        if linha_atual:
            linhas.append(' '.join(linha_atual))
        
        # Desenhar texto
        y = height // 3
        for linha in linhas:
            draw.text((width//2, y), linha, fill='black', anchor='mm')
            y += 50
        
        # Salvar imagem
        output_path = os.path.join(self.assets_dir, f'versiculo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        img.save(output_path)
        return output_path

    def gerar_post(self):
        """Gera um post completo com imagem e texto"""
        # Selecionar versículo aleatório
        referencia = list(self.versiculos.keys())[0]
        versiculo = self.versiculos[referencia]
        
        # Criar imagem
        imagem_path = self.criar_imagem_versiculo(versiculo, referencia)
        
        # Gerar texto do post
        texto = f"""✝️ {referencia}
📖 {versiculo}

{' '.join(self.hashtags[:5])}"""
        
        return {
            'imagem': imagem_path,
            'texto': texto,
            'hashtags': ' '.join(self.hashtags[5:])
        }

def main():
    print("Iniciando gerador de conteúdo bíblico...")
    gerador = GeradorVideosBiblicos()
    
    # Gerar post de teste
    post = gerador.gerar_post()
    
    print("\nPost gerado com sucesso!")
    print(f"\nImagem salva em: {post['imagem']}")
    print("\nTexto do post:")
    print("-" * 50)
    print(post['texto'])
    print("\nHashtags adicionais:")
    print(post['hashtags'])
    print("-" * 50)

if __name__ == "__main__":
    main()
