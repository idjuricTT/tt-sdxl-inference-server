
from config.settings import settings
from tt_model_runners.base_device_runner import DeviceRunner
from tt_model_runners.mock_runner import MockRunner


def get_device_runner(worker_id: str) -> DeviceRunner:
        model_runner = settings.model_runner
        if model_runner == "tt-sdxl":
            from tt_model_runners.sdxl_runner import TTSDXLRunner
            return TTSDXLRunner(worker_id)
        elif model_runner == "tt-sd3.5":
            from tt_model_runners.sd35_runner import TTSD35Runner
            return TTSD35Runner(worker_id)
        elif model_runner == "mock":
            from tt_model_runners.mock_runner import MockRunner
            return MockRunner(worker_id)
        else:
            raise ValueError(f"Unsupported model runner: {model_runner}")