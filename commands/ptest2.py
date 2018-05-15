# coding: utf-8

nNumeroDeLinhas = int(raw_input())
nQuantiaDeXis = 0
nQuantiaDeBola = 0

bInvalido = False
for i in xrange (nNumeroDeLinhas):
	linhaEntrada = raw_input()
	if len(linhaEntrada) != nNumeroDeLinhas:
		bInvalido = True
		break
	else:
		for j in xrange (len(linhaEntrada)):
			if linhaEntrada[j] == 'x':
				nQuantiaDeXis += 1
			elif linhaEntrada[j] == 'o':
				nQuantiaDeBola += 1


if bInvalido == False:
	if nQuantiaDeBola > nQuantiaDeXis:
		print 'Bola ganhou com %d pontos.' % nQuantiaDeBola
	elif nQuantiaDeXis > nQuantiaDeBola:
		print 'Xis ganhou com %d pontos.' % nQuantiaDeXis
	else: 
		print 'Empate em %d pontos.' % nQuantiaDeXis
else:
	print 'Tabuleiro inválido.'   
