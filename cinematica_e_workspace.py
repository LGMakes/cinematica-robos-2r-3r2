# Robô 2R e 3R

# bibliotecas:
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

θ1, θ2, θ3 = sp.symbols('θ1 θ2 θ3')
a1, a2, a3 = sp.symbols('a1 a2 a3')

# Cinemática direta:
x_2r = a1*sp.cos(θ1) + a2*sp.cos(θ1+θ2) 
y_2r = a1*sp.sin(θ1) + a2*sp.sin(θ1+θ2) 

x_3r = a1*sp.cos(θ1) + a2*sp.cos(θ1+θ2) + a3*sp.cos(θ1+θ2+θ3)
y_3r = a1*sp.sin(θ1) + a2*sp.sin(θ1+θ2) + a3*sp.sin(θ1+θ2+θ3)

# Matrizes homogêneas
def dh_matrix(theta, length):
    return sp.Matrix([
        [sp.cos(theta), -sp.sin(theta), 0, length*sp.cos(theta)],
        [sp.sin(theta),  sp.cos(theta), 0, length*sp.sin(theta)],
        [0,              0,             1, 0                   ],
        [0,              0,             0, 1                   ]
    ])

A0_1  =  dh_matrix(θ1, a1)
A1_2  =  dh_matrix(θ2, a2)
A2_3  =  dh_matrix(θ3, a3)

A0_2 = sp.simplify(A0_1 * A1_2)
A0_3 = sp.simplify(A0_1 * A1_2 * A2_3)

# Prints
# 2R
print("Cinemática direta 2R:")
sp.pprint("x= " + str(x_2r))
sp.pprint("y = " + str(y_2r))
print("\nMatriz homogênea 2R:\n")
sp.pprint(A0_2) 
# 3R
print("\nCinemática direta 3R:")         
sp.pprint("x = " + str(x_3r))
sp.pprint("y = " + str(y_3r))
print("\nMatriz homogênea 3R:\n")
sp.pprint(A0_3)

# Análise do espaço de trabalho
# 2R
def workspace_2r(a1, a2, n=1000):
    θ1 = np.linspace(0, 2*np.pi, n)
    θ2 = np.linspace(0, 2*np.pi, n)

    X, Y = [], []

    for t1 in θ1:
        for t2 in θ2:
            x = a1*np.cos(t1) + a2*np.cos(t1+t2)
            y = a1*np.sin(t1) + a2*np.sin(t1+t2)
            X.append(x)
            Y.append(y)

    plt.figure(figsize=(6,6))
    plt.scatter(X, Y, s=1, alpha=0.5)
    plt.gca().set_aspect('equal')
    plt.title(f"Espaço de trabalho do robô planar 2R (a1={a1}, a2={a2})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

#3R
def workspace_3r(a1, a2, a3, n=900):
    θ1 = np.linspace(0, 2*np.pi, n)
    θ2 = np.linspace(0, 2*np.pi, n)
    θ3 = np.linspace(0, 2*np.pi, n)

    X, Y = [], []

    for t1 in θ1:
        for t2 in θ2:
            for t3 in θ3:
                x = a1*np.cos(t1) + a2*np.cos(t1+t2) + a3*np.cos(t1+t2+t3)
                y = a1*np.sin(t1) + a2*np.sin(t1+t2) + a3*np.sin(t1+t2+t3)
                X.append(x)
                Y.append(y)

    plt.figure(figsize=(6,6))
    plt.scatter(X, Y, s=1, alpha=0.5)
    plt.gca().set_aspect('equal')
    plt.title(f"Espaço de trabalho do robô planar 3R (a1={a1}, a2={a2}, a3={a3})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

# Chamadas
workspace_2r(a1=2, a2=1.5)  
workspace_3r(a1=2, a2=1.5, a3=1)