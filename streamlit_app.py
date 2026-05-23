import streamlit as st
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Belajar</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Sidebar Menu -->
        <nav class="sidebar">
            <h2>Menu Dashboard</h2>
            <ul>
                <li onclick="showSection('todo')" class="active">To Do List</li>
                <li onclick="showSection('timer')">Timer Belajar</li>
                <li onclick="showSection('music')">Musik Fokus</li>
            </ul>
        </nav>

        <!-- Konten Utama -->
        <main class="content">
            
            <!-- Bagian To Do List -->
            <div id="todo" class="section active-section">
                <h1>To-Do List Harian</h1>
                <div class="input-group">
                    <input type="text" id="taskInput" placeholder="Apa tugasmu hari ini?">
                    <button onclick="addTask()">Tambah</button>
                </div>
                <ul id="taskList"></ul>
            </div>

            <!-- Bagian Timer -->
            <div id="timer" class="section">
                <h1>Timer Belajar (Pomodoro)</h1>
                <div class="timer-display" id="display">25:00</div>
                <div class="timer-controls">
                    <button onclick="startTimer()">Mulai</button>
                    <button onclick="stopTimer()">Berhenti</button>
                    <button onclick="resetTimer()">Reset</button>
                </div>
            </div>

            <!-- Bagian Musik -->
            <div id="music" class="section">
                <h1>Musik Fokus (Lo-Fi)</h1>
                <div class="music-player">
                    <p>Tekan Play untuk memulai musik.</p>
                    <!-- Ganti src dengan link musik Anda atau file di repo -->
                    <audio id="audioPlayer" controls>
                        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
                        Browser Anda tidak mendukung audio.
                    </audio>
                </div>
            </div>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    background-color: #f4f4f9;
    color: #333;
}

.container {
    display: flex;
    height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 250px;
    background-color: #2c3e50;
    color: white;
    padding: 20px;
}

.sidebar h2 {
    margin-bottom: 30px;
    text-align: center;
}

.sidebar ul {
    list-style: none;
    padding: 0;
}

.sidebar li {
    padding: 15px;
    cursor: pointer;
    border-radius: 5px;
    transition: background 0.3s;
    margin-bottom: 5px;
}

.sidebar li:hover, .sidebar li.active-menu {
    background-color: #34495e;
}

/* Konten Utama */
.content {
    flex: 1;
    padding: 40px;
}

.section {
    display: none; /* Defaultnya disembunyikan */
    animation: fadeIn 0.5s;
}

.active-section {
    display: block;
}

/* TO DO LIST */
.input-group {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

input[type="text"] {
    padding: 10px;
    width: 70%;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    padding: 10px 20px;
    background-color: #27ae60;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover { background-color: #2ecc71; }

ul { list-style: none; padding: 0; }
li.task-item {
    background: white;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
}

/* TIMER */
.timer-display {
    font-size: 80px;
    font-weight: bold;
    text-align: center;
    margin: 40px 0;
    color: #2c3e50;
}

/* MUSIC */
.music-player {
    text-align: center;
    margin-top: 50px;
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

audio {
    width: 100%;
    margin-top: 20px;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
// --- LOGIKA MENU ---
function showSection(sectionId) {
    // Sembunyikan semua section
    const sections = document.querySelectorAll('.section');
    sections.forEach(sec => sec.classList.remove('active-section'));

    // Tampilkan section yang diklik
    document.getElementById(sectionId).classList.add('active-section');

    // Update menu aktif
    const menuItems = document.querySelectorAll('.sidebar li');
    menuItems.forEach(item => item.classList.remove('active-menu'));
    
    // Cari elemen LI yang sesuai dengan onclick (simplifikasi)
    event.target.classList.add('active-menu');
}

// --- LOGIKA TO DO LIST ---
function addTask() {
    const input = document.getElementById('taskInput');
    const taskText = input.value;

    if (taskText === '') {
        alert("Tulis tugasnya dulu!");
        return;
    }

    const li = document.createElement('li');
    li.className = 'task-item';
    li.innerHTML = `${taskText} <button style="background:red" onclick="this.parentElement.remove()">Hapus</button>`;

    document.getElementById('taskList').appendChild(li);
    input.value = '';
}

// --- LOGIKA TIMER ---
let timerInterval;
let timeLeft = 25 * 60; // 25 menit dalam detik
let isRunning = false;

function updateTimerDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    document.getElementById('display').textContent = 
        `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    timerInterval = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            updateTimerDisplay();
        } else {
            clearInterval(timerInterval);
            alert("Waktu belajar selesai! Istirahatlah.");
            isRunning = false;
        }
    }, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
    isRunning = false;
}

function resetTimer() {
    stopTimer();
    timeLeft = 25 * 60;
    updateTimerDisplay();
}
