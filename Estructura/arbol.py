# -*- coding: utf-8 -*-

class NodoArbol:
    def __init__(self, llave, lba):
        self.llave = llave
        self.lbas = [lba]  # Soporta llaves duplicadas
        self.izquierdo = None
        self.derecho = None

class IndiceArbol:
    """Estructura de indexacion en memoria para acelerar busquedas."""
    def __init__(self):
        self.raiz = None

    def insertar(self, llave, lba):
        if not self.raiz:
            self.raiz = NodoArbol(llave, lba)
        else:
            self._insertar(self.raiz, llave, lba)

    def _insertar(self, nodo, llave, lba):
        if llave == nodo.llave:
            nodo.lbas.append(lba)
        elif llave < nodo.llave:
            if not nodo.izquierdo:
                nodo.izquierdo = NodoArbol(llave, lba)
            else:
                self._insertar(nodo.izquierdo, llave, lba)
        else:
            if not nodo.derecho:
                nodo.derecho = NodoArbol(llave, lba)
            else:
                self._insertar(nodo.derecho, llave, lba)

    def buscar(self, llave):
        return self._buscar(self.raiz, llave)

    def _buscar(self, nodo, llave):
        if not nodo:
            return []
        if llave == nodo.llave:
            return nodo.lbas
        elif llave < nodo.llave:
            return self._buscar(nodo.izquierdo, llave)
        else:
            return self._buscar(nodo.derecho, llave)
