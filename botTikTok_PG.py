import pyautogui as pg
from time import sleep
import json
import openai
import os
import pyperclip
import subprocess
from config import (
    get_chrome_path,
    get_deepseek_api_base,
    get_deepseek_api_key,
    get_download_video_path,
    get_downloads_dir,
    get_project_video_path,
)


def obter_proximo_video(caminho_json):
    tentativas = 0
    max_tentativas = 100

    while tentativas < max_tentativas:
        try:
            with open(caminho_json, 'r', encoding='utf-8') as arquivo:
                videos = json.load(arquivo)
            for video in videos:
                if not video['enviado']:
                    nome_arquivo = os.path.join(str(get_downloads_dir()), f"{video['nome']}.mp4")
                    if os.path.exists(nome_arquivo) and nome_arquivo.endswith('.mp4'):
                        return video['nome'], videos
                    else:
                        # Atualiza o status de envio para True se o arquivo não existir ou não for .mp4
                        video['enviado'] = True
                        atualizar_status_video(caminho_json, videos)
            return None, videos
        except Exception as e:
            print(f"Erro ao tentar obter o próximo vídeo: {e}")
            tentativas += 1
            sleep(2)  # Espera 2 segundos antes de tentar novamente

    print("Número máximo de tentativas atingido ao tentar obter o próximo vídeo.")
    return None, []

def atualizar_status_video(caminho_json, videos):
    with open(caminho_json, 'w', encoding='utf-8') as arquivo:
        json.dump(videos, arquivo, indent=4, ensure_ascii=False)

def gera_prompt_video():
    """
    Gera títulos otimizados para marketplace
    """
    openai.api_key = get_deepseek_api_key()
    openai.api_base = get_deepseek_api_base()

    prompt_sistema = f"""
    Você é um especialista em criar descrições envolventes e virais para vídeos do TikTok sobre conteúdo bíblico e cristão.
    Sua tarefa é gerar uma descrição GENÉRICA e atraente para o TikTok que funcione para QUALQUER tipo de vídeo sobre Bíblia, Deus, Jesus e histórias cristãs.
    A descrição NÃO deve mencionar detalhes específicos do conteúdo do vídeo, mas sim:
    - Falar sobre o canal de forma geral
    - Convidar para seguir/se inscrever
    - Incentivar engajamento (curtir, comentar, compartilhar)
    - Ser inspiradora e convidativa
    
    Diretrizes obrigatórias:
    1. **Conteúdo**: Crie uma descrição que fale sobre o canal de vídeos divertidos e inspiradores sobre a Bíblia, Deus, Jesus e histórias bíblicas, SEM mencionar o tema específico do vídeo atual.
    
    2. **Chamadas para ação**: Inclua convites como:
    - Seguir o canal para mais conteúdo
    - Curtir e comentar
    - Compartilhar com amigos
    - Ativar notificações
    
    3. **Tamanho**: Entre 120-180 caracteres.
    
    4. **Tom**: Casual, amigável, divertido e inspirador. Pode usar emojis estrategicamente (2-4 emojis no máximo).
    
    5. **IMPORTANTE**: NÃO inclua hashtags na descrição. Gere APENAS o texto da descrição.
    
    Formato final obrigatório:
    [Descrição genérica sobre o canal com CTAs e emojis - SEM HASHTAGS]
    
    LEMBRE-SE: A descrição deve ser AMBÍGUA e funcionar para QUALQUER vídeo do canal, seja sobre milagres, parábolas, personagens bíblicos, ensinamentos, histórias engraçadas, reflexões, etc.
    
    Agora gere UMA descrição genérica para o canal:
    """

    response = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt_sistema}
        ]
    )
    
    return response['choices'][0]['message']['content']



nome_video, videos = obter_proximo_video('./videos_criados.json')
error = 0
arquivo_downloads = get_download_video_path()
arquivo_projetos = get_project_video_path()





sleep(2)
# Abre uma nova guia e vai para o local
#pg.keyDown('ctrl')
#pg.press('t')
#pg.keyUp('ctrl')
#sleep(2)
#pg.write('https://www.tiktok.com/tiktokstudio/upload?from=creator_center/')
#sleep(1)
#pg.press('backspace')
#sleep(1)
#pg.press('Enter')
subprocess.Popen([get_chrome_path(), "https://www.tiktok.com/tiktokstudio/upload?from=creator_center/"])




# Aguarda aparecer o botão 
while True:
    try:
        posicao = pg.locateCenterOnScreen('./img/seleciona_video.png', confidence=0.9)
        if posicao is not None:
            pg.click(posicao)
            break
    except:pass

    try:
        posicao = pg.locateCenterOnScreen('./img/mais_carregar.png', confidence=0.9)
        if posicao is not None:
            pg.click(posicao)
            sleep(2)
    except:pass


# Aguarda aparecer a janela de inserir o video
while True:
    try:
        posicao = pg.locateCenterOnScreen('./img/janela_video.png', confidence=0.9)
        if posicao is not None:
            sleep(2)
            pg.write("video")
            
            sleep(2)
            pg.press('down')
            sleep(1)
            pg.press('Enter')
            sleep(5)
            break
    except:pass

    try:
        posicao = pg.locateCenterOnScreen('./img/janela_video2.png', confidence=0.9)
        if posicao is not None:
            sleep(2)
            pg.write("video")
            
            sleep(2)
            pg.press('down')
            sleep(1)
            pg.press('Enter')
            sleep(5)
            break
    except:pass

    try:
        posicao = pg.locateCenterOnScreen('./img/janela_video3.png', confidence=0.9)
        if posicao is not None:
            sleep(2)
            pg.write("video")
            
            sleep(2)
            pg.press('down')
            sleep(1)
            pg.press('Enter')
            sleep(5)
            break
    except:pass


# Clica na descricao do video
while True:
    try:
        posicao = pg.locateCenterOnScreen('./img/descricao_video.png', confidence=0.9)
        if posicao is not None:
            pg.click(posicao)
            sleep(1)
            pg.press('tab')
            sleep(1)

            pg.keyDown('ctrl')
            pg.press('a')
            pg.keyUp('ctrl')
            sleep(1)

            descricao = gera_prompt_video()
            pyperclip.copy(descricao)
            pg.hotkey('ctrl', 'v')
            sleep(0.5)
            pg.press('Enter')
            sleep(0.5)
            pg.press('Enter')
            sleep(0.5)
            pg.press('Enter')

            pg.write("#biblia", interval=0.1)
            sleep(2)
            pg.press('Enter')
            pg.press('space')
            sleep(0.2)

            pg.write("#jesus", interval=0.1)
            sleep(2)
            pg.press('Enter')
            pg.press('space')
            sleep(0.2)
            
            pg.write("#cristo", interval=0.1)
            sleep(2)
            pg.press('Enter')
            pg.press('space')
            sleep(0.2)

            pg.write("#fe", interval=0.1)
            sleep(2)
            pg.press('Enter')
            pg.press('space')
            sleep(0.2)

            pg.write("#vidacrista", interval=0.1)
            sleep(2)
            pg.press('Enter')
            pg.press('space')
            sleep(0.2)
            
            pg.write("#evangelico", interval=0.1)
            sleep(2)
            pg.press('Enter')
            pg.press('space')
            sleep(0.2)

            pg.write("#reflexao", interval=0.1)
            sleep(2)
            pg.press('Enter')
            pg.press('space')
            sleep(0.2)
            
            pg.write("#motivacao", interval=0.1)
            sleep(2)
            pg.press('Enter')
            pg.press('space')
            sleep(0.2)

            pg.write("#gospel", interval=0.1)
            sleep(2)
            pg.press('Enter')
            pg.press('space')
            sleep(0.2)
            break
    except:pass


# Vai para baixo até encontrar o botão
while True:
    try:
        posicao = pg.locateCenterOnScreen('./img/publicar_video.png', confidence=0.9)
        if posicao is not None:
            sleep(2)
            posicao = pg.locateCenterOnScreen('./img/publicar_video.png', confidence=0.9)
            pg.click(posicao)
            sleep(3)
            break
    except:pass

    pg.scroll(-300, x=500, y=500)


# Clica no confirmar a publicacao
while True:
    try:
        posicao = pg.locateCenterOnScreen('./img/publicar_agora_video.png', confidence=0.9) 
        if posicao is not None:
            pg.click(posicao)
            sleep(2)
    except:pass

    try:
        posicao = pg.locateCenterOnScreen('./img/mais_carregar.png', confidence=0.9)
        if posicao is not None:
            sleep(10)
            break
    except:pass


# Altera para não usar o mesmo video
for video in videos:
    if video['enviado'] == False:
        video['enviado'] = True
        break
atualizar_status_video('./videos_criados.json', videos)


# Deleta o vídeo após a postagem
if os.path.exists(arquivo_downloads):
    os.remove(arquivo_downloads)

if os.path.exists(arquivo_projetos):
    os.remove(arquivo_projetos)


pg.keyDown('ctrl')
pg.press('w')
pg.keyUp('ctrl')