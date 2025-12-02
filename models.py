from django.db import models

# --- Modelos del Sistema de Gestión de Centro de Reciclaje ---

## ♻️ Material_Reciclable
class Material_Reciclable(models.Model):
    # Clave Primaria 'id' creada automáticamente (representa id_material)
    nombre_material = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tipo_material = models.CharField(max_length=50)
    precio_por_kg = models.DecimalField(max_digits=5, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    es_toxico = models.BooleanField(default=False)
    punto_acopio_recomendado = models.CharField(max_length=100, blank=True)
    codigo_identificacion = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_material

# ---
## 🏢 Centro_Acopio
class Centro_Acopio(models.Model):
    # Clave Primaria 'id' creada automáticamente (representa id_centro)
    nombre_centro = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    horario_atencion = models.TextField()
    capacidad_toneladas = models.DecimalField(max_digits=10, decimal_places=2)
    latitud = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.nombre_centro

# ---
## 👤 Donante
class Donante(models.Model):
    # Clave Primaria 'id' creada automáticamente (representa id_donante)
    nombre_donante = models.CharField(max_length=255)
    tipo_donante = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    direccion_donante = models.CharField(max_length=255, blank=True)
    ruc_dni = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    es_anonimo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_donante if not self.es_anonimo else "Donante Anónimo"

# ---
## 👷 Empleado_Reciclaje
class Empleado_Reciclaje(models.Model):
    # Clave Primaria 'id' creada automáticamente (representa id_empleado)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    fecha_contratacion = models.DateField()
    cargo = models.CharField(max_length=50)
    turno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    certificaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.cargo})"

# ---
## 📥 Recepcion_Material
class Recepcion_Material(models.Model):
    # Clave Primaria 'id' creada automáticamente (representa id_recepcion)

    # Relaciones Muchos a Uno (Foreign Key)
    # id_material
    id_material = models.ForeignKey(Material_Reciclable, on_delete=models.PROTECT, related_name='recepciones')
    # id_centro
    id_centro = models.ForeignKey(Centro_Acopio, on_delete=models.PROTECT, related_name='recepciones')
    # id_donante
    id_donante = models.ForeignKey(Donante, on_delete=models.PROTECT, related_name='recepciones')
    # id_empleado_recepciono
    id_empleado_recepciono = models.ForeignKey(Empleado_Reciclaje, on_delete=models.PROTECT, related_name='recepciones_realizadas')

    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=2)
    estado_material = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Recepción {self.id} - {self.fecha_recepcion.strftime('%Y-%m-%d %H:%M')}"

# ---
## ⚙️ Procesamiento_Material
class Procesamiento_Material(models.Model):
    # Clave Primaria 'id' creada automáticamente (representa id_procesamiento)

    # Relaciones Muchos a Uno (Foreign Key)
    # id_recepcion
    id_recepcion = models.ForeignKey(Recepcion_Material, on_delete=models.PROTECT, related_name='procesamientos')
    # id_empleado_procesa
    id_empleado_procesa = models.ForeignKey(Empleado_Reciclaje, on_delete=models.PROTECT, related_name='procesos_realizados')

    fecha_inicio_procesamiento = models.DateTimeField()
    fecha_fin_procesamiento = models.DateTimeField(null=True, blank=True)
    tipo_proceso = models.CharField(max_length=100)
    cantidad_resultante_kg = models.DecimalField(max_digits=10, decimal_places=2)
    subproductos = models.TextField(blank=True)
    costo_procesamiento = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Procesamiento {self.id} - Recepción: {self.id_recepcion_id}"

# ---
## 💰 Venta_Material
class Venta_Material(models.Model):
    # Clave Primaria 'id' creada automáticamente (representa id_venta)

    # Relaciones Muchos a Uno (Foreign Key)
    # id_material
    id_material = models.ForeignKey(Material_Reciclable, on_delete=models.PROTECT, related_name='ventas')
    # id_empleado_venta
    id_empleado_venta = models.ForeignKey(Empleado_Reciclaje, on_delete=models.PROTECT, related_name='ventas_realizadas')

    # id_cliente_comprador (Se mantiene como IntegerField ya que la entidad Cliente no está definida)
    id_cliente_comprador = models.IntegerField() 

    fecha_venta = models.DateTimeField(auto_now_add=True)
    cantidad_kg_vendido = models.DecimalField(max_digits=10, decimal_places=2)
    precio_por_kg_venta = models.DecimalField(max_digits=5, decimal_places=2)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Venta {self.id} - {self.id_material.nombre_material} - Total: {self.total_venta}"
