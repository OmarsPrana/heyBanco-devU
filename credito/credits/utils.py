from datetime import datetime, date
from credits.models import CreditRequest 
def validar_solicitud(data):
    try:
        # Convertir la fecha de nacimiento
        fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], "%Y-%m-%d").date()
    except ValueError:
        return {"aprobado": False, "razon_rechazo": "Formato de fecha inválido."}

    # Calcular la edad
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )

    # Validar si es menor de edad
    if edad < 18:
        return {"aprobado": False, "razon_rechazo": "El cliente es menor de edad."}

    # Si pasa la validación de edad, continuar con las validaciones de crédito
    ingresos_mensuales = float(data['ingresos_mensuales'])
    importe_solicitado = float(data['importe_solicitado'])

    # Tabla de límites de crédito
    tabla_ingresos = [
        (5000, 9999.99, 15000, 7500),
        (10000, 19999.99, 25000, 12000),
        (20000, 39999.99, 50000, 30000),
        (40000, float('inf'), 100000, 50000),
    ]

    # Verificar historial crediticio
    tiene_historial = CreditRequest.tiene_historial_crediticio(data['rfc'])

    for min_ingreso, max_ingreso, max_historial, max_sin_historial in tabla_ingresos:
        if min_ingreso <= ingresos_mensuales <= max_ingreso:
            max_credito = max_historial if tiene_historial else max_sin_historial
            if importe_solicitado > max_credito:
                return {"aprobado": False, "razon_rechazo": f"El importe máximo permitido es {max_credito}."}
            return {"aprobado": True, "razon_rechazo": None}

    return {"aprobado": False, "razon_rechazo": "No se cumplen las condiciones para el crédito."}
