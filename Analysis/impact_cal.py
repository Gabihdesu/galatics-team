import streamlit as st
import math

# ==============================
# Configuração da página
# ==============================
st.set_page_config(page_title="Simulador de Impacto", layout="centered")

st.title("🌍 Simulador de Impacto de Asteroide")
st.write("Ajuste os valores abaixo para estimar o impacto. Os cálculos usam modelos geofísicos simplificados.")

# CONSTANTES
RHO_IMPACTOR = 3000.0  # kg/m³ (Densidade típica de asteroide rochoso)
RHO_TARGET_GCM3 = 2.5  # g/cm³ (Densidade típica de rocha alvo)
JOULES_PER_MT_TNT = 4.184e15 # Conversão de Joules para Megatons de TNT
G_EARTH = 9.8  # m/s²
SEISMIC_EFFICIENCY = 1e-4 # 0.01% da energia total convertida em sísmica
CRATER_COLLAPSE_FACTOR = 1.3 # Fator de colapso da cratera

# ==============================
# Função de cálculo do impacto
# ==============================
def calcular_impacto(diametro, velocidade, angulo):
    # 1. CÁLCULO DA ENERGIA
    massa = (math.pi / 6) * (diametro ** 3) * RHO_IMPACTOR
    velocidade_m_s = velocidade * 1000
    
    # Energia Cinética Total (Joules)
    energia_joules = 0.5 * massa * velocidade_m_s ** 2
    energia_megatons = energia_joules / JOULES_PER_MT_TNT

    # Efeito do ângulo: O ângulo afeta o formato e profundidade, 
    # mas a energia total liberada é K. Para Cratera, usamos (sin(theta))^gamma
    fator_angulo_cratera = math.sin(math.radians(angulo)) ** (2/3)
    
    # 2. TAMANHO DA CRATERA (Escala de Energia e Densidade)
    # Fórmula simplificada: Dc = Cf * (g_earth/g_target)^(1/6) * (E_MT * rho_i / rho_t)^(1/3.4) * fator_angulo
    # Usando rho_i=2.6 g/cm3 e rho_t=2.5 g/cm3
    dens_ratio = 2.6 / RHO_TARGET_GCM3
    
    # Note: O termo gravitacional é 1 para a Terra. Aplicamos a correção do ângulo.
    cratera_km = CRATER_COLLAPSE_FACTOR * (energia_megatons * dens_ratio) ** (1/3.4) * fator_angulo_cratera
    
    # 3. TERREMOTO (Magnitude Sísmica - M)
    # Assumimos uma eficiência sísmica (eta_s) para calcular a energia sísmica (Es)
    energia_sismica_joules = SEISMIC_EFFICIENCY * energia_joules
    
    # Relação Gutenberg-Richter simplificada: M = 0.67 * log10(Es) - 5.87
    if energia_sismica_joules > 0:
        terremoto_mag = 0.67 * math.log10(energia_sismica_joules) - 5.87
    else:
        terremoto_mag = 0.0

    # 4. RAIO DE DESTRUIÇÃO (Jato de Ar e Térmico)
    # Raio de Sobrevôo/Choque (Assumindo dano estrutural significativo, escala E^(1/3))
    # Fator de 1.8 é uma aproximação para ~10 kPa de sobrepressão
    raio_choque_km = 1.8 * (energia_megatons ** (1/3))
    
    # Raio Térmico (Queimaduras de 2º Grau, escala E^(1/3))
    # Fator de 11 é uma aproximação comum
    raio_termico_km = 11.0 * (energia_megatons ** (1/3))
    

    return {
        "massa_bilhoes_ton": massa / 1e12,
        "energia_megatons": energia_megatons,
        "cratera_km": cratera_km,
        "terremoto_mag": terremoto_mag,
        "raio_choque_km": raio_choque_km,
        "raio_termico_km": raio_termico_km
    }

# ==============================
# Sliders interativos
# ==============================
diametro = st.slider("🌑 Diâmetro do impactor (metros)", min_value=1, max_value=2000, value=100, step=1)
velocidade = st.slider("🚀 Velocidade (km/s)", min_value=1.0, max_value=70.0, value=20.0, step=0.5)
angulo = st.slider("🎯 Ângulo de impacto (graus)", min_value=1, max_value=90, value=45, step=1) # Mínimo 1 para evitar log(0) ou sin(0) em alguns casos

# ==============================
# Cálculo em tempo real
# ==============================
resultado = calcular_impacto(diametro, velocidade, angulo)

# ==============================
# Exibição dos resultados
# ==============================
st.subheader("📊 Resultados da Simulação")

st.metric("Massa Estimada (Bilhão de Toneladas)", f"{resultado['massa_bilhoes_ton']:.2e}")

col1, col2 = st.columns(2)

with col1:
    st.metric("Energia liberada (MT TNT)", f"{resultado['energia_megatons']:.2e}")
    st.metric("Tamanho da cratera (km)", f"{resultado['cratera_km']:.2f}")
    st.metric("Magnitude do Terremoto", f"{resultado['terremoto_mag']:.2f}")

with col2:
    st.metric("Raio do Jato de Ar (km)", f"{resultado['raio_choque_km']:.2f}")
    st.metric("Raio Térmico (km)", f"{resultado['raio_termico_km']:.2f}")
    st.write("") # Espaço para alinhamento

st.caption("⚙️ Cálculos baseados em modelos de escala (scaling laws) de impacto geofísico.")