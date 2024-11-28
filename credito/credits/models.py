from django.db import models
from datetime import date

class CreditRequest(models.Model):
    nombre = models.CharField(max_length=100)
    rfc = models.CharField(max_length=13)  # Ya no es único
    fecha_nacimiento = models.DateField()
    importe_solicitado = models.DecimalField(max_digits=10, decimal_places=2)
    ingresos_mensuales = models.DecimalField(max_digits=10, decimal_places=2)
    historial_crediticio = models.BooleanField(default=False)  # Se calcula dinámicamente
    solicitud_en_proceso = models.BooleanField(default=False)
    aprobado = models.BooleanField(null=True, blank=True)
    razon_rechazo = models.TextField(null=True, blank=True)
    fecha_solicitud = models.DateField(auto_now_add=True)  # Fecha automática al crear una solicitud

    def calcular_edad(self):
        """Calcula la edad del solicitante."""
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    @classmethod
    def tiene_historial_crediticio(cls, rfc):
        """
        Verifica si el RFC tiene historial crediticio (solicitudes aprobadas en los últimos 2 años).
        """
        hace_dos_anos = date.today().replace(year=date.today().year - 2)
        return cls.objects.filter(rfc=rfc, aprobado=True, fecha_solicitud__gte=hace_dos_anos).exists()