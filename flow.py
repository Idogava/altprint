import numpy as np

def flow_math(w, h, df, adjust):
    """
    Calcula o fator multiplicador de fluxo de filamento, usandfo o modelo
    do retângulo com bordas circulares.

    Args:
    w: comprimento do raster
    h: altura do raster
    df: diametro do filamento
    adjust: fator de calibração

    Returns:
    flow: fator multiplicador do fluxo
    """
    a = 4 * w * h + (np.pi - 4) * h**2
    b = np.pi * df**2
    flow = adjust * a / b
    return flow


def extrude(x, y, flow):
    """
    Gera o vetor com as coordenadas da extrusão do filamento.

    Args:
    x: vetor com as componentes x dos pontos
    y: vetor com as componentes y dos pontos
    flow: fator multiplicador do fluxo

    Returns:
    extrusion: vetor com as coordenadas da extrusão do filamento.
    """
    extrusion = np.zeros(len(x))
    for i in range(1, len(x)):
        dx = abs(x[i] - x[i - 1])
        dy = abs(y[i] - y[i - 1])
        extrusion[i] = np.sqrt((dx**2) + (dy**2)) * flow + extrusion[i-1]
    return extrusion
