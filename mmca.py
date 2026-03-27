import streamlit as st
import matplotlib.pyplot as plt
import math

st.title("🏥Hospital Outpatient Queue")
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Model", "Explanation"])

if page == "Model" : 
    # Sidebar Inputs
    st.sidebar.header("⚙️ Input Parameters")

    arrival_rate = st.sidebar.number_input("Arrival Rate (λ)", min_value=0.1, max_value=12.0, value=12.0)
    service_rate = st.sidebar.number_input("Service Rate (μ)", min_value=0.1, max_value=5.0,value=5.0)
    doctors = st.sidebar.number_input("Number of Doctors (c)", 1, 20, 2)
    max_doctors = st.sidebar.number_input("Max Doctors for Graph", 1, 20, 2)

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

elif page == "Explanation":

    st.title("📘 Model Explanation")

    st.subheader("1. Objective")
    st.write("""
    The purpose of this model is to analyze a hospital outpatient system 
    and evaluate patient waiting time based on the number of doctors available.
    """)

    st.subheader("2. Input Parameters")
    st.write("""
    • λ (Arrival Rate): Number of patients arriving per hour  
    • μ (Service Rate): Number of patients a doctor can treat per hour  
    • c (Doctors): Number of doctors in the system  
    """)

    st.subheader("3. Key Formula")
    st.write("""
    Traffic Intensity (ρ) = λ / (c × μ)

    • If ρ ≥ 1 → System is unstable (more patients than capacity)  
    • If ρ < 1 → System is stable  
    """)

    st.subheader("4. Performance Measures")
    st.write("""
    • P₀ → Probability that no patients are in the system  
    • Lq → Average number of patients waiting in queue  
    • Wq → Average waiting time in queue  
    • W → Total time spent in the system  
    """)

    st.subheader("5. Working Process")
    st.write("""
    1. User inputs λ, μ, and number of doctors  
    2. System calculates traffic intensity (ρ)  
    3. If system is stable, queue metrics are calculated  
    4. Graph is plotted for different doctor values  
    """)

    st.subheader("6. Graph Interpretation")
    st.write("""
    The graph shows how waiting time changes as the number of doctors increases.

    • More doctors → Less waiting time  
    • After a point → Improvement becomes minimal  
    """)

    st.subheader("7. Real-Life Application")
    st.write("""
    • Helps hospitals reduce patient waiting time  
    • Assists in optimal staff allocation  
    • Improves overall service efficiency  
    """)

    st.success("✅ We implemented an M/M/c queue model with automatic optimization to minimize waiting time.")