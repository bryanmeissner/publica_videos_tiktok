import pyautogui as pg
from time import sleep
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
    get_img_path,
    get_project_video_path,
    get_videos_json_path,
    load_videos_json,
    save_videos_json,
)


def obter_proximo_video(caminho_json=None):
    caminho = caminho_json or get_videos_json_path()
    tentativas = 0
    max_tentativas = 5

    while tentativas < max_tentativas:
        try:
            videos = load_videos_json(caminho)
            for video in videos:
                if not video.get('enviado'):
                    nome_arquivo = os.path.join(str(get_downloads_dir()), f"{video['nome']}.mp4")
                    caminho_download = get_download_video_path()
                    caminho_projeto = get_project_video_path()
                    if (
                        (os.path.exists(nome_arquivo) and nome_arquivo.endswith('.mp4'))
                        or (os.path.exists(caminho_download) and caminho_download.endswith('.mp4'))
                        or (os.path.exists(caminho_projeto) and caminho_projeto.endswith('.mp4'))
                    ):
                        return video['nome'], videos
                    else:
                        # Atualiza o status de envio para True se o arquivo não existir ou não for .mp4
                        video['enviado'] = True
                        atualizar_status_video(caminho, videos)
            return None, videos
        except Exception as e:
            print(f"Erro ao tentar obter o próximo vídeo: {e}")
            tentativas += 1
            sleep(2)  # Espera 2 segundos antes de tentar novamente

    print("Número máximo de tentativas atingido ao tentar obter o próximo vídeo.")
    return None, []

def atualizar_status_video(caminho_json, videos):
    save_videos_json(videos, caminho_json)

def gera_prompt_video():
    """
    Gera uma descrição genérica e viral para vídeos do TikTok usando DeepSeek.
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



def main():
    caminho_json = get_videos_json_path()
    nome_video, videos = obter_proximo_video(caminho_json)
    if not nome_video:
        print("Nenhum vídeo pendente encontrado para publicação.")
        return

    arquivo_downloads = get_download_video_path()
    arquivo_projetos = get_project_video_path()

    sleep(2)
    subprocess.Popen([get_chrome_path(), "https://www.tiktok.com/tiktokstudio/upload?from=creator_center/"])

    # Aguarda aparecer o botão
    while True:
        try:
            posicao = pg.locateCenterOnScreen(get_img_path('seleciona_video.png'), confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                break
        except Exception:
            pass

        try:
            posicao = pg.locateCenterOnScreen(get_img_path('mais_carregar.png'), confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(2)
        except Exception:
            pass

    # Aguarda aparecer a janela de inserir o video
    caminho_upload = os.path.abspath(arquivo_projetos)
    while True:
        for img_janela in ('janela_video.png', 'janela_video2.png', 'janela_video3.png'):
            try:
                posicao = pg.locateCenterOnScreen(get_img_path(img_janela), confidence=0.9)
                if posicao is not None:
                    sleep(2)
                    pyperclip.copy(caminho_upload)
                    pg.hotkey('ctrl', 'v')
                    sleep(1)
                    pg.press('enter')
                    sleep(5)
                    break
            except Exception:
                pass
        else:
            continue
        break
    # Clica na descricao do video
    while True:
        try:
            posicao = pg.locateCenterOnScreen(get_img_path('descricao_video.png'), confidence=0.9)
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
        except Exception:
            pass

    # Vai para baixo até encontrar o botão
    while True:
        try:
            posicao = pg.locateCenterOnScreen(get_img_path('publicar_video.png'), confidence=0.9)
            if posicao is not None:
                sleep(2)
                posicao = pg.locateCenterOnScreen(get_img_path('publicar_video.png'), confidence=0.9)
                pg.click(posicao)
                sleep(3)
                break
        except Exception:
            pass

        pg.scroll(-300, x=500, y=500)

    # Clica no confirmar a publicacao
    while True:
        try:
            posicao = pg.locateCenterOnScreen(get_img_path('publicar_agora_video.png'), confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(2)
        except Exception:
            pass

        try:
            posicao = pg.locateCenterOnScreen(get_img_path('mais_carregar.png'), confidence=0.9)
            if posicao is not None:
                sleep(10)
                break
        except Exception:
            pass

    # Altera para não usar o mesmo video
    for video in videos:
        if not video.get('enviado') and video.get('nome') == nome_video:
            video['enviado'] = True
            break
    atualizar_status_video(caminho_json, videos)

    # Deleta o vídeo após a postagem
    if os.path.exists(arquivo_downloads):
        os.remove(arquivo_downloads)

    if os.path.exists(arquivo_projetos):
        os.remove(arquivo_projetos)

    pg.keyDown('ctrl')
    pg.press('w')
    pg.keyUp('ctrl')


if __name__ == "__main__":
    main()
