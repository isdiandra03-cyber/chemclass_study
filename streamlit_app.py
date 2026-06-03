import streamlit as st
import time
from datetime import datetime
import pandas as pd
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Belajar",
    page_icon="📚",
    layout="wide"
)

# --- INISIALISASI SESSION STATE ---
if 'theme' not in st.session_state:
    st.session_state.theme = "White"

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

if 'time_left' not in st.session_state:
    st.session_state.time_left = 25 * 60

if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "🏠 Dashboard"

# ============================================================
# 🎨 FUNGSI apply_theme - GANTI WARNA BACKGROUND & FONT
# ============================================================

def apply_theme(theme):
    if theme == "White":
        # === THEME WHITE (TERANG) ===
        st.markdown("""
           <style>
            /* Background Utama - Putih */
            .stApp {
                background-color: #ffffff;
            }
            
            /* Font untuk semua teks */
            h1, h2, h3, h4, h5, h6, p, label, span, div {
                color: #1a1a1a !important;
            }
            
            /* Font khusus untuk metrics */
            .stMetric .stMetricLabel {
                color: #333333 !important;
            }
            .stMetric .stMetricValue {
                color: #1a1a1a !important;
            }
            
            /* Sidebar */
            section[data-testid="stSidebar"] {
                background-color: #f8f9fa;
            }
            
            /* Input fields */
            .stTextInput > div > div > input {
                background-color: #ffffff;
                color: #1a1a1a;
                border: 1px solid #ddd;
            }
            
            /* Card / Container */
            .custom-card {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                color: #1a1a1a;
            }
            
            /* Tombol */
            .stButton > button {
                background-color: #3498db;
                color: white !important;
            }
            
            /* Progress bar */
            .stProgress > div > div > div {
                background-color: #3498db;
            }
            
            /* Info/Warning/Success messages */
            .stAlert {
                color: #1a1a1a;
            }
            </style>
        """, unsafe_allow_html=True)
        
    else:
        # === THEME BLACK (GELAP) - FONT PUTIH ===
        st.markdown("""
            <style>
            /* Background Utama - Hitam */
            .stApp {
                background-color: #1a1a1a;
            }
            
            /* Font untuk semua teks - PUTIH */
            h1, h2, h3, h4, h5, h6, p, label, span, div {
                color: #ffffff !important;
            }
            
            /* Font untuk Streamlit elements */
            .stMarkdown, .stMarkdown p {
                color: #ffffff !important;
            }
            
            /* Metrics */
            .stMetric .stMetricLabel {
                color: #e0e0e0 !important;
            }
            .stMetric .stMetricValue {
                color: #ffffff !important;
            }
            
            /* Sidebar - Abu gelap */
            section[data-testid="stSidebar"] {
                background-color: #2d2d2d;
            }
            
            /* Input fields */
            .stTextInput > div > div > input {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                border: 1px solid #555;
            }
            
            /* Input label */
            .stTextInput label {
                color: #ffffff !important;
            }
            
            /* Selectbox / Dropdown */
            .stSelectbox label {
                color: #ffffff !important;
            }
            .stSelectbox > div > div > div {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
            }
            
            /* Radio button */
            .stRadio label {
                color: #ffffff !important;
            }
            
            /* Card / Container */
            .custom-card {
                background-color: #2d2d2d;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.5);
                color: #ffffff;
            }
            
            /* Tombol - Warna berbeda untuk Black theme */
            .stButton > button {
                background-color: #e74c3c !important;
                color: #ffffff !important;
            }
            
            /* Checkbox */
            .stCheckbox label {
                color: #ffffff !important;
            }
            
            /* Progress bar */
            .stProgress > div > div > div {
                background-color: #e74c3c;
            }
            
            /* Alert/Info/Warning/Success messages */
            .stAlert {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
            }
            
            /* Separator */
            hr {
                border-color: #555555 !important;
            }
            
            /* Audio player */
            .stAudio {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

# ============================================================
# 🚀 SIDEBAR - PENGATURAN THEME & MENU
# ============================================================

with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    
    # === PILIHAN THEME ===
    st.markdown("### 🎨 Tema Background")
    theme_option = st.radio(
        "Pilih tema:",
        ["⬜ White (Terang)", "⬛ Black (Gelap)"],
        index=0 if st.session_state.theme == "White" else 1
    )
    
    if "White" in theme_option:
        st.session_state.theme = "White"
    else:
        st.session_state.theme = "Black"
    
    # Terapkan tema saat pertama kali load
    apply_theme(st.session_state.theme)
    
    st.markdown("---")

# === MENU UTAMA DI SIDEBAR ===
st.sidebar.markdown("---")
st.sidebar.title("📚 Menu Dashboard")

menu_options = [
    "🏠 Dashboard", 
    "✅ To-Do List", 
    "⏱️ Timer Belajar", 
    "🎵 Musik Fokus", 
    "🧪Indikator asam dan basa"
]

selected_menu = st.sidebar.radio(
    "Pilih Menu:", 
    menu_options,
    label_visibility="collapsed"
)

if selected_menu == "🏠 Dashboard":
    st.title("🏠 Dashboard")

elif selected_menu == "✅ To-Do List":
    st.title("✅ To-Do List")

elif selected_menu == "⏱️ Timer Belajar":
    st.title("⏱️ Timer Belajar")

elif selected_menu == "🎵 Musik Fokus":
    st.title("🎵 Musik Fokus")

elif selected_menu == "🧪Indikator asam dan basa":
    st.title("🧪Indikator asam dan basa")

# ============================================================
# 📝 FUNGSI-FUNGSI TO-DO LIST
# ============================================================

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

# ============================================================
# 📌 KONTEN UTAMA PER MENU
# ============================================================

# ═══════════════════════════════════════════════════════════
# 1️⃣ DASHBOARD UTAMA
# ═══════════════════════════════════════════════════════════
if selected_menu == "🏠 Dashboard":
    st.markdown("# 📚 Dashboard Belajar")
    st.markdown("Selamat datang! Pilih menu di sidebar untuk memulai.")
    
    # Metric Cards
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
        st.metric("🎨 Tema Saat Ini", st.session_state.theme)
    
    st.markdown("---")
    
    # Informasi
    if st.session_state.theme == "White":
        st.success("💡 Tip: Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat)!")
    else:
        st.info("💡 Tip: Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat) untuk hasil maksimal!")

# ═══════════════════════════════════════════════════════════
# 2️⃣ TO-DO LIST
# ═══════════════════════════════════════════════════════════
elif selected_menu == "✅ To-Do List":
    st.markdown("# 📝 To-Do List Harian")
    
    # Input tugas
    col_input1, col_input2 = st.columns([4, 1])
    with col_input1:
        new_task = st.text_input(
            "Tambah tugas baru:", 
            placeholder="Contoh: Mengerjakan PR Matematika"
        )
    with col_input2:
        st.write("")  # Spasi
        if st.button("➕ Tambah", type="primary"):
            add_task(new_task)
            st.rerun()
    
    st.markdown("---")
    
    # Tampilkan daftar tugas
    if len(st.session_state.tasks) == 0:
        st.warning("📭 Daftar tugas kosong. Tambahkan tugas di atas ya!")
    else:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([1, 6, 1])
            
            with col1:
                st.checkbox(
                    "", 
                    value=task["done"], 
                    key=f"check_{i}", 
                    on_change=toggle_task, 
                    args=(i,)
                )
            
            with col2:
                if task["done"]:
                    st.markdown(f"~~{task['name']}~~ ✅")
                else:
                    st.markdown(f"**{task['name']}**")
                st.caption(f"Jam: {task['timestamp']}")
            
            with col3:
                if st.button("🗑️", key=f"del_{i}"):
                    delete_task(i)
                    st.rerun()
            
            st.markdown("---")

# ═══════════════════════════════════════════════════════════════════
# 3️⃣ TIMER BELAJAR
# ═══════════════════════════════════════════════════════════
elif selected_menu == "⏱️ Timer Belajar":
    st.markdown("# ⏱️ Timer Belajar (Pomodoro)")
    
    col_timer1, col_timer2 = st.columns([1, 1])
    
    with col_timer1:
        st.markdown("### ⚙️ Pengaturan Waktu")
        mode = st.selectbox(
            "Pilih Mode:", 
            [
                "25 menit (Belajar)", 
                "5 menit (Istirahat)", 
                "15 menit (Istirahat Panjang)"
            ]
        )
        
        if mode == "25 menit (Belajar)":
            default_time = 25 * 60
        elif mode == "5 menit (Istirahat)":
            default_time = 5 * 60
        else:
            default_time = 15 * 60
        
        if st.button("🔄 Reset Timer"):
            st.session_state.time_left = default_time
            st.session_state.timer_running = False
            st.rerun()
    
    with col_timer2:
        # Tampilan Timer Besar
        menit = st.session_state.time_left // 60
        detik = st.session_state.time_left % 60
        waktu_formatted = f"{menit:02d}:{detik:02d}"
        
        # Indikator warna
        if menit <= 5:
            warna = "🔴"
            status_text = "Waktunya Istirahat!"
        elif menit <= 10:
            warna = "🟡"
            status_text = "Hampir Istirahat"
        else:
            warna = "🟢"
            status_text = "Fokus Penuh"
        
        # Card timer
        if st.session_state.theme == "White":
            bg_color = "#2d2d2d"
            text_color = "#ffffff"
        else:
            bg_color = "#ffffff"
            text_color = "#1a1a1a"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 50px; background: {bg_color}; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='font-size: 100px; margin: 0; color: {text_color};'>{waktu_formatted}</h1>
            <p style='font-size: 24px; color: {text_color};'>{warna} {status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Kontrol
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            if st.button("▶️ MULAI", type="primary"):
                st.session_state.timer_running = True
                st.rerun()
        with col_k2:
            if st.button("⏹️ BERHENTI"):
                st.session_state.timer_running = False
                st.rerun()
    
    # Update timer setiap detik
    if st.session_state.timer_running:
        if st.session_state.time_left > 0:
            time.sleep(1)
            st.session_state.time_left -= 1
            st.rerun()
        else:
            st.session_state.timer_running = False
            st.balloons()
            st.success("⏰ Waktu belajar selesai! Saatnya istirahat.")

# ═══════════════════════════════════════════════════════════
# 4️⃣ MUSIK FOKUS
# ═══════════════════════════════════════════════════════════
elif selected_menu == "🎵 Musik Fokus":
    st.markdown("# 🎵 Musik Fokus")
    
    st.markdown("""
    <div style='text-align: center; padding: 30px; border-radius: 15px;'>
        <h3>🎧 Pemutar Musik</h3>
        <p>Pilih musik favorit untuk fokus belajar:</p>
    </div>
    """)
    
    # Pilihan musik
    musik_options = {
        "🎵 Lo-Fi Chill Beats": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "🌊 Ambient Nature Sounds": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "🌙 Piano Relaksasi": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "⚡ Deep Focus Techno": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "☕ Coffee Shop Vibes": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"
    }
    
    selected_music = st.selectbox("Pilih Trek:", list(musik_options.keys()))
    
    # Audio player
    st.audio(musik_options[selected_music], format='audio/mp3', start_time=0)
    
    st.markdown("---")
    st.info("💡 Catatan: Jika audio tidak muncul, coba pilih trek lain.")
# ==========================================
# 1. DATASET KIMIA (PRESETS ZAT & INDIKATOR)
# ==========================================
elif selected_menu == "Indikator asam dan basa":
    # Semua resource dan logika lokal dimasukkan ke dalam sub-menu ini agar tidak bocor
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

    def hitung_warna_indikator(ph, ind_data):
        low, high = ind_data["range"]
        if ind_data["name"] == "Indikator Universal":
            if ph < 3: return "#dc2626"
            elif ph < 5: return "#f97316"
            elif ph < 6.5: return "#eab308"
            elif ph < 7.5: return "#16a34a"
            elif ph < 9: return "#0284c7"
            elif ph < 11: return "#1d4ed8"
            else: return "#581c87"
        
        if ph < low:
            return ind_data["low_color"]
        elif ph > high:
            return ind_data["high_color"]
        else:
            return ind_data["mid_color"]

    st.title("🧪 ChemClass - Indikator Asam dan Basa")
    st.write("Belajar sains asam-basa bersama ChemClass!")

    menu_tabs = st.tabs(["📊 LAB SIMULATOR"])

    with menu_tabs[0]:
        col_input, col_display = st.columns([5, 7])
        
        with col_input:
            st.subheader("💡 Parameter Simulasi")
            
            preset_names = [chem["name"] for chem in CHEMICALS]
            pilihan_preset = st.selectbox("Pilih Preset Zat Kimia:", preset_names, index=2)
            selected_chem = next(chem for chem in CHEMICALS if chem["name"] == pilihan_preset)
            
            pilihan_ind = st.selectbox(
                "Pilihan Kertas Indikator:",
                options=list(INDICATORS.keys()),
                format_func=lambda x: INDICATORS[x]["name"]
            )
            selected_ind_data = INDICATORS[pilihan_ind]
            
            st.write("---")
            st.markdown("**Kontrol pH Manual (Dial):** Modifikasi nilai derajat keasaman secara langsung")
            simulated_ph = st.slider("Mengatur pH:", min_value=0.0, max_value=14.0, value=selected_chem["pH"], step=0.1)

        with col_display:
            st.subheader("🔮 Simulator Beaker Reaktif")
            
            liquid_color = hitung_warna_indikator(simulated_ph, selected_ind_data)
            
            # Memperbaiki string CSS typo 'Q' pada box-shadow bawaan kode awal
            container_html = f"""
            <div class="beaker-container" style="text-align: center;">
                <span style="font-size: 11px; font-weight: bold; color: #d8b4fe; display: block; margin-bottom: 15px; letter-spacing: 0.1em; font-family: monospace;">LABORATORIUM METRIK UNGU</span>
                <div style="
                    width: 140px; 
                    height: 160px; 
                    border: 4px solid rgba(168, 85, 247, 0.4); 
                    border-top: none;
                    border-radius: 0 0 16px 16px; 
                    margin: 0 auto; 
                    position: relative;
                    box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
                ">
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
            
            st.markdown(f"""
            <div class="chemical-hud" style="margin-top:20px; padding:15px; background: rgba(168, 85, 247, 0.1); border-radius:10px;">
                <h4 style="margin-top:0px; color: #e9d5ff !important; font-family: monospace;">📋 INFORMASI SENYAWA</h4>
                <b>Nama Senyawa:</b> {selected_chem['name']} ({selected_chem['formula']})<br/>
                <b>Nama Populer:</b> {selected_chem['common']}<br/>
                <b>Ionisasi Disosiasi:</b> <code>{selected_chem['dissociation']}</code><br/>
                <b>Kategori Kelas:</b> {selected_chem['category']}
            </div>
            """, unsafe_allow_html=True)
