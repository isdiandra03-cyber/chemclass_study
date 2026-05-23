import streamlit as st
import time
from datetime import datetime
import pandas as pd
import numpy as np

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Belajar",
    page_icon="📚",
    layout="wide"
)

# --- CSS TAMBAHAN UNTUK TAMPILAN CANTIK ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    .menu-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .timer-display {
        font-size: 80px;
        font-weight: bold;
        text-align: center;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

if 'time_left' not in st.session_state:
    st.session_state.time_left = 25 * 60  # 25 menit

if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "🏠 Dashboard"

# --- FUNGSI-FUNGSI ---

def add_task(task_name):
    if task_name:
        st.session_state.tasks.append({
            "name": task_name,
            "done": False,
            "timestamp": datetime.now().strftime("%H:%M")
        })

def toggle_task(index):
    st.session_state.tasks[index]["done"] = not st.session_state.tasks[index]["done"]

def delete_task(index):
    st.session_state.tasks.pop(index)

# --- SIDEBAR MENU ---
st.sidebar.title("📚 Menu Dashboard")
menu_options = ["🏠 Dashboard", "✅ To-Do List", "⏱️ Timer Belajar", "🎵 Musik Fokus", "ChemClass-Indikator"]
selected_menu = st.sidebar.radio("Pilih Menu:", menu_options, index=menu_options.index(st.session_state.current_menu) if st.session_state.current_menu in menu_options else 0)

st.session_state.current_menu = selected_menu

# --- LOGIKA TAMPILAN PER MENU ---

# ============================
# 1. MENU DASHBOARD UTAMA
# ============================
if selected_menu == "🏠 Dashboard":
    st.markdown("# 📚 Dashboard Belajar")
    st.markdown("Selamat datang! Pilih menu di sidebar untuk memulai.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Total Tugas", len(st.session_state.tasks))
    with col2:
        tugas_belum = sum(1 for t in st.session_state.tasks if not t["done"])
        st.metric("⏳ Tugas Tertunda", tugas_belum)
    with col3:
        tugas_selesai = sum(1 for t in st.session_state.tasks if t["done"])
        st.metric("✅ Tugas Selesai", tugas_selesai)
    with col4:
        if st.session_state.timer_running:
            st.metric("⏱️ Timer", "Aktif")
        else:
            st.metric("⏱️ Timer", "Standby")

    st.markdown("---")
    st.info("💡 Tip: Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat) untuk hasil maksimal!")

# ============================
# 2. MENU TO-DO LIST
# ============================
elif selected_menu == "✅ To-Do List":
    st.markdown("# 📝 To-Do List Harian")
    
    with st.container():
        col_input1, col_input2 = st.columns([4, 1])
        with col_input1:
            new_task = st.text_input("Tambah tugas baru:", placeholder="Contoh: Mengerjakan PR Matematika", key="input_task")
        with col_input2:
            st.write("") 
            if st.button("➕ Tambah", type="primary"):
                add_task(new_task)
                st.rerun()
    
    st.markdown("---")
    
    if len(st.session_state.tasks) == 0:
        st.warning("📭 Daftar tugas kosong. Tambahkan tugas di atas!")
    else:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([1, 6, 1])
            
            with col1:
                checkbox = st.checkbox("", value=task["done"], key=f"check_{i}", on_change=toggle_task, args=(i,))
            
            with col2:
                if task["done"]:
                    st.markdown(f"~~{task['name']}~~ ✅")
                else:
                    st.markdown(f"**{task['name']}**")
            
            with col3:
                if st.button("🗑️", key=f"del_{i}"):
                    delete_task(i)
                    st.rerun()
            
            st.markdown("---")

# ============================
# 3. MENU TIMER BELAJAR
# ============================
elif selected_menu == "⏱️ Timer Belajar":
    st.markdown("# ⏱️ Timer Belajar (Pomodoro)")
    
    col_timer1, col_timer2 = st.columns([1, 1])
    
    with col_timer1:
        st.markdown("### Pengaturan Waktu")
        mode = st.selectbox("Pilih Mode:", ["25 menit (Belajar)", "5 menit (Istirahat)", "15 menit (Istirahat Panjang)", "Custom"])
        
        if mode == "25 menit (Belajar)":
            default_time = 25 * 60
        elif mode == "5 menit (Istirahat)":
            default_time = 5 * 60
        elif mode == "15 menit (Istirahat Panjang)":
            default_time = 15 * 60
        else:
            menit = st.number_input("Menit:", min_value=1, max_value=120, value=25)
            default_time = menit * 60
        
        if st.button("🔄 Reset Timer"):
            st.session_state.time_left = default_time
            st.session_state.timer_running = False
            st.rerun()
    
    with col_timer2:
        # Tampilan Timer Besar
        menit = st.session_state.time_left // 60
        detik = st.session_state.time_left % 60
        waktu_formatted = f"{menit:02d}:{detik:02d}"
        
        # Ubah warna berdasarkan waktu
        if menit <= 5:
            warna = "🔴"
        elif menit <= 10:
            warna = "🟡"
        else:
            warna = "🟢"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 50px; background: white; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='font-size: 100px; margin: 0; color: #2c3e50;'>{waktu_formatted}</h1>
            <p style='font-size: 24px;'>{warna} Status</p>
        </div>
        """, unsafe_allow_html=True)
        
        # KONTROL START/STOP
        col_kontrol1, col_kontrol2 = st.columns(2)
        with col_kontrol1:
            if st.button("▶️ MULAI", type="primary", disabled=st.session_state.timer_running):
                st.session_state.timer_running = True
                st.rerun()
        with col_kontrol2:
            if st.button("⏹️ BERHENTI", disabled=not st.session_state.timer_running):
                st.session_state.timer_running = False
                st.rerun()
    
    # Auto update timer (refresh setiap detik)
    if st.session_state.timer_running:
        if st.session_state.time_left > 0:
            time.sleep(1)
            st.session_state.time_left -= 1
            st.rerun()
        else:
            st.session_state.timer_running = False
            st.balloons()
            st.success("⏰ Waktu selesai! Silakan istirahat atau mulai sesi berikutnya.")
            st.rerun()

# ============================
# 4. MENU MUSIK FOKUS
# ============================
elif selected_menu == "🎵 Musik Fokus":
    st.markdown("# 🎵 Musik Fokus")
    
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: white; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h3>🎧 Pemutar Musik</h3>
        <p>Pilih musik favorit untuk fokus belajar:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Opsi memilih musik
    musik_options = {
        "🎵 Lo-Fi Chill Beats": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "🌊 Ambient Nature Sounds": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "🌙 Piano Relaksasi": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "⚡ Deep Focus Techno": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "☕ Coffee Shop Vibes": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"
    }
    
    selected_music = st.selectbox("Pilih Trek:", list(musik_options.keys()))
    
    audio_url = musik_options[selected_music]
    
    # Tampilkan audio player
    st.audio(audio_url, format='audio/mp3', start_time=0)
    
    st.markdown("---")
    st.info("💡 Catatan: Jika audio tidak muncul, coba pilih trek lain. Beberapa trek adalah contoh gratis.")

# ==========================================
# 5. KONFIGURASI HALAMAN & ENERGI ESTETIKA (NEON PURPLE)
# ==========================================
st.set_page_config(
    page_title="ChemClass Lab - Streamlit Edition",
    page_icon="🧪",
    layout="wide",
)

# ==========================================
# 1. DATASET KIMIA (PRESETS ZAT & INDIKATOR)
# ==========================================
if page == "Introduction":
    st.title("HAIIIII")


elif page == "Simulasi":
    st.title("Coba simulasi ini")
CHEMICALS = [
    {"id": "hcl", "name": "Asam Klorida (HCl)", "formula": "HCl", "pH": 1.0, "type": "asam", "category": "Laboratorium", "common": "Asam kuat pembersih porselen", "dissociation": "HCl → H⁺ + Cl⁻"},
    {"id": "h2so4", "name": "Asam Sulfat (Air Aki)", "formula": "H₂SO₄", "pH": 1.5, "type": "asam", "category": "Laboratorium", "common": "Air aki kendaraan pekat", "dissociation": "H₂SO₄ → 2H⁺ + SO₄²⁻"},
    {"id": "vinegar", "name": "Asam Asetat (Cuka Makan)", "formula": "CH₃COOH", "pH": 3.0, "type": "asam", "category": "Sehari-hari", "common": "Cuka dapur encer", "dissociation": "CH₃COOH ⇌ H⁺ + CH₃COO⁻"},
    {"id": "lemon", "name": "Asam Sitrat (Sari Lemon)", "formula": "C₆H₈O₇", "pH": 2.2, "type": "asam", "category": "Sehari-hari", "common": "Air perasan jeruk segar", "dissociation": "C₆H₈O₇ ⇌ H⁺ + C₆H₇O₇⁻"},
    {"id": "water", "name": "Air Murni (H₂O)", "formula": "H₂O", "pH": 7.0, "type": "netral", "category": "Sehari-hari", "common": "Air suling / Aquades netral", "dissociation": "H₂O ⇌ H⁺ + OH⁻"},
    {"id": "baking_soda", "name": "Soda Kue (NaHCO₃)", "formula": "NaHCO₃", "pH": 8.5, "type": "basa", "category": "Sehari-hari", "common": "Bahan pengembang roti rumahan", "dissociation": "NaHCO₃ → Na⁺ + HCO₃⁻"},
    {"id": "limewater", "name": "Kalsium Hidroksida (Air Kapur)", "formula": "Ca(OH)₂", "pH": 11.5, "type": "basa", "category": "Laboratorium", "common": "Air kapur sirih jernih", "dissociation": "Ca(OH)₂ → Ca²⁺ + 2OH⁻"},
    {"id": "naoh", "name": "Natrium Hidroksida (Sodapi)", "formula": "NaOH", "pH": 13.0, "type": "basa", "category": "Laboratorium", "common": "Sodapi pekat penghancur sumbatan", "dissociation": "NaOH → Na⁺ + OH⁻"}
]

INDICATORS = {
    "lakmus": {
        "name": "Kertas Lakmus (Litmus)",
        "range": (4.5, 8.3),
        "low_color": "#ef4444", "low_label": "MERAH ASAM",
        "high_color": "#3b82f6", "high_label": "BIRU BASA",
        "mid_color": "#a855f7", "mid_label": "UNGU REAKSI"
    },
    "pp": {
        "name": "Phenolphthalein (PP)",
        "range": (8.2, 10.0),
        "low_color": "#f8fafc", "low_label": "TIDAK BERWARNA",
        "high_color": "#ec4899", "high_label": "MERAH MUDA PEKAT",
        "mid_color": "#fbcfe8", "mid_label": "MERAH MUDA SEMU"
    },
    "btb": {
        "name": "Bromothymol Blue (BTB)",
        "range": (6.0, 7.6),
        "low_color": "#eab308", "low_label": "KUNING ASAM",
        "high_color": "#1d4ed8", "high_label": "BIRU BASA",
        "mid_color": "#22c55e", "mid_label": "HIJAU NETRAL"
    },
    "mr": {
        "name": "Metil Merah (Methyl Red)",
        "range": (4.4, 6.2),
        "low_color": "#ef4444", "low_label": "MERAH ASAM",
        "high_color": "#eab308", "high_label": "KUNING BASA",
        "mid_color": "#f97316", "mid_label": "JINGGA TRANSISI"
    },
    "universal": {
        "name": "Indikator Universal",
        "range": (0.0, 14.0),
        "low_color": "#dc2626", "low_label": "MERAH (pH KOROSIF)",
        "high_color": "#581c87", "high_label": "UNGU (pH BASA KUAT)",
        "mid_color": "#16a34a", "mid_label": "HIJAU (pH NETRAL)"
    }
}

# ==========================================
# 2. HEADER UTAMA
# ==========================================
st.title("🧪 ChemClass Lab - Python Edition")
st.write("Belajar sains asam-basa dan koding Python pemula sekaligus dalam satu platform terpadu.")

menu = st.tabs(["📊 LAB SIMULATOR"])

# ==========================================
# HELPER: FUNGSI PENENTU WARNA CAIRAN
# ==========================================
def hitung_warna_indikator(ph, ind_data):
    low, high = ind_data["range"]
    if ind_data["name"] == "Indikator Universal":
        if ph < 3: return "#dc2626"  # Merah asam kuat
        elif ph < 5: return "#f97316"  # Oranye
        elif ph < 6.5: return "#eab308"  # Kuning
        elif ph < 7.5: return "#16a34a"  # Hijau netral
        elif ph < 9: return "#0284c7"  # Biru muda
        elif ph < 11: return "#1d4ed8"  # Biru tua
        else: return "#581c87"  # Ungu basa kuat
    
    if ph < low:
        return ind_data["low_color"]
    elif ph > high:
        return ind_data["high_color"]
    else:
        return ind_data["mid_color"]

# ==========================================
# TAB 1: LAB SIMULATOR
# ==========================================
with menu[0]:
    col_input, col_display = st.columns([5, 7])
    
    with col_input:
        st.subheader("💡 Parameter Simulasi")
        
        # Pilihan Preset Senyawa
        preset_names = [chem["name"] for chem in CHEMICALS]
        pilihan_preset = st.selectbox("Pilih Preset Zat Kimia:", preset_names, index=2) # Default cuka
        selected_chem = next(chem for chem in CHEMICALS if chem["name"] == pilihan_preset)
        
        # Pilihan Indikator
        pilihan_ind = st.selectbox(
            "Pilihan Kertas Indikator:",
            options=list(INDICATORS.keys()),
            format_func=lambda x: INDICATORS[x]["name"]
        )
        selected_ind_data = INDICATORS[pilihan_ind]
        
        # Slider pH Manual
        st.write("---")
        st.markdown("**Kontrol pH Manual (Dial):** Modifikasi nilai derajat keasaman secara langsung")
        simulated_ph = st.slider("Mengatur pH:", min_value=0.0, max_value=14.0, value=selected_chem["pH"], step=0.1)

    with col_display:
        st.subheader("🔮 Simulator Beaker Reaktif")
        
        # Ambil warna secara dinamis berdasarkan pH slider
        liquid_color = hitung_warna_indikator(simulated_ph, selected_ind_data)
        
        # Visualisasi Gelas Beaker khas dengan border bersinar ungu neon
        container_html = f"""
        <div class="beaker-container">
            <span style="font-size: 11px; font-weight: bold; color: #d8b4fe; display: block; margin-bottom: 15px; letter-spacing: 0.1em; font-family: monospace;">LABORATORIUM METRIK UNGU</span>
            <div style="
                width: 140px; 
                height: 160px; 
                border: 4px solid rgba(168, 85, 247, 0.4); 
                border-top: none;
                border-radius: 0 0 16px 16px; 
                margin: 0 auto; 
                position: relative;
            Q    box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
            ">
                <!-- Cairan Kimia Reaktif -->
                <div style="
                    position: absolute; 
                    bottom: 8px; 
                    left: 6px; 
                    right: 6px; 
                    height: {int(simulated_ph * 4.5) + 50}px; 
                    background-color: {liquid_color}; 
                    border-radius: 0 0 10px 10px;
                    transition: background-color 0.4s ease, height 0.4s ease;
                    box-shadow: inset 0 4px 8px rgba(255,255,255,0.15);
                "></div>
                <!-- Garis Skala Pengukur -->
                <div style="position: absolute; left: 10px; top: 30px; border-left: 2px solid rgba(168, 85, 247, 0.3); height: 100px; display: flex; flex-direction: column; justify-content: space-between; text-align: left; padding-left: 5px; font-size: 8px; font-family: monospace; color: #d8b4fe;">
                    <span>-- 150ml</span>
                    <span>-- 100ml</span>
                    <span>-- 50ml</span>
                </div>
            </div>
            <div style="margin-top: 20px; font-weight: bold; font-size: 20px; color: #f3e8ff; text-shadow: 0 0 8px {liquid_color};">
                Nilai pH Cairan: <span style="color: {liquid_color};">{simulated_ph:.1f}</span>
            </div>
        </div>
        """
        st.markdown(container_html, unsafe_allow_html=True)
        
        # HUD Panel Informasi senyawa pilihan dengan aksen senada
        st.markdown(f"""
        <div class="chemical-hud">
            <h4 style="margin-top:0px; color: #e9d5ff !important; font-family: monospace;">📋 INFORMASI SENYAWA</h4>
            <b>Nama Senyawa:</b> {selected_chem['name']} ({selected_chem['formula']})<br/>
            <b>Nama Populer:</b> {selected_chem['common']}<br/>
            <b>Ionisasi Disosiasi:</b> <code>{selected_chem['dissociation']}</code><br/>
            <b>Kategori Kelas:</b> {selected_chem['category']}
        </div>
        """, unsafe_allow_html=True)
)
