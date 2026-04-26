'''
Representación del tiro parabólico de la bala de un cañón que dispara con
una velocidad inicial de 500 m/s a una altura de 1.5 m. 
'''
import numpy as np
import unidades as u
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar
import moduloTFC as mod

v0 = 500*u.m/u.s
theta = np.pi/4 #rad (45º)
g = 9.81 #m/s^2
t0 = 0
x0 = 0
z0 = 1.5 
ni = 1000

print('Este programa estudia la trayectoria de un proyectil lanzado por un cañón situado que dispara con una velocidad inicial de 500 m/s a una altura de ... m')

#Calculamos el alcance para theta 45º
v0x, v0z = mod.polares_a_cartesianas(500, theta)
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
k=5e-4
#Integramos obteniendo las posiciones y las velocidades para cada eje
x, z, vx, vz= mod.integracion(mod.f, t0, tf, ni, x0, z0, v0x, v0z)

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

#El ángulo ideal para disparar un objetivo en coordenada x:
anguloideal= root_scalar(mod.funcion_de_error, args=(objetivox))
