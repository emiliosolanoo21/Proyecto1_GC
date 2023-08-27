from math import isclose

def MxM(m1, m2):
    r = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m1[0])):
                r[i][j] += m1[i][k]*m2[k][j]
    return r

def MxV(m, v):
    r = [0, 0, 0, 0]
    for i in range(len(m)):
        for j in range(len(m[0])):
            r[i] += m[i][j]*v[j]
    return r

def barycentricCoords(A, B, C, P):
    
    # Se saca el �rea de los subtri�ngulos y del tri�ngulo
    # mayor usando el Shoelace Theorem, una f�rmula que permite
    # sacar el �rea de un pol�gono de cualquier cantidad de v�rtices.

    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    # Si el �rea del tri�ngulo es 0, retornar nada para
    # prevenir divisi�n por 0.
    if areaABC == 0:
        return None

    # Determinar las coordenadas baric�ntricas dividiendo el 
    # �rea de cada subtri�ngulo por el �rea del tri�ngulo mayor.
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Si cada coordenada est� entre 0 a 1 y la suma de las tres
    # es igual a 1, entonces son v�lidas.
    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
        return (u, v, w)
    else:
        return None
