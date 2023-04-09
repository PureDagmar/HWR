from multiprocessing import cpu_count

from pydantic import BaseSettings


class Config(BaseSettings):
    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'


class LogConfig(Config):
    level: str = "INFO"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        case_sensitive = False
        fields = {
            "level": {
                "env": ["log_level"]
            },
        }


class ServiceConfig(Config):
    service_name: str = "shifo-ocr"
    API_TOKEN: str
    PORT: int
    log_config: LogConfig
    WORKERS: int = cpu_count()
    RELOAD: bool = False
    MODEL_NAME: str = "OCRBlanksClassicationModel"
    mask: str = "./service/api/data/mask.jpg"
    goodMatchPercent: float = 0.15
    xBorder: int = 50
    yBorder: int = 5
    formMapPath: str = './service/api/config/form_map.yml'
    pathToSave: str = './service/api/result.yml'
    height: int = 42
    width: int = 30
    device: str = 'cuda:0'


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )


sc = get_config()
