import streamlit as st
import random
import logica_juego as juego
import time
from logica_juego import Jugador

# Configuración de página
st.set_page_config(page_title='Amigo robado')
st.title('¡El amigo robado!')

# --- GESTIÓN DE ESTADO ---
if 'mi_nombre' not in st.session_state:
    st.session_state.mi_nombre = None
if 'sala_actual' not in st.session_state:
    st.session_state.sala_actual = None
if 'partida_iniciada' not in st.session_state:
    st.session_state.partida_iniciada = False
if 'confirmar_cierre' not in st.session_state:
    st.session_state.confirmar_cierre = False
if 'animacion_globos' not in st.session_state:
    st.session_state.animacion_globos = False
if 'showtime_realizada' not in st.session_state:
    st.session_state.showtime_realizada = False

# --- PANTALLA 1: LOGIN ---
if st.session_state.mi_nombre is None:
    nombre_input = st.text_input('Escribe tu nombre aquí', key='txt_guardar_nombre')
    if st.button('Guardar', key='btn_guardar_nombre'):
        if nombre_input:
            st.session_state.mi_nombre = nombre_input
            st.rerun()
        else:
            st.warning('Por favor, escribe tu nombre')
else:
    st.text(f'¡Bienvenido {st.session_state.mi_nombre}!')

# --- PANTALLA 2: SELECCIÓN DE SALA ---
if st.session_state.sala_actual is None:
    tab1, tab2 = st.tabs(["Unirse a una partida", "Crear una partida"])
    
    with tab1:
        st.header('Únete a una sala')
        contenedor_mensaje = st.empty()
        codigo_union = st.text_input('Código de 6 cifras', key='txt_union', max_chars=6)
        if st.button('Unirse', key='btn_union'):
            if codigo_union and codigo_union.isnumeric() and len(codigo_union) == 6:
                partida = juego.obtener_partida(codigo_union)
                if partida:
                    if partida.agregar_a(st.session_state.mi_nombre):
                        st.session_state.sala_actual = codigo_union
                        st.rerun()
                    else:
                        contenedor_mensaje.warning('Nombre repetido.')
                else:
                    contenedor_mensaje.warning('Esa sala no existe.')
            else:
                contenedor_mensaje.warning('Código inválido.')

    with tab2:
        st.header('Crea una partida')
        if st.button('Crear Sala', key='btn_crear'):
            if st.session_state.mi_nombre is None:
                st.warning('¡Danos un nombre antes de crear una partida!')
            else:
                codigo = str(random.randint(100000, 999999))
                while not juego.crear_partida(codigo):
                    codigo = str(random.randint(100000, 999999))
                sala = juego.obtener_partida(codigo)
                sala.agregar_a(st.session_state.mi_nombre)
                sala.admin = Jugador(st.session_state.mi_nombre)
                st.session_state.sala_actual = codigo
                st.rerun()

# --- PANTALLA 3: DENTRO DE LA SALA ---
else:
    sala = juego.obtener_partida(st.session_state.sala_actual)

    if sala is None:
        st.error("⚠️ La sala ha expirado.")
        if st.button("Volver al Inicio"):
            st.session_state.sala_actual = None
            st.session_state.partida_iniciada = False
            st.session_state.mi_nombre = None 
            st.rerun()
        st.stop() 

    st.session_state.partida_iniciada = sala.esIniciada

    # --- MODO LOBBY ---
    if not sala.esIniciada:
        st.header('¡Sala creada!')
        st.metric(label="Código de la Sala", value=sala.codigo)
        admin_nombre = sala.admin.nombre if sala.admin else "Desconocido"
        st.info(f'👑 Administrador: {admin_nombre}')
        st.divider()
        st.write(f'👥 Jugadores ({len(sala.jugadores)}):')
        for p in sala.jugadores:
            st.write(f"👤 {p.nombre}")
        st.divider()

        es_admin = (sala.admin and st.session_state.mi_nombre == sala.admin.nombre)
        if es_admin:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 Actualizar"):
                    st.rerun()
            with c2:
                if len(sala.jugadores) >= 2:
                    if st.button("🚀 EMPEZAR", type="primary"):
                        sala.iniciar_partida()
                        st.rerun()
                else:
                    st.caption("Faltan jugadores.")
        else:
            st.write("⏳ Esperando...")
            time.sleep(2)
            st.rerun()

    # --- MODO JUEGO ---
    else:
        # A) Animación de carga (VERSIÓN GIF - A PRUEBA DE BOMBAS)
        if not st.session_state.showtime_realizada:
            contenedor_intro = st.empty()
            with contenedor_intro:
                # Usamos un GIF de Giphy (Barajando cartas)
                # Puedes cambiar este enlace por cualquier GIF que encuentres en Google
                url_gif = "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif"
                
                # Centramos la imagen usando columnas "invisibles" para que no salga gigante
                c_izq, c_centro, c_der = st.columns([1, 2, 1])
                with c_centro:
                    st.image("assets/Showtime.gif", use_container_width=True)
                    st.markdown("<h2 style='text-align: center;'>Barajando cartas...</h2>", unsafe_allow_html=True)
            
            time.sleep(4) # Tiempo para ver el GIF
            contenedor_intro.empty()
            st.session_state.showtime_realizada = True
            st.rerun()

        # B) Efecto Globos
        if not st.session_state.animacion_globos:
            st.balloons()
            st.session_state.animacion_globos = True

        st.header('¡Juego en Marcha!')

        mi_jugador = next((p for p in sala.jugadores if p.nombre == st.session_state.mi_nombre), None)
        if mi_jugador:
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"🔢 **Tu Número:**\n# {mi_jugador.numero}")
            with c2:
                st.info(f"✨ **Tu Poder:**\n{mi_jugador.poder}")
        
        st.divider()
        st.write("📋 Mesa:")
        for p in sala.jugadores:
            if p.nombre == st.session_state.mi_nombre:
                st.write(f"👉 **{p.nombre}** (Tú)")
            else:
                st.write(f"👤 {p.nombre}")

        st.divider()
        es_admin = (sala.admin and st.session_state.mi_nombre == sala.admin.nombre)
        if es_admin:
            if not st.session_state.confirmar_cierre:
                if st.button("❌ Terminar"):
                    st.session_state.confirmar_cierre = True
                    st.rerun()
            else:
                st.warning("¿Borrar sala?")
                if st.button("✅ SÍ"):
                    juego.finalizar_partida(sala.codigo)
                    st.session_state.sala_actual = None
                    st.session_state.confirmar_cierre = False
                    st.rerun()
        else:
            time.sleep(5)
            st.rerun()