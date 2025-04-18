import os
import io
import base64
from datetime import datetime
from PIL import Image
import requests

def send_generation_request(host, params, files=None):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('STABILITY_KEY')}"
    }
    
    if files is None:
        response = requests.post(f"{host}/v1/generation/{params['engine']}/text-to-image", headers=headers, json={
            "text_prompts": params.get('text_prompts', []),
            "cfg_scale": params.get('cfg_scale', 7),
            "height": params.get('height', 1024),
            "width": params.get('width', 1024),
            "samples": params.get('samples', 1),
            "steps": params.get('steps', 50),
        })
    else:
        response = requests.post(f"{host}/v1/generation/{params['engine']}/image-to-image", headers=headers, files=files, data={
            "init_image_mode": "IMAGE_STRENGTH",
            "image_strength": params.get('image_strength', 0.35),
            "text_prompts[0][text]": params['text_prompts'][0]['text'],
            "cfg_scale": params.get('cfg_scale', 7),
            "samples": params.get('samples', 1),
            "steps": params.get('steps', 50),
        })
    
    if response.status_code != 200:
        raise Exception('Non-200 response: ' + str(response.text))
    
    return response.json()

def gerar_imagem_biblica(prompt, engine="stable-diffusion-xl-1024-v1-0"):
    # Configurar os parâmetros da requisição
    params = {
        'engine': engine,
        'text_prompts': [
            {
                'text': prompt,
                'weight': 1
            },
            {
                'text': 'blurry, low quality, distorted, cartoon, anime',
                'weight': -1
            }
        ],
        'cfg_scale': 7,
        'height': 1024,
        'width': 1024,
        'samples': 1,
        'steps': 50,
    }
    
    # Criar diretório para salvar as imagens se não existir
    if not os.path.exists('imagens_biblicas'):
        os.makedirs('imagens_biblicas')
    
    # Fazer a requisição para gerar a imagem
    response = send_generation_request('https://api.stability.ai', params)
    
    # Processar e salvar as imagens geradas
    for i, image in enumerate(response['artifacts']):
        # Gerar nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"imagens_biblicas/rei_de_juda_{timestamp}_{i}.png"
        
        # Decodificar e salvar a imagem
        image_data = base64.b64decode(image['base64'])
        img = Image.open(io.BytesIO(image_data))
        img.save(image_path)
        print(f"Imagem salva em: {image_path}")
        
    return image_path

# Lista de prompts para gerar imagens bíblicas
prompts = [
    "A majestic biblical king of Judah on a throne, wearing royal robes and crown, dramatic lighting, realistic style, detailed textures, 4k, masterpiece, highly detailed",
    "Ancient Jerusalem temple with divine light shining down, biblical architecture, golden details, dramatic atmosphere, photorealistic, masterpiece, highly detailed",
    "Jesus Christ preaching on a mountain, surrounded by followers, sunset sky, divine rays of light, cinematic composition, ultra detailed, masterpiece, highly detailed",
    "The Lion of Judah, majestic and powerful, biblical symbolism, golden mane, divine light, realistic style, 4k resolution, masterpiece, highly detailed",
    "Biblical scroll with ancient Hebrew text, illuminated by candlelight, detailed parchment texture, atmospheric lighting, photorealistic, masterpiece, highly detailed"
]

if __name__ == "__main__":
    # Verificar se a API key está configurada
    if not os.getenv('STABILITY_KEY'):
        print("Por favor, configure sua API key do Stability AI usando:")
        print('export STABILITY_KEY="sua-api-key-aqui"')
        exit(1)
        
    # Gerar uma imagem para cada prompt
    for i, prompt in enumerate(prompts, 1):
        print(f"\nGerando imagem {i}/5...")
        print(f"Prompt: {prompt}")
        try:
            image_path = gerar_imagem_biblica(prompt)
            print(f"Imagem {i} gerada com sucesso!")
        except Exception as e:
            print(f"Erro ao gerar imagem {i}:", str(e))
