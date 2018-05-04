x = float(raw_input())
y = float(raw_input())

if x>0 and y>0:
  print "Primeiro quadrante."
elif x>0 and y<0:
  print "Quarto quadrante."
elif x<0 and y>0:
  print"Segundo quadrante."
elif x<0 and y<0:
  print "Terceiro quadrante."
elif x == 0 and y != 0 :
    print "Sobre eixo."
elif y == 0 and x != 0:
    print "Sobre eixo."
elif x == 0 and y == 0:
    print "Centro."                
####
# group: prog1-20152
# mode: mtp3
# open_datetime: None
# create_datetime: 2016-03-04T11:57:33.154560
# revision: 1
# activity: 5893009501585408-1.0.1
# assignment: 6572659487801344
# ip: 150.165.75.252
# timestamp: 2016-03-04T12:31:04.750700
