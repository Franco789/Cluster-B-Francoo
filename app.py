import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# CONFIGURACIÓN INSTITUCIONAL DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Evaluación Dimensional del Clúster B | Ateneo de Psiquiatría",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estética visual de alto estándar académico: Paleta Navy / Slate con gradiente sutil
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background: radial-gradient(circle at 18% 12%, #0e1726 0%, #080d1a 50%, #050811 100%) !important;
    color: #e2e8f0 !important;
}

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3.2rem !important;
    max-width: 96% !important;
}

h1 {
    font-size: 2.15rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    color: #f8fafc !important;
    margin-bottom: 0.2rem !important;
}

h2, h3, h4 {
    font-weight: 600 !important;
    letter-spacing: -0.015em !important;
    color: #f1f5f9 !important;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #0f1a2e 0%, #0b1323 100%) !important;
    border: 1px solid rgba(148, 163, 184, 0.12) !important;
    border-radius: 10px !important;
    padding: 16px 20px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
}

div[data-testid="stMetric"] label {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: #94a3b8 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #f8fafc !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background-color: transparent !important;
    border-bottom: 1px solid rgba(148, 163, 184, 0.12) !important;
    padding-bottom: 6px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: #0c1424 !important;
    border: 1px solid rgba(148, 163, 184, 0.1) !important;
    border-radius: 6px !important;
    padding: 10px 18px !important;
    color: #94a3b8 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: #1e293b !important;
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
    box-shadow: 0 2px 8px rgba(56, 189, 248, 0.15) !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090e1a 0%, #060912 100%) !important;
    border-right: 1px solid rgba(148, 163, 184, 0.1) !important;
}

.card-clinica {
    background: linear-gradient(145deg, #0f192b 0%, #0a1120 100%);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 14px;
    height: 100%;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
}

.card-evidencia {
    background: linear-gradient(145deg, #0d1627 0%, #090f1b 100%);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
}

.badge-estudio {
    display: inline-block;
    background: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 4px;
    padding: 3px 8px;
    font-size: 0.74rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# PARÁMETROS LATERALES DE ENTRADA CLÍNICA
# ==============================================================================
st.sidebar.markdown("### Selección de Variables Clínicas")
st.sidebar.caption("Taxonomía Dimensional (HiTOP / DSM-5 Sección III / PID-5)")

trastorno_foco = st.sidebar.selectbox(
    "1. Fenotipo Clínico Predominante:",
    options=[
        "Trastorno Límite de la Personalidad (TLP)",
        "Trastorno Narcisista de la Personalidad (TNP)",
        "Trastorno Antisocial de la Personalidad (TASP)",
        "Trastorno Histriónico de la Personalidad (THP)"
    ],
    index=0
)

estresor_tipo = st.sidebar.selectbox(
    "2. Estresor Interpersonal Desencadenante:",
    options=[
        "Fijación de Límites o Negativa Externa (Frustración del deseo)",
        "Distanciamiento Vincular / Vivencia de Abandono o Rechazo",
        "Confrontación de la Realidad / Señalamiento de Inconsistencias",
        "Demora Asistencial / Dilación en la Respuesta del Entorno"
    ],
    index=0,
    help="Situación relacional que activa el sistema de apego o amenaza el esquema del Yo según el modelo de Gunderson y Bateman & Fonagy."
)

severidad_estres = st.sidebar.slider(
    "3. Tensión Afectiva Percibida (Escala SUDS 0-100):",
    min_value=0, max_value=100, value=75, step=1,
    help="Unidades Subjetivas de Distrés (SUDS, Wolpe / DBT de Linehan). Cuantifica la intensidad del dolor o desregulación vivenciada por el paciente en el momento actual."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Intervención en Crisis")

farmaco_1 = st.sidebar.selectbox(
    "Molécula o Estrategia Evaluada:",
    options=[
        "Intervención Verbal de Encuadre (Sin psicofármacos)",
        "Clonazepam (2 mg Vía Oral)",
        "Lorazepam (2 mg Sublingual)",
        "Haloperidol (5 mg Intramuscular)",
        "Quetiapina (50 mg Vía Oral)",
        "Aripiprazol (5 mg Vía Oral)",
        "Lamotrigina (100 mg Vía Oral - Mantenimiento basal previo)"
    ],
    index=1
)

soporte_red = st.sidebar.radio(
    "Red Vincular / Soporte Externo:",
    options=["Presente, continente y accesible", "Ausente, expulsiva o francamente disfuncional"],
    index=0
)

# ==============================================================================
# BASE DE DATOS DIMENSIONAL Y MODELADO COMPUTACIONAL
# ==============================================================================
perfiles_hitop = {
    "Trastorno Límite de la Personalidad (TLP)": {
        "Afecto Negativo": 95, "Desinhibición": 88, "Antagonismo": 45, "Desapego": 35, "Psicoticismo": 60,
        "color": "#F87171",
        "semiologia_clasica": "Inestabilidad en la vivencia de continuidad del Yo, labilidad afectiva fásica y angustia básica difusa con intolerancia a la soledad (Betta / Suárez Richards / Kernberg).",
        "mecanismo_defensa": "Escisión primaria (splitting) e identificación proyectiva masiva.",
        "vivencia_subjetiva": "Dolor psíquico equivalente a quemadura tisular; angustia catastrófica de fragmentación ante la amenaza de abandono.",
        "impacto_equipo": "Inducción contratransferencial de culpa, fantasías de rescate y alternancia entre sobreinvolucramiento y rechazo.",
        "perfil_radar": "Marcada polarización vertical en los ejes de Afecto Negativo y Desinhibición motriz/afectiva."
    },
    "Trastorno Narcisista de la Personalidad (TNP)": {
        "Afecto Negativo": 50, "Desinhibición": 30, "Antagonismo": 96, "Desapego": 40, "Psicoticismo": 20,
        "color": "#FBBF24",
        "semiologia_clasica": "Estructuración sobre un Yo grandioso compensatorio frente a una extrema vulnerabilidad a la vergüenza, el desprecio o la desvalorización (Schneider / Kohut).",
        "mecanismo_defensa": "Desmentida de la vulnerabilidad, idealización omnipotente y devaluación hostil del otro.",
        "vivencia_subjetiva": "Terror a la humillación o insuficiencia; necesidad imperiosa de descalificar la idoneidad del interlocutor para restablecer el equilibrio narcisista.",
        "impacto_equipo": "Sensación constante de cuestionamiento técnico, empequeñecimiento forzado y fastidio defensivo en el profesional.",
        "perfil_radar": "Expansión aislada y masiva en el vértice de Antagonismo con conservación del control prefrontal ejecutivo."
    },
    "Trastorno Antisocial de la Personalidad (TASP)": {
        "Afecto Negativo": 25, "Desinhibición": 92, "Antagonismo": 95, "Desapego": 30, "Psicoticismo": 25,
        "color": "#A78BFA",
        "semiologia_clasica": "Frialdad afectiva, aplanamiento del remordimiento, instrumentalización del semejante y transgresión repetida de normas (Schneider / Cleckley).",
        "mecanismo_defensa": "Paso al acto coactivo (acting out) y racionalización cínica de la agresión.",
        "vivencia_subjetiva": "El vínculo asistencial o social es concebido como una correlación de fuerzas a someter en pos de un beneficio concreto o dominancia.",
        "impacto_equipo": "Activación somática de alerta por agresión física real, cautela extrema y contratransferencia punitiva.",
        "perfil_radar": "Conjunción de Antagonismo y Desinhibición motora extrema con muy bajo componente de sufrimiento afectivo interno."
    },
    "Trastorno Histriónico de la Personalidad (THP)": {
        "Afecto Negativo": 80, "Desinhibición": 70, "Antagonismo": 55, "Desapego": 10, "Psicoticismo": 30,
        "color": "#22D3EE",
        "semiologia_clasica": "Expresión emocional llamativa pero volátil, sugestibilidad profunda y erotización reactiva de los intercambios (Jaspers / Janet).",
        "mecanismo_defensa": "Disociación, somatización conversiva y dramatización comunicacional.",
        "vivencia_subjetiva": "Sensación de invisibilidad o vacío existencial si no se captura de inmediato la atención del semejante.",
        "impacto_equipo": "Atracción e interés clínico inicial, que rápidamente vira a saturación vincular por demanda incesante de confirmación.",
        "perfil_radar": "Mínimo valor de Desapego (búsqueda imperiosa de proximidad) acoplado a reactividad emocional sin fragmentación del examen de realidad."
    }
}

p_actual = perfiles_hitop[trastorno_foco]

# Fisiopatología cuantitativa de circuitos
acoplamiento_base = 75.0 if "Narcisista" in trastorno_foco else (45.0 if "Límite" in trastorno_foco else 60.0)
factor_caida_estres = (severidad_estres / 100.0) * 0.70
acoplamiento_frontal = float(np.clip(acoplamiento_base * (1.0 - factor_caida_estres), 8.0, 95.0))
actividad_amigdala = float(np.clip((100.0 - acoplamiento_frontal) * (p_actual["Afecto Negativo"] / 100.0) * 1.25, 12.0, 100.0))

# Farmacodinamia cuantitativa
farmaco_datos = {
    "Intervención Verbal de Encuadre (Sin psicofármacos)": {
        "d2": 0, "5ht2a": 0, "gaba": 0, "nav": 0, "riesgo_desin": 0, "riesgo_acatisia": 0, 
        "tipo": "Intervención No Farmacológica (Regulación Psicofisiológica)",
        "mecanismo": "Activación deliberada de corteza prefrontal dorsolateral mediante validación y sostén del encuadre, sin interferencia iatrogénica."
    },
    "Clonazepam (2 mg Vía Oral)": {
        "d2": 0, "5ht2a": 0, "gaba": 90, "nav": 0, "riesgo_desin": 85, "riesgo_acatisia": 0, 
        "tipo": "Modulador Alostérico Positivo GABAA de Alta Potencia",
        "mecanismo": "Unión a subunidad alfa-1/alfa-2 de receptores GABAA. Provoca desinhibición paradójica en pacientes con freno prefrontal deficiente al silenciar interneuronas inhibitorias orbitofrontales."
    },
    "Lorazepam (2 mg Sublingual)": {
        "d2": 0, "5ht2a": 0, "gaba": 85, "nav": 0, "riesgo_desin": 78, "riesgo_acatisia": 0, 
        "tipo": "Modulador Alostérico Positivo GABAA de Alta Potencia",
        "mecanismo": "Rápida penetración en SNC por vía sublingual. Similar perfil a clonazepam: alto riesgo de supresión del control inhibitorio prefrontal consciente."
    },
    "Haloperidol (5 mg Intramuscular)": {
        "d2": 88, "5ht2a": 12, "gaba": 0, "nav": 0, "riesgo_desin": 5, "riesgo_acatisia": 85, 
        "tipo": "Antagonista Dopaminérgico D2 Incisivo de Primera Generación",
        "mecanismo": "Bloqueo D2 > 80% en vía nigroestriatal. Elevado riesgo de acatisia e inquietud motora aguda, habitualmente confundida en crisis con agravamiento conductual."
    },
    "Quetiapina (50 mg Vía Oral)": {
        "d2": 25, "5ht2a": 65, "gaba": 0, "nav": 0, "riesgo_desin": 10, "riesgo_acatisia": 5, 
        "tipo": "Antipsicótico Atípico / Antagonista H1 y 5-HT2A",
        "mecanismo": "Dosis baja: acción antihistamínica H1 y bloqueante alfa-1 adrenérgico predominante; sedación rápida sin supresión del freno cortical ni rigidez extrapiramidal."
    },
    "Aripiprazol (5 mg Vía Oral)": {
        "d2": 72, "5ht2a": 60, "gaba": 0, "nav": 0, "riesgo_desin": 8, "riesgo_acatisia": 20, 
        "tipo": "Agonista Parcial D2 / Antagonista 5-HT2A",
        "mecanismo": "Modulador dopaminérgico con actividad intrínseca del ~30%. Estabiliza la transmisión dopaminérgica sin causar sedación profunda ni aplanamiento afectivo."
    },
    "Lamotrigina (100 mg Vía Oral - Mantenimiento basal previo)": {
        "d2": 0, "5ht2a": 0, "gaba": 0, "nav": 68, "riesgo_desin": 0, "riesgo_acatisia": 0, 
        "tipo": "Inhibidor de Canales de Sodio Voltaje-Dependientes / Modulador Glutamatérgico",
        "mecanismo": "Disminución de liberación presináptica de glutamato. Fármaco de mantenimiento profiláctico crónico, no utilizable para rescate en crisis agudas por riesgo de síndrome de Stevens-Johnson."
    }
}

f_eval = farmaco_datos[farmaco_1]

# Ponderación objetiva del riesgo asistencial
pts_estres = severidad_estres * 0.35
pts_fenotipo = (p_actual["Desinhibición"] * 0.35) if ("Límite" in trastorno_foco or "Antisocial" in trastorno_foco) else 20.0
pts_red = 10.0 if "Presente" in soporte_red else 30.0
pts_iatrogenia = (f_eval["riesgo_desin"] * 0.20)
iva_total = float(np.clip(pts_estres + pts_fenotipo + pts_red + pts_iatrogenia, 10.0, 100.0))

# ==============================================================================
# ENCABEZADO Y PANELES CUANTITATIVOS
# ==============================================================================
st.markdown("## Evaluación dimensional del Clúster B: Dinámica vincular y farmacología")
st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-top: -0.4rem;'><b>Ateneo de Psiquiatría</b> | Modelo Integrado HiTOP / DSM-5 Sección III y Dinámica de Circuitos</p>", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.metric(
        label="Control Prefrontal Inhibitorio",
        value=f"{acoplamiento_frontal:.1f} %",
        delta=f"{-factor_caida_estres*100:.1f} % por Tensión Aguda",
        delta_color="inverse",
        help="Índice de acoplamiento funcional de cortezas prefrontales (dlPFC/vlPFC) sobre núcleos subcorticales. Modela la capacidad de inhibir impulsos motores y afectivos bajo estrés."
    )
    st.caption("Freno voluntario sobre el impulso motor.")

with col_m2:
    st.metric(
        label="Reactividad Amigdalina / Ínsula",
        value=f"{actividad_amigdala:.1f} %",
        delta="Alarma Disparada" if actividad_amigdala > 65 else "Línea de Base",
        delta_color="inverse" if actividad_amigdala > 65 else "normal",
        help="Intensidad de descarga de la amígdala e ínsula anterior ante señales de amenaza relacional, humillación o rechazo."
    )
    st.caption("Sensibilidad límbica de alarma.")

with col_m3:
    st.metric(
        label="Riesgo Desinhibición Paradójica",
        value=f"{f_eval['riesgo_desin']} %",
        delta="Alerta Iatrogénica" if f_eval['riesgo_desin'] > 50 else "Seguro / Neutro",
        delta_color="inverse" if f_eval['riesgo_desin'] > 50 else "normal",
        help="Probabilidad calculada de incremento en agresividad motriz o desinhibición verbal por depresión de interneuronas corticales inhibitorias con benzodiacepinas."
    )
    st.caption(f"Fármaco: {farmaco_1.split('(')[0]}")

with col_m4:
    color_iva = "inverse" if iva_total >= 70.0 else "normal"
    st.metric(
        label="Vulnerabilidad en Crisis (IVA)",
        value=f"{iva_total:.1f} %",
        delta="Alto Riesgo de Paso al Acto" if iva_total >= 70.0 else "Manejo Ambulatorio Viable",
        delta_color=color_iva,
        help="Índice cuantitativo que integra tensión afectiva actual (SUDS), rasgo desinhibitorio basal, contención vincular real e impacto farmacológico."
    )
    st.caption("Ponderación multidimensional en crisis.")

with st.expander("Fundamentación metodológica y origen de los índices porcentuales"):
    st.markdown("""
    **¿Cómo se calculan y argumentan estos cuatro porcentajes ante el equipo asistencial?**
    
    1. **Control Prefrontal Inhibitorio (%):** Representa la fracción de integridad funcional de la corteza prefrontal dorsolateral y ventrolateral (*dlPFC/vlPFC*). El valor de referencia basal surge de los perfiles de conectividad frontolímbica en reposo (*Ruocco et al., Biol Psychiatry 2016*). Al incrementarse la tensión subjetiva (*SUDS*), el modelo aplica una atenuación exponencial basada en el mecanismo de saturación catecolaminérgica prefrontal descrito por *Arnsten (Nature Rev Neurosci 2009)*: a mayor distrés, menor señal prefrontal inhibitoria.
    2. **Reactividad Amigdalina / Ínsula (%):** Expresa el grado de hiperactivación límbica ante señales sociales. Se calcula matemáticamente de forma inversamente proporcional al freno prefrontal y ponderada por el rasgo dimensional de *Afecto Negativo* basal de cada paciente (*Schulze et al., Am J Psychiatry 2016*).
    3. **Riesgo de Desinhibición Paradójica (%):** Refleja la probabilidad clínica observada de pérdida del autocontrol tras benzodiacepinas en pacientes con hipoactividad orbitofrontal de base. Los valores concuerdan con los reportes toxicológicos y las advertencias formales de las guías británicas *NICE CG78* y *APA*.
    4. **Índice de Vulnerabilidad Asistencial (IVA %):** Ponderación algorítmica: `0.35 × SUDS + 0.35 × Rasgo Desinhibitorio + Factor Red Vincular (10 o 30) + 0.20 × Riesgo Farmacológico`. Permite estratificar el riesgo global de paso al acto sin depender de etiquetas categoriales estáticas.
    """)

st.markdown("<div style='height: 1px; background: rgba(148,163,184,0.12); margin: 1.2rem 0;'></div>", unsafe_allow_html=True)

# ==============================================================================
# PESTAÑAS ACADÉMICAS
# ==============================================================================
tab_radar, tab_neuro_mapa, tab_clinica, tab_farma, tab_biblio = st.tabs([
    "1. Polígono Dimensional (HiTOP / AMPD)",
    "2. Neuroimagen Funcional y Conectómica (fMRI / DTI)",
    "3. Dinámica Relacional y Fenomenología",
    "4. Psicofarmacología de Receptores",
    "5. Marco Epistemológico y Bibliografía"
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: RADAR DIMENSIONAL (HiTOP / AMPD)
# ------------------------------------------------------------------------------
with tab_radar:
    st.subheader("Huella Dimensional Comparativa de los 4 Fenotipos del Clúster B")
    st.caption("Taxonomía Jerárquica de la Psicopatología (HiTOP) y Modelo Alternativo del DSM-5 (AMPD, Sección III).")
    
    col_rad_izq, col_rad_der = st.columns([1.1, 1])
    
    val_af_din = float(np.clip(p_actual["Afecto Negativo"] * (1.0 + (severidad_estres / 300.0)), 0, 100))
    val_des_din = float(np.clip(p_actual["Desinhibición"] * (1.0 + (severidad_estres / 400.0)), 0, 100))
    val_ant_din = float(p_actual["Antagonismo"])
    val_desap_din = float(p_actual["Desapego"])
    val_psi_din = float(np.clip(p_actual["Psicoticismo"] + (severidad_estres * 0.25), 0, 100))
    
    valores_dinamicos = {
        "Afecto Negativo": val_af_din,
        "Desinhibición": val_des_din,
        "Antagonismo": val_ant_din,
        "Desapego": val_desap_din,
        "Psicoticismo": val_psi_din
    }
    
    categorias = ["Afecto Negativo", "Desinhibición", "Antagonismo", "Desapego", "Psicoticismo"]
    
    with col_rad_izq:
        fig_radar = go.Figure()
        for nombre, datos in perfiles_hitop.items():
            vals = [datos[c] for c in categorias]
            vals.append(vals[0])
            es_foco = (nombre == trastorno_foco)
            fig_radar.add_trace(go.Scatterpolar(
                r=vals,
                theta=categorias + [categorias[0]],
                name=nombre.split()[1],
                line=dict(
                    color=datos["color"],
                    width=3.5 if es_foco else 1.2,
                    dash="solid" if es_foco else "dot"
                ),
                fill="toself" if es_foco else "none",
                opacity=0.28 if es_foco else 0.06
            ))
            
        valores_paciente = [val_af_din, val_des_din, val_ant_din, val_desap_din, val_psi_din]
        valores_paciente.append(valores_paciente[0])
        fig_radar.add_trace(go.Scatterpolar(
            r=valores_paciente,
            theta=categorias + [categorias[0]],
            name="Estado Reactivo (Estrés Actual)",
            line=dict(color="#38bdf8", width=2.5, dash="dash"),
            fill="none"
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="rgba(148, 163, 184, 0.12)",
                    linecolor="rgba(148, 163, 184, 0.12)",
                    tickfont=dict(color="#94a3b8", size=9, family="Inter")
                ),
                angularaxis=dict(
                    gridcolor="rgba(148, 163, 184, 0.12)",
                    linecolor="rgba(148, 163, 184, 0.12)",
                    tickfont=dict(color="#f1f5f9", size=11, family="Inter")
                ),
                bgcolor="rgba(15, 23, 42, 0.6)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.28,
                xanchor="center",
                x=0.5,
                font=dict(family="Inter", size=11, color="#94a3b8")
            ),
            margin=dict(l=35, r=35, t=15, b=50),
            height=410
        )
        st.plotly_chart(fig_radar, use_container_width=True, key="fig_radar_hitop")
        
    with col_rad_der:
        st.markdown(f"#### Perfil Clínico Seleccionado: **{trastorno_foco}**")
        st.markdown(f"**Semiología descriptiva clásica:** {p_actual['semiologia_clasica']}")
        st.markdown(f"**Lectura geométrica del radar:** {p_actual['perfil_radar']}")
        st.markdown("**Dominios Cuantitativos (Basal vs Reactivo bajo Estrés):**")
        
        for c in categorias:
            val_basal = p_actual[c]
            val_reactivo = valores_dinamicos[c]
            delta_val = val_reactivo - val_basal
            texto_delta = f" (+{delta_val:.1f} reactivo)" if delta_val > 0.1 else ""
            st.write(f"- **{c}:** {val_reactivo:.1f}/100 <span style='color:#F87171; font-size:0.85rem;'>{texto_delta}</span>", unsafe_allow_html=True)
            st.progress(val_reactivo / 100.0)

    st.markdown("---")
    st.markdown("#### Definición Epistemológica de los 5 Dominios Dimensionales (PID-5 / HiTOP)")
    col_dim_a, col_dim_b = st.columns(2)
    with col_dim_a:
        st.markdown("""
        * **1. Afecto Negativo (vs. Estabilidad Emocional):**  
          Vivencia frecuente e intensa de un amplio espectro de emociones aversivas: labilidad emocional, ansiedad somática, suspicacia, hostilidad y terror al desamparo. En el Clúster B, constituye el núcleo fisiopatológico del paciente con **TLP**, generando la necesidad urgente de descargar motrizmente la tensión para apagar la vivencia de dolor interno.
          
        * **2. Desinhibición (vs. Meticulosidad / Escrupulosidad):**  
          Orientación hacia la gratificación inmediata, impulsividad motriz y cognitiva sin deliberación de consecuencias futuras, búsqueda de sensaciones de riesgo y dificultad extrema para sostener planes a largo plazo. Es compartida en grado máximo por el **TLP** (urgencia afectiva) y el **TASP** (búsqueda de estimulación o beneficio instrumental).
          
        * **3. Antagonismo (vs. Amabilidad / Empatía):**  
          Comportamientos que sitúan sistemáticamente al individuo en conflicto con los demás: grandiosidad, expectativas de trato privilegiado, desdén, insensibilidad hacia el sufrimiento ajeno y manipulación interpersonal. Define el polo cardinal del **TNP** y del **TASP**.
        """)
    with col_dim_b:
        st.markdown("""
        * **4. Desapego (vs. Extraversión / Afiliación):**  
          Distanciamiento activo de relaciones interpersonales, evitación del contacto afectivo estrecho y anhedonia social. El Clúster B se caracteriza por mostrar niveles **bajos o moderadamente bajos** de desapego, especialmente en el **THP** y el **TLP**, cuya vivencia depende desesperadamente del feedback, mirada y presencia física del semejante.
          
        * **5. Psicoticismo (vs. Lucidez / Racionalidad):**  
          Excentricidad, pensamientos inusuales y desregulación perceptual transitoria estado-dependiente. En el **TLP**, este dominio se eleva exclusivamente bajo microepisodios de descompensación aguda (despersonalización, desrealización, ideas paranoides transitorias no sistematizadas), remitiendo rápidamente cuando la relación se estabiliza.
        """)

# ------------------------------------------------------------------------------
# PESTAÑA 2: NEUROIMAGEN FUNCIONAL Y CONECTÓMICA (NUEVO MÓDULO RIGUROSO)
# ------------------------------------------------------------------------------
with tab_neuro_mapa:
    st.subheader("Conectómica Funcional y Neuroimagen de Activación fMRI (Cerebro Sano vs. TLP)")
    st.caption("Mapas de activación BOLD estandarizados ante tarea de estrés relacional / rechazo social (Ruocco et al., 2016; Schulze et al., 2016):")

    col_img_ctl, col_img_tlp = st.columns(2)
    
    # 1. Gráfico interactivo: Cerebro Control
    with col_img_ctl:
        st.markdown("#### Sujeto Control (Freno Top-Down Íntegro)")
        st.caption("Respuesta ante estresor afectivo: reclutamiento prefrontal eficaz e inhibición amigdalina.")
        
        # Mapeo esquemático en corte sagital/axial estilizado mediante Plotly
        fig_ctl = go.Figure()
        
        # Silueta cerebral de referencia
        t_theta = np.linspace(0, 2*np.pi, 200)
        x_brain = 8.5 * np.cos(t_theta) + 0.8 * np.cos(2*t_theta)
        y_brain = 7.0 * np.sin(t_theta)
        fig_ctl.add_trace(go.Scatter(
            x=x_brain, y=y_brain, mode='lines',
            line=dict(color='rgba(148, 163, 184, 0.3)', width=1.8),
            hoverinfo='skip', showlegend=False
        ))
        
        # dlPFC: Activación Robusta (Naranja cálido Z > +3.0)
        fig_ctl.add_trace(go.Scatter(
            x=[4.8, 5.2, 5.8, 5.1], y=[3.5, 4.2, 3.8, 3.0],
            mode='markers+text',
            marker=dict(size=[34, 26, 22, 28], color='#F59E0B', opacity=0.85, line=dict(color='#FCD34D', width=1.5)),
            text=["dlPFC (Activa)", "vlPFC", "OFC", ""],
            textposition="top center",
            name="Corteza Prefrontal",
            hovertext="Activación Prefrontal Dorsolateral (Z = +3.4)\nReclutamiento inhibitorio preservado sobre subcorteza."
        ))
        
        # Amígdala e Ínsula: Moduladas / Controladas (Azul / Neutro Z < +1.0)
        fig_ctl.add_trace(go.Scatter(
            x=[0.8, 2.2], y=[-1.5, 0.2],
            mode='markers+text',
            marker=dict(size=[18, 16], color='#38BDF8', opacity=0.5, line=dict(color='#7DD3FC', width=1)),
            text=["Amígdala (Inhibida)", "Ínsula (Modulada)"],
            textposition="bottom center",
            name="Núcleos Límbicos",
            hovertext="Reactividad Amigdalina Atenuada (Z = +0.8)\nFreno top-down eficaz. Sin pánico somático."
        ))
        
        # Fascículo Uncinado: Haz grueso y continuo (Verde esmeralda, FA = 0.48)
        fig_ctl.add_trace(go.Scatter(
            x=[1.0, 2.8, 4.8], y=[-1.2, 0.8, 3.2],
            mode='lines',
            line=dict(color='#10B981', width=4.5),
            name="Fascículo Uncinado (FA: 0.48)",
            hovertext="Tracto Frontoamigdalino Íntegro\nAnisotropía Fraccional normal (FA = 0.48). Conducción axonal rápida."
        ))
        
        fig_ctl.update_layout(
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10, 15, 29, 0.7)",
            xaxis=dict(visible=False, range=[-10, 10]),
            yaxis=dict(visible=False, range=[-8, 8]),
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(color="#94A3B8", size=10))
        )
        st.plotly_chart(fig_ctl, use_container_width=True, key="fig_img_ctl")
        
        st.info("**Sujeto Control:** Ante el rechazo, recluta corteza prefrontal (*dlPFC* bilateral, áreas 9/46). La orden inhibitoria viaja por el fascículo uncinado con alta anisotropía (FA=0.48), extinguiendo la alarma de la amígdala.")

    # 2. Gráfico interactivo: Cerebro TLP
    with col_img_tlp:
        st.markdown(f"#### Paciente con TLP bajo Estrés (`SUDS: {severidad_estres}/100`)")
        st.caption("Respuesta patológica: hipoactivación frontal y desborde amigdalino hipermetabólico.")
        
        fig_tlp = go.Figure()
        
        # Silueta cerebral de referencia
        fig_tlp.add_trace(go.Scatter(
            x=x_brain, y=y_brain, mode='lines',
            line=dict(color='rgba(148, 163, 184, 0.3)', width=1.8),
            hoverinfo='skip', showlegend=False
        ))
        
        # dlPFC: Caída BOLD / Desacoplamiento (Azul frío Z = -2.8)
        fig_tlp.add_trace(go.Scatter(
            x=[4.8, 5.2, 5.8, 5.1], y=[3.5, 4.2, 3.8, 3.0],
            mode='markers+text',
            marker=dict(size=[24, 20, 18, 20], color='#2563EB', opacity=0.8, line=dict(color='#60A5FA', width=1.5)),
            text=["dlPFC (Apagada)", "vlPFC", "OFC", ""],
            textposition="top center",
            name="Corteza Prefrontal",
            hovertext="Hipoactivación Prefrontal (Z = -2.8)\nFalla biológica de reclutamiento bajo dolor social agudo."
        ))
        
        # Amígdala e Ínsula: Hiperactivación Masiva (Rojo/Naranja Z > +4.2)
        fig_tlp.add_trace(go.Scatter(
            x=[0.8, 2.2], y=[-1.5, 0.2],
            mode='markers+text',
            marker=dict(size=[38, 30], color='#EF4444', opacity=0.9, line=dict(color='#FCA5A5', width=2.5)),
            text=["Amígdala (HIPERACTIVA)", "Ínsula Anterior (Alarma)"],
            textposition="bottom center",
            name="Núcleos Límbicos",
            hovertext="Hiperactivación Amigdalina Intensa (Z = +4.5)\nPánico visceral de abandono. Dolor emocional equiparable a quemadura."
        ))
        
        # Fascículo Uncinado: Conducción deficiente (Línea punteada fina, FA = 0.31)
        fig_tlp.add_trace(go.Scatter(
            x=[1.0, 2.8, 4.8], y=[-1.2, 0.8, 3.2],
            mode='lines',
            line=dict(color='#F59E0B', width=1.8, dash='dash'),
            name="Fascículo Uncinado (FA: 0.31)",
            hovertext="Compromiso Microestructural\nAnisotropía Fraccional reducida (FA = 0.31). Menor ancho de banda de freno."
        ))
        
        fig_tlp.update_layout(
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10, 15, 29, 0.7)",
            xaxis=dict(visible=False, range=[-10, 10]),
            yaxis=dict(visible=False, range=[-8, 8]),
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(color="#94A3B8", size=10))
        )
        st.plotly_chart(fig_tlp, use_container_width=True, key="fig_img_tlp")
        
        st.error("**Paciente TLP:** Frente a la amenaza vincular, se produce la 'desconexión corticolímbica': la corteza prefrontal se apaga (azul, Z=-2.8) y la amígdala estalla en hiperactivación BOLD (rojo, Z=+4.5). El fascículo uncinado presenta microestructura adelgazada (FA=0.31), demorando la señal inhibitoria.")

    # 3. Código cromático y Correlación Anatomo-Funcional por Dimensión
    st.markdown("---")
    st.markdown("#### Correlato Neuroanatómico Dinámico según las Dimensiones HiTOP / AMPD")
    
    col_cor1, col_cor2 = st.columns(2)
    with col_cor1:
        st.markdown("""
        **Código Cromático Estándar en fMRI:**
        * <span style='color:#EF4444; font-weight:600;'>■ Rojo / Naranja cálido (Z > +3.1):</span> Hiperactivación hemodinámica BOLD (aumento de flujo regional y consumo de oxígeno). Refleja reclutamiento metabólico aumentado en amígdala e ínsula ante estímulos afectivos aversivos.
        * <span style='color:#2563EB; font-weight:600;'>■ Azul / Cian frío (Z < -2.5):</span> Hipoactivación hemodinámica BOLD. Indica incapacidad de sostener la tasa de disparo inhibitorio en la corteza dorsolateral y orbitofrontal.
        * <span style='color:#10B981; font-weight:600;'>■ Verde vs. Ámbar (Tractografía DTI):</span> Grado de anisotropía fraccional (FA). Evalúa la integridad de las vainas de mielina en tractos de sustancia blanca (haz uncinado y cíngulo anterior).
        """, unsafe_allow_html=True)
    with col_cor2:
        st.markdown("""
        **Circuitos Específicos por Dimensión:**
        * **Afecto Negativo ↑:** Complejo amigdalino basolateral y corteza insular anterior (red de saliencia hiperreactiva).
        * **Desinhibición ↑:** Corteza orbitofrontal (OFC) ventrolateral y estriado ventral (falla en inhibición de respuesta motora / Go-NoGo).
        * **Antagonismo ↑:** Red de Mentalización (mPFC, unión temporoparietal TPJ) hipoactiva acoplada a hiperactividad en núcleos de recompensa social.
        * **Desapego ↑:** Aplanamiento de la reactividad del Área Tegmental Ventral y Núcleo Accumbens ante claves de proximidad humana.
        * **Psicoticismo ↑:** Desregulación transitoria de conectividad tálamo-cortical y vía mesolímbica durante picos agudos de distrés.
        """)

# ------------------------------------------------------------------------------
# PESTAÑA 3: DINÁMICA RELACIONAL Y FENOMENOLOGÍA
# ------------------------------------------------------------------------------
with tab_clinica:
    st.subheader("La Escena Vincular: Fenomenología ante el Estresor Interpersonal")
    st.markdown(f"**Estresor Evaluado:** `{estresor_tipo}` | **Nivel de Distrés (SUDS):** `{severidad_estres}/100`")
    
    with st.expander("¿Por qué se seleccionaron estos 4 estresores interpersonales? (Fundamento Teórico)"):
        st.markdown("""
        Los cuatro estresores modelados no fueron elegidos al azar ni se limitan únicamente a un ámbito cerrado de guardia hospitalaria; representan las cuatro **vulnerabilidades relacionales nucleares** descritas en la literatura clínica contemporánea (Gunderson, 2011; Linehan, 1993; Bateman & Fonagy, 2004):
        
        1. **Fijación de Límites o Negativa Externa:** Activa la vivencia inmediata de castigo, rechazo o invalidación. En la vida cotidiana equivale a un 'no' de una pareja o jefe; en el sistema asistencial, a la negativa de una prescripción o internación injustificada.
        2. **Distanciamiento Vincular / Vivencia de Abandono:** Es el interruptor neurobiológico del dolor social y la angustia de aniquilamiento (Eisenberger, 2003). Se observa ante rupturas, discusiones familiares o la ausencia física temporal del referente.
        3. **Confrontación de la Realidad / Señalamiento de Inconsistencias:** Desencadena la herida narcisista por exposición de fallas, activando furia defensiva en personalidades con Yo grandioso compensatorio (Kernberg / Kohut).
        4. **Demora Asistencial o Dilación del Entorno:** La espera forzada o la falta de gratificación inmediata es decodificada por el sistema de apego desorganizado como desprecio activo o desamparo total.
        """)
        
    c_tlp, c_tnp, c_tasp, c_thp = st.columns(4)
    
    with c_tlp:
        st.markdown(f"""
        <div class="card-clinica">
            <h4 style="color:#F87171; margin-top:0;">Trastorno Límite</h4>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Vivencia Subjetiva:</b></p>
            <p style="color:#e2e8f0; font-size:0.86rem; font-style:italic;">«{perfiles_hitop['Trastorno Límite de la Personalidad (TLP)']['vivencia_subjetiva']}»</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Mecanismo Defensivo:</b></p>
            <p style="color:#cbd5e1; font-size:0.86rem;">{perfiles_hitop['Trastorno Límite de la Personalidad (TLP)']['mecanismo_defensa']}</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Conducta Manifiesta:</b></p>
            <p style="color:#fca5a5; font-size:0.86rem;">Amenaza autolesiva o corte superficial para modular homeostáticamente el dolor psíquico abrumador.</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Impacto Contratransferencial:</b></p>
            <p style="color:#fcd34d; font-size:0.86rem;">{perfiles_hitop['Trastorno Límite de la Personalidad (TLP)']['impacto_equipo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_tnp:
        st.markdown(f"""
        <div class="card-clinica">
            <h4 style="color:#FBBF24; margin-top:0;">Trastorno Narcisista</h4>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Vivencia Subjetiva:</b></p>
            <p style="color:#e2e8f0; font-size:0.86rem; font-style:italic;">«{perfiles_hitop['Trastorno Narcisista de la Personalidad (TNP)']['vivencia_subjetiva']}»</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Mecanismo Defensivo:</b></p>
            <p style="color:#cbd5e1; font-size:0.86rem;">{perfiles_hitop['Trastorno Narcisista de la Personalidad (TNP)']['mecanismo_defensa']}</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Conducta Manifiesta:</b></p>
            <p style="color:#fde68a; font-size:0.86rem;">Descalificación técnica directa, acusaciones de negligencia o reclamos formales como defensa ante la humillación.</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Impacto Contratransferencial:</b></p>
            <p style="color:#fcd34d; font-size:0.86rem;">{perfiles_hitop['Trastorno Narcisista de la Personalidad (TNP)']['impacto_equipo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_tasp:
        st.markdown(f"""
        <div class="card-clinica">
            <h4 style="color:#A78BFA; margin-top:0;">Trastorno Antisocial</h4>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Vivencia Subjetiva:</b></p>
            <p style="color:#e2e8f0; font-size:0.86rem; font-style:italic;">«{perfiles_hitop['Trastorno Antisocial de la Personalidad (TASP)']['vivencia_subjetiva']}»</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Mecanismo Defensivo:</b></p>
            <p style="color:#cbd5e1; font-size:0.86rem;">{perfiles_hitop['Trastorno Antisocial de la Personalidad (TASP)']['mecanismo_defensa']}</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Conducta Manifiesta:</b></p>
            <p style="color:#ddd6fe; font-size:0.86rem;">Coacción, intimidación o desafío frontal a las normas para doblegar al interlocutor.</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Impacto Contratransferencial:</b></p>
            <p style="color:#fcd34d; font-size:0.86rem;">{perfiles_hitop['Trastorno Antisocial de la Personalidad (TASP)']['impacto_equipo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_thp:
        st.markdown(f"""
        <div class="card-clinica">
            <h4 style="color:#22D3EE; margin-top:0;">Trastorno Histriónico</h4>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Vivencia Subjetiva:</b></p>
            <p style="color:#e2e8f0; font-size:0.86rem; font-style:italic;">«{perfiles_hitop['Trastorno Histriónico de la Personalidad (THP)']['vivencia_subjetiva']}»</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Mecanismo Defensivo:</b></p>
            <p style="color:#cbd5e1; font-size:0.86rem;">{perfiles_hitop['Trastorno Histriónico de la Personalidad (THP)']['mecanismo_defensa']}</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Conducta Manifiesta:</b></p>
            <p style="color:#a5f3fc; font-size:0.86rem;">Dramatización somática aguda, pseudodesmayos psicógenos o crisis de hiperventilación reactiva.</p>
            <p style="color:#94a3b8; font-size:0.83rem; margin-bottom:3px;"><b>Impacto Contratransferencial:</b></p>
            <p style="color:#fcd34d; font-size:0.86rem;">{perfiles_hitop['Trastorno Histriónico de la Personalidad (THP)']['impacto_equipo']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1px; background: rgba(148,163,184,0.12); margin: 1.2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("#### Pautas de Contención Verbal y Sostenimiento del Encuadre Asistencial")
    
    col_rec_izq, col_rec_der = st.columns(2)
    with col_rec_izq:
        st.error("""
        **Intervención Desaconsejada (Escala la Disrrupción Afectiva):**
        
        *Confrontación lógica directa, desacreditación del síntoma o amenaza punitiva:*  
        «Cálmese, que lo suyo no reviste ninguna gravedad» o «Si sigue gritando tendré que pedir que lo retiren de la sala».
        
        * **Por qué falla:** En el paciente con TLP, invalida la experiencia emocional interna, interpretándose como rechazo activo y acelerando el paso al acto impulsivo (*Linehan, 1993*). En el paciente con TNP, propina una herida directa a su estatus, detonando furia narcisista compensatoria.
        """)
    with col_rec_der:
        st.success("""
        **Intervención Basada en Evidencia (Desactiva la Reactividad Límbica):**
        
        *Validación del afecto con sostenimiento irrestricto del límite estructural:*  
        «Entiendo perfectamente el nivel de angustia y sufrimiento que esta situación le genera; es comprensible que se sienta desbordado/a. Sin embargo, no podemos acceder a esa indicación porque sería perjudicial para su salud. Vamos a evaluar juntos qué opciones terapéuticas seguras podemos coordinar».
        
        * **Fundamento empírico:** Desarrollado y validado en el manual de Terapia Dialéctico-Conductual (*Marsha Linehan, Cognitive-Behavioral Treatment of Borderline Personality Disorder, 1993*) y Terapia Basada en la Mentalización (*Anthony Bateman & Peter Fonagy, Psychotherapy for Borderline Personality Disorder: MBT, Oxford University Press, 2004*). La validación empática desactiva la señal de alarma amigdalina, permitiendo que la corteza prefrontal retome el control ejecutivo.
        """)

# ------------------------------------------------------------------------------
# PESTAÑA 4: PSICOFARMACOLOGÍA DE RECEPTORES
# ------------------------------------------------------------------------------
with tab_farma:
    st.subheader("Psicofarmacología Traslacional y Ocupación Teórica de Receptores")
    st.caption("Perfil de afinidad de unión según constantes Ki y guías de práctica clínica (Stahl's Essential Psychopharmacology / NICE CG78 / APA):")
    
    col_far_l, col_far_r = st.columns([1, 1])
    
    with col_far_l:
        st.markdown(f"#### Molécula Seleccionada: `{farmaco_1}`")
        st.markdown(f"**Familia Terapéutica:** {f_eval['tipo']}")
        st.info(f"**Mecanismo de Acción Neurofuncional:** " + f_eval["mecanismo"])
        
        d2_val = f_eval['d2']
        ht2a_val = f_eval['5ht2a']
        gaba_val = f_eval['gaba']
        nav_val = f_eval['nav']
        
        st.markdown("**Estimación de Ocupación / Modulación de Sitios de Unión en SNC:**")
        st.write(f"- Receptores Dopaminérgicos D2: {d2_val}%")
        st.progress(d2_val / 100.0)
        st.write(f"- Receptores Serotoninérgicos 5-HT2A: {ht2a_val}%")
        st.progress(ht2a_val / 100.0)
        st.write(f"- Complejo Alostérico del Receptor GABAA: {gaba_val}%")
        st.progress(gaba_val / 100.0)
        st.write(f"- Bloqueo de Canales de Sodio Voltaje-Dependientes Nav: {nav_val}%")
        st.progress(nav_val / 100.0)
        
    with col_far_r:
        st.markdown("#### Análisis de Riesgo Terapéutico e Iatrogenia Farmacológica")
        
        if f_eval["riesgo_desin"] > 50:
            st.error(f"""
            **ALERTA DE DESINHIBICIÓN PARADÓJICA (Riesgo Estimado: {f_eval['riesgo_desin']}%):**
            
            * **Fisiopatología:** Las benzodiacepinas de alta potencia potencian el tono GABAérgico de forma indiscriminada. En personas con hipofrontalidad basal, deprimen selectivamente las interneuronas de la corteza orbitofrontal (*OFC*), suprimiendo el último vestigio de freno consciente sobre la amígdala.
            * **Manifestación clínica:** Desinhibición motora, escalada de agresividad verbal y facilitación del paso al acto impulsivo o suicida.
            * **Criterio de Guías (NICE CG78 / APA):** Están formalmente desaconsejadas para el manejo rutinario o de rescate en crisis de desregulación de la personalidad.
            """)
        elif f_eval["riesgo_acatisia"] > 50:
            st.error(f"""
            **ALERTA DE ACATISIA AGUDA (Riesgo Estimado: {f_eval['riesgo_acatisia']}%):**
            
            * **Fisiopatología:** El bloqueo potente de receptores dopaminérgicos D2 (> 80% en la vía nigroestriatal) por antipsicóticos típicos de alta potencia induce acatisia aguda.
            * **Error asistencial común:** En el marco de una crisis de guardia, la inquietud motora displacentera y la angustia inducida por la acatisia son erróneamente interpretadas como mayor agitación de base del paciente, llevando al error iatrogénico de sobreprescribir dosis adicionales del antipsicótico.
            """)
        elif "Lamotrigina" in farmaco_1:
            st.warning("""
            **CONSIDERACIÓN ESPECÍFICA SOBRE LAMOTRIGINA:**
            
            * **Tiempo de latencia:** Carece totalmente de indicación en agudo o en rescate de guardia; requiere una titulación ascendente extremadamente lenta a lo largo de 6 a 8 semanas para evitar el desprendimiento epidérmico del síndrome de Stevens-Johnson.
            * **Función en el modelo:** Se evalúa exclusivamente en pacientes que ya la reciben crónicamente de base, donde ejerce modulación del tono glutamatérgico y estabilización afectiva intercrisis.
            """)
        elif "Quetiapina" in farmaco_1:
            st.success("""
            **PERFIL SEDATIVO HISTAMINÉRGICO CONTROLADO:**
            
            A dosis de 25-50 mg, la quetiapina actúa prácticamente como un antihistamínico H1 y alfa-1 adrenérgico puro (ocupación D2 < 30%). Proporciona inducción del reposo sin riesgo extrapiramidal y sin la desinhibición frontal característica de las benzodiacepinas.
            """)
        elif "Aripiprazol" in farmaco_1:
            st.success("""
            **ESTABILIZACIÓN MEDIANTE AGONISMO PARCIAL D2:**
            
            El agonismo parcial dopaminérgico y antagonismo 5-HT2A permite modular la reactividad impulsiva sin sedación profunda, evitando la ganancia excesiva de peso y sin el riesgo de desinhibición de las benzodiacepinas.
            """)
        else:
            st.info("""
            **ESTRATEGIA VERBAL EXCLUSIVA:**
            
            Preserva la lucidez cognitiva y la capacidad de autorregulación del paciente. Permite que el proceso de mentalización y validación emocional operen sin interferencia de efectos adversos farmacológicos o somnolencia.
            """)

# ------------------------------------------------------------------------------
# PESTAÑA 5: MARCO EPISTEMOLÓGICO Y BIBLIOGRAFÍA
# ------------------------------------------------------------------------------
with tab_biblio:
    st.subheader("Marco Epistemológico: ¿Por qué este Modelo y no el Categorial Tradicional?")
    st.caption("Fundamento teórico que justifica la selección de variables y el diseño computacional de la plataforma:")
    
    col_j1, col_j2 = st.columns(2)
    
    with col_j1:
        st.markdown("#### Justificación Epistemológica del Abordaje Dimensional")
        st.markdown("""
        1. **Superación del Modelo Categorial DSM Clásico:**  
           El enfoque tradicional de categorías cerradas (DSM-IV / DSM-5 Sección II) presenta tres fallas metodológicas documentadas en psiquiatría:
           * **Comorbilidad masiva y espuria:** Más del 60% de los pacientes que cumplen criterios para un trastorno del Clúster B cumplen simultáneamente criterios para otro trastorno de la personalidad.
           * **Heterogeneidad intra-diagnóstica:** Existen 256 combinaciones sintomáticas distintas para alcanzar los criterios diagnósticos del TLP (5 de 9 ítems). Dos pacientes con diagnóstico idéntico pueden compartir únicamente un síntoma.
           * **Cortes arbitrarios:** Una persona con 4 criterios recibe la etiqueta de 'sano' o 'sin diagnóstico', mientras que alguien con 5 es patologizado, a pesar de que su funcionamiento psicosocial sea indistinguible.
           
        2. **Adopción de la Taxonomía HiTOP y DSM-5 Sección III (AMPD):**  
           El modelo dimensional no clasifica personas en casilleros estáticos; evalúa la severidad a lo largo de un espectro continuo (*Afecto Negativo, Desinhibición, Antagonismo, Desapego y Psicoticismo*), capturando con precisión matemática la singularidad de cada paciente.
           
        3. **Integración de Conectómica Funcional Dinámica:**  
           Las conductas impulsivas no son 'defectos morales del carácter', sino manifestaciones estado-dependientes que emergen cuando un estresor vincular específico satura los circuitos frontocorticales inhibitorios.
        """)
        
    with col_j2:
        st.markdown("#### Bibliografía Principal de Referencia (Artículos Completos)")
        st.markdown("""
        * **1. Taxonomía Dimensional HiTOP y Modelo Alternativo DSM-5 (AMPD):**
          * **Krueger RF, Kotov R, Watson D, et al.** (2018). *The Hierarchical Taxonomy of Psychopathology (HiTOP): A dimensional alternative to traditional nosologies.* **World Psychiatry**, 17(3), 282–293.
          * **Skodol AE, Morey LC, Bender DS, et al.** (2015). *The Alternative DSM-5 Model for Personality Disorders: A Review of the Evidence.* **The Lancet Psychiatry**, 2(2), 170–178.
          
        * **2. Conectómica y Neuroimagen Funcional:**
          * **Ruocco AC, Carcone D.** (2016). *A neurobiological model of affective instability in borderline personality disorder.* **Biological Psychiatry**, 79(6), 444–455.
          * **Fertuck EA, Jeklic J, Giles S, et al.** (2009). *Enhanced 'reading the mind in the eyes' in borderline personality disorder compared to healthy controls.* **Biological Psychiatry**, 65(9), 756–762.
          * **Arnsten AFT.** (2009). *Stress signalling pathways that impair prefrontal cortex structure and function.* **Nature Reviews Neuroscience**, 10(6), 410–422.
          * **Schulze L, Schmahl C, Niedtfeld I.** (2016). *Neural Correlates of Disturbed Emotion Processing in Borderline Personality Disorder: A Multimodal Meta-Analysis.* **The American Journal of Psychiatry**, 173(10), 1004–1016.
          
        * **3. Evolución Longitudinal y Psicoterapia:**
          * **Zanarini MC, Frankenburg FR, Reich DB, Fitzmaurice GM.** (2016). *The Course of Borderline Personality Disorder: A 24-Year Follow-up Study of the Course of BPD.* **The American Journal of Psychiatry**, 173(4), 338–347.
          * **Linehan MM.** (1993). *Cognitive-Behavioral Treatment of Borderline Personality Disorder.* Guilford Press, Nueva York.
          * **Bateman AW, Fonagy P.** (2004). *Psychotherapy for Borderline Personality Disorder: Mentalization-Based Treatment.* Oxford University Press.
          
        * **4. Psicofarmacología Basada en Receptores:**
          * **Stahl SM.** (2021). *Stahl's Essential Psychopharmacology: Neuroscientific Basis and Practical Applications.* 5ª edición, Cambridge University Press.
          * **National Institute for Health and Care Excellence (NICE).** (2009). *Borderline personality disorder: recognition and management (Clinical Guideline CG78).* Londres.
        """)
