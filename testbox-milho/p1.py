# coding: utf-8

quantidade_espigas = int(raw_input())

if quantidade_espigas > 0:
    preco_espiga = 0.6
    preco_total = 0

    if quantidade_espigas < 25:
        preco_total = quantidade_espigas*((preco_espiga*.5)+preco_espiga)
    elif quantidade_espigas >= 25 and quantidade_espigas <= 50:
        preco_total = quantidade_espigas*((preco_espiga*.3)+preco_espiga)
    elif quantidade_espigas > 50:
        preco_total = quantidade_espigas*((preco_espiga*.2)+preco_espiga)

    print "O comprador deve pagar R$%.2f por %d espiga(s) de milho." % (preco_total, quantidade_espigas)

