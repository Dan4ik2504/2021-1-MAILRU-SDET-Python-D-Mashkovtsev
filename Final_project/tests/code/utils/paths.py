import sys
from pathlib import Path


class _Paths:
    @property
    def repo_root(self):
        return Path(__file__).parent.parent.absolute()

    @staticmethod
    def mass_replace(string, lst):
        """
        Mass replacement of characters in a string
        :param string: The string in which the characters will be replaced
        :param lst: List/tuple of tuples. Example: (("/", "\\"), ('*', 'x'))
        """
        for symbols in lst:
            string = string.replace(*symbols)
        return string

    def different_os_path(self, path: str):
        """Changing the path to be able to work on different operating systems"""
        if sys.platform.startswith('win'):
            symbols = (
                ("/", "\\"),
                (':', '_'),
                ('*', 'x'),
                ('"', "'"),
                ('?', '_qm_'),
                ('<', '_lt_'),
                ('>', '_gt_'),
                ('|', '_vl_'),
            )
            path = self.mass_replace(path, symbols)
        return path


paths = _Paths()
