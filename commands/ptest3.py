# coding: utf-8


n = int(raw_input())

linhas = []

X = 0
bola = 0
cond = True

for e in range(n):
    linha = raw_input()
    if len(linha) == n:
        for c in linha:
            if c == 'x':
                X += 1
            if c == 'o':
                bola += 1
    else:
        cond = False
        print 'Tabuleiro inválido.'
        break

if cond:
    if X > bola:
        print 'Xis ganhou com %d pontos.' % X
    elif bola > X:
        print 'Bola ganhou com %d pontos.' % bola
    else:
        print 'Empate em %d pontos.' % X
