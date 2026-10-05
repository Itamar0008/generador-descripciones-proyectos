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
# FUNCIONES
# ============================================================

def numero_letras(numero):
    numeros = {
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
        30: "treinta"
    }

    return numeros.get(numero, str(numero))


def nombre_nivel(numero):
    nombres = {
        1: "Primer nivel",
        2: "Segundo nivel",
        3: "Tercer nivel",
        4: "Cuarto nivel",
        5: "Quinto nivel",
        6: "Sexto nivel",
        7: "Séptimo nivel",
        8: "Octavo nivel",
        9: "Noveno nivel",
        10: "Décimo nivel"
    }

    return nombres.get(numero, f"Nivel {numero}")


def descripcion_habitaciones(grupo):
    cantidad = grupo["cantidad"]
    texto = grupo["descripcion"].strip()

    if cantidad == 1:
        if texto:
            return f"Una {texto}"
        return "Una habitación"

    if texto:
        return f"{numero_letras(cantidad).capitalize()} {texto}"

    return (
        f"{numero_letras(cantidad).capitalize()} habitaciones"
    )


def generar_descripcion(proyecto):

    # --------------------------------------------------------
    # INTRODUCCIÓN
    # --------------------------------------------------------

    tipo = proyecto["tipo"]
    niveles = proyecto["niveles_generales"]

    if tipo == "Vivienda":

        if niveles == 1:
            introduccion = (
                "El proyecto presentado consiste en la construcción "
                "de una vivienda de un nivel de altura"
            )

        elif niveles == 2:
            introduccion = (
                "El proyecto presentado consiste en la construcción "
                "de una vivienda de dos niveles de altura"
            )

        else:
            introduccion = (
                "El proyecto presentado consiste en la construcción "
                f"de una vivienda de {numero_letras(niveles)} "
                "niveles de altura"
            )

    elif tipo == "Complejo turístico":

        introduccion = (
            "El proyecto presentado consiste en la construcción "
            "de un complejo turístico"
        )

    elif tipo == "Edificación comercial":

        introduccion = (
            "El proyecto presentado consiste en la construcción "
            f"de una edificación de {numero_letras(niveles)} "
            "niveles de altura"
        )

    elif tipo == "Edificación institucional":

        introduccion = (
            "El proyecto presentado consiste en la construcción "
            f"de una edificación de {numero_letras(niveles)} "
            "niveles de altura"
        )

    else:

        introduccion = (
            "El proyecto presentado consiste en la construcción "
            "de una edificación"
        )

    texto = introduccion + ", con las siguientes características:\n\n"

    # --------------------------------------------------------
    # EXTERIORES
    # --------------------------------------------------------

    if proyecto["exteriores"]:

        texto += "EXTERIORES:\n"

        for exterior in proyecto["exteriores"]:

            exterior = exterior.strip()

            if exterior:
                texto += f"- {exterior}\n"

        texto += "\n"

    # --------------------------------------------------------
    # EDIFICACIONES
    # --------------------------------------------------------

    texto += "EDIFICACIONES:\n"

    for edificio in proyecto["edificios"]:

        nombre = edificio["nombre"].strip()

        if not nombre:
            nombre = "Una edificación"

        niveles_edificio = edificio["niveles"]

        # Texto del nivel
        if niveles_edificio == 1:
            texto_niveles = "un nivel de altura"
        elif niveles_edificio == 2:
            texto_niveles = "dos niveles de altura"
        else:
            texto_niveles = (
                f"{numero_letras(niveles_edificio)} "
                "niveles de altura"
            )

        texto += (
            f"{nombre} de {texto_niveles}, que contiene:\n"
        )

        # ----------------------------------------------------
        # NIVELES
        # ----------------------------------------------------

        for nivel in edificio["niveles_lista"]:

            numero = nivel["numero"]

            # Si es un soterrado
            if nivel["tipo"] == "Soterrado":

                texto += "Soterrado:\n"

            else:

                texto += f"{nombre_nivel(numero)}:\n"

            # ------------------------------------------------
            # ESPACIOS
            # ------------------------------------------------

            for elemento in nivel["elementos"]:

                elemento = elemento.strip()

                if elemento:
                    texto += f"- {elemento}\n"

            # ------------------------------------------------
            # HABITACIONES
            # ------------------------------------------------

            for grupo in nivel["habitaciones"]:

                texto_habitacion = descripcion_habitaciones(
                    grupo
                )

                texto += f"- {texto_habitacion}\n"

            texto += "\n"

    return texto.strip()


# ============================================================
# SESSION STATE
# ============================================================

if "edificios" not in st.session_state:
    st.session_state.edificios = []

if "exteriores" not in st.session_state:
    st.session_state.exteriores = []

if "descripcion_generada" not in st.session_state:
    st.session_state.descripcion_generada = ""


# ============================================================
# ENCABEZADO
# ============================================================

st.title("🏗️ Generador de Descripciones de Proyectos")

st.write(
    "Construya la descripción del proyecto agregando directamente "
    "los elementos que necesita."
)

st.divider()


# ============================================================
# 1. INFORMACIÓN GENERAL
# ============================================================

st.header("1. Información general")

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
        max_value=50,
        value=1,
        step=1
    )

with col3:

    niveles_generales = st.number_input(
        "Cantidad de niveles",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )


# ============================================================
# 2. EXTERIORES
# ============================================================

st.header("2. Exteriores")

st.caption(
    "Escriba cada característica exterior y agregue tantas "
    "como necesite."
)


# Ajustar cantidad de elementos exteriores
while len(st.session_state.exteriores) < 1:
    st.session_state.exteriores.append("")


for i in range(len(st.session_state.exteriores)):

    col1, col2 = st.columns([10, 1])

    with col1:

        st.session_state.exteriores[i] = st.text_input(
            f"Elemento exterior {i + 1}",
            value=st.session_state.exteriores[i],
            placeholder=(
                "Ej.: Acceso peatonal y vehicular"
            ),
            key=f"exterior_{i}"
        )

    with col2:

        st.write("")
        st.write("")

        if st.button(
            "✕",
            key=f"eliminar_exterior_{i}"
        ):

            st.session_state.exteriores.pop(i)
            st.rerun()


if st.button(
    "＋ Agregar elemento exterior",
    key="agregar_exterior"
):

    st.session_state.exteriores.append("")
    st.rerun()


# ============================================================
# 3. EDIFICACIONES
# ============================================================

st.divider()

st.header("3. Edificaciones")

st.caption(
    "Agregue cada edificación y configure sus niveles."
)


# Ajustar cantidad de edificaciones
while len(st.session_state.edificios) < cantidad_edificaciones:

    st.session_state.edificios.append({
        "nombre": "",
        "niveles": 1,
        "niveles_lista": [
            {
                "numero": 1,
                "tipo": "Nivel",
                "elementos": [""],
                "habitaciones": []
            }
        ]
    })


if len(st.session_state.edificios) > cantidad_edificaciones:

    st.session_state.edificios = (
        st.session_state.edificios[
            :cantidad_edificaciones
        ]
    )


# ============================================================
# EDIFICACIONES
# ============================================================

for i, edificio in enumerate(
    st.session_state.edificios
):

    st.subheader(f"🏢 Edificación {i + 1}")

    col1, col2 = st.columns([3, 1])

    with col1:

        edificio["nombre"] = st.text_input(
            "Nombre / descripción de la edificación",
            value=edificio["nombre"],
            placeholder=(
                "Ej.: Una vivienda"
            ),
            key=f"edificio_nombre_{i}"
        )

    with col2:

        nuevos_niveles = st.number_input(
            "Cantidad de niveles",
            min_value=1,
            max_value=20,
            value=edificio["niveles"],
            step=1,
            key=f"edificio_niveles_{i}"
        )

        edificio["niveles"] = nuevos_niveles

    # --------------------------------------------------------
    # CREAR NIVELES
    # --------------------------------------------------------

    while len(edificio["niveles_lista"]) < nuevos_niveles:

        numero_nuevo = (
            len(edificio["niveles_lista"]) + 1
        )

        edificio["niveles_lista"].append({
            "numero": numero_nuevo,
            "tipo": "Nivel",
            "elementos": [""],
            "habitaciones": []
        })

    if len(edificio["niveles_lista"]) > nuevos_niveles:

        edificio["niveles_lista"] = (
            edificio["niveles_lista"][
                :nuevos_niveles
            ]
        )

    # --------------------------------------------------------
    # NIVELES
    # --------------------------------------------------------

    for j, nivel in enumerate(
        edificio["niveles_lista"]
    ):

        numero_nivel = j + 1

        with st.expander(
            f"📐 {nombre_nivel(numero_nivel)}",
            expanded=True
        ):

            # -----------------------------------------------
            # TIPO DE NIVEL
            # -----------------------------------------------

            tipo_nivel = st.selectbox(
                "Tipo de nivel",
                [
                    "Nivel",
                    "Soterrado"
                ],
                index=(
                    1
                    if nivel["tipo"] == "Soterrado"
                    else 0
                ),
                key=f"tipo_nivel_{i}_{j}"
            )

            nivel["tipo"] = tipo_nivel

            # -----------------------------------------------
            # ELEMENTOS / ESPACIOS
            # -----------------------------------------------

            st.markdown("**Espacios y características**")

            if "elementos" not in nivel:
                nivel["elementos"] = [""]

            if len(nivel["elementos"]) == 0:
                nivel["elementos"].append("")

            for k in range(
                len(nivel["elementos"])
            ):

                col1, col2 = st.columns([10, 1])

                with col1:

                    nivel["elementos"][k] = (
                        st.text_input(
                            f"Elemento {k + 1}",
                            value=nivel["elementos"][k],
                            placeholder=(
                                "Ej.: Sala – comedor – cocina"
                            ),
                            key=(
                                f"elemento_{i}_{j}_{k}"
                            )
                        )
                    )

                with col2:

                    st.write("")
                    st.write("")

                    if st.button(
                        "✕",
                        key=(
                            f"eliminar_elemento_"
                            f"{i}_{j}_{k}"
                        )
                    ):

                        nivel["elementos"].pop(k)
                        st.rerun()

            if st.button(
                "＋ Agregar espacio / elemento",
                key=f"agregar_elemento_{i}_{j}"
            ):

                nivel["elementos"].append("")
                st.rerun()

            # -----------------------------------------------
            # HABITACIONES
            # -----------------------------------------------

            st.markdown("---")

            st.markdown("**Habitaciones**")

            st.caption(
                "Puede crear diferentes grupos de habitaciones. "
                "Ej.: 1 habitación con baño + 1 habitación."
            )

            if "habitaciones" not in nivel:
                nivel["habitaciones"] = []

            # -----------------------------------------------
            # GRUPOS DE HABITACIONES
            # -----------------------------------------------

            for h, grupo in enumerate(
                nivel["habitaciones"]
            ):

                st.markdown(
                    f"**Grupo de habitaciones {h + 1}**"
                )

                col1, col2, col3 = st.columns(
                    [1, 4, 1]
                )

                with col1:

                    grupo["cantidad"] = st.number_input(
                        "Cantidad",
                        min_value=1,
                        max_value=100,
                        value=grupo["cantidad"],
                        step=1,
                        key=(
                            f"cantidad_hab_"
                            f"{i}_{j}_{h}"
                        )
                    )

                with col2:

                    grupo["descripcion"] = st.text_input(
                        "Descripción",
                        value=grupo["descripcion"],
                        placeholder=(
                            "Ej.: habitación con baño"
                        ),
                        key=(
                            f"descripcion_hab_"
                            f"{i}_{j}_{h}"
                        )
                    )

                with col3:

                    st.write("")
                    st.write("")

                    if st.button(
                        "✕",
                        key=(
                            f"eliminar_hab_"
                            f"{i}_{j}_{h}"
                        )
                    ):

                        nivel["habitaciones"].pop(h)
                        st.rerun()

            if st.button(
                "＋ Agregar grupo de habitaciones",
                key=f"agregar_habitacion_{i}_{j}"
            ):

                nivel["habitaciones"].append({
                    "cantidad": 1,
                    "descripcion": ""
                })

                st.rerun()


# ============================================================
# 4. GENERAR DESCRIPCIÓN
# ============================================================

st.divider()

st.header("4. Generar descripción")

if st.button(
    "📝 GENERAR DESCRIPCIÓN",
    type="primary",
    use_container_width=True
):

    proyecto = {
        "tipo": tipo_proyecto,
        "niveles_generales": niveles_generales,
        "exteriores": st.session_state.exteriores,
        "edificios": st.session_state.edificios
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
        "Revise y edite el texto si es necesario:",
        value=st.session_state.descripcion_generada,
        height=650
    )

    st.download_button(
        "⬇️ Descargar descripción",
        data=st.session_state.descripcion_generada,
        file_name="descripcion_proyecto.txt",
        mime="text/plain",
        use_container_width=True
    )
