import math

def colisao_ponto_circulo(px, py, cx, cy, raio):
    
    distancia = math.sqrt((px - cx)**2 + (py - cy)**2)
    
    
    if distancia <= raio:
        return True
    else:
        return False