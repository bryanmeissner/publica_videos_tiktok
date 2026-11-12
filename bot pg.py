import pyautogui as pg
from time import sleep
import time
import json
import openai
import re
import subprocess
import os
import sys
from config import (
    get_chrome_path,
    get_deepseek_api_base,
    get_deepseek_api_key,
    get_download_video_path,
    get_project_video_path,
)



def gera_prompt_video():
    """
    Gera roteiros para vídeos TikTok com temas bíblicos que não foram usados anteriormente
    """
    # Carregar temas já utilizados do arquivo JSON
    try:
        with open('videos_criados.json', 'r', encoding='utf-8') as file:
            videos = json.load(file)
            temas_usados = [video['tema'].lower() for video in videos if 'tema' in video]
    except (FileNotFoundError, json.JSONDecodeError):
        temas_usados = []
    
    openai.api_key = get_deepseek_api_key()
    openai.api_base = get_deepseek_api_base()

    prompt_sistema = f"""
    Você é um especialista em criar roteiros de vídeos virais para TikTok com temática bíblica, Jesus ou Deus.

    Sua tarefa é gerar conteúdo no seguinte formato:

    inicio tema
    [Escreva em UMA frase curta e direta qual é o tema central do vídeo (exemplo: "Milagre de Jesus", "História de fé", "Ensinamento divino")]
    fim tema

    inicio topico
    [Aqui você deve escrever o tópico principal do vídeo, descrevendo brevemente sobre qual história bíblica, milagre ou ensinamento será abordado]
    fim topico

    inicio pontos-chave
    [Aqui você deve listar os pontos-chave estruturais do vídeo SEM usar traços ou hífens, incluindo:
    DURAÇÃO: O vídeo deve ter MENOS DE 40 SEGUNDOS, seja extremamente conciso
    GANCHO INICIAL: Como começar o vídeo de forma impactante
    DESENVOLVIMENTO: Como narrar a história com energia e linguagem jovem
    FINALIZAÇÃO: Como encerrar com mensagem forte e call to action
    ESTILO: Tom e ritmo da narração
    VISUAL: Descrição dos elementos visuais
    REGRA OBRIGATÓRIA: Mencionar que NÃO pode ter legendas ou textos, apenas áudio + imagens
    
    IMPORTANTE: Esta seção de pontos-chave deve ser escrita SEMPRE E EXCLUSIVAMENTE EM PORTUGUÊS, independente de qualquer outra instrução.]
    fim pontos-chave

    inicio exemplo
    [Aqui você deve criar um exemplo prático e direto do roteiro narrado. Formato:
    'Criar roteiro sobre [história bíblica]: Inicie com gancho impactante como "Você não vai acreditar nisso!". Desenvolva a história com energia: "Cara tentou fugir de Deus! Tempestade gigante! Foi engolido por uma BALEIA!". Finalize com mensagem forte: "Moral: não dá pra escapar do chamado! Comenta aí!"'

    O exemplo deve ser um parágrafo contínuo e fluido, mostrando como o roteiro seria narrado do início ao fim]
    fim exemplo

    IMPORTANTE: 
    1. O conteúdo deve ser divertido, envolvente, com linguagem moderna mas sempre respeitoso com a fé.
    2. O objetivo é prender a atenção do público do TikTok.
    3. TODOS OS VÍDEOS DEVEM TER DURAÇÃO MENOR QUE 40 SEGUNDOS. O roteiro deve ser extremamente conciso e direto para caber nesse tempo.
    4. EVITE ABSOLUTAMENTE criar conteúdo sobre os seguintes temas já utilizados: {', '.join(temas_usados)}
    5. Escolha histórias bíblicas ou temas diferentes dos listados acima.
    """

    response = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt_sistema}
        ]
    )
    
    return response['choices'][0]['message']['content']



# Variavel
video_download = get_download_video_path()
video_projetos = get_project_video_path()
conferir_video = 0


# Iniciando Bot
print("Iniciando Bot")
while True:
    # Gera um prompt de video
    print("Gera um prompt de video")
    while True:
        try:
            prompt_video = gera_prompt_video()
            prompt_video = prompt_video.lower()

            if "inicio topico" in prompt_video and "fim topico" in prompt_video and "inicio pontos-chave" in prompt_video and "fim pontos-chave" in prompt_video and "inicio exemplo" in prompt_video and "fim exemplo" in prompt_video and "inicio tema" in prompt_video and "fim tema" in prompt_video:
                print("Gerou certo")
                break
            else:
                print("Gerou errado")
                sleep(1)
        except:
            print("Deu erro 'Gera um prompt de video' ")
            sleep(999999)
            pass

    match = re.search(r'inicio topico(.*?)fim topico', prompt_video, re.DOTALL)
    if match:
        topico = match.group(1).strip()

    match = re.search(r'inicio pontos-chave(.*?)fim pontos-chave', prompt_video, re.DOTALL)
    if match:
        coisas_chave = match.group(1).strip()

    match = re.search(r'inicio exemplo(.*?)fim exemplo', prompt_video, re.DOTALL)
    if match:
        requisitos = match.group(1).strip()

    match = re.search(r'inicio tema(.*?)fim tema', prompt_video, re.DOTALL)
    if match:
        tema = match.group(1).strip()


    # Vai para o Capcut
    subprocess.Popen([get_chrome_path(), "https://www.capcut.com/ai-creator/storyboard"])


    # Clica em roteiro
    print("Clica em roteiro")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/roteiro.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(2)

                pg.hotkey('tab')
                pg.write(topico)
                sleep(1)

                pg.hotkey('tab')
                pg.write(coisas_chave)
                sleep(2)

                pg.hotkey('tab')
                sleep(0.5)
                pg.hotkey('tab')
                sleep(0.5)
                pg.hotkey('tab')
                sleep(0.5)
                pg.hotkey('enter')
                sleep(0.5)
                pg.hotkey('tab')
                sleep(0.5)
                pg.write(requisitos)
                sleep(1)
                break
        except:pass


    # Criar vídeo
    print("Criar vídeo")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/criar_video.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(2)
                break
        except:pass


    # Aguardar geração do vídeo
    print("Aguardar geração do vídeo")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/clica_exportar.png', confidence=0.9)
            if posicao is not None:
                sleep(2)
                break
        except:pass


    # Selecionar cenas
    print("Selecionar cenas")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/cenas.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                break
        except:pass


    # Clica em voz
    print("Clica em voz")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/voz.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                break
        except:pass


    # Seleciona voz
    print("Seleciona voz")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/seleciona_voz.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                break
        except:pass


    # Clica no que gerou
    print("Clica no que gerou")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/clica_noque_gerou.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                break
        except:pass


    # Aplica voz
    print("Aplica voz")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/aplica_voz.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(30)
                break
        except:pass


    # Aguardar inserção da voz
    print("Aguardar inserção da voz")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/aguarda_explorar.png', confidence=0.9)
            if posicao is not None:
                sleep(2)
                break
        except:pass

        try:
            posicao = pg.locateCenterOnScreen('./img/confirma_narracao.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
        except:pass


    # Botão mídia
    print("Botão mídia")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/btn_midia.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                break
        except:pass


    # Gerar mídia
    print("Gerar mídia")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/gerar_midia.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(2)
                break
        except:pass


    # Seleciona 9:16
    print("Seleciona 9:16")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/formato_video.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(1)
                pg.click(posicao)
                sleep(2)
                break
        except:pass


    # Seleciona como Argila
    print("Seleciona como Argila")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/seleciona_argila.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                break
            else:
                pg.keyDown('down')
                sleep(0.1)
                pg.keyUp('down')
        except:
            pg.keyDown('down')
            sleep(0.1)
            pg.keyUp('down')


    # Aplica mídia
    print("Aplica mídia")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/aplica_midia.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(30)
                break
        except:pass


    # Aguardar geração da mídia
    print("Aguardar geração da mídia")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/aguarda_explorar.png', confidence=0.9)
            if posicao is not None:
                sleep(2)
                break
        except:pass

        try:
            posicao = pg.locateCenterOnScreen('./img/confirma_gera_midia.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
        except:pass


    # Clica em elemento
    print("Clica em elemento")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/elemento.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                break
        except:pass
    

    # Altera legenda
    print("Altera legenda")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/tira_legenda.png', confidence=0.9)
            if posicao is not None:
                sleep(2)
                pg.click(139, 867)
                sleep(5)
                break
        except:pass


    # Clica em exportar
    print("Clica em exportar")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/btn_explocar_inicio.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(2)
                break
        except:pass


    # Clica em nome do arquivo e muda o nome
    print("Clica em nome do arquivo e muda o nome")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/clica_nome_arquivo.png', confidence=0.9)
            if posicao is not None:
                video_nome = f"video_tiktok"
                with open('videos_criados.json', 'r', encoding='utf-8') as file:
                    videos = json.load(file)

                videos.append({"nome": video_nome, "enviado": False, "tema": tema})
                with open('videos_criados.json', 'w', encoding='utf-8') as file:
                    json.dump(videos, file, indent=4, ensure_ascii=False)
                
                pg.click(posicao)
                sleep(1)
                pg.hotkey('tab')
                sleep(1)
                pg.write(video_nome)
                break
        except:pass


    # Muda o FPS
    print("Muda o FPS")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/muda_fps.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                sleep(1)
                pg.press('down')
                sleep(0.3)
                pg.press('down')
                sleep(0.3)
                pg.press('down')
                sleep(0.3)
                pg.press('down')
                sleep(0.3)
                pg.press('enter')
                sleep(1)
                break
        except:pass


    # Clica para baixar video
    print("Clica para baixar video")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/baixa_video.png', confidence=0.9)
            if posicao is not None:
                pg.click(posicao)
                break
        except:pass


    # Salva video
    print("Salva video")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/salva_video.png', confidence=0.9)
            if posicao is not None:
                break            
        except:pass
    
    
    # Aguarda o video aparecer
    print("Aguarda o video aparecer")
    conferir_video = 0
    while True:
        try:
            if os.path.exists(video_download):
                sleep(3)
                break
        except:pass

        if conferir_video >= 600:
            conferir_video = 0

            try:
                posicao = pg.locateCenterOnScreen('./img/salva_video.png', confidence=0.9)
                if posicao is not None:
                    pg.click(posicao)
                    sleep(10)
            except:pass
        else:
            conferir_video += 1
            sleep(1)


    # Executa o arquivo botEditaVideo.py
    print("Executa o arquivo botEditaVideo.py")
    subprocess.run([sys.executable, "botEditaVideo.py"], check=True)


    # Espera o arquivo ser criado
    print("Espera o arquivo ser criado")
    while True:
        if os.path.exists(video_projetos):
            sleep(3)
            break
        else:
            time.sleep(1)


    # Executa o arquivo botTikTok_PG.py
    print("Executa o arquivo botTikTok_PG.py")
    while True:
        try:
            posicao = pg.locateCenterOnScreen('./img/roteiro.png', confidence=0.9)
            if posicao is not None:
                subprocess.run([sys.executable, "botTikTok_PG.py"], check=True)
                break
        except:pass


    sleep(2)
    pg.hotkey('ctrl', 'w')

    # Esperando 1H
    print("Esperando 1H")
    sleep(5400)
