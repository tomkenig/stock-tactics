import pip
from pip._internal import main as pipmain

def install_whl(path):
    pipmain(['install', path])

install_whl('G:\Mój dysk\PRO\stock-tactics\TA_Lib-0.4.20-cp39-cp39-win_amd64.whl')