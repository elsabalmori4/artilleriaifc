'''
Representación del tiro parabólico de la bala de un cañón considerando: 
x0, y0 = 0 
theta = pi/4
v0 = 500 m/s
'''
import numpy as np
import unidades as u
import cinematica as cn
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import moduloTFC as mod

v0 = 500*u.m/u.s
theta = np.pi/4
g = 9.81
t0 = 0
x0 = 0
z0 = 0
ni = 100

#Calculamos el alcance para theta 45º
v0x, v0z = cn.polares_a_cartesianas(500, theta)
xmax = cn.alcancemax_tiroparabolico(v0x, v0z)
print('El alcance máximo es: ' +str(xmax) +str(' m'))

tmax = xmax/(v0*np.cos(theta))
tf = tmax
#Calculamos los tiempos
t = np.linspace(0, tmax, ni)
posix = cn.mru(v0x,t)
posiz = cn.mrua_posicion(v0z, t)

plt.figure()
plt.plot(posix, posiz)
plt.title('Disparo teórico sin rozamiento $\theta$ = 45º')
plt.xlabel('x (m)')
plt.ylabel('z (m)')
plt.grid()
plt.show()

#Con rozamiento
k=5e-4
x, z, vx, vz= mod.integracion(mod.f, t0, tf, ni, x0, z0, v0x, v0z)

print(z)


zrealp = np.where(z>=0)[0][-1]
print(zrealp)
zrealn = zrealp+1
xrealp = x[zrealp]
xrealn = x[zrealn]
zrn = z[zrealn]
zrp = z[zrealp]

print(x[zrealp])
print(x[zrealn])
print(zrn)
print(zrp)

xcero = mod.interpolación(xrealp, xrealn, zrp, zrn)
print(xcero)

puntosx = x[0:47]
puntosxfinal = np.append(puntosx, xcero)
puntosz = z[0:47]
puntoszfinal = np.append(puntosz, 0)
print(puntosxfinal)
print(puntoszfinal) 

plt.figure()
plt.plot(puntosxfinal, puntoszfinal)
plt.title('Disparo con rozamiento $\theta$ = 45º')
plt.xlabel('x (m)')
plt.ylabel('z (m)')
plt.grid()

plt.show()

