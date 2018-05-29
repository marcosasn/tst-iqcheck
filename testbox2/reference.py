# coding: utf-8
# Autor: João Arthur Brunet Monteiro
# Questão: Jogo de Tabuleiro - Linger
# 30/08/2017

tamanho_tabuleiro = int(raw_input())
tabuleiro_invalido = False
pontos_xis = 0
pontos_bola = 0

for i in range(tamanho_tabuleiro):
    linha = raw_input()

    if len(linha) != tamanho_tabuleiro:
        tabuleiro_invalido = True
        break

    for simbolo in linha:
        if simbolo == 'x':
            pontos_xis += 1
        
        else:
            pontos_bola += 1

if tabuleiro_invalido:
    print 'Tabuleiro inválido.'

elif pontos_xis > pontos_bola:
    print "Xis ganhou com %d pontos." % pontos_xis

elif pontos_bola > pontos_xis:
    print "Bola ganhou com %d pontos." % pontos_bola

else:
    print "Empate em %d pontos." % pontos_xis
