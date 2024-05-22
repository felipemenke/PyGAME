def colisao_entre_retangulos(x1, y1, largura1, altura1, x2, y2, largura2, altura2):
    
    if (x1 < x2 + largura2 and x1 + largura1 > x2 and
        y1 < y2 + altura2 and y1 + altura1 > y2):
        return True
    else:
        return False
    