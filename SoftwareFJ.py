
import logging
from abc import ABC, abstractmethod

# Preparar log
logging.basicConfig(
    filename='errores_sistema.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
) 


# Creacion de clases de excepciones personalizadas
class SistemaGestionError(Exception):
    pass

class ClienteInvalidoError(SistemaGestionError):
    pass

class ServicioNoDisponibleError(SistemaGestionError):
    pass

class ReservaInvalidaError(SistemaGestionError):
    pass

# Creacion de clase entidad (abstraccion y encapsulacion)
class EntidadGeneral(ABC):
    def _init_(self, id_entidad):
        self._id_entidad = id_entidad

    @abstractmethod
    def mostrar_detalles(self):
        pass


class Cliente(EntidadGeneral):
    def _init_(self, id_entidad, nombre, documento, correo):
        # Llamar al constructor de la clase padre (EntidadGeneral)
        super()._init_(id_entidad)
        
        # Inicializar atributos usando setters para validacion automatica
        self.nombre = nombre
        self.documento = documento
        self.correo = correo

    #propiedad nombre
    @property
    def nombre(self): 
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # erificar si el nombre es una cadena valida y no esta vacia
        if not isinstance(valor, str) or not valor.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor

    # Propiedad documento
    @property
    def documento(self): 
        return self.__documento

    @documento.setter
    def documento(self, valor):
        #asegurarse de que el documento contenga solo numeros
        if not str(valor).isdigit():
            raise ClienteInvalidoError("Documento debe ser numérico.")
        self.__documento = valor

    #Propiedad correo
    @property
    def correo(self): 
        return self.__correo

    @correo.setter
    def correo(self, valor):
        #Validacion basica para verificar el simbolo '@' en el correo
        if "@" not in str(valor):
            raise ClienteInvalidoError("Correo electrónico inválido.")
        self.__correo = valor

    # Metodo para mostrar informacion del cliente
    def mostrar_detalles(self):
        return f"Cliente: {self.nombre} | ID: {self.documento}"

# Clase servicio (polimorfismo y herencia)
class Servicio(ABC):
    def _init_(self, id_servicio, nombre_servicio, precio_base):
        #Inicializar atributos comunes del servicio
        if precio_base <= 0:
            raise ServicioNoDisponibleError("El precio base debe ser mayor a cero.")
        self.id_servicio = id_servicio
        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, duracion, **kwargs):
        pass

class ReservaSalas(Servicio):
    def calcular_costo(self, duracion, impuesto=0.19): 
        #Metodo sobrecargado que incluye calculo de impuesto
        return (self.precio_base * duracion) * (1 + impuesto)

class AlquilerEquipos(Servicio):
    def calcular_costo(self, duracion, seguro=15000):
        #Calculo que incluye un cargo fijo de seguro
        return (self.precio_base * duracion) + seguro

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion, es_remoto=True):
        # metodo polimorfico: el precio cambia si el servicio es remoto o presencial
        tarifa = self.precio_base if es_remoto else self.precio_base * 1.5
        return tarifa * duracion