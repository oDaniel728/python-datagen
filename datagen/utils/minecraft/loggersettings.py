class LoggerSettings():
    def __init__(
        self, 
        enabled: bool = True,
        log_debug: bool = False, 
        log_success: bool = True, 
        log_info: bool = True, 
        log_warning: bool = True, 
        log_error: bool = True, 
        log_task: bool = True
    ) -> None:
        self.enabled = enabled
        self.log_debug = log_debug
        self.log_success = log_success
        self.log_info = log_info
        self.log_warning = log_warning
        self.log_error = log_error
        self.log_task = log_task

    @classmethod
    def from_dict(cls, data=None) -> "LoggerSettings":
        if not data:
            return cls()
        enabled = data.get("enabled", True)
        levels = data.get("levels", {})
        return cls(
            enabled=enabled,
            log_debug=levels.get("debug", False),
            log_success=levels.get("success", True),
            log_info=levels.get("info", True),
            log_warning=levels.get("warning", True),
            log_error=levels.get("error", True),
            log_task=levels.get("task", True),
        )

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "levels": {
                "debug": self.log_debug,
                "success": self.log_success,
                "info": self.log_info,
                "warning": self.log_warning,
                "error": self.log_error,
                "task": self.log_task,
            }
        }
    
    def disable_debug(self):
        self.log_debug = False
        return self
    def enable_debug(self):
        self.log_debug = True
        return self
    
    def disable_success(self):
        self.log_success = False
        return self
    def enable_success(self):
        self.log_success = True
        return self
    
    def disable_info(self):
        self.log_info = False
        return self
    def enable_info(self):
        self.log_info = True
        return self
    
    def disable_warning(self):
        self.log_warning = False
        return self
    def enable_warning(self):
        self.log_warning = True
        return self

    def disable_error(self):
        self.log_error = False
        return self
    def enable_error(self):
        self.log_error = True
        return self
    
    def disable_task(self):
        self.log_task = False
        return self
    def enable_task(self):
        self.log_task = True
        return self