#Questao02: Plano Cartesiano

x = float(raw_input())
y = float(raw_input())

if x > 0 and y > 0:
    print 'Primeiro quadrante.'
elif x > 0 and y < 0:
    print 'Quarto quadrante.'
elif x < 0 and y > 0:
    print 'Segundo quadrante.'
elif x < 0 and y < 0:
    print 'Terceiro quadrante.'
elif x == 0 and y != 0:
    print 'Sobre eixo.'
elif x != 0 and y == 0:
    print 'Sobre eixo.'
else:
    print 'Centro.'
####
# group: prog1-20152
# mode: mtp3
# open_datetime: None
# create_datetime: 2016-03-04T08:44:34.819000
# revision: 3
# activity: 5893009501585408-1.0.1
# assignment: 5960200909488128
# ip: 150.165.54.139
# timestamp: 2016-03-04T10:57:19.051540
