import streamlit as st
import time
from datetime import datetime
import pandas as pd

# ============================================================
# 🎨 KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="Dashboard Belajar",
    page_icon="📚",
    layout="wide"
)

# ============================================================
# 🚀 INISIALISASI SESSION STATE
# ============================================================

if 'theme' not in st.session_state:
    st.session_state.theme = "White"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = ""

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

if 'time_left' not in st.session_state:
    st.session_state.time_left = 25 * 60

# ============================================================
# 🎨 FUNGSI apply_theme
# ============================================================

def apply_theme(theme):
    if theme == "White":
        st.markdown("""
            <style>
            .stApp { background-color: #ffffff; }
            h1, h2, h3, h4, h5, h6, p, label, span, div { color: #1a1a1a !important; }
            .stMetric .stMetricLabel { color: #333333 !important; }
            .stMetric .stMetricValue { color: #1a1a1a !important; }
            section[data-testid="stSidebar"] { background-color: #f8f9fa; }
            .stTextInput > div > div > input { background-color: #ffffff; color: #1a1a1a; border: 1px solid #ddd; }
            .stButton > button { background-color: #3498db; color: white !important; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp { background-color: #1a1a1a; }
            h1, h2, h3, h4, h5, h6, p, label, span, div { color: #ffffff !important; }
            .stMarkdown, .stMarkdown p { color: #ffffff !important; }
            .stMetric .stMetricLabel { color: #e0e0e0 !important; }
            .stMetric .stMetricValue { color: #ffffff !important; }
            section[data-testid="stSidebar"] { background-color: #2d2d2d; }
            .stTextInput > div > div > input { background-color: #2d2d2d !important; color: #ffffff !important; border: 1px solid #555; }
            .stSelectbox label, .stRadio label { color: #ffffff !important; }
            .stSelectbox > div > div > div { background-color: #2d2d2d !important; color: #ffffff !important; }
            .stButton > button { background-color: #e74c3c !important; color: #ffffff !important; }
            .stCheckbox label { color: #ffffff !important; }
            .stAlert { background-color: #2d2d2d !important; color: #ffffff !important; }
            </style>
        """, unsafe_allow_html=True)

# ============================================================
# 📝 FUNGSI-FUNGSI LOGIN
# ============================================================

def check_login(username, password):
    # Contoh user & password (bisa diubah)
    users = {
        "admin": "123456",
        "user": "2024",
        "student": "belajar"
    }
    
    if username in users and users[username] == password:
        return True
    return False

def login_user():
    st.session_state.logged_in = True
    st.session_state.username = st.session_state.input_username

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.tasks = []
    st.session_state.timer_running = False
    st.session_state.time_left = 25 * 60

# ============================================================
# 📝 FUNGSI-FUNGSI LAINNYA
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
# 🚪 HALAMAN LOGIN
# ============================================================

if not st.session_state.logged_in:
    # Terapkan tema dulu
    apply_theme(st.session_state.theme)
    
    # Logo dan Judul
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <h1 style='font-size: 60px;'>📚</h1>
        <h1>Dashboard Belajar</h1>
        <p>Silakan login untuk melanjutkan</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form Login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 Login")
            
            st.session_state.input_username = st.text_input(
                "👤 Username", 
                placeholder="Masukkan username"
            )
            
            password = st.text_input(
                "🔑 Password", 
                type="password",
                placeholder="Masukkan password"
            )
            
            submit = st.form_submit_button("🚀 Masuk", type="primary")
            
            if submit:
                if check_login(st.session_state.input_username, password):
                    login_user()
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
        
        # Info akun contoh
        st.markdown("---")
        st.markdown("""
        **📋 Akun Contoh:**
        - Username: `admin` | Password: `123456`
        - Username: `user` | Password: `2024`
        - Username: `student` | Password: `belajar`
        """)
    
    # Stop execution here if not logged in
    st.stop()

# ============================================================
# 🚀 JIKA SUDAH LOGIN - TAMPILKAN DASHBOARD
# ============================================================

# Terapkan tema
apply_theme(st.session_state.theme)

# ============================================================
# 📌 SIDEBAR - PENGATURAN & MENU
# ============================================================

with st.sidebar:
    # Info User yang login
    st.markdown(f"### 👤 {st.session_state.username}")
    st.markdown("---")
    
    # Pengaturan Theme
    st.markdown("## ⚙️ Pengaturan")
    
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
    
    st.markdown("---")
    
    # Tombol Logout
    if st.button("🚪 Logout"):
        logout_user()
        st.rerun()

# === MENU UTAMA ===

st.sidebar.markdown("---")
st.sidebar.title("📚 Menu Dashboard")

menu_options = [
    "🏠 Dashboard", 
    "✅ To-Do List", 
    "⏱️ Timer Belajar", 
    "🎵 Musik Fokus", 
    "🎨 Indikator Warna"
]

selected_menu = st.sidebar.radio(
    "Pilih Menu:", 
    menu_options,
    label_visibility="collapsed"
)

# ============================================================
# 📌 KONTEN UTAMA PER MENU
# ============================================================

# ═══════════════════════════════════════════════════════════
# 1️⃣ DASHBOARD UTAMA
# ═══════════════════════════════════════════════════════════
if selected_menu == "🏠 Dashboard":
    st.markdown(f"# 📚 Dashboard Belajar")
    st.markdown(f"Selamat datang, **{st.session_state.username}**! 👋")
    st.markdown("Pilih menu di sidebar untuk memulai.")
    
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
        st.metric("🎨 Tema", st.session_state.theme)
    
    st.markdown("---")
    st.success("💡 Tip: Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat)!")

# ═══════════════════════════════════════════════════════════
# 2️⃣ TO-DO LIST
# ═══════════════════════════════════════════════════════════
elif selected_menu == "✅ To-Do List":
    st.markdown "# 📝 To-Do List Harian"
    
    col_input1, col_input2 = st.columns([4, 1])
    with col_input1:
        new_task = st.text_input("Tambah tugas baru:", placeholder="Contoh: Mengerjakan PR Matematika")
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
                st.checkbox("", value=task["done"], key=f"check_{i}", on_change=toggle_task, args=(i,))
            
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

# ═══════════════════════════════════════════════════════════
# 3️⃣ TIMER BELAJAR
# ═══════════════════════════════════════════════════════════
elif selected_menu == "⏱️ Timer Belajar":
    st.markdown("# ⏱️ Timer Belajar (Pomodoro)")
    
    col_timer1, col_timer2 = st.columns([1, 1])
    
    with col_timer1:
        st.markdown("### ⚙️ Pengaturan Waktu")
        mode = st.selectbox("Pilih Mode:", ["25 menit (Belajar)", "5 menit (Istirahat)", "15 menit (Istirahat Panjang)"])
        
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
        menit = st.session_state.time_left // 60
        detik = st.session_state.time_left % 60
        waktu_formatted = f"{menit:02d}:{detik:02d}"
        
        if menit <= 5:
            warna = "🔴"
            status_text = "Waktunya Istirahat!"
        elif menit <= 10:
            warna = "🟡"
            status_text = "Hampir Istirahat"
        else:
            warna = "🟢"
            status_text = "Fokus Penuh"
        
        bg_color = "#2d2d2d" if st.session_state.theme == "Black" else "#ffffff"
        text_color = "#ffffff" if st.session_state.theme == "Black" else "#1a1a1a"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 50px; background: {bg_color}; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='font-size: 100px; margin: 0; color: {text_color};'>{waktu_formatted}</h1>
            <p style='font-size: 24px; color: {text_color};'>{warna} {status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            if st.button("▶️ MULAI", type="primary"):
                st.session_state.timer_running = True
                st.rerun()
        with col_k2:
            if st.button("⏹️ BERHENTI"):
                st.session_state.timer_running = False
                st.rerun()
    
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
    
    st.markdown("### 🎧 Pemutar Musik")
    st.markdown("Pilih musik favorit untuk fokus belajar:")
    
    musik_options = {
        "🎵 Lo-Fi Chill Beats": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "🌊 Ambient Nature Sounds": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "🌙 Piano Relaksasi": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "⚡ Deep Focus Techno": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "☕ Coffee Shop Vibes": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"
    }
    
    selected_music = st.selectbox("Pilih Trek:", list(musik_options.keys()))
    st.audio(musik_options[selected_music], format='audio/mp3', start_time=0)
    
    st.markdown("---")
    st.info("💡 Catatan: Jika audio tidak muncul, coba pilih trek lain.")

# ═══════════════════════════════════════════════════════════
# 5️⃣ INDIKATOR WARNA
# ═══════════════════════════════════════════════════════════
elif selected_menu == "🎨 Indikator Warna":
    st.markdown("# 🎨 Simulasi Indikator Warna")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Status Keseluruhan")
        
        total = len(st.session_state.tasks)
        if total > 0:
            selesai = sum(1 for t in st.session_state.tasks if t["done"])
            progress = selesai / total
            
            st.progress(progress)
            st.markdown(f"**Progres:** {int(progress * 100)}%")
            
            if progress >= 1.0:
                st.success("✅ Semua tugas selesai!")
            elif progress >= 0.7:
                st.info("🟡 Hampir selesai!")
            elif progress >= 0.3:
                st.warning("🟠 Sedang berjalan...")
            else:
                st.error("🔴 Baru memulai!")
        else:
            st.warning("Belum ada tugas. Tambahkan di menu To-Do List!")
    
    with col2:
        st.markdown("### ⏱️ Status Timer")
        
        menit = st.session_state.time_left // 60
        detik = st.session_state.time_left % 60
        
        if st.session_state.timer_running:
            if menit >= 20:
                st.success("🟢 Fokus Penuh")
            elif menit >= 10:
                st.warning("🟡 Fokus Baik")
            elif menit >= 5:
                st.info("🟠 Hampir Istirahat")
            else:
                st.error("🔴 Waktunya Istirahat!")
        else:
            st.info("⚪ Timer Standby")
        
        st.markdown(f"**Sisa Waktu:** {menit:02d}:{detik:02d}")
    
    st.markdown("---")
    st.markdown("### 📈 Grafik Aktivitas")
    
    if total > 0:
        data = {'Status': ['Selesai', 'Tertunda'], 'Jumlah': [sum(1 for t in st.session_state.tasks if t["done"]), sum(1 for t in st.session_state.tasks if not t["done"])]}
        df = pd.DataFrame(data)
        st.bar_chart(df.set_index('Status'))
    else:
        st.info("Tidak ada data untuk ditampilkan.")
