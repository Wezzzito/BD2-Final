class SectorSimulado:
    """
    Representa la unidad mínima de almacenamiento físico en el disco duro.
    """
    def __init__(self, id_sector, capacidad_bytes):
        self.id = id_sector
        self.capacidad_bytes = capacidad_bytes
        self.espacio_disponible = capacidad_bytes
        self.registros = []  # Lista para almacenar los diccionarios/filas de datos

    def guardar_registro(self, registro, tamano_registro_bytes):
        """Intenta almacenar un registro si hay espacio suficiente."""
        if self.espacio_disponible >= tamano_registro_bytes:
            self.registros.append(registro)
            self.espacio_disponible -= tamano_registro_bytes
            return True
        return False


class DiscoSimulado:
    """
    Simula la geometría física de un disco duro personalizable y calcula
    las direcciones lógicas (LBA) y físicas (CHSR) únicas para cada registro.
    """
    def __init__(self, platos, pistas, sectores_por_pista, tamano_sector_bytes):
        # Parámetros obligatorios de configuración física según la rúbrica
        self.platos = platos
        self.superficies = platos * 2  # Cada plato tiene una cara superior e inferior
        self.pistas = pistas
        self.sectores_por_pista = sectores_por_pista
        self.tamano_sector_bytes = tamano_sector_bytes
        
        # Cálculos derivados del hardware
        self.total_sectores = self.superficies * self.pistas * self.sectores_por_pista
        self.capacidad_total_bytes = self.total_sectores * self.tamano_sector_bytes
        
        # Estructura lógica del disco: Diccionario indexado por LBA (Logical Block Addressing)
        # Esto mapea el disco en una lista plana desde el sector 0 hasta N-1
        self.sectores_lba = {}
        for lba in range(self.total_sectores):
            self.sectores_lba[lba] = SectorSimulado(lba, tamano_sector_bytes)

    def lba_a_chsr(self, lba):
        """
        Traduce una dirección lógica lineal (LBA) a coordenadas geométricas físicas:
        Cilindro/Pista (C), Head/Superficie (H), Sector en pista (S).
        """
        # 1. Cuántos sectores hay en un cilindro completo (todas las superficies en una pista)
        sectores_por_cilindro = self.superficies * self.sectores_por_pista
        
        # 2. Calcular la pista/cilindro correspondiente
        pista = lba // sectores_por_cilindro
        residuo_pista = lba % sectores_por_cilindro
        
        # 3. Calcular la superficie (cabeza lectora) dentro de ese cilindro
        superficie = residuo_pista // self.sectores_por_pista
        
        # 4. Calcular el sector específico dentro de esa pista (indexado desde 0)
        sector_en_pista = residuo_pista % self.sectores_por_pista
        
        return {
            "pista": pista,
            "superficie": superficie,
            "sector": sector_en_pista
        }

    def chsr_a_lba(self, pista, superficie, sector):
        """
        Traduce coordenadas físicas de geometría a una dirección lógica LBA única.
        Útil para ubicar celdas desde la cuadrícula visual de la interfaz.
        """
        return (pista * self.superficies * self.sectores_por_pista) + (superficie * self.sectores_por_pista) + sector

