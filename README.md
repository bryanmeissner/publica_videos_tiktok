# Bot de Criação e Publicação de Vídeos (CapCut + DeepSeek + TikTok)

Automação em Python para gerar roteiros com IA (DeepSeek), criar vídeos no CapCut, acelerar a velocidade com FFmpeg e publicar no TikTok via Playwright ou PyAutoGUI.

## Pré-requisitos

- Python 3.10 ou superior
- [FFmpeg](https://ffmpeg.org/) instalado e disponível no `PATH` (ou configurado via `FFMPEG_PATH`)
- Google Chrome (para os scripts baseados em `pyautogui`)
- Navegador Firefox do Playwright (para os scripts baseados em `playwright`)

## Instalação

1. Clone o repositório e crie um ambiente virtual:
   ```bash
   python -m venv .venv
   # Linux/macOS:
   source .venv/bin/activate
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   ```

2. Instale as dependências Python e o navegador do Playwright:
   ```bash
   pip install -r requirements.txt
   playwright install firefox
   ```

## Configuração (arquivos locais não versionados)

Nunca versione arquivos com chaves de API, cookies de sessão ou histórico pessoal. Os templates de exemplo já estão incluídos no repositório.

1. **Variáveis de ambiente (`.env`)**:
   ```bash
   cp .env.example .env
   ```
   Preencha `DEEPSEEK_API_KEY` com a sua chave real e ajuste os caminhos opcionais caso necessário.

2. **Cookies de sessão (`cookies_tiktok.json` / `cookies_capcut.json`)**:
   Exporte os cookies do navegador no formato JSON usando `cookies.example.json` como referência:
   - `cookies_capcut.json` (para `bot_playwright.py`)
   - `cookies_tiktok.json` (para `botTikTok.py`)

   Ou defina `CAPCUT_COOKIES_FILE` e `TIKTOK_COOKIES_FILE` no `.env`.

3. **Histórico de vídeos (`videos_criados.json`)**:
   ```bash
   cp videos_criados.example.json videos_criados.json
   ```
   Se omitido, o sistema inicializa a lista vazia automaticamente na primeira gravação.

## Scripts disponíveis

- `config.py`: Carrega `.env`, valida variáveis/cookies e resolve caminhos portáveis.
- `bot pg.py`: Fluxo completo via interface gráfica (`pyautogui`) — gera roteiro no DeepSeek, cria e baixa vídeo no CapCut, chama `botEditaVideo.py` e `botTikTok_PG.py`.
- `bot_playwright.py`: Automação de criação e download no CapCut via Playwright.
- `botEditaVideo.py`: Acelera vídeo (`1.3x` por padrão) com FFmpeg mantendo o áudio sincronizado.
- `botTikTok.py`: Publica o próximo vídeo pendente no TikTok Studio via Playwright.
- `botTikTok_PG.py`: Publica o próximo vídeo pendente no TikTok Studio via `pyautogui`.

## Aviso de segurança

O `.gitignore` já bloqueia `.env`, `.env.*`, `*cookies*.json`, `*session*.json`, `videos_criados.json`, `videos/`, `downloads/` e arquivos de mídia. Sempre confira `git status` antes de realizar um commit ou push.
