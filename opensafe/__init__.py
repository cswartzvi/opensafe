import os
import pathlib
import subprocess
from typing import Iterable, Union


class Safe:

    def __init__(self, database: Union[str, pathlib.Path],
                 executable: Union[str, pathlib.Path]) -> None:
        self._database = pathlib.Path(database)
        self._executable = str(pathlib.Path(executable).resolve())

    def _execute(self, command: str) -> str:
        """Executes the SourceSafe command line executeable."""
        env = os.environ.copy()
        env['SSDIR'] = str(self._database.resolve())
        args = [self._executable] + command.split()
        completed = subprocess.run(args, env=env, capture_output=True)
        if completed.returncode != 0:
            raise RuntimeError(f"Non-zero return code: {command}")
        return completed.stdout.decode('utf-8')

    def get(self, items: Iterable[str]):
        items = ' '.join(items)
        return self._execute(f"Get {items}")

    def history(self, items: Iterable[str]):
        items = ' '.join(items)
        return self._execute(f"History {items}")
