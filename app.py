import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🚗🌉 Análisis Dinámico de un Vehículo sobre un Puente")

st.markdown("""
Este simulador resuelve el siguiente problema:

- Un vehículo de **masa m = 1000 kg** cruza un puente de **longitud L = 20 m**, a una velocidad constante **v = 10 m/s**.
- El puente es una **viga simplemente apoyada de Euler-Bernoulli**, con:
  - Masa distribuida: **μ = 200 kg/m**
  - Módulo de elasticidad: **E = 2.1×10¹¹ Pa**
  - Momento de inercia: **I = 8×10⁻⁵ m⁴**
""")

# Parámetros físicos
m = 1000          # kg
L = 20            # m
v = 10            # m/s
mu = 200          # kg/m
E = 2.1e11        # Pa
I = 8e-5          # m^4

# 1. Cálculo de la frecuencia natural fundamental
f1 = (1 / (2 * L**2)) * np.pi * np.sqrt(E * I / (mu * L**2))  # Hz
omega1 = 2 * np.pi * f1

st.subheader("📌 Resultados de la Frecuencia Natural")

st.write(f"Frecuencia natural fundamental del puente: **{f1:.3f} Hz**")
st.write(f"Velocidad del vehículo: **{v} m/s**")

# 2. Verificar resonancia
# Frecuencia de excitación = velocidad / longitud de onda (asumimos primera forma modal: λ = 2L)
f_exc = v / (2 * L)

if np.isclose(f_exc, f1, rtol=0.1):
    st.error("⚠️ ¡Hay riesgo de resonancia dinámica! (frecuencia de excitación ≈ frecuencia natural)")
else:
    st.success("✅ No hay resonancia significativa (frecuencia de excitación ≠ frecuencia natural)")

# 3. Simulación de respuesta dinámica (aproximada)
st.subheader("📈 Simulación de la deflexión en el centro del puente")

t_total = L / v
t = np.linspace(0, t_total, 500)
x_vehicle = v * t

# Primera forma modal en el centro: sin(pi*L/2L) = sin(pi/2) = 1
# Aproximación simplificada de deflexión modal
# u(t) = A * sin(ω₁ * t), donde A depende de la masa del vehículo

# Suponiendo una amplitud máxima proporcional a la carga dinámica
A = (m * 9.81) / (mu * L) * 0.01  # Factor de escala arbitrario
u_t = A * np.sin(omega1 * t) * (x_vehicle <= L)

# 4. Gráfica
fig, ax = plt.subplots()
ax.plot(t, u_t * 1000, label="Deflexión (mm)", color='blue')
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Deflexión en el centro (mm)")
ax.set_title("Deflexión dinámica en el centro del puente")
ax.grid(True)
ax.legend()
st.pyplot(fig)
