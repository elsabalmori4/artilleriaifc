'''
Módulo para la simulación del tiro parabólico con rozamiento
'''
import numpy as np
import matplotlib.pyplot as plt
import unidades as u
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar
k = 5e-4
g = 9.81


def f(t, xzvxvz):
	'''
	Función a integrar por solve_ivp
	'''
	x = xzvxvz[0]
	z = xzvxvz[1]
	vx = xzvxvz[2]
	vz =  xzvxvz[3]
	g = 9.81
	raiz = (vx**2 + vz**2)**0.5
	
	dxdt = vx
	dzdt = vz
	dvxdt = -k*vx*raiz
	dvzdt =  -g-k*vz*raiz
	return [dxdt, dzdt, dvxdt, dvzdt]

def alcancemax_tiroparabolico (v0x, v0y, y0 = 0):
	'''
	Esta función me calcula el alcance máximo de un cuerpo que describe
	un movimiento parabólico
	'''
	t = (2*(y0+v0y))/g
	return v0x*t



	
	
def polares_a_cartesianas (r, theta):
	'''
	Esta función hace el paso de coordenadas polares a coordenadas
	cartesianas
	'''
	x = r*np.cos(theta)
	y = r*np.sin(theta)
	return x, y

def mru (v, t,r0 = 0):
	'''
	Esta función calcula la posición de un móvil que describe un mru
	'''
	return r0 + v*t


def mrua_posicion (v0, t, r0 = 0, a = -g):
	'''
	Esta función calcula la posición de un móvil que describe un mrua
	'''
	return r0 + v0*t +0.5*a*t**2


def integracion (f, t0, tf, ni,x0, z0, v0x, v0z):
	'''
	Esta función nos integra las ec. diferenciales para hallar los valores de x, z, vx y vz
	'''
	tp = np.linspace(t0, tf, ni)
	xzvxvz = solve_ivp(f, [tp[0], tp[-1]], [x0, z0, v0x, v0z], t_eval=tp).y 
	x = xzvxvz[0, :]
	z = xzvxvz[1, :]
	vx = xzvxvz[2, :]
	vz = xzvxvz[3, :]
	
	return x, z, vx, vz
	

def interpolación (x1, x2, y1, y2):
	'''
	Esta función nos devuelve el punto en el que y = 0 haciendo una interpolación
	'''
	m = (y2-y1)/(x2-x1)
	n = y1 - m*x1
	x = -n/m
	return x
	


def alcance (theta):
	'''
	Esta función nos calcula el alcande que tendrá un proyectil de artillería
	dado un ángulo de disparo concreto
	'''
	alpha = np.radians(theta)
	v = eval(input('Introduzca velocidad de disparo en m/s'))

	
	v0 = v*u.m/u.s
	
	v0x, v0z = polares_a_cartesianas(v0, alpha) #Obtenemos las componentes iniciales de v
	x0, z0, t0 = 0, 0, 0
	ni = 1000
	xmax = alcancemax_tiroparabolico(v0x, v0z)
	tmax = xmax/(v0*np.cos(alpha))
	tf = tmax
	
	x, z, vx, vz = integracion(f, t0, tf, ni, x0, z0, v0x, v0z) #Integramos las ecuaciones diferenciales

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
	xcero = interpolación(xpos, xneg, zpos, zneg)
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
	plt.title(r'Trayectoria disparo con rozamiento para $\theta$ = 45º')
	plt.xlabel('x (m)')
	plt.ylabel('z (m)')
	plt.grid()
	plt.show()
	return ('El alcance máximo para theta = ' +str(theta) + 'º es ' +str(xcero)+' m')  
	


	
def funcion_de_error(angulo, objetivox):
	'''
	Esta función devuelve la diferencia entre donde cae el proyectil y 
	donde está el blanco (objetivox).
	'''
	return alcance(angulo)- objetivox
	


def angulo_disparo (xcero):
	'''
	Esta función nos devuelve el ángulo con el que debemos disparar para acertar
	un objetivo en un punto x usando rootscalar
	'''
	angulo = root_scalar(funcion_de_error, args=(xcero), bracket=[0, np.pi/2], method = 'bisección')
	return angulo.root
