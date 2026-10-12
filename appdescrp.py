import streamlit as st
from collections import OrderedDict
import re

st.set_page_config(
    page_title="Generador de descripciones de proyectos",
    page_icon="🏗️",
    layout="wide",
)

st.title("Generador de descripciones de proyectos")
st.caption(
    "Plantillas reutilizables para redactar descripciones de proyectos. "
    "El catálogo conserva las expresiones proporcionadas; puedes editar o añadir texto libre."
)

# Catálogo fiel al listado proporcionado por la usuaria.
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

# Seis descripciones originales, conservadas como plantillas de referencia.
PLANTILLAS = {
    "1 — Vivienda de dos niveles con piscina y asoleadero": {
        "tipo": "vivienda",
        "niveles": 2,
        "encabezado": "El proyecto presentado consiste en la construcción de una vivienda de dos niveles de altura, con las siguientes características:",
        "titulo_exteriores": "EXTERIOR",
        "exteriores": [
            "Acceso peatonal y vehicular", "Piscina con asoleadero", "Áreas verdes"
        ],
        "edificacion": "Una vivienda de dos niveles de altura, que contiene:",
        "niveles_texto": {
            "Primer nivel": [
                "Marquesina doble", "Entrada", "Vestíbulo", "Escaleras",
                "Sala – comedor - cocina con desayunador", "Área de lavado",
                "Terraza  - comedor con área BBQ", "½ baño",
                "Cuarto de equipos de bombeo", "Dormitorio de servicio con baño",
                "Habitación con baño"
            ],
            "Segundo nivel": [
                "Tres habitaciones con baño y balcón (una con vestidor)"
            ]
        },
    },
    "2 — Vivienda de un nivel con gimnasio": {
        "tipo": "vivienda",
        "niveles": 1,
        "encabezado": "El proyecto presentado consiste en la construcción de una vivienda de un nivel de altura, con las siguientes características:",
        "titulo_exteriores": "EXTERIORES",
        "exteriores": [
            "Acceso peatonal y vehicular", "Áreas verdes", "Estacionamientos vehiculares"
        ],
        "edificacion": "Una edificación con un nivel de altura, que contiene:",
        "niveles_texto": {
            "Primer nivel": [
                "Entrada", "Sala – comedor – cocina", "Baño", "Gimnasio",
                "Terraza con desayunador", "Habitación con baño"
            ]
        },
    },
    "3 — Edificación de tres niveles con oficinas y salón de eventos": {
        "tipo": "edificación",
        "niveles": 3,
        "encabezado": "El proyecto presentado consiste en la construcción de una edificación de tres niveles de altura, con las siguientes características:",
        "titulo_exteriores": "EXTERIORES",
        "exteriores": [
            "Acceso peatonal y vehicular", "Estacionamientos vehiculares",
            "Estacionamientos para motores",
            "Cuarto para planta eléctrica y medidor eléctrico",
            "Cuarto de equipos de bombeo", "½ Baños para ambos sexos",
            "Depósito para basura", "Áreas verdes"
        ],
        "edificacion": "Una edificación con tres niveles de altura, que contiene:",
        "niveles_texto": {
            "Primer nivel": [
                "Entradas", "Dos escaleras", "Sala de espera", "Recepción",
                "Área de servicio", "Área de cajeros", "Cuarto de control eléctrico",
                "Baño para ambos sexos", "Oficina", "Bóveda", "Archivo", "Depósito"
            ],
            "Segundo nivel": [
                "Área de estar", "Cinco cubículos de oficina", "Tres oficinas",
                "Sala de reuniones", "Cuarto de limpieza", "Baños para ambos sexos",
                "Cocina – comedor – sala de estar para empleados"
            ],
            "Tercer nivel": [
                "Salón de eventos con escenario", "Terraza con kitchenette",
                "Baños para ambos sexos", "Depósito"
            ],
        },
    },
    "4 — Vivienda de dos niveles con jacuzzi, hoguera y cine": {
        "tipo": "vivienda",
        "niveles": 2,
        "encabezado": "El proyecto presentado consiste en la construcción de una vivienda de dos niveles de altura, con las siguientes características:",
        "titulo_exteriores": "EXTERIOR",
        "exteriores": [
            "Acceso peatonal y vehicular", "Piscina con asoleadero", "Jacuzzi",
            "Hoguera", "Áreas verdes"
        ],
        "edificacion": "Una vivienda de dos niveles de altura, que contiene:",
        "niveles_texto": {
            "Primer nivel": [
                "Marquesina doble", "Vestíbulo", "½ baño", "Escaleras",
                "Sala – comedor - cocina con desayunador", "Cocina caliente con despensa",
                "Bodega", "Cine", "Gimnasio", "Terraza", "Área de lavado", "Depósito",
                "Baño", "Gazebo con área BBQ", "Dormitorio de servicio con baño",
                "Habitación con vestidor y baño"
            ],
            "Segundo nivel": [
                "Sala de estar", "Cuatro habitaciones con baño (tres con vestidor)",
                "Habitación Principal con vestidor, baño, piscina y balcón"
            ],
        },
    },
    "5 — Vivienda de dos niveles con piscina y dos habitaciones arriba": {
        "tipo": "vivienda",
        "niveles": 2,
        "encabezado": "El proyecto presentado consiste en la construcción de una vivienda de dos niveles de altura, con las siguientes características:",
        "titulo_exteriores": "EXTERIOR",
        "exteriores": [
            "Acceso peatonal y vehicular", "Piscina con asoleadero",
            "Depósito para basura", "Áreas verdes"
        ],
        "edificacion": "Una vivienda de dos niveles de altura, que contiene:",
        "niveles_texto": {
            "Primer nivel": [
                "Marquesina doble", "Entrada",
                "Escaleras con almacén y cuarto de equipos debajo",
                "Cuartos de equipos de bombeo", "Sala – comedor - cocina con desayunador",
                "Área de lavado", "Terraza", "Dormitorio de servicio con baño",
                "Habitación con baño"
            ],
            "Segundo nivel": [
                "Dos habitaciones con baño y terraza"
            ],
        },
    },
    "6 — Vivienda de dos niveles con cocina fría y estudio": {
        "tipo": "vivienda",
        "niveles": 2,
        "encabezado": "El proyecto presentado consiste en la construcción de una vivienda de dos niveles de altura, con las siguientes características:",
        "titulo_exteriores": "EXTERIOR",
        "exteriores": [
            "Acceso peatonal y vehicular", "Piscina", "Depósito para basura", "Áreas verdes"
        ],
        "edificacion": "Una vivienda de dos niveles de altura, que contiene:",
        "niveles_texto": {
            "Primer nivel": [
                "Marquesina doble", "Entrada", "Escalera", "Sala – comedor",
                "Cocina fría con desayunador", "Cocina caliente", "Área de lavado",
                "Terraza con comedor", "Dormitorio de servicio con baño",
                "Habitación con vestidor y baño"
            ],
            "Segundo nivel": [
                "Sala de estar", "Estudio", "Tres habitaciones con vestidor y baño"
            ],
        },
    },
}

def pluralizar_descripcion(texto: str, cantidad: int) -> str:
    """Pluralización prudente para opciones simples; las frases compuestas se conservan."""
    texto = texto.strip()
    if cantidad <= 1:
        return texto
    exactas = {
        "Habitación con baño": "habitaciones con baño",
        "Habitación con vestidor y baño": "habitaciones con vestidor y baño",
        "Baño": "Baños",
        "½ baño": "½ baños",
        "½ Baño": "½ Baños",
        "Oficina": "Oficinas",
        "Entrada": "Entradas",
        "Escalera": "Escaleras",
        "Terraza": "Terrazas",
        "Piscina": "Piscinas",
        "Depósito": "Depósitos",
        "Balcón": "Balcones",
        "Gimnasio": "Gimnasios",
        "Cine": "Cines",
        "Vestíbulo": "Vestíbulos",
    }
    if texto in exactas:
        plural = exactas[texto]
        # Las frases comienzan con mayúscula en el catálogo; conservarla.
        plural = plural[0].upper() + plural[1:]
        return f"{cantidad} {plural.lower()}"
    # Para combinaciones no contempladas, evita alterar la frase técnica.
    return f"{cantidad} × {texto}"

def bullets(items):
    return "\n".join(f"- {item}" for item in items if str(item).strip())

def construir_descripcion(tipo, niveles, exteriores, interiores, encabezado_personalizado="", titulo_exteriores="EXTERIORES", frase_edificacion=""):
    tipo = tipo.strip() or "proyecto"
    try:
        n = int(niveles)
    except (ValueError, TypeError):
        n = 1
    if n == 1:
        frase_niveles = "un nivel de altura"
    else:
        frase_niveles = f"{n} niveles de altura"
    primera = encabezado_personalizado.strip()
    if not primera:
        primera = f"El proyecto presentado consiste en la construcción de {tipo} de {frase_niveles}, con las siguientes características:"
    partes = [primera, "", titulo_exteriores, ""]
    if exteriores:
        partes.append(bullets(exteriores))
    partes.extend(["", "EDIFICACIONES", ""])
    if frase_edificacion.strip():
        partes.append(frase_edificacion.strip())
    elif tipo.lower().startswith("vivienda"):
        partes.append(f"Una vivienda de {frase_niveles}, que contiene:")
    else:
        partes.append(f"Una edificación con {frase_niveles}, que contiene:")
    for nivel, espacios in interiores.items():
        limpios = [x.strip() for x in espacios if str(x).strip()]
        if limpios:
            partes.extend(["", f"{nivel}:", bullets(limpios)])
    return "\n".join(partes).strip()

def copiar_plantilla_a_estado(nombre):
    p = PLANTILLAS[nombre]
    st.session_state.tipo_proyecto = p["tipo"]
    st.session_state.cantidad_niveles = p["niveles"]
    st.session_state.encabezado_personalizado = p.get("encabezado", "")
    st.session_state.titulo_exteriores = p.get("titulo_exteriores", "EXTERIORES")
    st.session_state.frase_edificacion = p.get("edificacion", "")
    st.session_state.exteriores_texto = "\n".join(p["exteriores"])
    for i in range(1, 7):
        key = f"nivel_{i}_texto"
        nivel_nombre = ["Primer nivel", "Segundo nivel", "Tercer nivel",
                        "Cuarto nivel", "Quinto nivel", "Soterrado"][i-1]
        st.session_state[key] = "\n".join(p["niveles_texto"].get(nivel_nombre, []))

def lineas(texto):
    return [line.strip().lstrip("-•").strip() for line in texto.splitlines() if line.strip()]

# --- Barra lateral: plantillas de referencia ---
st.sidebar.header("Plantillas de referencia")
opcion_plantilla = st.sidebar.selectbox(
    "Cargar una de las seis descripciones originales",
    ["Proyecto nuevo"] + list(PLANTILLAS.keys()),
    key="selector_plantilla",
)
if "inicializado" not in st.session_state:
    st.session_state.inicializado = True
    st.session_state.tipo_proyecto = "vivienda"
    st.session_state.cantidad_niveles = 2
    st.session_state.exteriores_texto = ""
    st.session_state.encabezado_personalizado = ""
    st.session_state.titulo_exteriores = "EXTERIORES"
    st.session_state.frase_edificacion = ""
    for i in range(1, 7):
        st.session_state[f"nivel_{i}_texto"] = ""

if st.sidebar.button("Cargar plantilla seleccionada", use_container_width=True):
    if opcion_plantilla == "Proyecto nuevo":
        st.session_state.tipo_proyecto = "vivienda"
        st.session_state.cantidad_niveles = 1
        st.session_state.exteriores_texto = ""
        st.session_state.encabezado_personalizado = ""
        st.session_state.titulo_exteriores = "EXTERIORES"
        st.session_state.frase_edificacion = ""
        for i in range(1, 7):
            st.session_state[f"nivel_{i}_texto"] = ""
    else:
        copiar_plantilla_a_estado(opcion_plantilla)
        st.session_state.encabezado_personalizado = ""
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Las seis plantillas son ejemplos editables. El texto original se usa como referencia y no se guarda sobre el catálogo.")

# --- Datos generales ---
st.header("1. Datos generales del proyecto")
c1, c2 = st.columns([2, 1])
with c1:
    st.text_input("Tipo de proyecto / edificación", key="tipo_proyecto",
                  help="Ejemplos: vivienda, edificación. Puedes escribir el término que corresponda.")
with c2:
    st.number_input("Cantidad de niveles", min_value=1, max_value=20, step=1, key="cantidad_niveles")

st.text_area(
    "Encabezado personalizado (opcional)",
    key="encabezado_personalizado",
    height=75,
    placeholder="Déjalo vacío para generar el encabezado automáticamente. Puedes pegar aquí una redacción aprobada."
)
c3, c4 = st.columns(2)
with c3:
    st.text_input("Título de exteriores", key="titulo_exteriores")
with c4:
    st.text_input(
        "Frase introductoria de edificaciones (opcional)",
        key="frase_edificacion",
        placeholder="Ej.: Una vivienda de dos niveles de altura, que contiene:"
    )

st.info(
    "Para conservar la fidelidad documental, las listas de abajo admiten texto libre. "
    "Puedes pegar cada elemento en una línea, editarlo o añadir frases que no estén en el catálogo."
)

# --- Exterior ---
st.header("2. Exteriores")
tab_catalogo, tab_texto = st.tabs(["Consultar catálogo original", "Editar elementos del proyecto"])
with tab_catalogo:
    st.caption("Catálogo completo según el listado proporcionado. Los elementos repetidos en la sección de revisión se conservan allí también.")
    for categoria, grupos in CATALOGO["EXTERIORES"].items():
        with st.expander(categoria):
            for item in grupos:
                st.markdown(f"- {item}")
with tab_texto:
    st.text_area(
        "Un elemento exterior por línea",
        key="exteriores_texto",
        height=190,
        placeholder="Ejemplo:\nAcceso peatonal y vehicular\nPiscina con asoleadero\nÁreas verdes"
    )

# --- Interior por nivel ---
st.header("3. Interiores por nivel")
st.caption(
    "Puedes conservar una frase compuesta tal como aparece en tus documentos o combinar espacios. "
    "Cada línea se incorpora a la descripción sin cambiar automáticamente sus términos."
)
niveles_disponibles = [
    "Primer nivel", "Segundo nivel", "Tercer nivel",
    "Cuarto nivel", "Quinto nivel", "Soterrado"
]
n_niveles = int(st.session_state.get("cantidad_niveles", 1))
nivel_a_etiqueta = {
    1: "Primer nivel", 2: "Segundo nivel", 3: "Tercer nivel",
    4: "Cuarto nivel", 5: "Quinto nivel"
}
niveles_a_mostrar = [nivel_a_etiqueta[i] for i in range(1, min(n_niveles, 5)+1)]
if n_niveles > 5:
    st.warning("La interfaz de texto muestra hasta el quinto nivel y el soterrado. Si tu proyecto tiene más niveles, puedes describirlos en el campo adicional.")

tabs = st.tabs(niveles_a_mostrar + ["Soterrado", "Catálogo completo"])
for idx, nivel in enumerate(niveles_a_mostrar):
    with tabs[idx]:
        st.text_area(
            f"Elementos del {nivel.lower()} — uno por línea",
            key=f"nivel_{idx+1}_texto",
            height=190,
            placeholder="Ejemplo:\nMarquesina doble\nEntrada\nSala – comedor - cocina con desayunador\nHabitación con baño"
        )
soterrado_index = len(niveles_a_mostrar)
with tabs[soterrado_index]:
    st.text_area(
        "Elementos del soterrado — uno por línea",
        key="nivel_6_texto",
        height=150,
        placeholder="Escribe aquí los espacios del soterrado, si corresponde."
    )
with tabs[-1]:
    for seccion, categorias in CATALOGO.items():
        st.subheader(seccion)
        for categoria, items in categorias.items():
            with st.expander(categoria):
                for item in items:
                    st.markdown(f"- {item}")

# --- Generador de combinaciones con cantidad ---
st.header("4. Añadir una combinación con cantidad")
st.write(
    "Selecciona una frase del catálogo y una cantidad. Para las combinaciones especiales, "
    "puedes conservar la frase completa o escribir una descripción propia. Al añadirla, se coloca "
    "en el nivel elegido; también puedes editar el texto directamente en el campo de ese nivel."
)
seccion_catalogo = st.selectbox("Sección", list(CATALOGO.keys()), index=1)
categorias_catalogo = list(CATALOGO[seccion_catalogo].keys())
categoria_catalogo = st.selectbox("Categoría", categorias_catalogo)
opciones_catalogo = CATALOGO[seccion_catalogo][categoria_catalogo]
combinacion = st.selectbox("Elemento o combinación original", opciones_catalogo)
c_a, c_b, c_c = st.columns([1, 2, 2])
with c_a:
    cantidad_combo = st.number_input("Cantidad", min_value=1, max_value=100, value=1, step=1, key="cantidad_combo")
with c_b:
    nivel_combo = st.selectbox("Añadir al nivel", niveles_disponibles, index=0)
with c_c:
    texto_personalizado = st.text_input(
        "Texto personalizado (opcional)",
        placeholder="Si lo completas, se usará este texto en lugar del elemento del catálogo."
    )

def texto_combo_final():
    base = texto_personalizado.strip() if texto_personalizado.strip() else combinacion
    if texto_personalizado.strip():
        if cantidad_combo > 1:
            return f"{cantidad_combo} × {base}"
        return base
    # Si la frase ya expresa una cantidad o una combinación compuesta, no se modifica.
    compuestas = [
        "Tres habitaciones", "Dos habitaciones", "Cuatro habitaciones",
        "Habitación Principal", "Dormitorio de servicio", "Sala – comedor",
        "Sala - comedor", "Cocina – comedor", "Terraza techada",
        "Gazebo con área BBQ", "Escaleras con almacén", "Dos escaleras",
        "Cinco cubículos", "Tres oficinas", "Baños para ambos sexos",
        "½ Baños para ambos sexos",
    ]
    if cantidad_combo == 1:
        return base
    if any(base.startswith(x) for x in compuestas):
        return f"{cantidad_combo} × {base}"
    return pluralizar_descripcion(base, int(cantidad_combo))

if st.button("Añadir combinación al nivel", type="primary"):
    texto_nuevo = texto_combo_final()
    if nivel_combo == "Soterrado":
        key = "nivel_6_texto"
    else:
        indice_nivel = niveles_disponibles.index(nivel_combo) + 1
        key = f"nivel_{indice_nivel}_texto"
    actual = st.session_state.get(key, "")
    st.session_state[key] = (actual.rstrip() + "\n" + texto_nuevo).strip() if actual.strip() else texto_nuevo
    st.success(f"Se añadió «{texto_nuevo}» a {nivel_combo}.")
    st.rerun()

# --- Generación de texto ---
st.header("5. Descripción generada")
exteriores = lineas(st.session_state.get("exteriores_texto", ""))
interiores = {}
for i, nivel in enumerate(niveles_a_mostrar, start=1):
    interiores[nivel] = lineas(st.session_state.get(f"nivel_{i}_texto", ""))
if st.session_state.get("nivel_6_texto", "").strip():
    interiores["Soterrado"] = lineas(st.session_state["nivel_6_texto"])

tipo = st.session_state.get("tipo_proyecto", "vivienda")
cantidad_niveles = st.session_state.get("cantidad_niveles", 1)
encabezado = st.session_state.get("encabezado_personalizado", "")
descripcion = construir_descripcion(
    tipo, cantidad_niveles, exteriores, interiores, encabezado,
    st.session_state.get("titulo_exteriores", "EXTERIORES"),
    st.session_state.get("frase_edificacion", "")
)

st.text_area("Texto final editable", value=descripcion, height=420, key="texto_final_editable")
st.download_button(
    "Descargar descripción en TXT",
    data=st.session_state.get("texto_final_editable", descripcion),
    file_name="descripcion_proyecto.txt",
    mime="text/plain",
    use_container_width=True,
)
st.caption(
    "Nota: las cantidades de combinaciones especiales se muestran como «n × frase» para evitar "
    "alterar términos técnicos o cambiar accidentalmente el sentido de la descripción. "
    "Revisa el texto final antes de incorporarlo a un documento oficial."
)
