from django.shortcuts import render
from .models import CreditRequest
from .utils import validar_solicitud

def solicitar_credito(request):
    if request.method == "POST":
        # Capturar los datos del formulario
        data = {
            "nombre": request.POST.get("nombre"),
            "rfc": request.POST.get("rfc"),
            "fecha_nacimiento": request.POST.get("fecha_nacimiento"),
            "importe_solicitado": request.POST.get("importe_solicitado"),
            "ingresos_mensuales": request.POST.get("ingresos_mensuales"),
        }

        # Verificar si ya existe una solicitud en proceso para este RFC
        if CreditRequest.objects.filter(rfc=data['rfc'], aprobado=True).exists():
            return render(request, "credits/solicitud.html", {
                "error": "Ya existe una solicitud en proceso para este RFC. Por favor, espere a que se complete."
            })

        # Verificar si ya existe una solicitud en proceso para este RFC
        

        # Validar la solicitud
        resultado = validar_solicitud(data)

        # Finalizar cualquier solicitud anterior en proceso
        CreditRequest.objects.filter(rfc=data['rfc'], solicitud_en_proceso=True).update(solicitud_en_proceso=False)

        # Crear la nueva solicitud
        nueva_solicitud = CreditRequest.objects.create(
            nombre=data['nombre'],
            rfc=data['rfc'],
            fecha_nacimiento=data['fecha_nacimiento'],
            importe_solicitado=data['importe_solicitado'],
            ingresos_mensuales=data['ingresos_mensuales'],
            historial_crediticio=CreditRequest.tiene_historial_crediticio(data['rfc']),
            solicitud_en_proceso=True,  # La solicitud estará en proceso hasta que se decida
            aprobado=resultado['aprobado'],
            razon_rechazo=resultado.get('razon_rechazo'),
        )

        # Si la solicitud es aprobada o rechazada, finalizarla
        if resultado['aprobado'] or resultado['razon_rechazo']:
            nueva_solicitud.solicitud_en_proceso = False
            nueva_solicitud.save()

        # Preparar el monto aprobado o vacío
        resultado['importe_aprobado'] = data['importe_solicitado'] if resultado['aprobado'] else ''

        # Renderizar la plantilla `resultado.html`
        return render(request, "credits/resultado.html", {"resultado": resultado})

    # Si es GET, renderizar el formulario
    return render(request, "credits/solicitud.html")