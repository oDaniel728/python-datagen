class LoggerSettings():
    def __init__(
        self, 
        enabled: bool = True,
        log_debug: bool = False, 
        log_success: bool = True, 
        log_info: bool = True, 
        log_warning: bool = True, 
        log_error: bool = True, 
        log_task: bool = True,
        whitelist_enabled: bool = False,
        whitelist_values: list[str] | None = None,
    ) -> None:
        self.enabled = enabled
        self.log_debug = log_debug
        self.log_success = log_success
        self.log_info = log_info
        self.log_warning = log_warning
        self.log_error = log_error
        self.log_task = log_task
        self.whitelist_enabled = whitelist_enabled
        self.whitelist_values = whitelist_values or []

    @classmethod
    def from_dict(cls, data=None) -> "LoggerSettings":
        if not data:
            return cls()
        enabled = data.get("enabled", True)
        levels = data.get("levels", {})
        whitelist = data.get("whitelist", {})
        return cls(
            enabled=enabled,
            log_debug=levels.get("debug", False),
            log_success=levels.get("success", True),
            log_info=levels.get("info", True),
            log_warning=levels.get("warning", True),
            log_error=levels.get("error", True),
            log_task=levels.get("task", True),
            whitelist_enabled=whitelist.get("enabled", False),
            whitelist_values=whitelist.get("values", []),
        )

    def to_dict(self):
        result: dict = {
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
        if self.whitelist_enabled or self.whitelist_values:
            result["whitelist"] = {
                "enabled": self.whitelist_enabled,
                "values": self.whitelist_values,
            }
        return result
    
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

    def enable_whitelist(self):
        self.whitelist_enabled = True
        return self
    def disable_whitelist(self):
        self.whitelist_enabled = False
        return self
    
    def add_to_whitelist(self, name: str):
        if name not in self.whitelist_values:
            self.whitelist_values.append(name)
        return self
    
    def remove_from_whitelist(self, name: str):
        if name in self.whitelist_values:
            self.whitelist_values.remove(name)
        return self
    
    def is_namespace_allowed(self, namespace: str) -> bool:
        if not self.whitelist_enabled:
            return True
        return namespace in self.whitelist_values