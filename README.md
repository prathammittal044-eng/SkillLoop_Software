<div align="center">

# 🔄 SkillLoop

**Decentralized Campus Skill Barter & Proof-of-Work Verification Platform**

*Bridging the college "degree-to-skill" divide through peer-to-peer knowledge exchange, AI-powered adaptive testing, live WebRTC video mentoring, and dynamic ATS-verified resumes.*

[![Nuxt 3](https://img.shields.io/badge/Nuxt-4.5.2-00DC82?style=for-the-badge&logo=nuxtdotjs&logoColor=white)](https://nuxt.com/)
[![Vue 3](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.io-4.8-010101?style=for-the-badge&logo=socketdotio&logoColor=white)](https://socket.io/)
[![WebRTC](https://img.shields.io/badge/WebRTC-Real--Time-333333?style=for-the-badge&logo=webrtc&logoColor=white)](https://webrtc.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-8E75C2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

[Features](#-key-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [One-Click Hosting](#-one-click-public-hosting) • [Project Structure](#-project-structure)

</div>

---

## 💡 The Problem & The Solution

In traditional college ecosystems, students face critical hurdles:
1. **The Financial Barrier in Mentorship:** Paid tutoring platforms are prohibitively expensive for college students, while free forums lack 1-on-1 commitment.
2. **Skill Decay (Stale Certifications):** A 2nd-year student passes a quiz in React, forgets it by 4th year, but static platforms still falsely certify them as an "Expert" to recruiters.
3. **Resume Puffery:** Resumes are filled with unverified self-assertions and generic bullet points with no cryptographic accountability or peer review.
4. **Campus NAT & Firewall Isolation:** College Wi-Fi networks enforce strict symmetric NAT and firewalls that block standard P2P video calling between students.

### 🌟 How SkillLoop Solves This:

* ⏱️ **Zero-Currency TimeBank Economy:** 1 hour of teaching = 1 Time Credit. Learn any skill in exchange for teaching yours. Zero money ever changes hands.
* 💓 **Proof-of-Work Half-Life (6-Month Decay Engine):** Verifications aren't static trophies; they behave like a heartbeat. Verifications expire after 180 days unless renewed through an **A.E.E. (Applied Exchange & Execution)** session with a peer.
* 📄 **Cryptographic ATS Resume Studio:** Automatically compiles verified skills, peer ratings, and campus node signatures into an ATS-friendly, recruiter-ready resume with real-time scoring (0–100%).
* 🎥 **Firewall-Traversing WebRTC Video Calling:** Powered by Metered STUN/TURN relay infrastructure, enabling ultra-low-latency 1-on-1 video calls, screen sharing, and code debugging across any college Wi-Fi or cellular network.

---

## ✨ Key Features

### 1. ⏱️ The TimeBank Ledger
- **Equitable Exchange:** Every user starts with welcome credits. Teaching a peer earns +1 credit; booking a mentor spends 1 credit.
- **Peer Reputation Engine:** Students rate each session (1–5 stars) with written peer feedback, directly updating campus leaderboard ranks.

### 2. 💓 Proof-of-Work Half-Life (Skill Decay System)
- **Active Heartbeat (0–120 Days):** Verified green badge with days remaining displayed on profile and resume.
- **Warning Window (121–180 Days):** Amber warning indicator prompting the mentor to teach or execute the skill.
- **Decayed Status (>180 Days):** Stale skills become dormant and hidden from verified recruiter queries until revived.
- **A.E.E. Handshake Protocol:** When a mentor conducts a session, they log execution notes. Once the learner confirms the session, the mentor's 180-day heartbeat resets automatically and both earn bonus platform XP.

### 3. 🎯 AI-Powered Adaptive Quiz Engine
- **Dynamic Question Generation:** Integrates with Google Gemini AI to generate timed, difficulty-tiered multiple-choice quizzes tailored to programming languages, frameworks, and engineering concepts.
- **Anti-Cheat Enforcement:** Strict timers (15s per question), anti-inspect guards, and immediate automated scoring.
- **Instant Verification:** Achieving $\ge 70\%$ score instantly issues a verified skill badge with cryptographic hash.

### 4. 📄 Dynamic ATS Resume Studio
- **Dual Export Formats:**
  - **Modern Campus Node:** High-density, branded layout with campus node IDs, verification hashes, and TimeBank metrics.
  - **Classic ATS Standard:** Clean, single-column monochrome format optimized for enterprise Applicant Tracking Systems.
- **Real-Time Completeness Meter:** Dynamic 0–100% ATS score indicator providing actionable feedback to improve resume readiness.
- **Automatic DB Synchronization:** Pre-fills contact details, department, semester, coursework, and verified skill badges directly from the student's database record.
- **High-Fidelity PDF Export:** Native, browser-based one-click print-to-PDF formatting.

### 5. 📹 WebRTC Mentoring & Real-Time Collaboration
- **1-on-1 Video & Audio:** Peer-to-peer WebRTC connection with automated candidate queueing and graceful resolution fallback.
- **STUN/TURN Traversal:** Dual-tier ICE architecture with Google STUN + Metered.ca TURN relays for bypassing campus NATs and mobile carrier CGNATs.
- **Screen Sharing:** Instant desktop/window sharing for live peer code walkthroughs.
- **Socket.IO Chat:** Instant text messaging, typing indicators, file attachment sharing, and call signaling.
- **Built-in Diagnostics:** In-app connection tester validating camera, microphone, and ICE candidate generation before calls.

---

## 🏛️ Architecture

```
                          ┌─────────────────────────────────────┐
                          │         Student Web Client          │
                          │   (Nuxt 4 / Vue 3 + Tailwind CSS)   │
                          └──────────────┬──────────────────────┘
                                         │
                 HTTP REST API (3000 -> 5000)   Socket.IO / WebRTC Signaling
                                         │
                                         ▼
                          ┌─────────────────────────────────────┐
                          │         Flask Backend Engine        │
                          │     (Python 3.10+ / Eventlet)       │
                          └──────┬──────────┬──────────┬────────┘
                                 │          │          │
         ┌───────────────────────┘          │          └──────────────────────┐
         ▼                                  ▼                                 ▼
┌─────────────────┐             ┌─────────────────────┐             ┌─────────────────┐
│ SQLite Database │             │  Google Gemini AI   │             │   Metered.ca    │
│ (skillloop.db)  │             │   (Quiz Generator)  │             │  STUN/TURN RTC  │
└─────────────────┘             └─────────────────────┘             └─────────────────┘
```

---

## 🧰 Tech Stack

| Domain | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend Framework** | **Nuxt 4 / Vue 3** | Composition API, reactive state, fast Vite compilation |
| **Styling & UI** | **Tailwind CSS + Material Symbols** | Clean Material You inspired design palette |
| **Backend API** | **Python 3 / Flask 3.0** | REST API endpoints, session authentication, routing |
| **Real-Time Engine** | **Flask-SocketIO + Eventlet** | Chat, live presence, signaling, A.E.E. notifications |
| **WebRTC Infrastructure** | **RTCPeerConnection + Metered.ca** | Low-latency P2P video calling & TURN relay traversal |
| **Artificial Intelligence** | **Google Gemini (`gemini-1.5`)** | Dynamic quiz generation and assessment |
| **Database** | **SQLite 3** | ACID relational storage (`users`, `verifications`, `aee_sessions`) |
| **Tunneling / Hosting** | **Ngrok / Cloudflare** | Temporary public deployment for remote demoing |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** installed ([Download Python](https://www.python.org/))
- **Node.js 18+** installed ([Download Node.js](https://nodejs.org/))

---

### Option A: The 1-Click Launcher (Recommended for Windows)

Simply double-click:
```bash
Run.bat
```
This batch script automatically launches the Flask backend on port `5000` and the Nuxt frontend on port `3000` in separate, labeled command prompt windows!

---

### Option B: Manual Setup

#### 1. Clone the repository
```bash
git clone https://github.com/prathammittal044-eng/SkillLoop_Software.git
cd SkillLoop_Software
```

#### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
copy .env.example .env     # On Windows
cp .env.example .env       # On Linux/macOS
```
Open `.env` and add your **Google Gemini API Key** (free at [Google AI Studio](https://aistudio.google.com/)) and optional **Metered TURN** credentials.

#### 3. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start Flask server (Port 5000)
python app.py
```

#### 4. Frontend Setup
Open a new terminal window:
```bash
cd frontend

# Install Node dependencies
npm install

# Start Nuxt development server (Port 3000)
npm run dev
```

#### 5. Open in Browser
Navigate to **`http://localhost:3000`** in your browser to experience SkillLoop!

---

## 🌐 One-Click Public Hosting

Need to demonstrate SkillLoop to teammates, friends, or recruiters across different Wi-Fi networks?

Run:
```bash
start_hosting.bat
```

**What it does:**
1. Automatically clears any orphaned processes on ports `5000` and `3000`.
2. Starts the Flask backend.
3. Compiles and starts the Nuxt frontend.
4. Launches an **Ngrok HTTP Tunnel** exposing port `3000` to the internet.
5. Displays a secure **Public HTTPS URL** you can open on any mobile phone or external computer!

---

## 📁 Project Structure

```text
SkillLoop_Software/
├── app.py                     # Core Flask application, auth, REST endpoints, and decay engine
├── database.py                # SQLite connection pool, schema definitions, and migration logic
├── chat_events.py             # Socket.IO handlers for messaging & WebRTC signaling
├── chat_routes.py             # Chat history, active conversation lists, attachment uploads
├── turn_config.py             # STUN & Metered/Cloudflare TURN server credentials provider
├── institutions.py            # Indian campus database (ABESIT, IITs, DTU, AKGEC, etc.)
├── seed.py                    # Database seeder with realistic test users & skills
├── config.py                  # Environment and database configuration
├── requirements.txt           # Minimal, lightweight Python dependencies
├── skillloop.db               # Seeded SQLite database ready for immediate testing
├── Run.bat                    # 1-Click local launcher for backend + frontend
├── start_hosting.bat          # 1-Click public hosting launcher with Ngrok tunnel
│
├── frontend/                  # Nuxt 4 + Vue 3 Application
│   ├── pages/
│   │   ├── index.vue          # Landing page showcasing the SkillLoop value proposition
│   │   ├── login.vue          # Campus student authentication
│   │   ├── register.vue       # Student registration with skill & department selection
│   │   ├── dashboard.vue      # Main hub: TimeBank balance, skill heartbeat, A.E.E. logging
│   │   ├── chat.vue           # Real-time chat & WebRTC video calling with diagnostics
│   │   ├── quiz.vue           # Gemini AI adaptive skill verification tests
│   │   ├── resume.vue         # Interactive ATS Resume Studio with PDF export
│   │   └── leaderboard.vue    # Campus-wide peer rating and mentorship leaderboards
│   ├── nuxt.config.ts         # Nuxt configuration, Tailwind setup, proxy routes
│   └── package.json           # Frontend dependency manifest
│
├── stitch_html/               # Static design reference mockups
└── documentation/             # WebRTC context and architectural design guides
```

---

## 🧪 Testing Credentials

The pre-seeded `skillloop.db` includes demo accounts for immediate testing:

| Role | Username | Password | Time Credits | Primary Skills |
| :--- | :--- | :--- | :--- | :--- |
| **Student / Mentor** | `alice` | `password` | 10 | Python, React, WebRTC |
| **Student / Peer** | `bob99` | `password` | 5 | Java, Data Structures |
| **Student / Designer** | `eve_design` | `password` | 8 | UI/UX, Figma |

*Or register a new account instantly with your campus email.*

---

## 👨‍💻 Author

**Pratham Mittal**  
Computer Science & Engineering  
ABES Institute of Technology (ABESIT), Ghaziabad  
- GitHub: [@prathammittal044-eng](https://github.com/prathammittal044-eng)

---

## 📄 License

This project is developed as an academic and innovation prototype under the **MIT License**.
Feel free to fork, explore, and build upon it!
