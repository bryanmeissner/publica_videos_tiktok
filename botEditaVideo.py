import subprocess
import os
import time
from config import get_download_video_path, get_ffmpeg_path, get_project_video_path

def acelerar_video(arquivo_entrada, arquivo_saida, velocidade=2.0, caminho_ffmpeg='ffmpeg'):
    """
    Acelera um vídeo usando FFmpeg.
    
    Args:
        arquivo_entrada: Caminho do vídeo original
        arquivo_saida: Caminho para salvar o vídeo acelerado
        velocidade: Fator de aceleração (2.0 = 2x mais rápido, 0.5 = 2x mais lento)
        caminho_ffmpeg: Caminho completo do executável ffmpeg (padrão: 'ffmpeg')
    """
    
    # Verifica se o arquivo de entrada existe
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado!")
        return False
    
    # Calcula os filtros de vídeo e áudio
    filtro_video = f"setpts={1/velocidade}*PTS"
    filtro_audio = criar_filtro_audio(velocidade)
    
    comando = [
        caminho_ffmpeg,
        '-i', arquivo_entrada,
        '-filter:v', filtro_video,
        '-filter:a', filtro_audio,
        '-y',
        arquivo_saida
    ]
    
    while True:  # Loop infinito até o vídeo ser processado com sucesso
        try:
            print(f"Acelerando vídeo em {velocidade}x...")
            
            resultado = subprocess.run(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if resultado.returncode == 0:
                print("✓ Vídeo acelerado com sucesso!")
                return True
            else:
                print("✗ Erro ao processar o vídeo:")
                print(resultado.stderr)
                print("Tentando novamente em 2 segundos...")
                time.sleep(2)  # Aguarda 2 segundos antes de tentar novamente
            
        except FileNotFoundError:
            print("Erro: FFmpeg não encontrado. Certifique-se de que está instalado.")
            print("Instale com: sudo apt install ffmpeg (Linux) ou brew install ffmpeg (Mac)")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            print("Tentando novamente em 2 segundos...")
            time.sleep(2)

def criar_filtro_audio(velocidade):
    """
    Cria filtro de áudio, encadeando atempo se necessário.
    O atempo do FFmpeg só aceita valores entre 0.5 e 2.0.
    """
    if 0.5 <= velocidade <= 2.0:
        return f"atempo={velocidade}"
    
    # Para velocidades maiores, encadear múltiplos atempo
    filtros = []
    vel_restante = velocidade
    
    while vel_restante > 2.0:
        filtros.append("atempo=2.0")
        vel_restante /= 2.0
    
    while vel_restante < 0.5:
        filtros.append("atempo=0.5")
        vel_restante /= 0.5
    
    if vel_restante != 1.0:
        filtros.append(f"atempo={vel_restante}")
    
    return ",".join(filtros)

# Exemplo de uso
if __name__ == "__main__":
    video_entrada = get_download_video_path()
    video_saida = get_project_video_path()
    fator_velocidade = 1.3
    caminho_ffmpeg = get_ffmpeg_path()
    acelerar_video(video_entrada, video_saida, fator_velocidade, caminho_ffmpeg)