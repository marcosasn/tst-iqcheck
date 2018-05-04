# coding: utf-8
# 

valor_x = float(raw_input())
valor_y = float(raw_input())

if((valor_x == 0) and (valor_y == 0)):
    print "Centro."
elif((valor_x == 0) or (valor_y == 0)):
    print "Sobre eixo."
elif((valor_x > 0)and(valor_y > 0)):
    print "Primeiro quadrante."
elif((valor_x < 0)and(valor_y > 0)):
    print "Segundo quadrante."
elif((valor_x < 0)and(valor_y < 0)):
    print "Terceiro quadrante."
else:
    print "Quarto quadrante."
####
# group: prog1-20152
# mode: mtp3
# open_datetime: None
# create_datetime: 2016-03-04T12:03:59.389960
# revision: 1
# activity: 5893009501585408-1.0.1
# assignment: 6075923703005184
# ip: 150.165.75.252
# timestamp: 2016-03-04T12:31:17.731540
