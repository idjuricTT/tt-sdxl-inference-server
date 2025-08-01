import asyncio
from uuid import uuid4

from config.settings import settings
from domain.image_generate_request import ImageGenerateRequest
from model_services.device_worker import device_worker
from model_services.base_model import BaseModel
from model_services.scheduler import Scheduler
from resolver.scheduler_resolver import get_scheduler
from utils.helpers import log_execution_time
from utils.logger import TTLogger

class ImageService(BaseModel):

    @log_execution_time("SDXL service init")
    def __init__(self):
        self.scheduler: Scheduler = get_scheduler()
        self.logger = TTLogger()

    @log_execution_time("Scheduler image processing")
    async def processImage(self, imageGenerateRequest: ImageGenerateRequest) -> str:
        # set task id
        task_id = str(uuid4())
        imageGenerateRequest._task_id = task_id
        self.scheduler.process_request(imageGenerateRequest)
        future = asyncio.get_running_loop().create_future()
        self.scheduler.result_futures[task_id] = future
        try:
            result = await future
        except Exception as e:
            self.logger.error(f"Error processing image: {e}")
            raise e
        self.scheduler.result_futures.pop(task_id, None)
        return result

    def checkIsModelReady(self):
        """Detailed system status for monitoring"""
        return {
            'model_ready': self.scheduler.checkIsModelReady(),
            'queue_size': self.scheduler.task_queue.qsize() if hasattr(self.scheduler.task_queue, 'qsize') else 'unknown',
            'max_queue_size': settings.max_queue_size,
            'worker_count': len(self.scheduler.workers) if hasattr(self.scheduler, 'workers') else 'unknown',
            'runner_in_use': settings.model_runner,
        }

    @log_execution_time("Starting workers")
    def startWorkers(self):
        self.scheduler.startWorkers()

    def stopWorkers(self):
        return self.scheduler.stopWorkers()
