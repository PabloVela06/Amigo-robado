import random
from datetime import datetime, timedelta

class Jugador:
    def __init__(self,nombre):
        self.numero=0
        self.poder=''
        self.nombre=nombre

    def iniciar_jugador(self,poder,numero):
        self.poder=poder
        self.numero=numero

class Partida:
    def __init__(self,codigo_sala):
        self.codigo=codigo_sala
        self.jugadores=[]
        self.esIniciada=False
        self.lista_poderes=[
            'Bloquea el robo de tu regalo (Una vez que se vaya a efectuar con seguridad)',
            'Bloquea el robo de tu regalo (Una vez que se vaya a efectuar con seguridad)',
            'Bloquea el robo de tu regalo (Una vez que se vaya a efectuar con seguridad)',
            'Si alguien va a robar tu regalo, juega un pulso chino al mejor de 3. Si resultas ganador, bloqueas el robo de tu regalo',
            'Si alguien va a robar tu regalo, juega un pulso chino al mejor de 3. Si resultas ganador, bloqueas el robo de tu regalo',
            'Si alguien va a robar tu regalo, esa persona debe recitar el trabalenguas \'Tres tristes tigres trigaban trigo en un trigal\' a la primera y sin equivocarse',
            'Si alguien va a robar tu regalo, esa persona debe recitar el trabalenguas \'Tres tristes tigres trigaban trigo en un trigal\' a la primera y sin equivocarse',
            'Desvía el robo del regalo (Una vez que se vaya a efectuar con seguridad) a la persona de TU derecha. Puedes usar tu poder incluso si el regalo a robar no es tuyo',
            'Desvía el robo del regalo (Una vez que se vaya a efectuar con seguridad) a la persona de enfrente de TI. Puedes usar tu poder incluso si el regalo a robar no es tuyo',
            'Desvía el robo del regalo (Una vez que se vaya a efectuar con seguridad) a la persona que TÚ elijas. Puedes usar tu poder incluso si el regalo a robar no es tuyo',
            'Desvía el robo del regalo (Una vez que se vaya a efectuar con seguridad) a la persona que TÚ elijas. Puedes usar tu poder incluso si el regalo a robar no es tuyo',
            'Desvía el robo del regalo (Una vez que se vaya a efectuar con seguridad) a la persona de TU izquierda. Puedes usar tu poder incluso si el regalo a robar no es tuyo',
            'Cambia tu puesto con el jugador que quieras. Solo puedes usar este poder una vez llegado tu turno',
            'Cambia tu puesto con el jugador que tengas enfrente. Solo puedes usar este poder una vez llegado tu turno, siempre y cuando dicho jugador todavía no haya jugado',
            'Cambia tu puesto con el jugador que tengas a tu izquierda. Solo puedes usar este poder una vez llegado tu turno, siempre y cuando dicho jugador todavía no haya jugado',
            'Cambia tu puesto con el jugador que tengas a tu derecha. Solo puedes usar este poder una vez llegado tu turno, siempre y cuando dicho jugador todavía no haya jugado',
            'Puedes cambiar tu regalo (solo si lo tienes) con el de cualquier jugador antes del turno 10',
            'Puedes cambiar tu regalo (solo si lo tienes) con el de cualquier jugador antes del turno 10',
            'Solo puedes jugar este poder justo antes de que acabe el turno del jugador objetivo. Este jugador y otro de tu elección que ya haya jugado (puedes ser tú mismo, si ya has jugado) juegan a piedra, papel, tijera al mejor de 3. El ganador decidirá si cambiar o no su regalo con el de su contrincante',
            'Solo puedes jugar este poder justo cuando el jugador objetivo vaya a ABRIR un regalo. Elige el regalo que ese jugador abrirá',
            'Solo puedes jugar este poder justo cuando el jugador objetivo vaya a ABRIR un regalo. Elige el regalo que ese jugador abrirá',
            'Solo puedes jugar este poder justo cuando el jugador objetivo vaya a ABRIR un regalo. Ese jugador deberá elegir el regalo con los ojos vendados. Antes de escoger debera dar 5 vueltas sobre sí mismo para desorientarse',
            'Solo puedes jugar este poder cuando vayas a ABRIR un regalo. Selecciona 2 de ellos para poder tocarlos con total libertad. Acaba escogiendo uno de los dos para abrir',
            #Puedes intercambiar tu regalo con el jugador numero n (n={1,2,...,len(jugadores)) una vez que él y tú hayais jugado)
            'Puedes cambiar tu regalo con el último jugador que ha jugado. Necesitas tener un regalo para usar este poder',
            '',
            ]
        self.fecha_creacion=datetime.now()
        self.admin=None

    def agregar_a(self, nombre_jugador):
        if(not nombre_jugador):
            return False
        else:
            for e in self.jugadores:
                if e.nombre==nombre_jugador:
                    return False
            nuevo_jugador=Jugador(nombre_jugador)
            self.jugadores.append(nuevo_jugador)
        return True

    def iniciar_partida(self):
        if(self.esIniciada):
            return False
        else:
            cantidad=len(self.jugadores)
            numeros=list(range(1,cantidad+1))
            random.shuffle(numeros)

            poderes_a_asignar=self.lista_poderes.copy()
            poderes_a_asignar.append('Puedes intercambiar tu regalo con el jugador número '+str(random.randint(1,cantidad))+'una vez que él y tú hayais jugado. Puedes usar este poder en cualquier punto de la partida')
            faltan=0
            if len(poderes_a_asignar) < cantidad:
                faltan = cantidad - len(poderes_a_asignar)
            # Rellenamos con poderes vacíos o genéricos para que no explote
            poderes_a_asignar.extend(["Sin Poder Especial"] * faltan)
            random.shuffle(poderes_a_asignar)

            for e in self.jugadores:
                e.iniciar_jugador(poderes_a_asignar[0],numeros[0])
                del poderes_a_asignar[0]
                del numeros[0]
            self.esIniciada = True 
            return True


partidas={}

def crear_partida(codigo):
    eliminar_partidas_caducadas()
    if codigo in partidas:
        return False
    else:
        nueva_partida=Partida(codigo)
        partidas[codigo]=nueva_partida
        return True

def obtener_partida(codigo):
    return partidas.get(codigo)

def eliminar_partidas_caducadas():
    ahora=datetime.now()
    tiempo_limite=timedelta(hours=12)

    codigos_a_borrar=[]
    for codigo,sala in partidas.items():
        if (ahora-sala.fecha_creacion)>tiempo_limite:
            codigos_a_borrar.append(codigo)
    for codigo in codigos_a_borrar:
        del partidas[codigo]

def finalizar_partida(codigo):
    if codigo in partidas:
        del partidas[codigo] # Borra la sala del diccionario global
        return True

    return False
