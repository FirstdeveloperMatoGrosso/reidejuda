from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

def iniciar_servidor():
    # Criar diretório para o arquivo de verificação
    os.makedirs('static', exist_ok=True)
    
    # Configurar o handler
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory='.', **kwargs)
    
    # Iniciar servidor
    server = HTTPServer(('localhost', 8000), Handler)
    print("\nServidor iniciado em http://localhost:8000")
    print("Coloque o arquivo de verificação do TikTok na pasta 'static'")
    print("Pressione Ctrl+C para parar o servidor\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado!")
        server.server_close()

if __name__ == "__main__":
    iniciar_servidor()
