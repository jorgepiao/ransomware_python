## Ransomware en Python

Esta aplicacion esta probada para sistemas operativos linux. Consiste en encriptar los archivos encontrados en la carpeta "HOME" para hacerlos inutilizables.

Para desencriptarlos, se genera una clave aleatoria con el algoritmo sha512 de 32 digitos la cual se enviara por email automaticamente.

### Funcionamiento

Al ejecutar el archivo `ransom.py` el programa comenzara a buscar en todas las subcarpetas de la carpeta 'HOME' encriptando todo archivo que encuentre.

Al volver a ejecutar el archivo `ransom.py` pedira una clave, la cual se envio al email especificado, al ingresar esta clave los archivos se desencriptaran.