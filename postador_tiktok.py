import os
import json
from datetime import datetime
from typing import Dict, List
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PostadorTikTok:
    def __init__(self):
        self.email = os.getenv('TIKTOK_EMAIL')
        self.senha = os.getenv('TIKTOK_PASSWORD')
        self.cookies_file = 'tiktok_cookies.json'
        self.driver = None
        
    def _inicializar_driver(self):
        """Inicializa o driver do Selenium"""
        if not self.driver:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Modo headless
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(options=options)
    
    def _carregar_cookies(self) -> bool:
        """Carrega cookies salvos se existirem"""
        try:
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                return True
        except:
            pass
        return False
    
    def _salvar_cookies(self):
        """Salva cookies após login"""
        with open(self.cookies_file, 'w') as f:
            json.dump(self.driver.get_cookies(), f)
    
    def _fazer_login(self) -> bool:
        """Faz login no TikTok"""
        try:
            self.driver.get('https://www.tiktok.com/login')
            
            # Tentar carregar cookies primeiro
            if self._carregar_cookies():
                self.driver.get('https://www.tiktok.com/')
                if 'login' not in self.driver.current_url:
                    return True
            
            # Se não tiver cookies ou estiverem expirados, fazer login
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.send_keys(self.email)
            
            senha_input = self.driver.find_element(By.NAME, "password")
            senha_input.send_keys(self.senha)
            
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Esperar login completar
            time.sleep(5)
            
            if 'login' not in self.driver.current_url:
                self._salvar_cookies()
                return True
                
            return False
            
        except Exception as e:
            print(f"Erro ao fazer login: {str(e)}")
            return False
    
    def postar_video(self, video_path: str, titulo: str, tags: List[str]) -> Dict:
        """Posta um vídeo no TikTok usando automação web"""
        try:
            self._inicializar_driver()
            
            if not self._fazer_login():
                return {
                    'success': False,
                    'error': 'Falha ao fazer login'
                }
            
            # Ir para página de upload
            self.driver.get('https://www.tiktok.com/upload')
            
            # Esperar campo de upload aparecer
            upload_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            
            # Fazer upload do vídeo
            upload_input.send_keys(video_path)
            
            # Esperar vídeo carregar
            time.sleep(10)
            
            # Adicionar título
            caption_input = self.driver.find_element(By.CSS_SELECTOR, "[data-text='true']")
            caption_input.clear()
            caption_input.send_keys(f"{titulo}\n\n{' '.join(tags)}")
            
            # Clicar em postar
            post_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
            post_button.click()
            
            # Esperar postagem completar
            time.sleep(10)
            
            return {
                'success': True,
                'share_url': self.driver.current_url
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro ao postar vídeo: {str(e)}'
            }
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    def salvar_historico_posts(self, post_info: Dict):
        """Salva informações do post para histórico"""
        try:
            historico_path = 'historico_posts.json'
            historico = []
            
            # Carregar histórico existente
            if os.path.exists(historico_path):
                with open(historico_path, 'r', encoding='utf-8') as f:
                    historico = json.load(f)
            
            # Adicionar novo post
            post_info['data_post'] = datetime.now().isoformat()
            historico.append(post_info)
            
            # Salvar histórico atualizado
            with open(historico_path, 'w', encoding='utf-8') as f:
                json.dump(historico, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Erro ao salvar histórico: {str(e)}")
    
    def obter_estatisticas_post(self, post_id: str) -> Dict:
        """Obtém estatísticas de um post específico"""
        if not self.access_token or not self.open_id:
            return {}
            
        try:
            url = f"{self.base_url}/video/query/"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'open_id': self.open_id,
                'post_ids': [post_id]
            }
            
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if response.ok and result.get('data', {}).get('videos'):
                video = result['data']['videos'][0]
                return {
                    'visualizacoes': video.get('stats', {}).get('view_count', 0),
                    'likes': video.get('stats', {}).get('like_count', 0),
                    'comentarios': video.get('stats', {}).get('comment_count', 0),
                    'compartilhamentos': video.get('stats', {}).get('share_count', 0)
                }
            
            return {}
            
        except Exception as e:
            print(f"Erro ao obter estatísticas: {str(e)}")
            return {}
