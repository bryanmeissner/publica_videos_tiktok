import json
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
    load_cookies,
)




# Função para carregar o JSON e obter o próximo vídeo não enviado
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

cookies = load_cookies("TIKTOK_COOKIES_FILE", "cookies_tiktok.json")

descricao = gera_prompt_video()
caminho_json = './videos_criados.json'
nome_video, videos = obter_proximo_video('./videos_criados.json')
tentativas = 0


if nome_video:
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
            except:pass
        

        # Confirma verificação
        while True:
            try:
                if page.locator('button.Button__root--size-medium:nth-child(2)').is_visible():
                    page.click('button.Button__root--size-medium:nth-child(2)')
                    break
            except:pass

            if tentativas >= 10:
                tentativas = 0
                break
            else:
                tentativas += 1
                sleep(1)
        

        # Espera até terminar o upload
        while True:
            try:
                if page.locator('.info-status > span:nth-child(2)').is_visible():
                    texto = page.locator('.info-status > span:nth-child(2)').inner_text()

                    if "Uploaded" in texto:break
                    else:print(texto)
            except:
                break

            if tentativas >= 10:
                tentativas = 0
                break
            else:
                tentativas += 1
                sleep(1)
        

        # Escreve Descrição
        while True:
            try:
                if page.locator('.notranslate').is_visible():
                    page.fill('.notranslate', '')
                    page.type('.notranslate', descricao)
                    break
            except:pass
        

        # Clica em postar
        while True:
            try:
                if page.locator('.button-group > button:nth-child(1)').is_visible():
                    page.click('.button-group > button:nth-child(1)')
                    break
            except:pass


        # Confirma postagem
        while True:
            try:
                if page.locator('button.TUXButton:nth-child(2)').is_visible():
                    page.click('button.TUXButton:nth-child(2)')
                    break
            except:pass

            if tentativas >= 10:
                tentativas = 0
                break
            else:
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





