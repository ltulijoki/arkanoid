from os import mkdir
from os.path import exists, join
from valikko import valikko

if not exists(join("tiedostot", "tasot", "omat")):
    mkdir(join("tiedostot", "tasot", "omat"))

valikko()
