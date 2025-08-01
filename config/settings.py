from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_service:str = "image"
    log_level:str = "INFO"
    environment:str = "development"
    device_ids:str = "0"
    devices_per_runner:int = 1
    max_queue_size:int = 4
    max_batch_size:int = 4
    model_runner:str = "tt-sdxl"
    num_inference_steps:int = 20 # has to be hardcoded since we cannnot allow per image currently
    #model_runner:str = "tt-sd3.5"
    log_file: Optional[str] = None
    device_mesh_shape:tuple = (1, 1)
    mock_devices_count:int = 5
    model_config = SettingsConfigDict(env_file=".env") 

settings = Settings()

@lru_cache()
def get_settings() -> Settings:
    return Settings()