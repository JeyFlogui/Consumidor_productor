import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-2s) %(message)s')

class Consumir(object):
    def __init__(self, start=0):
        self.condicionElementoMAX = threading.Condition()
        self.condicionElemetoMIN = threading.Condition()
        self.elemento = 0

    def existeparaconsumir(self):
        with self.condicionElementoMAX:
            if self.elemento >= 10:
                logging.debug("No hay espacio para más elementos")
                self.condicionElementoMAX.wait()
            else:
                self.elemento += 1
                logging.debug("Elemento creado, elemento=%s", self.elemento)

        with self.condicionElemetoMIN:
            if self.elemento >= 5:
                logging.debug("Existen suficientes elementos para consumir")
                self.condicionElemetoMIN.notify()

    def decrementarElemento(self):
        with self.condicionElemetoMIN:
            while not self.elemento >= 5:
                logging.debug("Esperando elementos")
                self.condicionElemetoMIN.wait()
            self.elemento -= 5
            logging.debug("Elementos consumidos, elemento=%s", self.elemento)

        with self.condicionElementoMAX:
            logging.debug("Hay espacio para producir nuevos elementos")
            self.condicionElementoMAX.notify()

    def getElemento(self):
        return self.elemento


def crearElemento(consumir):
    while consumir.getElemento() <= 10:
        consumir.existeparaconsumir()
        time.sleep(5)


def tomarElemento(consumir):
    while consumir.getElemento() >= 0:
        consumir.decrementarElemento()
        time.sleep(1)

consumir = Consumir()
c1 = threading.Thread(name='c1', target=tomarElemento, args=(consumir,))
c2 = threading.Thread(name='c2', target=tomarElemento, args=(consumir,))
p = threading.Thread(name='p', target=crearElemento, args=(consumir,))

c1.start()
c2.start()
p.start()
p.join()
c2.join()