# coding: utf-8

tamanho = int(raw_input())
pontos_x = 0
pontos_o = 0
tabuleiro_valido = 1

for i in range(tamanho):
    if tabuleiro_valido:
        linha = raw_input()
    
        if len(linha) == tamanho:
            for char in range(tamanho):
                if linha[char] == 'x':
                    pontos_x += 1
                    
                else:
                    pontos_o += 1
                    
        else:
            tabuleiro_valido = 0
            
if tabuleiro_valido:    
    if pontos_x > pontos_o:
        print 'Xis ganhou com %d pontos.' % pontos_x
        
    elif pontos_o > pontos_x:
        print 'Bola ganhou com %d pontos.' % pontos_o
        
    else:
        print 'Empate em %d pontos.' % pontos_x

else:
    print 'Tabuleiro inválido.'
