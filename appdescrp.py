import streamlit as st


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Generador de Descripciones de Proyectos",
    page_icon="🏗️",
    layout="wide"
)


# ============================================================
# CATÁLOGOS
# ============================================================

EXTERIORES = [
    "Acceso peatonal",
    "Acceso vehicular",
    "Acceso peatonal y vehicular",
    "Áreas verdes",
    "Estacionamientos",
    "Estacionamiento para motores",
    "Piscina con asoleadero",
    "Jacuzzi",
    "Cuarto de bomba",
    "Cuarto de máquinas",
    "Cuarto para planta eléctrica",
    "Depósito de basura",
    "Cuarto útil",
    "Depósito",
    "Locker",
    "Otros"
]

ESPACIOS = [
    "Entrada",
    "Entrada principal",
    "Vestíbulo",
    "Escaleras",
    "Dos escaleras",
    "Sala",
    "Comedor",
    "Sala – comedor",
    "Sala – comedor – cocina",
    "Cocina",
    "Cocina con almacén",
    "Cocina fría",
    "Cocina caliente",
    "Cocina – comedor – sala de estar",
    "Desayunador",
    "Sala de estar",
    "Área de estar",
    "Estudio",
    "Área de estudio",
    "Área de lavado",
    "Terraza",
    "Terraza techada con comedor y área BBQ",
    "Terraza con jacuzzi",
    "Balcón",
    "½ baño",
    "Baño",
    "Baño para ambos sexos",
    "Dormitorio de servicio con baño",
    "Dos dormitorios de servicio con baño",
    "Área de recepción",
    "Área de restaurante",
    "Área de restaurante con bar",
    "Estación de servicio",
    "Área de servicio",
    "Área de caja",
    "Cuarto eléctrico",
    "Cuarto de bóveda",
    "Cuarto de archivo",
    "Cuarto de depósito",
    "Cuarto de limpieza",
    "Salón de eventos",
    "Kitchenette",
    "Gimnasio",
    "Jardín interior",
    "Espejos de agua",
    "Hoguera",
    "Cuarto de juegos",
    "Cuarto de máquinas",
    "Cuarto de equipos de bombeo",
    "Dos cuartos de equipos de bombeo",
    "Depósito para basura",
    "Bodega",
    "Área BBQ",
    "Otros"
]

ATRIBUTOS_HABITACION = [
    "Baño",
    "Vestidor",
    "Terraza",
    "Balcón"
]


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def numero_letras(numero):
    """
    Convierte números pequeños a palabras.
    """
    numeros = {
        0: "cero",
        1: "una",
        2: "dos",
        3: "tres",
        4: "cuatro",
        5: "cinco",
        6: "seis",
        7: "siete",
        8: "ocho",
        9: "nueve",
        10: "diez",
        11: "once",
        12: "doce",
        13: "trece",
        14: "catorce",
        15: "quince",
        16: "dieciséis",
        17: "diecisiete",
        18: "dieciocho",
        19: "diecinueve",
        20: "veinte",
        21: "veintiuna",
        22: "veintidós",
        23: "veintitrés",
        24: "veinticuatro",
        25: "veinticinco",
        26: "veintiséis",
        27: "veintisiete",
        28: "veintiocho",
        29: "veintinueve",
        30: "treinta",
    }

    return numeros.get(numero, str(numero))


def formato_cantidad(numero, singular, plural):
    """
    Devuelve:
    1 habitación
    4 habitaciones
    """
    if numero == 1:
        return f"una {singular}"

    return f"{numero_letras(numero)} {plural}"


def generar_habitaciones(datos):
    """
    Genera automáticamente la descripción de las habitaciones.
    """

    cantidad = datos["cantidad"]

    if cantidad == 0:
        return ""

    atributos = []

    if datos["banos"] > 0:
        if datos["banos"] == cantidad:
            atributos.append("baño")
        else:
            atributos.append(
                f"{numero_letras(datos['banos'])} con baño"
            )

    if datos["vestidores"] > 0:
        if datos["vestidores"] == cantidad:
            atributos.append("vestidor")
        else:
            atributos.append(
                f"{numero_letras(datos['vestidores'])} con vestidor"
            )

    if datos["terrazas"] > 0:
        if datos["terrazas"] == cantidad:
            atributos.append("terraza")
        else:
            atributos.append(
                f"{numero_letras(datos['terrazas'])} con terraza"
            )

    if datos["balcones"] > 0:
        if datos["balcones"] == cantidad:
            atributos.append("balcón")
        else:
            atributos.append(
                f"{numero_letras(datos['balcones'])} con balcón"
            )

    if not atributos:
        return formato_cantidad(
            cantidad,
            "habitación",
            "habitaciones"
        )

    # Caso en que todas tienen el mismo atributo
    if len(atributos) == 1 and (
        datos["banos"] == cantidad
        or datos["vestidores"] == cantidad
        or datos["terrazas"] == cantidad
        or datos["balcones"] == cantidad
    ):
        return (
            f"{formato_cantidad(cantidad, 'habitación', 'habitaciones')}"
            f" con {atributos[0]}"
        )

    return (
        f"{formato_cantidad(cantidad, 'habitación', 'habitaciones')} "
        f"({', '.join(atributos)})"
    )


def generar_descripcion(proyecto):
    """
    Construye la descripción institucional completa.
    """

    tipo = proyecto["tipo"]
    niveles = proyecto["niveles"]
    cantidad_edificaciones = proyecto["edificaciones"]

    # --------------------------------------------------------
    # INTRODUCCIÓN
    # --------------------------------------------------------

    if tipo == "Vivienda":

        if niveles == 1:
            texto = (
                "El proyecto presentado consiste en la construcción "
                "de una vivienda de un nivel de altura"
            )

        elif niveles == 2:
            texto = (
                "El proyecto presentado consiste en la construcción "
                "de una vivienda de dos niveles de altura"
            )

        else:
            texto = (
                "El proyecto presentado consiste en la construcción "
                f"de una vivienda de {numero_letras(niveles)} niveles de altura"
            )

    elif tipo == "Complejo turístico":

        texto = (
            "El proyecto presentado consiste en la construcción "
            "de un complejo turístico"
        )

    elif tipo == "Edificación comercial":

        texto = (
            "El proyecto presentado consiste en la construcción "
            f"de una edificación de {numero_letras(niveles)} niveles de altura"
        )

    elif tipo == "Edificación institucional":

        texto = (
            "El proyecto presentado consiste en la construcción "
            f"de una edificación de {numero_letras(niveles)} niveles de altura"
        )

    else:

        texto = (
            "El proyecto presentado consiste en la construcción "
            "de una edificación"
        )

    texto += ", con las siguientes características:\n\n"

    # --------------------------------------------------------
    # EXTERIORES
    # --------------------------------------------------------

    if proyecto["exteriores"]:

        texto += "EXTERIORES:\n"

        for exterior in proyecto["exteriores"]:

            if exterior == "Estacionamientos":
                cantidad = proyecto.get("cantidad_estacionamientos", 0)

                if cantidad > 0:
                    texto += (
                        f"- Estacionamientos "
                        f"({cantidad:02d} unidades)\n"
                    )
                else:
                    texto += "- Estacionamientos\n"

            else:
                texto += f"- {exterior}\n"

        texto += "\n"

    # --------------------------------------------------------
    # EDIFICACIONES
    # --------------------------------------------------------

    texto += "EDIFICACIONES:\n"

    for edificio in proyecto["lista_edificios"]:

        nombre = edificio["nombre"]
        niveles_edificio = edificio["niveles"]

        if niveles_edificio == 1:
            nivel_texto = "un nivel de altura"
        elif niveles_edificio == 2:
            nivel_texto = "dos niveles de altura"
        else:
            nivel_texto = (
                f"{numero_letras(niveles_edificio)} niveles de altura"
            )

        texto += (
            f"{nombre} de {nivel_texto}, que contiene:\n"
        )

        # ----------------------------------------------------
        # NIVELES
        # ----------------------------------------------------

        for nivel in edificio["lista_niveles"]:

            numero_nivel = nivel["numero"]

            if numero_nivel == 0:
                titulo = "Soterrado:"
            elif numero_nivel == 1:
                titulo = "Primer nivel:"
            elif numero_nivel == 2:
                titulo = "Segundo nivel:"
            elif numero_nivel == 3:
                titulo = "Tercer nivel:"
            elif numero_nivel == 4:
                titulo = "Cuarto nivel:"
            else:
                titulo = f"Nivel {numero_nivel}:"

            texto += f"{titulo}\n"

            for espacio in nivel["espacios"]:
                texto += f"- {espacio}\n"

            # Habitaciones
            if nivel["habitaciones"]["cantidad"] > 0:

                habitaciones_texto = generar_habitaciones(
                    nivel["habitaciones"]
                )

                texto += f"- {habitaciones_texto}\n"

            texto += "\n"

    return texto.strip()


# ============================================================
# SESSION STATE
# ============================================================

if "lista_edificios" not in st.session_state:
    st.session_state.lista_edificios = []

if "descripcion_generada" not in st.session_state:
    st.session_state.descripcion_generada = ""


# ============================================================
# ENCABEZADO
# ============================================================

st.title("🏗️ Generador de Descripciones de Proyectos")

st.write(
    "Herramienta para construir automáticamente la descripción "
    "de proyectos a partir de características seleccionadas."
)

st.divider()


# ============================================================
# 1. INFORMACIÓN GENERAL
# ============================================================

st.header("1. Información general del proyecto")

col1, col2, col3 = st.columns(3)

with col1:
    tipo_proyecto = st.selectbox(
        "Tipo de proyecto",
        [
            "Vivienda",
            "Complejo turístico",
            "Edificación comercial",
            "Edificación institucional",
            "Otro"
        ]
    )

with col2:
    cantidad_edificaciones = st.number_input(
        "Cantidad de edificaciones",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )

with col3:
    niveles_generales = st.number_input(
        "Cantidad de niveles",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )


# ============================================================
# 2. CARACTERÍSTICAS EXTERIORES
# ============================================================

st.header("2. Características exteriores")

exteriores_seleccionados = st.multiselect(
    "Seleccione las características exteriores",
    EXTERIORES
)

cantidad_estacionamientos = 0

if "Estacionamientos" in exteriores_seleccionados:

    cantidad_estacionamientos = st.number_input(
        "Cantidad de estacionamientos",
        min_value=1,
        max_value=500,
        value=1,
        step=1
    )


# ============================================================
# 3. EDIFICACIONES
# ============================================================

st.header("3. Edificaciones")

st.write(
    "Configure las edificaciones que forman parte del proyecto."
)

# Crear edificaciones automáticamente
while len(st.session_state.lista_edificios) < cantidad_edificaciones:

    numero = len(st.session_state.lista_edificios) + 1

    st.session_state.lista_edificios.append({
        "nombre": f"Una edificación",
        "niveles": 1,
        "lista_niveles": []
    })

# Eliminar sobrantes si se reduce la cantidad
if len(st.session_state.lista_edificios) > cantidad_edificaciones:

    st.session_state.lista_edificios = (
        st.session_state.lista_edificios[:cantidad_edificaciones]
    )


# ============================================================
# CONFIGURACIÓN DE CADA EDIFICACIÓN
# ============================================================

for i, edificio in enumerate(
    st.session_state.lista_edificios
):

    st.subheader(f"Edificación {i + 1}")

    col1, col2 = st.columns(2)

    with col1:

        nombre_edificio = st.text_input(
            "Descripción de la edificación",
            value=edificio["nombre"],
            key=f"nombre_edificio_{i}"
        )

        edificio["nombre"] = nombre_edificio

    with col2:

        niveles_edificio = st.number_input(
            "Cantidad de niveles",
            min_value=1,
            max_value=10,
            value=edificio["niveles"],
            step=1,
            key=f"niveles_edificio_{i}"
        )

        edificio["niveles"] = niveles_edificio

    # --------------------------------------------------------
    # Crear niveles
    # --------------------------------------------------------

    while len(edificio["lista_niveles"]) < niveles_edificio:

        numero_nuevo = len(edificio["lista_niveles"]) + 1

        edificio["lista_niveles"].append({
            "numero": numero_nuevo,
            "espacios": [],
            "habitaciones": {
                "cantidad": 0,
                "banos": 0,
                "vestidores": 0,
                "terrazas": 0,
                "balcones": 0
            }
        })

    if len(edificio["lista_niveles"]) > niveles_edificio:

        edificio["lista_niveles"] = (
            edificio["lista_niveles"][:niveles_edificio]
        )

    # --------------------------------------------------------
    # Configurar niveles
    # --------------------------------------------------------

    for j, nivel in enumerate(
        edificio["lista_niveles"]
    ):

        if j == 0:
            nombre_nivel = "Primer nivel"
        elif j == 1:
            nombre_nivel = "Segundo nivel"
        elif j == 2:
            nombre_nivel = "Tercer nivel"
        elif j == 3:
            nombre_nivel = "Cuarto nivel"
        else:
            nombre_nivel = f"Nivel {j + 1}"

        with st.expander(
            f"🏢 {nombre_nivel}",
            expanded=True
        ):

            nivel["numero"] = j + 1

            espacios = st.multiselect(
                "Espacios y características",
                ESPACIOS,
                default=nivel["espacios"],
                key=f"espacios_{i}_{j}"
            )

            nivel["espacios"] = espacios

            st.markdown("**Habitaciones**")

            cantidad_habitaciones = st.number_input(
                "Cantidad de habitaciones",
                min_value=0,
                max_value=100,
                value=nivel["habitaciones"]["cantidad"],
                step=1,
                key=f"habitaciones_{i}_{j}"
            )

            nivel["habitaciones"]["cantidad"] = (
                cantidad_habitaciones
            )

            if cantidad_habitaciones > 0:

                col1, col2 = st.columns(2)

                with col1:

                    banos = st.number_input(
                        "Habitaciones con baño",
                        min_value=0,
                        max_value=cantidad_habitaciones,
                        value=min(
                            nivel["habitaciones"]["banos"],
                            cantidad_habitaciones
                        ),
                        key=f"banos_{i}_{j}"
                    )

                    vestidores = st.number_input(
                        "Habitaciones con vestidor",
                        min_value=0,
                        max_value=cantidad_habitaciones,
                        value=min(
                            nivel["habitaciones"]["vestidores"],
                            cantidad_habitaciones
                        ),
                        key=f"vestidores_{i}_{j}"
                    )

                with col2:

                    terrazas = st.number_input(
                        "Habitaciones con terraza",
                        min_value=0,
                        max_value=cantidad_habitaciones,
                        value=min(
                            nivel["habitaciones"]["terrazas"],
                            cantidad_habitaciones
                        ),
                        key=f"terrazas_{i}_{j}"
                    )

                    balcones = st.number_input(
                        "Habitaciones con balcón",
                        min_value=0,
                        max_value=cantidad_habitaciones,
                        value=min(
                            nivel["habitaciones"]["balcones"],
                            cantidad_habitaciones
                        ),
                        key=f"balcones_{i}_{j}"
                    )

                nivel["habitaciones"]["banos"] = banos
                nivel["habitaciones"]["vestidores"] = vestidores
                nivel["habitaciones"]["terrazas"] = terrazas
                nivel["habitaciones"]["balcones"] = balcones


# ============================================================
# 4. GENERAR DESCRIPCIÓN
# ============================================================

st.divider()

st.header("4. Generar descripción")

if st.button(
    "📝 Generar descripción",
    type="primary",
    use_container_width=True
):

    proyecto = {
        "tipo": tipo_proyecto,
        "edificaciones": cantidad_edificaciones,
        "niveles": niveles_generales,
        "exteriores": exteriores_seleccionados,
        "cantidad_estacionamientos": cantidad_estacionamientos,
        "lista_edificios": st.session_state.lista_edificios
    }

    st.session_state.descripcion_generada = (
        generar_descripcion(proyecto)
    )


# ============================================================
# 5. RESULTADO
# ============================================================

if st.session_state.descripcion_generada:

    st.divider()

    st.header("5. Descripción generada")

    st.text_area(
        "Puede revisar y copiar el texto generado:",
        value=st.session_state.descripcion_generada,
        height=600
    )

    st.download_button(
        label="⬇️ Descargar descripción en TXT",
        data=st.session_state.descripcion_generada,
        file_name="descripcion_proyecto.txt",
        mime="text/plain",
        use_container_width=True
    )
