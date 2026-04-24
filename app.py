import streamlit as st
import pandas as pd
import time

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="ARP Spoofing vs DAI Simulator",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0e1117;
    color: white;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

section[data-testid="stSidebar"] {
    background-color: #161b22;
}

.log-box {
    background: #000000;
    color: #00ff88;
    padding: 15px;
    border-radius: 12px;
    font-family: monospace;
    min-height: 280px;
    border: 1px solid #30363d;
}

.success-box {
    background: #0f5132;
    padding: 18px;
    border-radius: 12px;
    color: white;
    font-size: 18px;
}

.danger-box {
    background: #842029;
    padding: 18px;
    border-radius: 12px;
    color: white;
    font-size: 18px;
}

.metric-card {
    background: #161b22;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("⚙️ Control Panel")

mode = st.sidebar.radio(
    "Select Simulation Mode",
    ["Without Defense", "With Dynamic ARP Inspection"]
)

run_btn = st.sidebar.button("▶ Run Simulation")
reset_btn = st.sidebar.button("🔄 Reset")

st.sidebar.markdown("---")
st.sidebar.info("This simulator demonstrates ARP cache poisoning and Dynamic ARP Inspection defense.")

# -------------------------
# Header
# -------------------------
st.title("🛡️ ARP Spoofing vs Dynamic ARP Inspection Simulator")
st.caption("Interactive Cybersecurity Dashboard")

# -------------------------
# Metrics
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Victim IP", "192.168.1.10")

with col2:
    st.metric("Gateway IP", "192.168.1.1")

with col3:
    st.metric("Attacker IP", "192.168.1.99")

st.divider()

# -------------------------
# Network Topology
# -------------------------
st.subheader("🌐 Network Topology")

st.code("""
 Victim PC (192.168.1.10)
          │
          ▼
      [ SWITCH ]
       /      \\
      ▼        ▼
Gateway      Attacker
192.168.1.1  192.168.1.99
""")

# -------------------------
# Placeholders
# -------------------------
log_placeholder = st.empty()
table_placeholder = st.empty()
result_placeholder = st.empty()

# -------------------------
# Functions
# -------------------------
def show_logs(logs):
    output = ""
    for line in logs:
        output += line + "\n"
        log_placeholder.markdown(
            f'<div class="log-box">{output}</div>',
            unsafe_allow_html=True
        )
        time.sleep(1)

def show_arp_table(cache):
    df = pd.DataFrame(
        list(cache.items()),
        columns=["IP Address", "MAC Address"]
    )
    st.subheader("📋 Victim ARP Cache")
    table_placeholder.table(df)

# -------------------------
# Simulation Logic
# -------------------------
if run_btn:

    arp_cache = {
        "192.168.1.1": "aa:11:bb:22:cc:33",
        "192.168.1.10": "aa:bb:cc:dd:ee:ff"
    }

    logs = []

    logs.append("[Phase 1] Normal ARP traffic detected...")
    show_logs(logs)
    show_arp_table(arp_cache)

    time.sleep(1)

    logs.append("[Phase 2] Attacker sends spoofed ARP reply...")
    show_logs(logs)

    time.sleep(1)

    if mode == "Without Defense":

        arp_cache["192.168.1.1"] = "11:22:33:44:55:66"

        logs.append("[ATTACK] Fake ARP accepted.")
        logs.append("[SUCCESS] Victim ARP cache poisoned.")
        show_logs(logs)

        show_arp_table(arp_cache)

        result_placeholder.markdown("""
        <div class="danger-box">
        ❌ <b>ATTACK SUCCEEDED</b><br>
        Traffic redirected through attacker.<br>
        Network is vulnerable to MITM attack.
        </div>
        """, unsafe_allow_html=True)

    else:

        logs.append("[DAI] ARP packet validation started.")
        logs.append("[BLOCKED] Spoofed ARP packet rejected.")
        show_logs(logs)

        show_arp_table(arp_cache)

        result_placeholder.markdown("""
        <div class="success-box">
        ✅ <b>ATTACK BLOCKED</b><br>
        Dynamic ARP Inspection protected the victim.<br>
        ARP cache remains clean.
        </div>
        """, unsafe_allow_html=True)

# -------------------------
# Reset
# -------------------------
if reset_btn:
    st.rerun()