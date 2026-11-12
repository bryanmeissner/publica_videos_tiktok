import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
        return
    except ImportError:
        pass

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env_file(BASE_DIR / ".env")


def get_deepseek_api_key() -> str:
    key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "DEEPSEEK_API_KEY não configurada. Defina no arquivo .env ou nas variáveis de ambiente."
        )
    return key


def get_deepseek_api_base() -> str:
    return os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1").strip()


def get_downloads_dir() -> Path:
    custom = os.getenv("DOWNLOADS_DIR", "").strip()
    return Path(custom) if custom else Path.home() / "Downloads"


def get_videos_dir() -> Path:
    custom = os.getenv("VIDEOS_DIR", "").strip()
    return Path(custom) if custom else BASE_DIR / "videos"


def get_downloads_output_dir() -> Path:
    custom = os.getenv("DOWNLOADS_OUTPUT_DIR", "").strip()
    return Path(custom) if custom else BASE_DIR / "downloads"


def get_download_video_path() -> str:
    custom = os.getenv("DOWNLOAD_VIDEO_PATH", "").strip()
    return custom if custom else str(get_downloads_dir() / "video_tiktok.mp4")


def get_project_video_path() -> str:
    custom = os.getenv("PROJECT_VIDEO_PATH", "").strip()
    return custom if custom else str(get_videos_dir() / "video.mp4")


def get_chrome_path() -> str:
    return os.getenv(
        "CHROME_PATH",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    )


def get_ffmpeg_path() -> str:
    default = r"C:\ffmpeg\bin\ffmpeg.exe" if os.name == "nt" else "ffmpeg"
    return os.getenv("FFMPEG_PATH", default)


def load_cookies(env_var: str, default_filename: str) -> list[dict]:
    cookies_file = Path(os.getenv(env_var, str(BASE_DIR / default_filename)))
    if not cookies_file.is_absolute():
        cookies_file = BASE_DIR / cookies_file
    if not cookies_file.exists():
        raise FileNotFoundError(
            f"Arquivo de cookies não encontrado: {cookies_file}. "
            f"Crie-o a partir de cookies.example.json ou configure {env_var}."
        )
    with cookies_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"O arquivo de cookies {cookies_file} deve conter uma lista JSON.")
    return data
