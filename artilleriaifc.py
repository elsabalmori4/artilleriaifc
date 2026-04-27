'''
Representación del tiro parabólico de la bala de un cañón que dispara con
una velocidad inicial de v0 m/s a insertar a una altura de 1.5 m. 
'''
import numpy as np
import unidades as u
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar
import moduloTFC as mod

#Constantes
g = 9.81 #aceleración de la gravedad (m/s^2)
k=5e-4 #coeficiente de rozamiento

print('Este programa estudia la trayectoria de un proyectil lanzado por un cañón situado que dispara con una velocidad inicial de 500 m/s a una altura de ... m')

#Parámetros de disparo
v0 = 500*u.m/u.s #velocidad inicial (m/s)
theta = np.pi/4 #ándulo de disparo (rad) (45º)
x0, z0, t0 = 0, 1.5, 0 #posición inicial
ni = 1000 #número de puntos

#convertimos la velocidad a cartesianas
v0x, v0z = mod.polares_a_cartesianas(v0, theta)

#calculamos el alcance sin rozamiento
xmax = mod.alcancemax_tiroparabolico(v0x, v0z, z0)
print('Se calcula el alcance máximo para un ángulo de 45º en un sistema sin rozamiento.')
print('El alcance máximo es: ' +str(xmax) +' m')
print('-'*20)

#El instante en el que llega al suelo (z=0)
tmax = xmax/(v0*np.cos(theta))
tf = tmax

#Para representar la trayectoria:
#Tiempos
t = np.linspace(t0, tmax, ni)
#Posición para cada instante
posix = mod.mru(v0x,t)
posiz = mod.mrua_posicion(v0z, t, z0)

#Se representa z frente a x
plt.figure()
plt.plot(posix, posiz)
plt.title('Trayectoria disparo sin rozamiento para $\theta$ = 45º')
plt.xlabel('x (m)')
plt.ylabel('z (m)')
plt.grid()
plt.show()

#Trayectoria para el mismo ángulo (45º) con rozamiento
print('Se calcula el alcance máximo para un ángulo de 45º en un sistema con rozamiento')

#Integramos obteniendo las posiciones y las velocidades para cada eje
x, z, vx, vz= mod.integracion(mod.f, t0, tmax, ni, x0, z0, v0x, v0z)

#Interpolación:
#Buscamos el último punto antes de llegar al suelo (índice)
zipos = np.where(z>=0)[0][-1]
#Un índice más: el primer punto de z negativo
zineg = zipos+1
#El valor que toma z
zpos = z[zipos]
zneg = z[zineg]
#El valor de x para estos z
xpos = x[zipos]
xneg = x[zineg]

#Valor de x calculado
xcero = mod.interpolación(xpos, xneg, zpos, zneg)
print('El alcance máximo aproximado es: '+ str(xcero)+' m')

#Para representar la trayectoria:
#Se quiere representar únicamente la parte en la que z es positiva.
puntosx = x[0:zipos]
puntosxfinal = np.append(puntosx, xcero)
puntosz = z[0:zipos]
puntoszfinal = np.append(puntosz, 0)

#Se representa z frente a x
plt.figure()
plt.plot(puntosxfinal, puntoszfinal)
plt.title('Trayectoria disparo con rozamiento para $\theta$ = 45º')
plt.xlabel('x (m)')
plt.ylabel('z (m)')
plt.grid()
plt.show()

'''
Aquí yo metería algo de root_scalar no? 
En plan lo de insertar el ángulo y la velocidad.
'''

#ANIMACIÓN
#Crear la figura para la animación
fig, ax = plt.subplots()
ax.set_xlim(0, np.max(x) + 10)
ax.set_ylim(0, np.max(z) + 10)
line, = ax.plot([], [], 'b-', label="Trayectoria")
point, = ax.plot([], [], 'ro', label="Proyectil")
ax.set_title('Trayectoria del proyectil')
ax.set_xlabel('x (m)')
ax.set_ylabel('z (m)')
ax.legend()

# Función de inicialización
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

# Función de actualización para la animación
def update(frame):
    line.set_data(x[:frame], z[:frame])
    point.set_data(x[frame], z[frame])
    return line, point

# Crear la animación
ani = FuncAnimation(fig, update, frames=range(1, len(x)), init_func=init, blit=True, interval=20)

# Mostrar la animación
plt.show()
