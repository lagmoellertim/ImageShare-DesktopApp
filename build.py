from build_tools import pyinstaller as pyi
import os

def getFolder(path):
    """
    Removes levels from the path
    :param path: String which contains a path, e.g. 'C:/'
    :return:
    """
    return "/".join(
        path.replace("\\","/").split("/")[:-1]
    )+"/"

build_tools_dir = os.path.join(
    getFolder(os.path.realpath(__file__)),
    "build_tools/"
)

if __name__ == "__main__":
    os.chdir(build_tools_dir)
    pyi.main()