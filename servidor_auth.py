from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Recebendo requisição para: {self.path}")
        
        # Extrair o nome do arquivo de verificação do TikTok
        if 'tiktok' in self.path and self.path.endswith('.txt'):
            filename = os.path.basename(self.path)
            print(f"Tentando servir arquivo de verificação: {filename}")
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    content = f.read()
                    print(f"Arquivo de verificação encontrado")
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(content)
                    return
            print(f"Arquivo de verificação não encontrado")
            self.send_response(404)
            self.end_headers()
            return
            
        # Para outros arquivos
        path = self.path.split('?')[0].lstrip('/')
        if not path:
            path = 'index.html'
            
        print(f"Caminho processado: {path}")
        
        # Verificar extensão do arquivo
        if path.endswith('.html'):
            content_type = 'text/html'
        else:
            content_type = 'text/plain'
            
        # Tentar abrir o arquivo
        try:
            with open(path, 'rb') as f:
                content = f.read()
                print(f"Arquivo encontrado: {path}")
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {path}")
            self.send_response(404)
            self.end_headers()

        # Extrair código de autorização da URL
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        # Página HTML com estilo
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Autenticação TikTok</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f0f2f5;
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    text-align: center;
                }
                .success {
                    color: #28a745;
                    font-size: 24px;
                    margin-bottom: 20px;
                }
                .code {
                    background: #f8f9fa;
                    padding: 10px;
                    border-radius: 5px;
                    font-family: monospace;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
        '''
        
        if 'code' in query_components:
            code = query_components['code'][0]
            html += f'''
                <div class="success">✅ Autenticação realizada com sucesso!</div>
                <p>Seu código de autorização é:</p>
                <div class="code">{code}</div>
                <p>Use este código no seu aplicativo.</p>
            '''
        else:
            html += '''
                <h1>Aguardando autenticação...</h1>
                <p>Por favor, autorize o aplicativo no TikTok.</p>
            '''
            
        html += '''
            </div>
        </body>
        </html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AuthHandler)
    print(f'Servidor rodando na porta {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
