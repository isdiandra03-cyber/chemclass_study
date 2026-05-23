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
menu_options = ["🏠 Dashboard", "✅ To-Do List", "⏱️ Timer Belajar", "🎵 Musik Fokus", "🎨 Indikator Warna"]
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

# ============================
# 5. MENU INDIKATOR WARNA
# ============================
elif selected_menu == "🎨 Indikator Warna":
    st.markdown("# 🎨 Simulasi Indikator Warna")
    
    st.markdown("Visualisasi indikator warna untuk membantu monitoring tugas dan timer.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Status Keseluruhan")
        
        # Hitung persentase progres
        total = len(st.session_state.tasks)
        if total > 0:
            selesai = sum(1 for t in st.session_state.tasks if t["done"])
            progress = selesai / total
            
            # Progress bar dengan warna
            st.progress(progress)
            st.write(f"**Progres:** {int(progress * 100)}%")
            
            # Indikator warna
            if progress >= 1.0:
                st.success("✅ Semua tugas selesai!")
            elif progress >= 0.7:
                st.info("🟡 Hampir selesai!")
            elif progress >= 0.3:
                st.warning("🟠 Sedang berjalan...")
            else:
                st.error("🔴 Baru memulai!")
        else:
            st.info("Belum ada tugas. Tambahkan di menu To-Do List!")
    
    with col2:
        st.subheader("⏱️ Status Timer")
        
        menit = st.session_state.time_left // 60
        if st.session_state.timer_running:
            if menit >= 20:
                st.success("🟢_Fokus Penuh")
            elif menit >= 10:
                st.warning("🟡_Fokus Baik")
            elif menit >= 5:
                st.info("🟠_Hampir Istirahat")
            else:
                st.error("🔴_Waktunya Istirahat!")
        else:
            st.info("⚪ Timer Standby")
    
    # Visualisasi Chart
    st.markdown("---")
    st.subheader("📈 Grafik Aktivitas")
    
    if total > 0:
        # Data untuk chart sederhana
        data = {
            'Status': ['Selesai', 'Tertunda'],
            'Jumlah': [
                sum(1 for t in st.session_state.tasks if t["done"]),
                sum(1 for t in st.session_state.tasks if not t["done"])
            ]
        }
        df = pd.DataFrame(data)
        st.bar_chart(df.set_index('Status'))
    else:
        st.info("Tidak ada data untuk ditampilkan.")
