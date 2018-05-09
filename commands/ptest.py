# coding: utf-8

n = int(raw_input())

xis = 0
bola = 0
invalido = 0
lista = []

for i in range(n):
    simbolos = raw_input()
    if len(simbolos) > n or len(simbolos) < n:
        invalido += 1
        print "Tabuleiro inválido."
        break
    else:
            
        for m in range(len(simbolos)):
            if simbolos[m] == 'x':
                xis += 1
            elif simbolos[m] == 'o':
                bola += 1
        
if invalido == 0:
    if xis > bola:
        print "Xis ganhou com %d pontos." % xis
    elif bola > xis:
        print "Bola ganhou com %d pontos." % bola
    else:
        print "Empate em %d pontos." % xis
