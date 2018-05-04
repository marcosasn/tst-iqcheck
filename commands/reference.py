# coding: utf-8
# Solucao de referencia atribuida, de forma ad hoc, a um aluno.
# Não foi encontrada solucao de referencia proposta por professor.
# Rever esta solref no futuro
# Sávio morais

x = float(raw_input())
y = float(raw_input())

if x > 0 and y > 0:
    print 'Primeiro quadrante.'
elif x < 0 and y > 0:
    print 'Segundo quadrante.'
elif x < 0 and y < 0:
    print 'Terceiro quadrante.'
elif x > 0 and y < 0:
    print 'Quarto quadrante.'
elif x == 0 and y == 0:
    print 'Centro.'
else:
    print 'Sobre eixo.'
####
# user: savio.morais@ccc.ufcg.edu.br
# group: prog1-20152
# mode: mtp3
# open_datetime: None
# create_datetime: 2016-03-04T12:03:25.785040
# revision: 1
# activity: 5893009501585408-1.0.1
# assignment: 6347460662263808
# ip: 150.165.75.252
# timestamp: 2016-03-04T12:13:34.147360
