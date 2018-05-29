# coding: utf-8
# Custo do Milho
# Referencia, Eliane Araujo

qtde = int(raw_input())

custo = 30./50
if qtde < 25:
    valor = 1.5 * custo
elif qtde <= 50:
   valor = 1.3 * custo
else:
    valor = 1.2 * custo

print "O comprador deve pagar R$%.2f por %d espiga(s) de milho." % (valor * qtde, qtde)
