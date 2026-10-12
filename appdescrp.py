import streamlit as st
from collections import OrderedDict
from copy import deepcopy

st.set_page_config(
    page_title="Generador de descripciones de proyectos",
    page_icon="🏗️",
    layout="wide",
)

st.title("Generador de descripciones de proyectos")
st.caption(
    "Selecciona elementos preconfigurados, indica cantidades y organiza los espacios por nivel. "
    "El catálogo conserva las expresiones originales proporcionadas."
)

# Catálogo original. Se conservan las categorías, los nombres y las repeticiones.
CATALOGO = OrderedDict({
    "EXTERIORES": OrderedDict({
        "Accesos y circulación": [
            "Acceso peatonal y vehicular",
            "Estacionamientos vehiculares",
            "Estacionamientos para motores",
            "Marquesina doble",
            "Balcón",
            "Balcón privado",
        ],
        "Recreación y esparcimiento": [
            "Piscina",
            "Piscina con asoleadero",
            "Jacuzzi",
            "Hoguera",
            "Fogata",
            "Gazebo con área BBQ",
        ],
        "Paisajismo y elementos ornamentales": [
            "Áreas verdes",
        ],
        "Instalaciones y servicios exteriores": [
            "Cuarto de equipos de bombeo",
            "Cuarto para planta eléctrica y medidor eléctrico",
            "Depósito para basura",
            "Duchas para piscina en exterior",
            "½ Baños para ambos sexos",
        ],
    }),
    "INTERIORES": OrderedDict({
        "Accesos y circulación": [
            "Entrada",
            "Entradas",
            "Vestíbulo",
            "Escalera",
            "Escaleras",
            "Dos escaleras",
        ],
        "Áreas sociales": [
            "Sala – comedor - cocina con desayunador",
            "Sala – comedor – cocina",
            "Sala - comedor",
            "Sala de estar",
            "Área de estar",
            "Sala de espera",
            "Recepción",
            "Terraza",
            "Terraza con desayunador",
            "Terraza con kitchenette",
            "Terraza con comedor",
            "Terraza techada con comedor y área BBQ",
        ],
        "Cocinas": [
            "Cocina con desayunador",
            "Cocina fría con desayunador",
            "Cocina caliente",
            "Cocina caliente con despensa",
            "Cocina – comedor – sala de estar para empleados",
            "Kitchenette",
            "Despensa",
        ],
        "Habitaciones": [
            "Habitación con baño",
            "Habitación con vestidor y baño",
            "Habitación Principal con vestidor, baño, piscina y balcón",
            "Tres habitaciones con baño y balcón (una con vestidor)",
            "Dos habitaciones con baño y terraza",
            "Tres habitaciones con vestidor y baño",
            "Tres habitaciones con baño y vestidor (dos con balcón)",
            "Cuatro habitaciones con baño (tres con vestidor)",
            "Dormitorio de servicio con baño",
        ],
        "Baños": [
            "½ baño",
            "½ Baño",
            "Baño",
            "Baño para ambos sexos",
            "Baños para ambos sexos",
        ],
        "Áreas de servicio": [
            "Área de lavado",
            "Área de servicio",
            "Cuarto de limpieza",
        ],
        "Almacenamiento": [
            "Depósito",
            "Bodega",
            "Archivo",
            "Escaleras con almacén y cuarto de equipos debajo",
        ],
        "Equipos e instalaciones": [
            "Cuarto de control eléctrico",
            "Cuarto de dispositivos para gas",
            "Cuartos de equipos de bombeo",
            "Bóveda",
        ],
        "Oficinas y trabajo": [
            "Oficina",
            "Tres oficinas",
            "Cinco cubículos de oficina",
            "Sala de reuniones",
            "Área de cajeros",
        ],
        "Recreación y bienestar": [
            "Gimnasio",
            "Cine",
            "Salón de eventos con escenario",
        ],
        "Elementos arquitectónicos especiales": [
            "Jardín interior",
            "Espejos de agua",
        ],
    }),
    "ELEMENTOS QUE PUEDEN REQUERIR REVISIÓN SEGÚN CRITERIO DEL PROYECTO": OrderedDict({
        "Elementos exteriores o semiabiertos sujetos a revisión": [
            "Terraza",
            "Terraza con desayunador",
            "Terraza con kitchenette",
            "Terraza con comedor",
            "Terraza techada con comedor y área BBQ",
            "Gazebo con área BBQ",
            "Balcón",
            "Balcón privado",
            "Jardín interior",
            "Espejos de agua",
        ],
    }),
})

# Las seis descripciones originales quedan disponibles como proyectos de ejemplo.
PLANTILLAS = {
    "1 — Vivienda de dos niveles": {
        "tipo": "vivienda",
        "niveles": 2,
        "exteriores": [
            ("Acceso peatonal y vehicular", 1), ("Piscina con asoleadero", 1), ("Áreas verdes", 1)
        ],
        "interiores": {
            "Primer nivel": [
                ("Marquesina doble", 1), ("Entrada", 1), ("Vestíbulo", 1), ("Escaleras", 1),
                ("Sala – comedor - cocina con desayunador", 1), ("Área de lavado", 1),
                ("Terraza  - comedor con área BBQ", 1), ("½ baño", 1),
                ("Cuarto de equipos de bombeo", 1), ("Dormitorio de servicio con baño", 1),
                ("Habitación con baño", 1)
            ],
            "Segundo nivel": [("Tres habitaciones con baño y balcón (una con vestidor)", 1)]
        },
    },
    "2 — Vivienda de un nivel": {
        "tipo": "vivienda",
        "niveles": 1,
        "exteriores": [
            ("Acceso peatonal y vehicular", 1), ("Áreas verdes", 1), ("Estacionamientos vehiculares", 1)
        ],
        "interiores": {
            "Primer nivel": [
                ("Entrada", 1), ("Sala – comedor – cocina", 1), ("Baño", 1), ("Gimnasio", 1),
                ("Terraza con desayunador", 1), ("Habitación con baño", 1)
            ]
        },
    },
    "3 — Edificación de tres niveles": {
        "tipo": "edificación",
        "niveles": 3,
        "exteriores": [
            ("Acceso peatonal y vehicular", 1), ("Estacionamientos vehiculares", 1),
            ("Estacionamientos para motores", 1),
            ("Cuarto para planta eléctrica y medidor eléctrico", 1),
            ("Cuarto de equipos de bombeo", 1), ("½ Baños para ambos sexos", 1),
            ("Depósito para basura", 1), ("Áreas verdes", 1)
        ],
        "interiores": {
            "Primer nivel": [
                ("Entradas", 1), ("Dos escaleras", 1), ("Sala de espera", 1), ("Recepción", 1),
                ("Área de servicio", 1), ("Área de cajeros", 1), ("Cuarto de control eléctrico", 1),
                ("Baño para ambos sexos", 1), ("Oficina", 1), ("Bóveda", 1), ("Archivo", 1), ("Depósito", 1)
            ],
            "Segundo nivel": [
                ("Área de estar", 1), ("Cinco cubículos de oficina", 1), ("Tres oficinas", 1),
                ("Sala de reuniones", 1), ("Cuarto de limpieza", 1), ("Baños para ambos sexos", 1),
                ("Cocina – comedor – sala de estar para empleados", 1)
            ],
            "Tercer nivel": [
                ("Salón de eventos con escenario", 1), ("Terraza con kitchenette", 1),
                ("Baños para ambos sexos", 1), ("Depósito", 1)
            ],
        },
    },
    "4 — Vivienda de dos niveles con jacuzzi y hoguera": {
        "tipo": "vivienda",
        "niveles": 2,
        "exteriores": [
            ("Acceso peatonal y vehicular", 1), ("Piscina con asoleadero", 1), ("Jacuzzi", 1),
            ("Hoguera", 1), ("Áreas verdes", 1)
        ],
        "interiores": {
            "Primer nivel": [
                ("Marquesina doble", 1), ("Vestíbulo", 1), ("½ baño", 1), ("Escaleras", 1),
                ("Sala – comedor - cocina con desayunador", 1), ("Cocina caliente con despensa", 1),
                ("Bodega", 1), ("Cine", 1), ("Gimnasio", 1), ("Terraza", 1), ("Área de lavado", 1),
                ("Depósito", 1), ("Baño", 1), ("Gazebo con área BBQ", 1),
                ("Dormitorio de servicio con baño", 1), ("Habitación con vestidor y baño", 1)
            ],
            "Segundo nivel": [
                ("Sala de estar", 1), ("Cuatro habitaciones con baño (tres con vestidor)", 1),
                ("Habitación Principal con vestidor, baño, piscina y balcón", 1)
            ],
        },
    },
    "5 — Vivienda de dos niveles con dos habitaciones arriba": {
        "tipo": "vivienda",
        "niveles": 2,
        "exteriores": [
            ("Acceso peatonal y vehicular", 1), ("Piscina con asoleadero", 1),
            ("Depósito para basura", 1), ("Áreas verdes", 1)
        ],
        "interiores": {
            "Primer nivel": [
                ("Marquesina doble", 1), ("Entrada", 1),
                ("Escaleras con almacén y cuarto de equipos debajo", 1),
                ("Cuartos de equipos de bombeo", 1), ("Sala – comedor - cocina con desayunador", 1),
                ("Área de lavado", 1), ("Terraza", 1), ("Dormitorio de servicio con baño", 1),
                ("Habitación con baño", 1)
            ],
            "Segundo nivel": [("Dos habitaciones con baño y terraza", 1)]
        },
    },
    "6 — Vivienda de dos niveles con cocina fría": {
        "tipo": "vivienda",
        "niveles": 2,
        "exteriores": [
            ("Acceso peatonal y vehicular", 1), ("Piscina", 1),
            ("Depósito para basura", 1), ("Áreas verdes", 1)
        ],
        "interiores": {
            "Primer nivel": [
                ("Marquesina doble", 1), ("Entrada", 1), ("Escalera", 1), ("Sala - comedor", 1),
                ("Cocina fría con desayunador", 1), ("Cocina caliente", 1), ("Área de lavado", 1),
                ("Terraza con comedor", 1), ("Dormitorio de servicio con baño", 1),
                ("Habitación con vestidor y baño", 1)
            ],
            "Segundo nivel": [
                ("Sala de estar", 1), ("Estudio", 1), ("Tres habitaciones con vestidor y baño", 1)
            ],
        },
    },
}

NOMBRES_NIVELES = [
    "Primer nivel", "Segundo nivel", "Tercer nivel", "Cuarto nivel",
    "Quinto nivel", "Sexto nivel", "Sótano"
]

def inicializar_estado():
    defaults = {
        "tipo_proyecto": "vivienda",
        "cantidad_niveles": 2,
        "exteriores_seleccionados": [],
        "interiores": {nivel: [] for nivel in NOMBRES_NIVELES},
        "revision_seleccionados": [],
        "encabezado": "El proyecto presentado consiste en la construcción de una vivienda de dos niveles de altura, con las siguientes características:",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = deepcopy(value)

def opciones_todas(seccion):
    return [item for grupo in CATALOGO[seccion].values() for item in grupo]

def mostrar_elementos(selecciones):
    """Genera líneas conservando las frases compuestas originales."""
    lineas = []
    for item in selecciones:
        texto = item["texto"]
        cantidad = int(item["cantidad"])
        # Las frases del catálogo se conservan literalmente si cantidad = 1.
        # Para cantidades mayores se usa multiplicador para no deformar expresiones técnicas.
        lineas.append(texto if cantidad == 1 else f"{cantidad} × {texto}")
    return lineas

def construir_texto():
    tipo = st.session_state.tipo_proyecto.strip()
    niveles = int(st.session_state.cantidad_niveles)
    frase_niveles = "un nivel de altura" if niveles == 1 else f"{niveles} niveles de altura"
    encabezado = st.session_state.encabezado.strip()
    if not encabezado:
        encabezado = (
            f"El proyecto presentado consiste en la construcción de {tipo} "
            f"de {frase_niveles}, con las siguientes características:"
        )

    partes = [encabezado, "", "EXTERIORES", ""]
    partes.extend(["- " + x for x in mostrar_elementos(st.session_state.exteriores_seleccionados)])
    partes.extend(["", "EDIFICACIONES", ""])
    if tipo.lower() == "vivienda":
        partes.append(f"Una vivienda de {frase_niveles}, que contiene:")
    else:
        partes.append(f"Una edificación con {frase_niveles}, que contiene:")

    for i, nivel in enumerate(NOMBRES_NIVELES[:min(niveles, 6)]):
        elementos = st.session_state.interiores.get(nivel, [])
        if elementos:
            partes.extend(["", f"{nivel}:", *["- " + x for x in mostrar_elementos(elementos)]])
    if st.session_state.interiores.get("Sótano"):
        partes.extend(["", "Sótano:", *["- " + x for x in mostrar_elementos(st.session_state.interiores["Sótano"])]])
    if st.session_state.revision_seleccionados:
        partes.extend(["", "ELEMENTOS QUE PUEDEN REQUERIR REVISIÓN SEGÚN CRITERIO DEL PROYECTO", ""])
        partes.extend(["- " + x for x in mostrar_elementos(st.session_state.revision_seleccionados)])
    return "\n".join(partes).strip()

def cargar_plantilla(nombre):
    p = PLANTILLAS[nombre]
    st.session_state.tipo_proyecto = p["tipo"]
    st.session_state.cantidad_niveles = p["niveles"]
    st.session_state.exteriores_seleccionados = [
        {"texto": texto, "cantidad": cantidad} for texto, cantidad in p["exteriores"]
    ]
    st.session_state.interiores = {nivel: [] for nivel in NOMBRES_NIVELES}
    for nivel, elementos in p["interiores"].items():
        st.session_state.interiores[nivel] = [
            {"texto": texto, "cantidad": cantidad} for texto, cantidad in elementos
        ]
    st.session_state.revision_seleccionados = []
    if p["tipo"] == "vivienda":
        st.session_state.encabezado = (
            f"El proyecto presentado consiste en la construcción de una vivienda de "
            f"{'un nivel' if p['niveles'] == 1 else str(p['niveles']) + ' niveles'} de altura, "
            "con las siguientes características:"
        )
    else:
        st.session_state.encabezado = (
            f"El proyecto presentado consiste en la construcción de una edificación de "
            f"{p['niveles']} niveles de altura, con las siguientes características:"
        )

inicializar_estado()

# Barra lateral para cargar ejemplos
st.sidebar.header("Plantillas de referencia")
plantilla_elegida = st.sidebar.selectbox(
    "Selecciona una plantilla original",
    ["Proyecto nuevo"] + list(PLANTILLAS.keys()),
)
if st.sidebar.button("Cargar plantilla", use_container_width=True):
    if plantilla_elegida == "Proyecto nuevo":
        st.session_state.tipo_proyecto = "vivienda"
        st.session_state.cantidad_niveles = 1
        st.session_state.exteriores_seleccionados = []
        st.session_state.interiores = {nivel: [] for nivel in NOMBRES_NIVELES}
        st.session_state.revision_seleccionados = []
        st.session_state.encabezado = ""
    else:
        cargar_plantilla(plantilla_elegida)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Las plantillas cargadas son editables. Seleccionar una nueva plantilla reemplaza la selección actual.")

# Datos generales
st.header("1. Datos generales")
c1, c2 = st.columns([2, 1])
with c1:
    st.selectbox("Tipo de proyecto", ["vivienda", "edificación"], key="tipo_proyecto")
with c2:
    st.number_input("Cantidad de niveles", min_value=1, max_value=6, step=1, key="cantidad_niveles")

with st.expander("Encabezado del proyecto (opcional)"):
    st.text_area(
        "El texto se puede dejar vacío para usar el encabezado automático.",
        key="encabezado",
        height=90,
    )

# Helper UI: add selected catalog item + count into state
def selector_agregar(titulo, seccion, destino, nivel=None, key_sufijo=""):
    st.subheader(titulo)
    categorias = list(CATALOGO[seccion].keys())
    col1, col2, col3 = st.columns([2, 3, 1])
    with col1:
        categoria = st.selectbox(
            "Categoría",
            categorias,
            key=f"{key_sufijo}_{seccion}_categoria",
        )
    with col2:
        elemento = st.selectbox(
            "Elemento preconfigurado",
            CATALOGO[seccion][categoria],
            key=f"{key_sufijo}_{seccion}_elemento",
        )
    with col3:
        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            max_value=100,
            value=1,
            step=1,
            key=f"{key_sufijo}_{seccion}_cantidad",
        )
    if st.button("Añadir elemento seleccionado", key=f"{key_sufijo}_{seccion}_agregar"):
        destino.append({"texto": elemento, "cantidad": int(cantidad)})
        st.success(f"Se añadió: {elemento} (cantidad: {cantidad}).")
        st.rerun()

def administrar_lista(titulo, lista, key_base):
    st.markdown(f"**{titulo} seleccionados**")
    if not lista:
        st.caption("Todavía no has añadido elementos.")
        return
    for i, item in enumerate(lista):
        c1, c2, c3 = st.columns([5, 1, 1])
        with c1:
            st.write(item["texto"])
        with c2:
            st.write(f"Cantidad: {item['cantidad']}")
        with c3:
            if st.button("Eliminar", key=f"{key_base}_eliminar_{i}"):
                lista.pop(i)
                st.rerun()

# Exteriores: selección totalmente preconfigurada
st.header("2. Exteriores")
st.caption("Elige la categoría, el elemento exacto del catálogo y la cantidad. No necesitas escribir los nombres.")
selector_agregar("Añadir exterior", "EXTERIORES", st.session_state.exteriores_seleccionados, key_sufijo="ext")
administrar_lista("Elementos exteriores", st.session_state.exteriores_seleccionados, "ext_lista")

# Interiores: cada nivel tiene su propia selección y cantidades
st.header("3. Interiores por nivel")
st.caption(
    "Selecciona cada elemento de las listas preconfiguradas. Para combinaciones especiales de habitaciones, "
    "usa la opción original completa, por ejemplo: «Tres habitaciones con baño y balcón (una con vestidor)»."
)
n = int(st.session_state.cantidad_niveles)
niveles_visibles = NOMBRES_NIVELES[:n]
tabs = st.tabs(niveles_visibles + ["Sótano"])
for idx, nivel in enumerate(niveles_visibles):
    with tabs[idx]:
        st.markdown(f"### {nivel}")
        cat_col, item_col, qty_col = st.columns([2, 3, 1])
        with cat_col:
            categoria = st.selectbox(
                "Categoría interior",
                list(CATALOGO["INTERIORES"].keys()),
                key=f"int_cat_{idx}",
            )
        with item_col:
            elemento = st.selectbox(
                "Elemento o combinación original",
                CATALOGO["INTERIORES"][categoria],
                key=f"int_item_{idx}",
            )
        with qty_col:
            cantidad = st.number_input(
                "Cantidad",
                min_value=1,
                max_value=100,
                value=1,
                step=1,
                key=f"int_qty_{idx}",
            )
        if st.button("Añadir al nivel", key=f"int_add_{idx}"):
            st.session_state.interiores[nivel].append(
                {"texto": elemento, "cantidad": int(cantidad)}
            )
            st.rerun()
        administrar_lista(
            f"Elementos del {nivel.lower()}",
            st.session_state.interiores[nivel],
            f"int_lista_{idx}",
        )

with tabs[-1]:
    st.markdown("### Sótano")
    cat_col, item_col, qty_col = st.columns([2, 3, 1])
    with cat_col:
        categoria_s = st.selectbox(
            "Categoría interior", list(CATALOGO["INTERIORES"].keys()), key="sot_cat"
        )
    with item_col:
        elemento_s = st.selectbox(
            "Elemento o combinación original",
            CATALOGO["INTERIORES"][categoria_s],
            key="sot_item",
        )
    with qty_col:
        cantidad_s = st.number_input(
            "Cantidad", min_value=1, max_value=100, value=1, step=1, key="sot_qty"
        )
    if st.button("Añadir al sótano", key="sot_add"):
        st.session_state.interiores["Sótano"].append(
            {"texto": elemento_s, "cantidad": int(cantidad_s)}
        )
        st.rerun()
    administrar_lista("Elementos del sótano", st.session_state.interiores["Sótano"], "sot_lista")

# Lista de revisión: se mantiene separada y con las opciones exactas que indicó la usuaria
st.header("4. Elementos que pueden requerir revisión según criterio del proyecto")
st.caption("Esta lista conserva los elementos señalados como exteriores o semiabiertos sujetos a revisión.")
revision_opciones = CATALOGO[
    "ELEMENTOS QUE PUEDEN REQUERIR REVISIÓN SEGÚN CRITERIO DEL PROYECTO"
]["Elementos exteriores o semiabiertos sujetos a revisión"]
rev_col1, rev_col2 = st.columns([4, 1])
with rev_col1:
    revision_item = st.selectbox("Elemento sujeto a revisión", revision_opciones, key="revision_item")
with rev_col2:
    revision_cantidad = st.number_input("Cantidad", min_value=1, max_value=100, value=1, key="revision_cantidad")
if st.button("Añadir elemento a revisión"):
    st.session_state.revision_seleccionados.append(
        {"texto": revision_item, "cantidad": int(revision_cantidad)}
    )
    st.rerun()
administrar_lista(
    "Elementos sujetos a revisión",
    st.session_state.revision_seleccionados,
    "revision_lista",
)

# Vista de catálogo íntegro
with st.expander("Consultar catálogo completo original"):
    for seccion, categorias in CATALOGO.items():
        st.markdown(f"## {seccion}")
        for categoria, elementos in categorias.items():
            st.markdown(f"**{categoria}**")
            for elemento in elementos:
                st.markdown(f"- {elemento}")

# Resultado
st.header("5. Descripción generada")
texto_final = construir_texto()
st.text_area("Vista previa del texto generado", value=texto_final, height=450, key="vista_previa")
st.download_button(
    "Descargar descripción en TXT",
    data=st.session_state.get("vista_previa", texto_final),
    file_name="descripcion_proyecto.txt",
    mime="text/plain",
    use_container_width=True,
)
st.info(
    "Nota: cuando una cantidad es mayor que uno, se presenta como «n × elemento» para conservar "
    "exactamente la expresión seleccionada, incluidas las combinaciones especiales. Revisa la redacción "
    "final antes de incorporarla a un documento oficial."
)
