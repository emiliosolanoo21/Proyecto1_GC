from math import isclose

def barycentricCoords(A, B, C, P):
    
    # Se saca el área de los subtriángulos y del triángulo
    # mayor usando el Shoelace Theorem, una fórmula que permite
    # sacar el área de un polígono de cualquier cantidad de vértices.

    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    # Si el área del triángulo es 0, retornar nada para
    # prevenir división por 0.
    if areaABC == 0:
        return None

    # Determinar las coordenadas baricéntricas dividiendo el 
    # área de cada subtriángulo por el área del triángulo mayor.
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Si cada coordenada está entre 0 a 1 y la suma de las tres
    # es igual a 1, entonces son válidas.
    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
        return (u, v, w)
    else:
        return None
