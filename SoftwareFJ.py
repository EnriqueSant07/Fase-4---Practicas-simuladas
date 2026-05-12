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
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad

    @abstractmethod
    def mostrar_detalles(self):
        pass


class Cliente(EntidadGeneral):
    def __init__(self, id_entidad, nombre, documento, correo):
        # Llamar al constructor de la clase padre (EntidadGeneral)
        super().__init__(id_entidad)
        
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
    def __init__(self, id_servicio, nombre_servicio, precio_base):
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
    
# Clase reserva
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        #inicializar reserva con cliente, servicio, duracion y estado por defecto
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def procesar(self):
        print(f"Procesando operacion #{self.id_reserva}")
        try:
            #validar si el objeto cliente es legitimo
            if not isinstance(self.cliente, Cliente):
                raise ClienteInvalidoError("Cliente invalido.")
                
            #Validar que la duracion sea un numero positivo
            if self.duracion <= 0:
                raise ReservaInvalidaError("La duracion debe ser un valor positivo.")
            
            # Calcular costo total usando polimorfismo
            if not isinstance(self.servicio, Servicio):
                raise ServicioNoDisponibleError("Servicio invalido.")
            costo = self.servicio.calcular_costo(self.duracion)
            
        except (ClienteInvalidoError, ReservaInvalidaError, ServicioNoDisponibleError) as e:
            #manejar errores especificos de logica de negocio
            self.estado = "FALLIDA"
            logging.error(f"ID {self.id_reserva}: {e}")
            print(f"ERROR CONTROLADO: {e}")
            
        except Exception as e:
            self.estado = "ERROR CRÍTICO"
            logging.error(f"ID {self.id_reserva} (Inesperado): {e}")
            print("ERROR INESPERADO: Revisar el log para mas detalles.")
            raise SistemaGestionError("Error crítico en el procesamiento de la reserva.") from e
            
        else:
            #este bloque se ejecuta solo si no se lanzaron excepciones
            self.estado = "EXITOSA"
            print(f"Reserva confirmada: {self.cliente.nombre} - Costo: ${costo:,.0f}")
            
        finally:
            # este bloque siempre se ejecuta sin importar si hubo error o no
            print(f"Estado final: {self.estado}")

    def cancelar(self):
        if self.estado == "EXITOSA":
            self.estado = "CANCELADA"
            print(f"Reserva #{self.id_reserva} cancelada.")
        else:
            raise ReservaInvalidaError("Solo se pueden cancelar reservas exitosas.")

#SIMULACION DE 10 OPERACIONES
def ejecutar_simulacion():
    s_sala = ReservaSalas(1, "Sala de Juntas", 40000)
    s_equipo = AlquilerEquipos(2, "Servidor Pro", 120000)
    s_asesor = AsesoriaEspecializada(3, "Consultoría PHP", 80000)

    # Lista para almacenar intentos de reserva
    operaciones = []

    try:
        # Crear objetos de clientes validos
        c1 = Cliente(1, "Kike", "1090123", "kike@mail.com")
        c2 = Cliente(2, "Laura", "5243100", "laura@mail.com")
        
        # Agregar intentos de reserva exitosos
        operaciones.append(Reserva(101, c1, s_sala, 4))
        operaciones.append(Reserva(102, c2, s_asesor, 2))
    except Exception as e: 
        print(f"Error de registro: {e}")

    print("\n--- Pruebas de registro (Simulando datos invalidos)")
    #Probando documento invalido como letras y correo invalido sin @
    for data in [("Error", "letras123", "mail@x.com"), ("Juan", "999", "sin_correo")]:
        try:
            Cliente(0, data[0], data[1], data[2])
        except ClienteInvalidoError as e:
            logging.error(f"Fallo en registro de cliente: {e}")
            print(f"Error de registro capturado: {e}")

    operaciones.append(Reserva(103, c1, s_equipo, -1))       
    
    operaciones.append(Reserva(104, "No es un objeto Cliente", s_sala, 5)) 
    
    operaciones.append(Reserva(105, c2, s_equipo, 10))      
    operaciones.append(Reserva(106, c1, s_asesor, 1))       
    
    operaciones.append(Reserva(107, c2, s_sala, 0))         

    operaciones.append(Reserva(108, c1, None, 3))           

    for op in operaciones:
        try:
            op.procesar()
        except SistemaGestionError:
            pass

if __name__ == "__main__":
    ejecutar_simulacion()