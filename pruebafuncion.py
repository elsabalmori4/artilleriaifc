import moduloTFC as mod

alpha = eval(input('Introduzca el ángulo de disparo en grados '))
v = eval(input('Introduzca velocidad de disparo en m/s '))

prueba = mod.alcance(alpha)
print(prueba)

objetivo = 4602.75

angulo = mod.angulo_disparo(objetivo)
print(angulo)
