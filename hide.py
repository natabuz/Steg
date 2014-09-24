#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

marker = 'nata';

class HideException(Exception): #Базовый класс для ошибок в модуле «скрыватель».
	pass

class UsageException(HideException): #Класс для ошибок использования утилиты.
	def __str__(self):
        	return self.message + '\nИспользование: hide.py [bmp-изображение] [любой файл]';

def bin(s): #Число в двоичную систему счисления.
	return str(s) if s <= 1 else bin(s >> 1) + str(s & 1);

def byte2bin(bytes): #Байты в виде битовых строк.
	for b in bytes:
        	yield bin(ord(b)).zfill(8);

def hide(bmp_filename, src_filename): #Помещает в BMP изображение любой файл, включая его название.
	src = open(src_filename, 'rb');
    	secret = marker + src_filename + marker + src.read() + marker;
    	src.close();

    	bmp = open(bmp_filename, 'rb+');
    	bmp.seek(55);
    	container = bmp.read();

    	need = 8 * len(secret) - len(container);
	
    	if need > 0:
        	raise HideException('Размера этого BMP файла недостаточно для сокрытия в нем файла.\nНужно еще %s байт.' % need);

    	cbits = byte2bin(container);

    	encrypted = [];

    	for sbits in byte2bin(secret):
        	for bit in sbits:
            		bits = cbits.next();
            		# Замена младшего бита в контейнерном байте
            		bits = bits[:-1] + bit;
            		b = chr(int(bits, 2));
            		# Замена байта в контейнере
            		encrypted.append(b);

    	bmp.seek(55);
    	bmp.write(''.join(encrypted));
    	bmp.close();

def main(argv=None):
	if argv is None:
        	argv = sys.argv;
    	try:
        	if len(argv) != 3:
            		raise UsageException('Нужен BMP файл.');

        	hide(argv[1], argv[2]);

    	except (IOError, HideException), err:
        	print >> sys.stderr, err;

        	return 2;

if __name__ == '__main__':
    sys.exit(main());
