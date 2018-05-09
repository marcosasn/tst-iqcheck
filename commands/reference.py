# coding: utf-8
# Linger
# Referencia, Eliane Araujo

tabuleiro_invalido = False
tam = int(raw_input())

bola, xis = 0, 0

for i in range(tam):
    linha = raw_input()
    if len(linha) != tam:
        tabuleiro_invalido = True
        break
    for i in range(tam):
        if linha[i] == 'o':
            bola += 1
        else:
            xis += 1

if tabuleiro_invalido:
    print "Tabuleiro inválido"
elif bola > xis:
    print "Bola ganhou com %d pontos." % bola
elif xis > bola:
    print "Xis ganhou com %d pontos." % xis
else:
    print "Empate em %d pontos." % bola
