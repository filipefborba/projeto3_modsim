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
from matplotlib.widgets import Slider, Button, RadioButtons

#Parâmetros
m = 0.175# Massa do disco (kg)
p = 1.23 # Densidade do Ar
A = 0.0531 # Área do dsico (mˆ2)
g = 9.81 # Gravidade (m/sˆ2)

Cl0 = 0.15
Cd0 = 0.08
Clalpha = 1.4
Cdalpha = 2.72
alpha0 = (-4*math.pi)/180

angulo = 7.5 # ângulo de arremesso em graus˚
alpha = (angulo * math.pi)/180 # ângulo de arremesso em radianos

def Func(S, t, alpha): # S = [x, y, vx, vy]
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
Valores = odeint(Func, Valores_iniciais, Tempos, (alpha,))

#Verificando a distância e altura máxima
lista_distancia_maxima = []
for i in range(len(Valores[:,1])):
    if Valores[i][1] > -0.05 and Valores[i][1] < 0.05:
        lista_distancia_maxima.append(Valores[i][0])
lista_altura_maxima = [max(Valores[:,1])]

################################################
#Sliders
################################################

#Gráfico Principal
#-----------------
#É o gráfico inicial, antes das interações com os sliders
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)
l, = plt.plot(Valores[:,0], Valores[:,1], lw=2, color='green')
plt.xlabel('Distância (m)')
plt.ylabel('Altura (m)')
plt.axis([0, 30, 0, 12])
plt.title(r'Trajetória do Frisbee')

#Definição e criação dos sliders
axcolor = 'lightgoldenrodyellow'
axvelocidade = plt.axes([0.22, 0.1, 0.65, 0.03], axisbg=axcolor)
axangulo = plt.axes([0.22, 0.15, 0.65, 0.03], axisbg=axcolor)
svelocidade = Slider(axvelocidade, 'Velocidade inicial', 10, 20, valinit=14)
sangulo = Slider(axangulo, 'Ângulo', 0, 60, valinit=angulo)

#Label da distância
distanciafinal = lista_distancia_maxima[0]
textstr = "Distância: {0:.2f} m".format(distanciafinal)
props = dict(boxstyle='round', facecolor='white', alpha=1)
axdistancia = ax.text(-0.05, -0.4, textstr, transform=ax.transAxes, fontsize=14,verticalalignment='top', bbox=props)

#Label da altura
alturafinal = lista_altura_maxima[0]
textstr2 = "Altura: {0:.2f} m".format(alturafinal)
axaltura = ax.text(0.3, -0.4, textstr2, transform=ax.transAxes, fontsize=14,verticalalignment='top', bbox=props)

#Atualização dos valores
def update(val):
    global distanciafinal
    global alturafinal
    lista_distancia_maxima.clear()
    lista_altura_maxima.clear()
    vel = svelocidade.val
    ang = sangulo.val
    alpha_atualizado = (ang * math.pi)/180
    vx0_atualizado = vel * math.cos(alpha_atualizado)
    vy0_atualizado = vel * math.sin(alpha_atualizado)
    Valores_iniciais = [x0, y0, vx0_atualizado, vy0_atualizado]
    valores_atualizados = odeint(Func, Valores_iniciais, Tempos, (alpha_atualizado,))
    l.set_xdata(valores_atualizados[:,0])
    l.set_ydata(valores_atualizados[:,1])
    fig.canvas.draw_idle()

    for i in range(len(valores_atualizados[:,1])):
        if valores_atualizados[i][1] > -0.05 and valores_atualizados[i][1] < 0.05:
            distanciafinal = valores_atualizados[i][0]
    alturafinal = valores_atualizados[i][1]

svelocidade.on_changed(update)
sangulo.on_changed(update)


#Botão de reset
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

#Função do botão reset
def reset(event):
    svelocidade.reset()
    sangulo.reset()
button.on_clicked(reset)

#Mudar cor da linha do gráfico
# rax = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor)
# radio = RadioButtons(rax, ('green', 'blue', 'red'), active=0)
# def colorfunc(label):
#     l.set_color(label)
#     fig.canvas.draw_idle()
# radio.on_clicked(colorfunc)

#Plotagem do Gráfico
plt.show()


lista_angulo = linspace(0,60,100000)
lista_velocidade = linspace(10,20,100000)


plt.plot(lista_x, lista_angulo, lw=2)
plt.xlabel('Distância (m)')
plt.ylabel('Ângulo (˚)')
plt.axis([0, max(lista_x), 0, max(lista_angulo)])
plt.title(r'Distância x Ângulo')
#plt.show()

plt.plot(lista_x, lista_velocidade, lw=2)
plt.xlabel('Distância (m)')
plt.ylabel('Velocidade inicial (m/s)')
plt.axis([0, max(lista_x), 0, max(lista_velocidade)])
plt.title(r'Distância x Velocidade Inicial (â = 7.5˚)')
#plt.show()