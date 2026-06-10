# -*- coding: utf-8 -*-
import os
import sys

# 1. ESTO OBLIGA A PYTHON A ENCONTRAR LAS CARPETAS SIN IMPORTAR TU EDITOR
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
if DIRECTORIO_ACTUAL not in sys.path:
    sys.path.insert(0, DIRECTORIO_ACTUAL)

# 2. PRUEBA DE IMPORTACIÓN DINÁMICA CON TOLERANCIA A MAYÚSCULAS/MINÚSCULAS
try:
    from Disco.almacenamiento import DiscoSimulado
except ImportError:
    from Disco.Almacenamiento import DiscoSimulado

try:
    from Disco.particiones import GestorParticiones
except ImportError:
    from Disco.Particiones import GestorParticiones

try:
    from Estructura.tabla import TablaRelacional
except ImportError:
    from Estructura.Tabla import TablaRelacional

try:
    from Estructura.arbol import IndiceArbol
except ImportError:
    from Estructura.Arbol import IndiceArbol


def simular_sistema():
    print("=== Inicializando Hardware ===")
    # Crear disco: 2 platos, 4 pistas, 5 sectores/pista, 512 bytes por sector
    disco = DiscoSimulado(platos=2, pistas=4, sectores_por_pista=5, tamano_sector_bytes=512)
    gestor = GestorParticiones(disco)
    
    print(f"\nSectores totales disponibles en LBA: {disco.total_sectores}")
    
    print("\n=== Creando Particiones ===")
    gestor.crear_particion("Particion_A", 15)
    gestor.crear_particion("Particion_B", 15)
    
    tabla = TablaRelacional(disco, gestor)
    indice_id = IndiceArbol()
    
    print("\n=== Insertando Datos de Prueba ===")
    usuarios = [
        {"id": 101, "nombre": "Andres", "edad": 21},
        {"id": 102, "nombre": "Carlos", "edad": 25},
        {"id": 103, "nombre": "Maria", "edad": 19}
    ]
    
    for user in usuarios:
        particion_actual = "Particion_A"
        lba_donde_caera = gestor.particiones[particion_actual].lba_actual_escritura
        
        if tabla.insertar_registro(particion_actual, user):
            # Indexamos en nuestro árbol binario
            indice_id.insertar(user["id"], lba_donde_caera)
            
    print("\n=== Prueba de Busqueda Indexada (Arbol) ===")
    lbas_encontrados = indice_id.buscar(102)
    for lba in lbas_encontrados:
        sector = disco.sectores_lba[lba]
        coords = disco.lba_a_chsr(lba)
        print(f"-> Registro indexado encontrado en LBA {lba} {coords}: {sector.registros}")

if __name__ == "__main__":
    simular_sistema()
