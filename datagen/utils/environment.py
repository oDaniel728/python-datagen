from datagen.globals import DatagenConfig


class Environment():
    """Provides access to environment-specific names from the config file.

    These names allow renaming namespaces, scoreboards, and data storages
    across the whole project without changing code.
    """

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _names():
        return DatagenConfig.config.get("environmentSettings", {}).get("names", {})

    @staticmethod
    def _lookup(category: str, key: str, fallback: str) -> str:
        names: dict = Environment._names().get(category, {})
        if isinstance(names, dict):
            return names.get(key, fallback)
        return fallback

    # ------------------------------------------------------------------ #
    #  Namespace names
    # ------------------------------------------------------------------ #

    @staticmethod
    def namespace(key: str, fallback: str = "") -> str:
        """Return the namespace name for *key* from
        ``environmentSettings.names.namespaces``.

        If the key is not found and *fallback* is provided, returns
        *fallback*; otherwise returns *key* itself as the default.
        """
        return Environment._lookup("namespaces", key, fallback or key)

    @staticmethod
    def namespace_minecraft() -> str:
        """Shortcut for `namespace("minecraft")`."""
        return Environment.namespace("minecraft", "minecraft")

    @staticmethod
    def namespace_temp() -> str:
        """Shortcut for `namespace("temp")`."""
        return Environment.namespace("temp", "temp")

    # ------------------------------------------------------------------ #
    #  Scoreboard names
    # ------------------------------------------------------------------ #

    @staticmethod
    def scoreboard(key: str, fallback: str = "") -> str:
        """Return the scoreboard name for *key* from
        ``environmentSettings.names.scoreboard``.

        If the key is not found and *fallback* is provided, returns
        *fallback*; otherwise returns *key* itself as the default.
        """
        return Environment._lookup("scoreboard", key, fallback or key)

    @staticmethod
    def scoreboard_temp() -> str:
        """Shortcut for `scoreboard("temp")`."""
        return Environment.scoreboard("temp", "temp")

    # ------------------------------------------------------------------ #
    #  Data storage names
    # ------------------------------------------------------------------ #

    @staticmethod
    def data_storage(key: str, fallback: str = "") -> str:
        """Return the data storage name for *key* from
        ``environmentSettings.names.dataStorage``.

        If the key is not found and *fallback* is provided, returns
        *fallback*; otherwise returns *key* itself as the default.
        """
        return Environment._lookup("dataStorage", key, fallback or key)

    @staticmethod
    def data_storage_temp() -> str:
        """Shortcut for `data_storage("temp")`."""
        return Environment.data_storage("temp", "temp")
