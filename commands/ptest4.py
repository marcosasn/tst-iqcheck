# coding: utf-8

ladoTabuleiro = int(raw_input())
pontos_x, pontos_o = 0, 0
tabuleiroValido = True
for i in range(ladoTabuleiro):
    posicaoJogadores = raw_input()
    if len(posicaoJogadores) != ladoTabuleiro:
        tabuleiroValido = False
        break
    else:
        for i in posicaoJogadores:
            if i == "x":
                pontos_x += 1
            else:
                pontos_o += 1
if tabuleiroValido:
    if pontos_x > pontos_o:
        print "Xis ganhou com %d pontos." % pontos_x
    elif pontos_o > pontos_x:
        print "Bola ganhou com %d pontos." % pontos_o
    else:
        print "Empate em %d pontos." % pontos_x
else:
    print "Tabuleiro inválido."
        
        
