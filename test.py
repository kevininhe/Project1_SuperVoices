from tasks import hola, sumar_numeros

# Para ejecutar una función en forma de tarea lo tenemos que hacer de esta forma:

hola.delay('Mundo!')

# Para ejecutar la función sumar:

sumar_numeros.delay(3, 2)
