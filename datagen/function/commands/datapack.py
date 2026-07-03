from typing import Literal

from datagen.function.commands.command import Command
from datagen.function.commands.customcommand import CustomCommand
from datagen.types.util.partialstring import PartialString


class Datapack():
    _TWhen = Literal["before", "after", "first", "last"]
    @staticmethod
    def enable(
        name: PartialString,
        when: _TWhen | None = None,
        existing: PartialString | None = None
    ) -> Command:
        """Enables a certain datapack, potentially

        Args:
            name (PartialString): Datapack's name to enable.
            when (_TWhen | None, optional): When to enable the datapack. Defaults to None.
            existing (PartialString | None, optional): Another datapack to consider when enabling. Defaults to None.

        Raises:
            ValueError: If 'when' is 'before' or 'after' and 'existing' is not provided.

        Returns:
            Command: _description_
        """
        if (when, existing) == (None, None):
            return CustomCommand(f"datapack enable {name}")
        if when in ["before", "after"] and existing is None:
            raise ValueError(f"When using 'before' or 'after', the 'existing' parameter must be provided.")
    
        return CustomCommand(f"datapack enable {name} {when} {existing if existing else ''}".strip())

    @staticmethod
    def disable(
        name: PartialString,
        when: _TWhen | None = None,
        existing: PartialString | None = None
    ) -> Command:
        """Disables a certain datapack, potentially

        Args:
            name (PartialString): Datapack's name to disable.
            when (_TWhen | None, optional): When to disable the datapack. Defaults to None.
            existing (PartialString | None, optional): Another datapack to consider when disabling. Defaults to None.

        Raises:
            ValueError: If 'when' is 'before' or 'after' and 'existing' is not provided.

        Returns:
            Command: The command to disable the datapack.
        """
        if (when, existing) == (None, None):
            return CustomCommand(f"datapack disable {name}")
        if when in ["before", "after"] and existing is None:
            raise ValueError(f"When using 'before' or 'after', the 'existing' parameter must be provided.")
    
        return CustomCommand(f"datapack disable {name} {when} {existing if existing else ''}".strip())
    
    _TWhat = Literal["available", "enabled"]
    @staticmethod
    def list(what: _TWhat | None = None) -> Command:
        """Lists datapacks based on the specified criteria.

        Args:
            what (_TWhat | None, optional): Specifies what to list. Can be 'available', 'enabled', or None. Defaults to None.

        Returns:
            Command: The command to list the datapacks.
        """
        if what is None:
            return CustomCommand("datapack list")
        return CustomCommand(f"datapack list {what}")