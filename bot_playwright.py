from playwright.sync_api import sync_playwright
from time import sleep
import time
import os
import subprocess
from config import get_downloads_output_dir, load_cookies


def abrir_pasta_downloads(download_path: str) -> None:
    if os.name == "nt":
        subprocess.Popen(["explorer", download_path])


coisas_chave = """
ABERTURA: Gancho explosivo tipo 'Você NÃO vai acreditar no que aconteceu' ou 'A história mais louca da Bíblia'
DESENVOLVIMENTO: Conte com entusiasmo máximo. Linguagem descontraída e moderna. Adicione reações: 'Imagina a cena!', 'Plot twist total!'. Mantenha respeito
ENCERRAMENTO: Lição impactante + interação 'Comenta aí' ou 'Quer mais histórias assim?'
TOM: Storytelling cativante, como quem conta fofoca interessante para os amigos
ELEMENTOS VISUAIS: Sequência de imagens dramáticas, mudanças rápidas de cena, música envolvente
REGRA ESSENCIAL: Proibido usar legendas ou qualquer texto escrito. Somente voz + imagens
"""
topico = "Vídeo viral para TikTok sobre passagens bíblicas surpreendentes com narração dinâmica"
requisitos = "Criar roteiro viral narrando Jonas e a baleia: 'Cara tentou FUGIR de Deus! Pegou um navio e... tempestade gigante! Foi jogado no mar e engolido por uma BALEIA! Ficou 3 dias na barriga dela orando. Moral: não dá pra escapar do chamado!'"


def main():
    cookies = load_cookies("CAPCUT_COOKIES_FILE", "cookies_capcut.json")

    # Define o caminho para salvar os downloads
    download_path = str(get_downloads_output_dir())
    os.makedirs(download_path, exist_ok=True)  # Garante que a pasta existe

    with sync_playwright() as p:
        # Inicia o Firefox em vez do Chromium
        browser = p.firefox.launch(headless=False)

        # Configurar o contexto para baixar automaticamente os arquivos
        context = browser.new_context(
            accept_downloads=True
        )

        page = context.new_page()

        # Configurar o download para salvar no diretório especificado
        def handle_download(download):
            print(f"Download iniciado: {download.suggested_filename}")
            try:
                # Salvar o arquivo no caminho especificado
                download_file_path = os.path.join(download_path, download.suggested_filename)
                download.save_as(download_file_path)
                print(f"Arquivo salvo com sucesso em: {download_file_path}")

                # Verificar se o arquivo foi realmente salvo
                if os.path.exists(download_file_path):
                    print(f"Verificado: arquivo existe em {download_file_path}")
                    print(f"Tamanho do arquivo: {os.path.getsize(download_file_path)} bytes")
                else:
                    print(f"ERRO: Arquivo não encontrado em {download_file_path} após download")
            except Exception as e:
                print(f"Erro ao salvar o download: {e}")

        # Registrar o evento de download
        context.on("download", handle_download)

        # Adiciona os cookies
        context.add_cookies(cookies)

        try:
            page.goto('https://www.capcut.com/ai-creator/storyboard', timeout=5000)
        except Exception:
            pass

        # Clica em Script
        print("Clica em Script")
        while True:
            try:
                if page.locator('#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-exited-EdpHT7 > div.menu-qRy85V > div:nth-child(1) > div.icon-tgHY7S').is_visible():
                    page.locator('#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-exited-EdpHT7 > div.menu-qRy85V > div:nth-child(1) > div.icon-tgHY7S').click()
                    break
            except Exception:
                pass

        # Digita um topico
        print("Digita um topico")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.outlineContentContainer-HB2kOP > div.themeTitleContainer-YLvDBB > textarea"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).fill(topico)
                    break
            except Exception:
                pass

        # Digita pontos chave
        print("Digita pontos chave")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.outlineContentContainer-HB2kOP > div.outlineEditorWrap-vrbRjS > div > div:nth-child(1) > div > ul > li"
                if page.locator(seletor).is_visible():
                    locator = page.locator(seletor)
                    locator.click()  # Garante que o campo está focado
                    locator.type(coisas_chave)  # Simula a digitação, incluindo '\n'
                    break
            except Exception:
                pass

        # Clica em mais requisitos
        print("Clica em mais requisitos")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.outlineContentContainer-HB2kOP > div.generateOptionsContainer-UtQiOc > div.lv-collapse.lv-collapse-borderless.collapseOptionContainer-EvTBcY > div:nth-child(2) > div > div"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Preenche mais requisitos
        print("Preenche mais requisitos")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.outlineContentContainer-HB2kOP > div.generateOptionsContainer-UtQiOc > div.lv-collapse.lv-collapse-borderless.collapseOptionContainer-EvTBcY > div.lv-collapse-item.lv-collapse-item-active.collapseItem-schYPu > div.lv-collapse-item-content.lv-collapse-item-content-expanded > div > div > textarea"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).fill(requisitos)
                    break
            except Exception:
                pass

        # Clica para gerar o video
        print("Clica para gerar o video")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.generateScriptWrapper-t_WM95 > div > button"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Espera ter gerado o video
        print("Espera ter gerado o video")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.content-Wl5toZ.ai-creator-layout-content-container > div.creationContent-sWeVTd > div.script-area-hSgSLg > div.scriptListContainer-YU1hO1 > div > div.generateBarWrap-fz5NxP.generateBar-Hc5cjV > div > div > div > div.lv-space.lv-space-horizontal.lv-space-align-center > div:nth-child(2) > button"
                if page.locator(seletor).is_visible():
                    sleep(5)
                    break
            except Exception:
                pass

        # Clica na cena
        print("Clica na cena")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.menu-qRy85V > div:nth-child(2)"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Clica no tipo de video
        print("Clica no tipo de video")
        while True:
            try:
                seletor = "#lv-tabs-0-panel-0 > div > div > div.recommendListWrap-gaJaXS > div.digitalHumanVerticalList-pO5mZU > div:nth-child(5) > div.cover-uqKnrM.common-digital-human-card-cover"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Clica na voz
        print("Clica na voz")
        while True:
            try:
                seletor = "#lv-tabs-0-tab-1 > span"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Seleciona uma voz
        print("Seleciona uma voz")
        while True:
            try:
                seletor = "#lv-tabs-0-panel-1 > div > div > div:nth-child(4) > div > div:nth-child(2) > div.content-oRP2oR"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Clica no que gerou
        print("Clica no que gerou")
        while True:
            try:
                seletor = 'div[id="ai-creator"]'
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Aplica a voz
        print("Aplica a voz")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.entry-wqm88m.revealing-XkE8GR.entered-m3NDX5 > div > div.pane-J6KINv > div.footer-PvsJgM > div:nth-child(2) > div > button"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    sleep(5)
                    break
            except Exception:
                pass

        # Confere se carregou a voz
        print("Confere se carregou a voz")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.content-Wl5toZ.ai-creator-layout-content-container > div.loadingMask-dHQZ6o > div > div.titleContainer-XxHfjH > div.loadingAction-LNIjyl"
                if page.locator(seletor).is_visible():
                    sleep(1)
                else:
                    sleep(5)
                    break
            except Exception:
                pass

        # Clica em midia
        print("Clica em midia")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.entry-wqm88m.revealing-XkE8GR.entered-m3NDX5 > div > div.tabsContainer-Bt6X4k > div > div:nth-child(2)"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Clica para gerar a midia com ia
        print("Clica para gerar a midia com ia")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.entry-wqm88m.revealing-XkE8GR.entered-m3NDX5 > div > div.brollContainer-EwIa0N > div > div:nth-child(2)"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Seleciona 9:16
        print("Seleciona 9:16")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.entry-wqm88m.revealing-XkE8GR.entered-m3NDX5 > div > div.content-lwOTXn > div.ratioArea-SHgz0v > div:nth-child(2)"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Seleciona imagem como massinha
        print("Seleciona imagem como massinha")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.entry-wqm88m.revealing-XkE8GR.entered-m3NDX5 > div > div.content-lwOTXn > div.styleList-rEpzy3 > div:nth-child(28) > img"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Confirma para gerar a midia
        print("Confirma para gerar a midia")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div > div.entry-wqm88m.revealing-XkE8GR.entered-m3NDX5 > div > div.footer-BnDEtx > div > div > button"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    sleep(5)
                    break
            except Exception:
                pass

        # Espera até gerar a midia
        print("Espera até gerar a midia")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.content-Wl5toZ.ai-creator-layout-content-container > div.loadingMask-dHQZ6o > div > div.titleContainer-XxHfjH > div.loadingAction-LNIjyl"
                if page.locator(seletor).is_visible():
                    sleep(1)
                else:
                    sleep(5)
                    break
            except Exception:
                pass

        # Clica em elementos
        print("Clica em elementos")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.menu-qRy85V > div:nth-child(3)"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    break
            except Exception:
                pass

        # Tira a legenda
        print("Tira a legenda")
        while True:
            try:
                seletor = "#ai-creator > div > div.container-U2ccFZ.ai-creator-layout-sider-container > div.side-panel-t5yN0g.side-panel-entered-EyGquW > div.panel-PO1lOz > div.panel-wrapper-eujt7F.entered-RxDjlv > div.content-Zpv76f.content-RqhFo7 > div > div:nth-child(1) > div.textPresetTitle-k9cmKs > button"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    sleep(5)
                    break
            except Exception:
                pass

        # Clica em exportar
        print("Clica em exportar")
        while True:
            try:
                seletor = ".button-b0vJEh"
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    sleep(2)
                    break
            except Exception:
                pass

        # Clica para baixar
        print("clica para baixar")
        while True:
            try:
                seletor = '.footerButton-ZW8_8C'
                if page.locator(seletor).is_visible():
                    page.locator(seletor).click()
                    print("Botão de download clicado!")
                    break
            except Exception as e:
                print(f"Erro ao clicar no botão: {e}")
                sleep(1)

        # Espera o download completar
        print("Aguardando download completar...")
        download_completed = False
        timeout = 180  # tempo máximo de espera em segundos (aumentado para 3 minutos)
        start_time = time.time()

        # Conta quantos arquivos estavam na pasta antes do download
        files_before = set(os.listdir(download_path))

        while not download_completed and (time.time() - start_time) < timeout:
            # Verifica se algum arquivo novo foi criado na pasta de downloads
            current_files = set(os.listdir(download_path))
            new_files = current_files - files_before

            # Verificar arquivos em download parcial
            mp4_files = [f for f in new_files if f.endswith('.mp4') and not f.endswith('.part') and not f.endswith('.crdownload')]
            temp_files = [f for f in new_files if f.endswith('.part') or f.endswith('.crdownload')]

            if temp_files:
                print(f"Download em andamento... Arquivos temporários: {temp_files}")

            if mp4_files:
                latest_file = max([os.path.join(download_path, f) for f in mp4_files], key=os.path.getctime)
                print(f"Download concluído! Arquivo salvo em: {latest_file}")
                print(f"Tamanho do arquivo: {os.path.getsize(latest_file)} bytes")
                download_completed = True

                abrir_pasta_downloads(download_path)
                break
            else:
                sleep(3)

        if not download_completed:
            print("Tempo esgotado. Verificando manualmente os arquivos na pasta...")
            current_files = set(os.listdir(download_path))
            new_files = current_files - files_before
            if new_files:
                print(f"Novos arquivos encontrados: {new_files}")
                abrir_pasta_downloads(download_path)
            else:
                print("Nenhum novo arquivo foi encontrado. Verifique o diretório de downloads do navegador.")

        print("Script finalizado")
        browser.close()


if __name__ == "__main__":
    main()
