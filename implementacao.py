"""
De acordo com o diagrama de corpo livre acima, podemos matematizar o modelo da seguinte forma:
Drag = Fd = −(Cd*ρ*A*v^2)/2 (Relação de Prandtl)
Lift = Fl = −(ρ*v^2*A*CL)(Princípio de Bernoulli)
#######################################################################################################
O que cada elemento é:
Cd = Coeficiente de arrasto = Cl = Cd0 + Cdα(α − α0)^2
Cl = Coeficiente de sustentação = Cl = Cl0 + Clα*α
Cd0, Cdα, Cl0, Clα e α0 = Constantes que dependem do Frisbee, no caso, são: Cd0 = 0.08, Cdα = 2.72, Cl0 = 0.15, CLα = 1.4.
α = Ângulo de Ataque
ρ = Densidade do ar = 1.23 kg/m3
A = Área do Frisbee = π*r^2 (Diâmetro = 0.26m)
v = Velocidade de lançamento do Frisbee = 14 m/s
#######################################################################################################
"""
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from numpy import linspace

#Parâmetros
m = 0.175# Massa do disco (kg)
p = 1.23 # Densidade do Ar
A = 0.0531 # Área do dsico (mˆ2)
g = 9.81 # Gravidade (m/sˆ2)

Cl0 = 0.15
Cd0 = 0.08
Clalpha = 1.4
Cdalpha = 2.72

angulo = 7.5 # ângulo de arremesso em graus˚
alpha = (angulo * math.pi)/180 # ângulo de arremesso em radianos
alpha0 = (-4*math.pi)/180

def Func(S, t): # S = [x, y, vx, vy]
    
    dxdt = S[2]
    dydt = S[3]
    Cl = Cl0 + (Clalpha * alpha)
    Cd = Cd0 + (Cdalpha * ((alpha - alpha0)**2))
    

    v = math.sqrt(S[2]**2 + S[3]**2)
    

    P = m*g 
    Lx = ((p * Cl * A * (v**2))/2) * (S[3]/v)
    Ly = ((p * Cl * A * (v**2))/2) * (S[2]/v)
    Dx = ((p * Cd * A * (v**2))/2) * (S[2]/v)
    Dy = ((p * Cd * A * (v**2))/2) * (S[3]/v)
    
    dVydt = (Ly - Dy - P) / m
    dVxdt = (Lx - Dx) / m
    
    return [dxdt, dydt, dVxdt, dVydt]


# Criando Lista tempo
Tempos = linspace(0, 10, 100000)

#Condição Inicial
x0 = 0
y0 = 1
vx0 = 14 * math.cos(alpha)
vy0 = 14 * math.sin(alpha)

Valores_iniciais = [x0, y0, vx0, vy0]


#Odeint - Realiza a integração numérica
Valores = odeint(Func, Valores_iniciais, Tempos)

#Plotagem do Gráfico
plt.plot(Valores[:,0], Valores[:,1])
plt.xlabel('Distância (m)')
plt.ylabel('Altura (m)')
plt.axis([0, max(Valores[:,0]), 0, 12])
plt.title(r'Trajetória do Frisbee')
plt.show()

plt.plot(Tempos, Valores[:,2])
plt.title(r'Vx')
plt.show()

plt.plot(Tempos, Valores[:,3])
plt.title(r'Vy')
plt.show()