# App-programacion
Propuesta de mejora de la app

LlegaBien
Integrantes: Matías, Paolo, Rogelio y Mateo.
LlegaBien es una aplicación de escritorio que permite al dueño de una empresa saber qué trabajadores tienen un traslado de riesgo, en qué colonias se concentran y cuánto le cuesta la rotación relacionada con el traslado.
Este documento explica qué tendrá nuestra versión mínima, cómo la programaremos y cómo adaptaremos la Starter App del curso, que actualmente trabaja con datos de tráfico en intersecciones.
1. Priorización MoSCoW
Responsable: Matías.
Must Have
Lo necesario para demostrar nuestra propuesta.
Pantalla de inicio con el problema, el usuario y la propuesta de valor.
Formulario para registrar a un trabajador.
Tabla con los trabajadores y su nivel de riesgo.
Semáforo de riesgo alto, medio y bajo.
Las tres colonias con más trabajadores en riesgo alto.
Calculadora del costo de la rotación.
Justificación: Sin estas funciones, la aplicación no permite saber qué pasa, dónde actuar y cuánto le cuesta a la empresa.
Should Have
Lo que mejora el valor de la aplicación.
Identificar la hora de entrada con mayor promedio de retardos por trabajador.
Calcular si una ruta de transporte se paga sola.
Generar alertas automáticas.
Mostrar mensajes claros cuando un dato del formulario está mal.
Justificación: Estas funciones hacen el diagnóstico más útil para tomar decisiones, aunque la aplicación puede funcionar sin ellas.
Could Have
Lo que haremos si alcanza el tiempo.
Gráfica de riesgo por colonia con Matplotlib, usando el Technology Booster.
Datos externos mediante una API para estimar tiempos de traslado en el periodo 3.
Guardar el reporte en un archivo.
Comparar dos encuestas, antes y después de un cambio.
Justificación: Estas mejoras permiten presentar mejor los resultados o tener más precisión. Las agregaremos con los boosters del curso si hay tiempo.
2. Funciones del sistema
Responsable de organizar esta sección: Paolo.
Cada integrante propuso al menos una función para la aplicación. También repartimos las funciones para que cada uno se encargue inicialmente de dos.
Matías propuso calcular_costo_rotacion y ruta_se_paga.
Paolo propuso clasificar_riesgo y validar_trabajador.
Rogelio propuso resumir_plantilla y colonias_con_mas_riesgo.
Mateo propuso hora_con_mas_retardos y generar_alertas.
F1. clasificar_riesgo
Nombre: clasificar_riesgo.
Propuesta por: Paolo.
Propósito: Clasificar el traslado de un trabajador como riesgo alto, medio o bajo. Reemplaza la función del mismo nombre que trae la plantilla, que utiliza flujo, velocidad e incidentes.
Parámetros:
Minutos de traslado del trabajador, como número entero.
Número de transbordos, como número entero.
Valor de retorno: Texto con el nivel ALTO, MEDIO o BAJO.
Algoritmo o pseudocódigo:
Si los minutos son mayores o iguales a 60, o los transbordos son mayores o iguales a 2, regresar ALTO.
Si no se cumple lo anterior, pero los minutos son mayores o iguales a 30, o los transbordos son iguales a 1, regresar MEDIO.
En los demás casos, regresar BAJO.
Casos de prueba:
65 minutos y 0 transbordos: ALTO.
45 minutos y 1 transbordo: MEDIO.
20 minutos y 0 transbordos: BAJO.
20 minutos y 2 transbordos: ALTO.
Casos límite:
60 minutos y 0 transbordos: ALTO.
59 minutos y 0 transbordos: MEDIO.
Responsable inicial: Paolo.
Prioridad: Must Have.
F2. resumir_plantilla
Nombre: resumir_plantilla.
Propuesta por: Rogelio.
Propósito: Crear el semáforo de la empresa, contando cuántos trabajadores hay en cada nivel de riesgo y qué porcentaje tarda 60 minutos o más. Reemplaza la función resumir_registros de la plantilla.
Parámetro: Lista de trabajadores con sus datos, obtenida de la función cargar_csv.
Valor de retorno: Diccionario con la cantidad de trabajadores en ALTO, MEDIO y BAJO, y el porcentaje que tarda 60 minutos o más.
Algoritmo o pseudocódigo:
Iniciar los contadores ALTO, MEDIO, BAJO y largos en cero.
Recorrer la lista de trabajadores.
Para cada trabajador, obtener su nivel con clasificar_riesgo y sumar uno al contador correspondiente.
Si sus minutos de traslado son 60 o más, sumar uno al contador largos.
Calcular el porcentaje dividiendo largos entre el total de trabajadores y multiplicando por 100.
Regresar los tres contadores y el porcentaje.
Caso de prueba:
Cuatro trabajadores con tiempos de 70, 40, 10 y 15 minutos, todos con cero transbordos.
Resultado esperado:
ALTO: 1 trabajador.
MEDIO: 1 trabajador.
BAJO: 2 trabajadores.
Porcentaje que tarda 60 minutos o más: 25.0 %.
Responsable inicial: Rogelio.
Prioridad: Must Have.
F3. colonias_con_mas_riesgo
Nombre: colonias_con_mas_riesgo.
Propuesta por: Rogelio.
Propósito: Identificar en qué colonias se concentran los trabajadores con riesgo alto.
Parámetros:
Lista de trabajadores.
Cantidad de colonias a mostrar, como número entero. Si no se indica, se mostrarán tres.
Valor de retorno: Lista de parejas con el nombre de la colonia y su cantidad de trabajadores en riesgo alto, ordenada de mayor a menor.
Algoritmo o pseudocódigo:
Crear un diccionario vacío para contar por colonia.
Recorrer la lista de trabajadores.
Si clasificar_riesgo devuelve ALTO, sumar uno al conteo de su colonia.
Ordenar las colonias de mayor a menor según su conteo.
Regresar las primeras tres colonias, o la cantidad solicitada.
Caso de prueba:
Colonia A con 3 trabajadores en riesgo alto.
Colonia B con 1 trabajador en riesgo alto.
Colonia C con 0 trabajadores en riesgo alto.
Resultado esperado: Una lista con las parejas A, 3 y B, 1. La colonia C no aparece porque no tiene trabajadores en riesgo alto.
Responsable inicial: Rogelio.
Prioridad: Must Have.
F4. calcular_costo_rotacion
Nombre: calcular_costo_rotacion.
Propuesta por: Matías.
Propósito: Estimar cuánto le cuesta al año la rotación a la empresa y qué parte corresponde al traslado.
Parámetros:
Número de empleados, como entero.
Rotación mensual en porcentaje, como decimal.
Costo por salida en pesos, como decimal.
Proporción de salidas causadas por el traslado, como decimal entre 0 y 1.
Valor de retorno: Diccionario con las salidas anuales, el costo total, las salidas por traslado y el costo por traslado.
Algoritmo o pseudocódigo:
Calcular las salidas anuales multiplicando el número de empleados por la rotación mensual, dividiendo entre 100 y multiplicando por 12. Redondear el resultado.
Calcular el costo total multiplicando las salidas anuales por el costo por salida.
Calcular las salidas por traslado multiplicando las salidas anuales por la proporción. Redondear el resultado.
Calcular el costo por traslado multiplicando las salidas por traslado por el costo por salida.
Regresar los cuatro resultados.
Caso de prueba:
120 empleados.
Rotación mensual de 6 %.
Costo por salida de $47,000.
Proporción por traslado de 0.2.
Resultado esperado:
86 salidas al año.
$4,042,000 de costo total anual.
17 salidas por traslado.
$799,000 de costo por traslado.
Responsable inicial: Matías.
Prioridad: Must Have.
F5. hora_con_mas_retardos
Nombre: hora_con_mas_retardos.
Propuesta por: Mateo.
Propósito: Encontrar la hora de entrada con mayor promedio de retardos por trabajador.
Parámetro: Lista de trabajadores con su hora de entrada y sus retardos al mes.
Valor de retorno: Pareja con la hora crítica y el promedio de retardos por trabajador en ese horario.
Algoritmo o pseudocódigo:
Crear un diccionario para sumar retardos por horario.
Crear otro diccionario para contar trabajadores por horario.
Recorrer la lista de trabajadores.
Sumar los retardos de cada trabajador al horario correspondiente y aumentar su conteo de trabajadores en uno.
Para cada horario, dividir sus retardos acumulados entre su cantidad de trabajadores.
Regresar el horario con el promedio más alto y ese promedio.
Caso de prueba:
A las 07:00 entran dos trabajadores con 3 y 1 retardos al mes.
A las 08:00 entran dos trabajadores con 0 y 1 retardos al mes.
Resultado esperado: Hora crítica 07:00, con un promedio de 2.0 retardos por trabajador.
Responsable inicial: Mateo.
Prioridad: Should Have.
F6. ruta_se_paga
Nombre: ruta_se_paga.
Propuesta por: Matías.
Propósito: Calcular cuántas renuncias tendría que evitar una ruta de transporte para cubrir su costo anual y evaluar si puede convenir.
Parámetros:
Costo mensual de la ruta en pesos, como decimal.
Costo por salida en pesos, como decimal.
Salidas por traslado al año, como entero obtenido de F4.
Valor de retorno: Pareja con las renuncias que se deben evitar y un valor verdadero o falso.
Algoritmo o pseudocódigo:
Multiplicar el costo mensual de la ruta por 12.
Dividir el costo anual de la ruta entre el costo por salida.
Redondear hacia arriba para obtener las renuncias que se deben evitar.
Si esa cantidad es menor o igual a las salidas por traslado, conviene será verdadero. En caso contrario, será falso.
Regresar la cantidad de renuncias y el valor de conviene.
Caso de prueba:
Ruta de $20,000 al mes, como dato de prueba.
Costo por salida de $47,000.
17 salidas por traslado al año.
Resultado esperado: 6 renuncias y verdadero.
La ruta tendría que evitar 6 renuncias al año para cubrir su costo.
Responsable inicial: Matías.
Prioridad: Should Have.
F7. generar_alertas
Nombre: generar_alertas.
Propuesta por: Mateo.
Propósito: Avisar al dueño qué resultados necesitan atención sin que tenga que buscarlos entre todos los datos.
Parámetros:
Porcentaje de trabajadores que tarda 60 minutos o más, como decimal obtenido de F2.
Lista de colonias con su cantidad de trabajadores en riesgo alto, obtenida de F3.
Valor de retorno: Lista de textos con las alertas. Si no hay ninguna, la lista estará vacía.
Algoritmo o pseudocódigo:
Crear una lista vacía de alertas.
Si el porcentaje es mayor a 20, agregar el mensaje “Más de 20 % de la plantilla tarda 60 minutos o más”.
Recorrer las colonias y sus conteos.
Si una colonia tiene 10 o más trabajadores en riesgo alto, agregar un mensaje con su nombre, el conteo y la recomendación de evaluar una ruta.
Regresar la lista de alertas.
Caso de prueba:
Porcentaje de 25.0 %.
Colonia A con 11 trabajadores en riesgo alto.
Colonia B con 4 trabajadores en riesgo alto.
Resultado esperado: Dos alertas.
“Más de 20 % de la plantilla tarda 60 minutos o más”.
“Colonia A: 11 trabajadores en riesgo alto, evaluar una ruta”.
Responsable inicial: Mateo.
Prioridad: Should Have.
F8. validar_trabajador
Nombre: validar_trabajador.
Propuesta por: Paolo.
Propósito: Revisar los datos del formulario antes de guardarlos para evitar que la aplicación se detenga por datos inválidos.
Parámetros: Minutos de traslado, transbordos y retardos como texto, tal como se escriben en el formulario.
Valor de retorno: Pareja con verdadero o falso y un mensaje para el usuario.
Algoritmo o pseudocódigo:
Intentar convertir los tres datos a números enteros.
Si la conversión falla, regresar falso y el mensaje “Minutos, transbordos y retardos deben ser números enteros”.
Si alguno es negativo, regresar falso y el mensaje “Los números no pueden ser negativos”.
Si todos son enteros no negativos, regresar verdadero y el mensaje “Datos correctos”.
Casos de prueba:
Datos “45”, “1” y “2”: Verdadero y “Datos correctos”.
Datos “abc”, “1” y “2”: Falso y “Minutos, transbordos y retardos deben ser números enteros”.
Minutos con valor negativo de cinco, transbordos “0” y retardos “0”: Falso y “Los números no pueden ser negativos”.
Responsable inicial: Paolo.
Prioridad: Should Have.
3. Personalización de la Starter App
Responsable: Rogelio.
Menú principal
Actualmente: Tiene el título “Movilidad Inteligente 2026” y cinco botones genéricos.
Cambio: El título será “LlegaBien”. Los botones serán Inicio, Registrar trabajador, Datos de la plantilla, Diagnóstico y Fuente de datos.
Archivo: src/app/main.py
Home
Actualmente: Tiene un texto de ejemplo y un botón “¿Por qué importa?” con un mensaje genérico.
Cambio: Explicaremos el problema, el usuario y la propuesta de valor.
Problema: Las empresas no saben cómo llegan sus trabajadores.
Usuario: Dueños y gerentes de Recursos Humanos de empresas medianas de León.
Propuesta de valor: Mostrar un diagnóstico con costos en pesos y posibles acciones.
El botón mostrará los datos de referencia incluidos en el proyecto: que el 47 % de los empleadores reconoce el traslado como causa de renuncia, según OCC Mundial et al., 2023, y que cada salida cuesta $47,000 en promedio, según Publimetro, 2022.
Archivo: src/app/win_home.py
Formulario
Actualmente: Registra una observación de tráfico con intersección, flujo, velocidad promedio e incidentes.
Cambio: Se llamará “Registrar trabajador” y pedirá colonia, hora de entrada, medio de transporte, minutos de traslado, transbordos y retardos al mes.
Los datos se revisarán con F8 y se guardarán en data/trabajadores_usuario.csv.
Archivo: src/app/win_form.py
Tabla CSV
Actualmente: Muestra sample_traffic.csv con fecha, hora, intersección, flujo, velocidad e incidentes.
Cambio: Mostrará data/trabajadores_ejemplo.csv con unos 30 trabajadores de prueba.
Las columnas serán número de trabajador, colonia, hora de entrada, medio de transporte, minutos, transbordos y retardos. También tendrá una columna de riesgo calculada con F1.
Archivos: src/app/win_table.py y carpeta data/.
Dashboard
Actualmente: Muestra flujo promedio, velocidad promedio e incidentes.
Cambio: Mostrará el semáforo de riesgo con F2 y el porcentaje de trabajadores que tarda 60 minutos o más.
También mostrará las tres colonias con más riesgo con F3, el horario con más retardos por trabajador con F5 y las alertas con F7.
Tendrá una calculadora con empleados, rotación, costo por salida y costo de la ruta, usando F4 y F6.
Con el Technology Booster agregaremos una gráfica de barras del riesgo por colonia.
Archivo: src/app/win_dashboard.py
API
Actualmente: Tiene una ventana de espera para el booster de API del periodo 3.
Cambio: Para el MVP usaremos las encuestas de los trabajadores, porque ya proporcionan los minutos de cada traslado. Las APIs de mapas suelen pedir registro y clave.
La ventana explicará de dónde vienen los datos. En el periodo 3 evaluaremos una API de rutas para estimar tiempos de traslado.
Archivo: src/app/win_external.py
Pruebas
Actualmente: Tiene dos pruebas de ejemplo para clasificar_riesgo y promedio.
Cambio: Agregaremos una prueba por cada caso de prueba definido para las funciones F1 a F8.
Archivo: tests/test_logic.py
4. Arquitectura mínima
Responsable: Mateo.
La arquitectura seguirá este orden:
Usuario → Tkinter → Funciones propias → Datos → Análisis → Visualización y decisión.
El usuario solo manejará las ventanas de Tkinter. Todos los cálculos estarán en src/core/logic.py. Esto permitirá que cada integrante programe sus funciones sin modificar las ventanas de los demás.
Usuario
Será el dueño o gerente de Recursos Humanos.
Podrá registrar trabajadores y consultar el diagnóstico.
Tkinter
Contendrá el menú y cinco ventanas: Inicio, Registrar trabajador, Datos, Diagnóstico y Fuente de datos.
Archivos: src/app/main.py y las ventanas de la carpeta src/app/.
Funciones propias
Aquí estarán las funciones F1 a F8: clasificación de riesgo, resumen de plantilla, colonias, costo de rotación, horarios, ruta, alertas y validación.
Archivo: src/core/logic.py
Datos
La información de los trabajadores y de la empresa se guardará en archivos CSV.
Usaremos data/trabajadores_ejemplo.csv para los datos de ejemplo.
La lectura se realizará con la función cargar_csv, ubicada en src/core/data_io.py.
Análisis
Se obtendrá el semáforo de riesgo, el porcentaje de trabajadores que tarda 60 minutos o más, las colonias con más riesgo, el horario con más retardos por trabajador, el costo de la rotación y el cálculo de si una ruta se paga sola.
Visualización y decisión
El dashboard mostrará alertas, una calculadora de costos y, como mejora prevista, una gráfica de riesgo por colonia.
Con los resultados, el dueño podrá evaluar una ruta de transporte, un cambio de horario o un esquema de auto compartido.
Archivo: src/app/win_dashboard.py
