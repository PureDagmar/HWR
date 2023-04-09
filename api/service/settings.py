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


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )


sc = get_config()
