from pathlib import Path


class _Paths:
    @property
    def repo_root(self):
        return Path(__file__).parent.parent.absolute()


paths = _Paths()
