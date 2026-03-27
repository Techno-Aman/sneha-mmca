import streamlit as st
import matplotlib.pyplot as plt
import math

st.title("🏥Hospital Outpatient Queue")

# Sidebar Inputs
st.sidebar.header("⚙️ Input Parameters")

arrival_rate = st.sidebar.number_input("Arrival Rate (λ)", min_value=0.1, max_value=12.0)
service_rate = st.sidebar.number_input("Service Rate (μ)", min_value=0.1, max_value=5.0)
doctors = st.sidebar.number_input("Number of Doctors (c)", 1, 20, 1)
max_doctors = st.sidebar.number_input("Max Doctors for Graph", 1, 20, 1)

# Function to calculate P0
def calculate_p0(lam, mu, c):
    sum_part = sum((lam/mu)**n / math.factorial(n) for n in range(c))
    last_part = ((lam/mu)**c) / (math.factorial(c) * (1 - (lam/(c*mu))))
    return 1 / (sum_part + last_part)

# Calculate rho
rho = arrival_rate / (doctors * service_rate)

st.subheader("📊 Results")

if rho >= 1:
    st.error("⚠️ System is unstable (ρ ≥ 1)")
else:
    P0 = calculate_p0(arrival_rate, service_rate, doctors)
    Lq = ((arrival_rate/service_rate)**doctors * rho /
          (math.factorial(doctors) * (1-rho)**2)) * P0
    Wq = Lq / arrival_rate
    W = Wq + (1/service_rate)

    st.write(f"**Traffic Intensity (ρ):** {round(rho,3)}")
    st.write(f"**Average Queue Length (Lq):** {round(Lq,3)}")
    st.write(f"**Waiting Time (Wq):** {round(Wq,3)} hours")
    st.write(f"**Total Time (W):** {round(W,3)} hours")

# Graph Section
st.subheader("📈 Doctors vs Waiting Time")

doctor_range = range(1, max_doctors + 1)
waiting_times = []

for c in doctor_range:
    rho = arrival_rate / (c * service_rate)

    if rho >= 1:
        waiting_times.append(None)
        continue

    P0 = calculate_p0(arrival_rate, service_rate, c)
    Lq = ((arrival_rate/service_rate)**c * rho /
          (math.factorial(c) * (1-rho)**2)) * P0
    Wq = Lq / arrival_rate
    waiting_times.append(Wq)

# Plot
fig, ax = plt.subplots()
ax.plot(list(doctor_range), waiting_times, marker='o')
ax.set_xlabel("Number of Doctors")
ax.set_ylabel("Waiting Time (hours)")
ax.set_title("Effect of Doctors on Waiting Time")
ax.grid()

st.pyplot(fig)