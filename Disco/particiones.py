# -*- coding: utf-8 -*-

class Particion:
    """
    Representa una division logica del espacio del disco duro (LBA).
    Cada particion tiene un nombre unico y controla su propio rango de sectores.
    """
    def __init__(self, nombre, lba_inicio, lba_fin):
        self.nombre = nombre
        self.lba_inicio = lba_inicio
        self.lba_fin = lba_fin
        
        # El puntero indica en que sector exacto nos toca escribir el proximo registro
        self.lba_actual_escritura = lba_inicio
        self.total_sectores_asignados = (lba_fin - lba_inicio) + 1

    def esta_llena(self):
        """Verifica si el puntero de escritura ya supero el limite de la particion."""
        return self.lba_actual_escritura > self.lba_fin


class GestorParticiones:
    """
    Controla la creacion de particiones en el disco y se asegura de que
    no se solapen (no ocupen los mismos sectores) ni se exceda el tamano del disco.
    """
    def __init__(self, disco_simulado):
        self.disco = disco_simulado
        self.particiones = {}  # Diccionario para guardar { "NombreParticion": Objeto Particion }

    def crear_particion(self, nombre, cantidad_sectores_deseados):
        """
        Calcula automaticamente los rangos LBA de inicio y fin para una nueva particion,
        garantizando que empiece justo donde termino la anterior.
        """
        # 1. Determinar donde empieza esta particion
        if not self.particiones:
            lba_inicio = 0  # Si es la primera particion, empieza en el sector 0
        else:
            # Si ya existen, buscamos el fin de la ultima particion creada y sumamos 1
            ultima_particion = list(self.particiones.values())[-1]
            lba_inicio = ultima_particion.lba_fin + 1

        # 2. Calcular donde termina la particion segun el tamano solicitado
        lba_fin = lba_inicio + cantidad_sectores_deseados - 1

        # 3. Validar que no nos estemos pasando del limite fisico del disco duro
        if lba_fin >= self.disco.total_sectores:
            print(f"X Error: No hay suficiente espacio para la particion '{nombre}'.")
            return False

        # 4. Si todo es correcto, creamos el objeto y lo guardamos
        nueva_particion = Particion(nombre, lba_inicio, lba_fin)
        self.particiones[nombre] = nueva_particion
        print(f"[-] Particion '{nombre}' creada con exito. Rango LBA: [{lba_inicio} - {lba_fin}].")
        return True

    def obtener_particion_de_registro(self, lba_registro):
        """
        Dado un sector logico (LBA), averigua a que particion pertenece.
        Muy util para mostrar estadisticas en la interfaz grafica.
        """
        for nombre, part in self.particiones.items():
            if part.lba_inicio <= lba_registro <= part.lba_fin:
                return nombre
        return "Sin Particion"
