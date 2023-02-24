# Emergencias-SIN

## Escenario básico
Se trata de modelar un problema de transporte de víctimas de accidentes a un
hospital. El objetivo de alto nivel a resolver es Deliver_victim, que toma como
parámetros la víctima a trasladar y el hospital al que se la debe trasladar. Para ello,
es necesario disponer de una ambulancia en la localización de la víctima, cargar a la
víctima en la ambulancia, conducir la ambulancia desde la localización actual hasta el
hospital y descargar a la víctima de la ambulancia en las urgencias del hospital.

Este objetivo se puede resolver de las siguientes formas:

1. Si ya disponemos de una ambulancia en el lugar del accidente, simplemente
utilizamos esta ambulancia para trasladar a la víctima.
2. En caso contrario, se debe traer una ambulancia hasta el lugar del accidente.
La ambulancia a escoger debe ser la que se encuentre más cerca.
3. En cualquier caso, si la víctima necesita una primera asistencia (su nivel de
gravedad supera un determinado umbral), cuando se dispone de la
ambulancia, se le atiende in-situ y luego se le traslada.

La información a representar en el problema es la siguiente:
- Víctima: nombre, edad, localización, nivel de gravedad
- Hospital: nombre, localización
- Ambulancia: nombre, localización, nivel de gravedad máximo que puede tratar
Además, se debe representar un grafo con las distancias entre las diferentes
localizaciones. Se asume que es posible viajar entre cualquier par de localizaciones y
el tiempo de viaje es proporcional a la distancia euclídea entre ambas.

## Ampliación 1: Asignación de ambulancia según el nivel de gravedad
En esta ampliación, la ambulancia que se asigne a una víctima debe poder tratar un
nivel de gravedad máximo superior o igual al nivel de gravedad de la víctima.

## Ampliación 2: Atención a más de una víctima
En esta ampliación, el objetivo de alto nivel se repetirá para tantas víctimas como se
definan en el estado inicial. Dichas víctimas podrán encontrarse en diferentes
localizaciones.
