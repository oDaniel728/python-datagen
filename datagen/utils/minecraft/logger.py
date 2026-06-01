from datetime import datetime

from datagen.utils.minecraft.loggersettings import LoggerSettings

class Logger():
    settings: LoggerSettings = LoggerSettings()
    
    instances = dict[str, "Logger"]()

    C_RED = "\033[31m"
    C_ORANGE = "\033[38;5;208m"
    C_GREEN = "\033[32m"
    C_GRAY = "\033[90m"
    C_BOLD = "\033[1m"
    C_RESET = "\033[0m"

    @staticmethod
    def _build_text(message: str, namespace: str, modifier: str = "", task: str = "") -> str:
        return f"{modifier}[{datetime.now().strftime('%H:%M:%S.%f')}] [{namespace}] {task}: {message}{Logger.C_RESET}"

    def __new__(cls, namespace: str):
        if namespace not in cls.instances:
            cls.instances[namespace] = super().__new__(cls)
        return cls.instances[namespace]
    
    def __init__(self, namespace: str):
        self.namespace = namespace

    def __del__(self):
        del Logger.instances[self.namespace]

    def info(self, message: str):
        if not Logger.settings.log_info: return
        print(self._build_text(message, self.namespace, Logger.C_RESET, "INFO"))

    def warn(self, message: str):
        if not Logger.settings.log_warning: return
        print(self._build_text(message, self.namespace, Logger.C_ORANGE, "WARN"))

    def error(self, message: str):
        if not Logger.settings.log_error: return
        print(self._build_text(message, self.namespace, Logger.C_RED + Logger.C_BOLD, "ERROR"))

    def success(self, message: str):
        if not Logger.settings.log_success: return
        print(self._build_text(message, self.namespace, Logger.C_GREEN + Logger.C_BOLD, "SUCCESS"))

    def debug(self, message: str):
        if not Logger.settings.log_debug: return
        print(self._build_text(message, self.namespace, Logger.C_GRAY, "DEBUG"))

    @staticmethod
    def start_task(task_name: str):
        if not Logger.settings.log_task: return
        print(Logger._build_text(f"Starting task '{task_name}'", "SYSTEM", Logger.C_BOLD, "TASK"))

    @staticmethod
    def end_task(task_name: str):
        if not Logger.settings.log_task: return
        print(Logger._build_text(f"Finished task '{task_name}'", "SYSTEM", Logger.C_BOLD, "TASK"))