# coding: utf-8

xis = 0
bola = 0
valido = True
n = int(raw_input())

for i in range(n):
    linha = raw_input()
    if len(linha) != n:
        valido = False
        print "Tabuleiro inválido."
        break
    else:
        for j in linha:
            if j == 'x':
                xis += 1
            else:
                bola += 1

if valido:
    if xis > bola:
        print "Xis ganhou com %d pontos." % xis
    elif bola > xis:
        print "Bola ganhou com %d pontos." % bola
    else:
        print "Empate em %d pontos." % xis
