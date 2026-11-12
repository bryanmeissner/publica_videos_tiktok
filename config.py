import json
import os
import platform
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"

_PLACEHOLDER_VALUES = {
    "sua_chave_deepseek_aqui",
    "COLE_SEU_VALOR_AQUI",
}


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
    if not key or key in _PLACEHOLDER_VALUES:
        raise RuntimeError(
            "DEEPSEEK_API_KEY não configurada. Defina uma chave válida no arquivo .env ou nas variáveis de ambiente."
        )
    return key


def get_deepseek_api_base() -> str:
    return os.getenv("DEEPSEEK_API_BASE", "").strip() or "https://api.deepseek.com/v1"


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
    custom = os.getenv("CHROME_PATH", "").strip()
    if custom:
        return custom

    system = platform.system()
    if system == "Windows":
        return r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if system == "Darwin":
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    return shutil.which("google-chrome") or shutil.which("chromium") or "google-chrome"


def get_ffmpeg_path() -> str:
    custom = os.getenv("FFMPEG_PATH", "").strip()
    if custom:
        return custom
    if os.name == "nt":
        return r"C:\ffmpeg\bin\ffmpeg.exe"
    return shutil.which("ffmpeg") or "ffmpeg"


def get_img_path(filename: str) -> str:
    return str(IMG_DIR / filename)


def get_videos_json_path() -> Path:
    custom = os.getenv("VIDEOS_JSON_PATH", "").strip()
    if not custom:
        return BASE_DIR / "videos_criados.json"
    path = Path(custom)
    return path if path.is_absolute() else BASE_DIR / path


def load_videos_json(json_path: str | Path | None = None) -> list[dict]:
    path = Path(json_path) if json_path else get_videos_json_path()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"O arquivo {path} deve conter uma lista JSON.")
    return data


def save_videos_json(videos: list[dict], json_path: str | Path | None = None) -> None:
    path = Path(json_path) if json_path else get_videos_json_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(videos, f, indent=4, ensure_ascii=False)


def _normalize_same_site(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower()
    mapping = {
        "strict": "Strict",
        "lax": "Lax",
        "none": "None",
        "no_restriction": "None",
        "unspecified": "Lax",
    }
    return mapping.get(normalized)


def load_cookies(env_var: str, default_filename: str) -> list[dict]:
    raw_path = os.getenv(env_var, "").strip()
    cookies_file = Path(raw_path) if raw_path else (BASE_DIR / default_filename)
    if not cookies_file.is_absolute():
        cookies_file = BASE_DIR / cookies_file
    if not cookies_file.is_file():
        raise FileNotFoundError(
            f"Arquivo de cookies não encontrado: {cookies_file}. "
            f"Crie-o a partir de cookies.example.json ou configure {env_var}."
        )
    with cookies_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"O arquivo de cookies {cookies_file} deve conter uma lista JSON.")

    normalized_cookies: list[dict] = []
    for cookie in data:
        if not isinstance(cookie, dict):
            raise ValueError(f"Entrada de cookie inválida em {cookies_file}.")
        if cookie.get("value") in _PLACEHOLDER_VALUES:
            raise ValueError(
                f"O arquivo de cookies {cookies_file} ainda contém valor de exemplo. "
                "Substitua pelos cookies reais da sua sessão."
            )
        item = dict(cookie)
        same_site = _normalize_same_site(item.get("sameSite"))
        if same_site:
            item["sameSite"] = same_site
        else:
            item.pop("sameSite", None)
        normalized_cookies.append(item)
    return normalized_cookies
