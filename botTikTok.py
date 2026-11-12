from playwright.sync_api import sync_playwright
from time import sleep
import openai
import os
from config import (
    get_deepseek_api_base,
    get_deepseek_api_key,
    get_download_video_path,
    get_downloads_dir,
    get_project_video_path,
    get_videos_json_path,
    load_cookies,
    load_videos_json,
    save_videos_json,
)


# Função para carregar o JSON e obter o próximo vídeo não enviado
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

    3. **Tamanho**: Entre 120-180 caracteres (sem contar as hashtags).

    4. **Tom**: Casual, amigável, divertido e inspirador. Pode usar emojis estrategicamente (2-4 emojis no máximo).

    5. **Hashtags OBRIGATÓRIAS**: Após a descrição, adicione uma linha em branco e inclua AS SEGUINTES HASHTAGS QUE DEVEM APARECER EM TODA DESCRIÇÃO:
    #biblia #deus #jesus #cristao

    Depois dessas 4 hashtags obrigatórias, adicione mais 8 a 12 hashtags GENÉRICAS sobre o tema cristão/bíblico (exemplos: #fe, #historiasbiblicas, #palavradedeus, #vidacrista, #evangelico, #reflexao, #motivacao, #feemeacao, #igrejatiktok, #gospel, #vidacomcristo, #bibliasagrada, etc.).

    6. **IMPORTANTE**: As hashtags #biblia #deus #jesus #cristao devem SEMPRE ser as primeiras quatro hashtags, nessa ordem.

    Formato final obrigatório:
    [Descrição genérica sobre o canal com CTAs e emojis]

    #biblia #deus #jesus #cristao [8 a 12 hashtags genéricas adicionais]

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

    cookies = load_cookies("TIKTOK_COOKIES_FILE", "cookies_tiktok.json")
    descricao = gera_prompt_video()
    tentativas = 0

    with sync_playwright() as p:
        # Inicia o navegador
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        context.add_cookies(cookies)

        # Navega para a página de upload
        page.goto("https://www.tiktok.com/tiktokstudio/upload?from=upload")

        # Seleciona o arquivo para upload
        while True:
            try:
                if page.locator('button[class="upload-stage-btn Button__root Button__root--shape-default Button__root--size-large Button__root--type-primary Button__root--loading-false"]').is_visible():
                    caminho_arquivo = get_project_video_path()
                    page.set_input_files('input[type="file"]', caminho_arquivo)

                    for video in videos:
                        if video['nome'] == nome_video:
                            video['enviado'] = True
                            break
                    atualizar_status_video(caminho_json, videos)
                    break
            except Exception:
                pass

        # Confirma verificação
        tentativas = 0
        while True:
            try:
                if page.locator('button.Button__root--size-medium:nth-child(2)').is_visible():
                    page.click('button.Button__root--size-medium:nth-child(2)')
                    break
            except Exception:
                pass

            if tentativas >= 10:
                break
            tentativas += 1
            sleep(1)

        # Espera até terminar o upload
        tentativas = 0
        while True:
            try:
                if page.locator('.info-status > span:nth-child(2)').is_visible():
                    texto = page.locator('.info-status > span:nth-child(2)').inner_text()

                    if "Uploaded" in texto:
                        break
                    else:
                        print(texto)
            except Exception:
                break

            if tentativas >= 180:
                break
            tentativas += 1
            sleep(1)
        # Escreve Descrição
        while True:
            try:
                if page.locator('.notranslate').is_visible():
                    page.fill('.notranslate', '')
                    page.type('.notranslate', descricao)
                    break
            except Exception:
                pass

        # Clica em postar
        while True:
            try:
                if page.locator('.button-group > button:nth-child(1)').is_visible():
                    page.click('.button-group > button:nth-child(1)')
                    break
            except Exception:
                pass

        # Confirma postagem
        tentativas = 0
        while True:
            try:
                if page.locator('button.TUXButton:nth-child(2)').is_visible():
                    page.click('button.TUXButton:nth-child(2)')
                    break
            except Exception:
                pass

            if tentativas >= 10:
                break
            tentativas += 1
            sleep(1)

        # Deleta o vídeo após a postagem
        caminho_arquivo = get_project_video_path()
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

        caminho_arquivo = get_download_video_path()
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

        sleep(5)
        browser.close()


if __name__ == "__main__":
    main()
