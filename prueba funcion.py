import moduloTFC as mod
import matplotlib.pyplot as plt
import numpy as np

print(mod.alcance(45))

#Representamos el alcance frente a los ángulos
#angulos = np.linspace(1, 89, 300)
#alcances = mod.alcance(angulos)

#plt.figure()
#plt.plot(angulos, alcances)
#plt.title('Altura en función del ángulo con V0 = 700 m/s')
#plt.xlabel(r'$\theta$ (º)')
#plt.ylabel('z (m)')
#plt.grid()
#plt.show()

#Maximizamos la función con minimize_scalar
#alcancemaximo = mod.maximizacion(mod.alcance_neg)#IMPORTANTE: pasarle a maximizacion la función SIN argumentos, 
#ya que minimize scalar solo acepta funciones
#print(alcancemaximo)


objetivox = 4200

angulo = mod.angulo_disparo(objetivox)
print(angulo)


