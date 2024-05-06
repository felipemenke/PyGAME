def colisao_ponto_retangulo(px, py, rx, ry, largura, altura):
    
    if px >= rx and px <= rx + largura and py >= ry and py <= ry + altura:
        return True
    else:
        return False