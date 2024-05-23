import math

def colisao_entre_circulos(cx1, cy1, raio1, cx2, cy2, raio2):
    
    distancia_centros = math.sqrt((cx2 - cx1)**2 + (cy2 - cy1)**2)
    
    
    if distancia_centros <= raio1 + raio2:
        return True
    else:
        return False