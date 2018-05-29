# coding: utf-8

n = int(raw_input())
x = 0
o = 0
casa = ''

for i in range(n):
    casa = raw_input()
    
    if len(casa) == n:
        for j in range(len(casa)):
            if casa[j] == 'x':
                x += 1
            else:
                o += 1
    else:
        print 'Tabuleiro inválido.'
        x = -1
        break
        
if x != -1:
    if x > o:
        print 'Xis ganhou com %d pontos.' % x
    elif o > x:
        print 'Bola ganhou com %d pontos.' % o
    else:
        print 'Empate em %d pontos.' % x
