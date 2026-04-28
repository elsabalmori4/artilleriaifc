'''
Módulo para la simulación del tiro parabólico con rozamiento
'''
import numpy as np
import matplotlib.pyplot as plt
import unidades as u
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar
from scipy.optimize import minimize_scalar
from matplotlib.animation import FuncAnimation
k = 5e-4
g = 9.81


def funcion_integracion(t, xzvxvz):
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
	
	
	x = xzvxvz[0]
	z = xzvxvz[1]
	vx = xzvxvz[2]
	vz = xzvxvz[3]
	
	return x, z, vx, vz


def interpolación (x1, x2, y1, y2):
	'''
	Esta función nos devuelve el punto en el que y = 0 haciendo una interpolación
	'''
	m = (y2-y1)/(x2-x1)
	n = y1 - m*x1
	x = -n/m
	return x


def angulo_teorico (objetivox):
	'''
	Esta función devuelve los 2 ángulos TEÓRICOS sin rozamiento con los que alcanzar un objetivo de disparo
	'''
	v0 = 700
	a = 0.5*g*objetivox/v0**2
	c = -a
	angulo1 = (-1+np.sqrt(1-4*a*c))/2*a
	angulo2 = (-1-np.sqrt(1-4*a*c))/2*a
	return angulo1, angulo2


def alcance (theta):
	if type(theta) == np.ndarray:
			return np.array([alcance_simple(i) for i in theta])
	
	else:
		return alcance_simple(theta)


def alcance_simple (theta):
		'''
		Esta función nos calcula el alcande que tendrá un proyectil de artillería
		dado un ángulo de disparo y una velocidad concretos
		'''
		alpha = np.radians(theta)
		v = 700
	
		v0 = v*u.m/u.s
	
		v0x, v0z = polares_a_cartesianas(v0, alpha) #Obtenemos las componentes iniciales de v
		x0, z0, t0 = 0, 0, 0
		ni = 1000
		tmax = 2*v0*np.sin(alpha)/g

	
		x, z, vx, vz = integracion(funcion_integracion, t0, tmax, ni, x0, z0, v0x, v0z) #Integramos las ecuaciones diferenciales

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

		#Para representar la trayectoria:
		#Se quiere representar únicamente la parte en la que z es positiva.
		puntosx = x[0:zipos]
		puntosxfinal = np.append(puntosx, xcero)
		puntosz = z[0:zipos]
		puntoszfinal = np.append(puntosz, 0)

		#Se representa z frente a x
		#plt.figure()
		#plt.plot(puntosxfinal, puntoszfinal)
		#plt.title(r'Trayectoria disparo con rozamiento para $\theta$ = 45º')
		#plt.xlabel('x (m)')
		#plt.ylabel('z (m)')
		#plt.grid()
		#plt.show()
		return xcero



def alcance_sin_roz(theta):
	'''
	Esta función nos calcula el alcance de un proyectil sin considerar el rozamiento
	'''
	alpha = np.radians(theta)
	v = 700

	v0 = v*u.m/u.s
	
	v0x, v0z = polares_a_cartesianas(v0, alpha) #Obtenemos las componentes iniciales de v
	x0, z0, t0 = 0, 1.5, 0
	xmax = alcancemax_tiroparabolico(v0x, v0z, z0)
		return xmax

def representaciones (theta):
		'''
		Esta función representa para un ángulo la trayectoria sin rozamiento y
		con rozamiento (animado y sin animar)
		'''
		alpha = np.radians(theta)
		v = 700
	
		v0 = v*u.m/u.s
	
		v0x, v0z = polares_a_cartesianas(v0, alpha) #Obtenemos las componentes iniciales de v
		x0, z0, t0 = 0, 0, 0
		ni = 1000
		xmax = alcancemax_tiroparabolico(v0x, v0z, z0)
		tmax = 2*v0*np.sin(alpha)/g
		
		#Representar la trayectoria sin rozamiento
		#Tiempos
		t = np.linspace(t0, tmax, ni)
		#Posición para cada instante
		posix = mru(v0x,t)
		posiz = mrua_posicion(v0z, t, z0)
		
		#Se representa z frente a x
		plt.figure()
		plt.plot(posix, posiz)
		plt.title(r'Trayectoria disparo sin rozamiento para $\theta$ = '+ str(theta)+'º')
		plt.xlabel('x (m)')
		plt.ylabel('z (m)')
		plt.grid()
		plt.show()
	
		x, z, vx, vz = integracion(funcion_integracion, t0, tmax, ni, x0, z0, v0x, v0z) #Integramos las ecuaciones diferenciales

		#Interpolación:
		#Buscamos el último punto antes de llegar al suelo (índice)
		zipos = np.where(z>=0)[0]
if len(zipos)==0:
			return 0
		zipos = zipos[-1]  # Último índice con z >= 0
		# Evitar acceder fuera del límite de los índices
		if zipos + 1 < len(z):
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
		else: 
			xcero= x[zipos]
		#Valor de x calculado
		xcero = interpolación(xpos, xneg, zpos, zneg)

		#Para representar la trayectoria:
		#Se quiere representar únicamente la parte en la que z es positiva.
		puntosx = x[0:zipos]
		puntosxfinal = np.append(puntosx, xcero)
		puntosz = z[0:zipos]
		puntoszfinal = np.append(puntosz, 0)
		
		#Se representa z frente a x
		plt.figure()
		plt.plot(puntosxfinal, puntoszfinal)
		plt.title(r'Trayectoria disparo con rozamiento para $\theta$ = '+str(theta)+'º')
		plt.xlabel('x (m)')
		plt.ylabel('z (m)')
		plt.grid()
		plt.show()
		
		#ANIMACIÓN
		animar_trayectoria(theta)
		return None
+		

def animar_trayectoria(theta_):
	'''
	Esta función realiza la animación de la trayectoria de un proyectil 
	dado un ángulo de disparo y velocidad inicial.
	'''
	v0 = 700
	ni = 1000
	theta= np.radians(theta_)
	v0x, v0z= polares_a_cartesianas(v0, theta)
	x0, z0, t0= 0,0, 0
	tmax= 2*v0*np.sin(theta)/g
	t= np.linspace(t0, tmax, ni)
	x, z, vx, vz = integracion(funcion_integracion, t0, tmax, ni, x0, z0, v0x, v0z)
	
	#crear la figura
	fig, ax= plt.subplots()
	ax.set_xlim(0, np.max(x) + 10)
	ax.set_ylim(0, np.max(z) + 10)
	line, = ax.plot([], [], 'b-', label="Trayectoria")
	point, = ax.plot([], [], 'ro', label="Proyectil")
	ax.set_title(r'Trayectoria del proyectil con $\theta$ = '+str(theta_)+'º')
	ax.set_xlabel('x (m)')
	ax.set_ylabel('z (m)')
	ax.legend()
	
	# Función de inicialización (vaciar los datos)
	def init():
		line.set_data([], [])
		point.set_data([], [])
		return line, point
	
	# Función de actualización para cada frame
	def update(frame):
		line.set_data(x[:frame], z[:frame])  # Actualiza la línea
		point.set_data([x[frame]], [z[frame]])   # Mueve el proyectil
		return line, point
		
	# Crear la animación
	ani = FuncAnimation(fig, update, frames=range(1, len(x)), init_func=init, interval=10)
	# Mostrar la animación
	plt.show()	
	return None


def alcance_neg (theta):
	'''
	Esta función nos maximiza la función alcance
	'''
	return -alcance(theta)

	
def maximizacion (f):
	'''
	Esta función máximiza el alcance
	'''
	resultado = minimize_scalar(f, bounds=(20, 70))
	return -resultado.fun, resultado.x	
	

def funcion_de_error(angulo, objetivox):
	'''
	Esta función devuelve la diferencia entre donde cae el proyectil y 
	donde está el blanco (objetivox).
	'''
	return alcance(angulo)- objetivox
	

def angulo_disparo (objetivox):
	'''
	Esta función nos devuelve el ángulo con el que debemos disparar para acertar
	un objetivo en un punto x usando rootscalar
	'''
	alcancemaximo, thetamax = maximizacion(alcance_neg)
	
	if objetivox > alcancemaximo:
		return 'ERROR: El alcance seleccionado es mayor que el alcance máximo del proyectil'
	elif objetivox <= 0:
		return 'ERROR: el alcance seleccionado es negativo'
	else:
		angteorico1, angteorico2 = angulo_teorico(objetivox)
		
		angulo1 = root_scalar(funcion_de_error, args=(objetivox), x0 = angteorico1, method = 'secant')
		return  angulo1.root
