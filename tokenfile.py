import pathlib 
from exceptions import FileError

class TokenFile():
    """Class for reading and writing the token file.

    Attributes:
        fileName -- the file name to store token data
    """

    __fileName = 'tokens.ini'

    def tokenFileExists(self):
        """Checks if the token file exists.
        Returns boolean.
        """
        pl = pathlib.Path(self.__fileName)
        e = pl.exists()
        if e is True and pl.is_file() :
            return True
        else :
            return False

    def writeTokenFile(self, data):
        """Writes the updated token details to the token file.
        Takes list or tuple, and writes each element to a new line.
        """
        try:
            tokenFile = open(self.__fileName, 'w')
            dataStr = tuple(map(str, data))
            toWrite = '\n'.join(dataStr)
            tokenFile.write(toWrite)      
        except:
            raise FileError("Cannot create token file") from None

    def readTokenFile(self):
        """Reads from the token file.
        Returns a list with elements from each line.
        """
        tokenFile = open(self.__fileName, 'r')
        lines = tokenFile.readlines()
        return [i.replace("\n","") for i in lines]