import math

order_belt = {'Branca': 0, 'Azul': 1, 'Roxa': 2, 'Marrom': 3, 'Preta': 4 }

def calcula_aulas_necessarios_proximo_nivel(n):
    d = 1.47
    k = 30 / math.log(d)

    aulas = k * math.log(n + d)
    
    return round(aulas)