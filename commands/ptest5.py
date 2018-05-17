# coding: utf-8
lado_tabuleiro = int(raw_input())

quantidade_de_x = 0
quantidade_de_o = 0
for i in range(lado_tabuleiro):
	simbolos = raw_input()
	if len(simbolos) != lado_tabuleiro:
		print "Tabuleiro inválido."
		quantidade_de_o = 0
		quantidade_de_x = 0
		break
		
	else:
		for simbolo in simbolos:
			if simbolo == "x":
				quantidade_de_x += 1
			else:
				quantidade_de_o += 1
			
if quantidade_de_o > quantidade_de_x:
	print "Bola ganhou com %i pontos." % quantidade_de_o
	
elif quantidade_de_x > quantidade_de_o:
	print "Xis ganhou com %i pontos." % quantidade_de_x
	
elif quantidade_de_x == quantidade_de_o and quantidade_de_x != 0:
	print "Empate em %i pontos." % quantidade_de_o

			
			
			
			

