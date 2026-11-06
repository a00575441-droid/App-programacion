# App-programacion
Aqui estara lo que usaremos para la creación de la app

Paolo:
Nombre de la funcion: evaluar_riesgo_traslado
Propósito: Identificar si un trabajador tiene un traslado de alto riesgo para ayudar a Recursos Humanos a detectar quiénes necesitan apoyo.
Parámetros:
minutos_traslado (int): tiempo que tarda en llegar al trabajo.
transbordos (int): cantidad de cambios de transporte que realiza.
Valor de retorno: Un bool: True si tarda 60 minutos o más, o realiza 2 o más transbordos; False en cualquier otro caso.
Algoritmo o pseudocódigo:
FUNCIÓN 
evaluar_riesgo_traslado(minutos_traslado, transbordos):
    if minutos_traslado >= 60 or transbordos >= 2:
        return True
    else:
        return False
FIN FUNCIÓN
Caso de prueba: Si tarda 45 minutos y realiza 2 transbordos, retorna True, porque cumple el criterio de riesgo por transbordos.
