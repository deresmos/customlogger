import glob
import os
from datetime import datetime
from logging import FileHandler


class RunRotatingHandler(FileHandler):
    __filepath = None
    __defaultBackupCount = 3
    __defaultLogFmt = '%Y%m%d_%H%M%S.log'

    def __init__(self, dirpath, backup_count=None, fmt=None):
        fmt = fmt or self.__defaultLogFmt
        backup_count = backup_count or RunRotatingHandler.__defaultBackupCount

        filepath = self.getFilepath(dirpath, fmt, backup_count)

        super().__init__(filepath)

    def getFilepath(self, dirpath, fmt, backup_count):
        # If already set filepath, return the filepath
        if RunRotatingHandler.__filepath:
            return RunRotatingHandler.__filepath

        # Set the logfile name
        fmt = os.path.join(dirpath, fmt)
        filepath = datetime.today().strftime(fmt)
        dirname = os.path.dirname(filepath)

        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        # Get file list matching format
        match_filenames = [
            x for x in sorted(glob.glob(os.path.join(dirname, '*')))
            if self.isMatchLogFmt(x, fmt)
        ]

        # Delete the old file and set a new file path
        if len(match_filenames) >= backup_count:
            os.remove(match_filenames[0])

        RunRotatingHandler.__filepath = filepath
        return filepath

    @staticmethod
    def isMatchLogFmt(date_string, date_fmt):
        try:
            datetime.strptime(date_string, date_fmt)
        except ValueError:
            return False

        return True
