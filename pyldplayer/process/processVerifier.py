
import os

from pyldplayer._models.process.process import BaseProcessInterface
class ProcessVerifier(BaseProcessInterface):
    path : str

    def __init__(self) -> None:
        """
        checks if the path is valid
        """

        if not (
            os.path.exists(self.path)
            and os.path.isfile(self.path)
            and os.path.basename(self.path) == "ldconsole.exe"
        ):
            raise RuntimeError("Could not find ldconsole.exe")

        query_res = self.query(toList=True)

        if query_res[0] != 'dnplayer Command Line Management Interface':
            raise RuntimeError("Invalid path")
        
        assert os.path.exists(self.vmFolder)