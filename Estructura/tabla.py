# -*- coding: utf-8 -*-
import sys

class TablaRelacional:
    """
    Gestiona la insercion y lectura de registros directamente 
    sobre los bloques LBA del disco y sus particiones.
    """
    def __init__(self, disco, gestor_particiones):
        self.disco = disco
        self.gestor = gestor_particiones

    def insertar_registro(self, nombre_particion, registro):
        """
        Inserta una fila/registro calculando dinamicamente su espacio 
        y empaquetandolo en el sector LBA correspondiente.
        """
        if nombre_particion not in self.gestor.particiones:
            print("X Error: La particion especificada no existe.")
            return False
            
        particion = self.gestor.particiones[nombre_particion]
        
        if particion.esta_llena():
            print(f"X Error: La particion '{nombre_particion}' se encuentra llena.")
            return False

        # Calcular tamano aproximado en bytes del diccionario
        tamano_bytes = sys.getsizeof(str(registro))
        lba_destino = particion.lba_actual_escritura
        sector = self.disco.sectores_lba[lba_destino]

        # Intentar meter el registro en el sector actual
        exito = sector.guardar_registro(registro, tamano_bytes)
        
        if not exito:
            # Si el sector se lleno, saltamos al siguiente sector de la particion
            particion.lba_actual_escritura += 1
            if particion.esta_llena():
                print(f"X Error: Particion llena al saltar de sector.")
                return False
            
            lba_destino = particion.lba_actual_escritura
            sector = self.disco.sectores_lba[lba_destino]
            sector.guardar_registro(registro, tamano_bytes)

        return True

    def buscar_lineal(self, campo, valor):
        """Busqueda secuencial obligatoria por rubrica"""
        resultados = []
        for lba, sector in self.disco.sectores_lba.items():
            for reg in sector.registros:
                if str(reg.get(campo)) == str(valor):
                    coords = self.disco.lba_a_chsr(lba)
                    resultados.append({"registro": reg, "LBA": lba, "CHSR": coords})
        return resultados

    def buscar_por_rango(self, campo, valor_min, valor_max):
        """Busqueda por rango solicitada en los requerimientos"""
        resultados = []
        for lba, sector in self.disco.sectores_lba.items():
            for reg in sector.registros:
                val = reg.get(campo)
                if val is not None:
                    try:
                        if float(valor_min) <= float(val) <= float(valor_max):
                            coords = self.disco.lba_a_chsr(lba)
                            resultados.append({"registro": reg, "LBA": lba, "CHSR": coords})
                    except ValueError:
                        if str(valor_min) <= str(val) <= str(valor_max):
                            coords = self.disco.lba_a_chsr(lba)
                            resultados.append({"registro": reg, "LBA": lba, "CHSR": coords})
        return resultados
