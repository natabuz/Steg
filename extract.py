#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

marker = 'nata';

class ExtractException(Exception): #Базовый класс для ошибок в модуле «экстрактор».
	pass

class UsageException(ExtractException): #Класс для ошибок использования утилиты.
	def __str__(self):
        	return self.message + '\nИспользование: extract.py [bmp-изображение]';

def bin(s): #Число в двоичную систему счисления.
	return str(s) if s <= 1 else bin(s >> 1) + str(s & 1);

def byte2bin(bytes): #Байты в виде битовых строк.
	for b in bytes:
        	yield bin(ord(b)).zfill(8);

def decrypt_char(container): #Расшифровка символов
	sbits = '';

    	for cbits in byte2bin(container):
        	sbits += cbits[-1];

        	if len(sbits) == 8:
            		yield chr(int(sbits, 2));

            		sbits = '';

def extract(bmp_filename): #Извлекает из BMP скрытый файл, включая его название.
	bmp = open(bmp_filename, 'rb');
    	bmp.seek(55);
    	container = bmp.read();
    	bmp.close();

    	decrypted = [];

    	for b in decrypt_char(container):
        	decrypted.append(b);
        
        	if (len(marker) == len(decrypted) and marker != ''.join(decrypted)): # Определение, что в заданном изображении есть файл
			raise ExtractException('Изображение не содержит файла');

    	if len(decrypted) > len(marker):
        	decrypted = ''.join(decrypted).split(marker);
        	src_filename = decrypted[1];
        	src_data = decrypted[2];
        	src = open(src_filename, 'wb');
        	src.write(src_data);
        	src.close();

def main(argv=None):
	if argv is None:
        	argv = sys.argv;
    	try:
        	if len(argv) != 2:
			raise UsageException('Нужен BMP файл');

        	extract(argv[1]);

   	except (IOError, ExtractException), err:
        	print >> sys.stderr, err;

        	return 2;

if __name__ == '__main__':
    sys.exit(main());
