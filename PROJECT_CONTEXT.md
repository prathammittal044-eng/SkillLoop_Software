# SkillLoop — Quick AI Context & Memory Checkpoint

> **Full Documentation:** See `../../Documentation/` for complete architectural guides, database schemas, and setup manuals.

* **Developer:** Pratham Mittal (ABESIT Ghaziabad, CSE Semester 3)
* **Project:** SkillLoop (College Peer-to-Peer Barter Skill Exchange Platform)
* **Stack:** Nuxt 3 (Port 3000) + Flask / Flask-SocketIO (Port 5000) + SQLite (`skillloop.db`)
* **Design System:** Material You palette (`#543ce0` primary, `#fbf4ff` background, `#f6edff` container, `#34284f` on-surface). Google Material Symbols throughout.
* **Key Features Completed:**
  1. **Resume Studio (`frontend/pages/resume.vue`):** ABESIT search, current student enrollment toggle, categorized skills (Languages, Frameworks, Tools), live ATS canvas, PDF export.
  2. **Chat & Video Calling (`frontend/pages/chat.vue`):** OpenRelay TURN servers, candidate queueing fix, progressive media fallback (HD $\to$ SD $\to$ Video only $\to$ Audio only), screen sharing, in-app diagnostic test.
  3. **Dashboard, Quiz & Leaderboard:** Harmonized navbars, verified skill badges, credit balance tracking.

### To Resume Work After Reset:
1. Ensure Flask is running: `py app.py`
2. Ensure Nuxt is running: `cd frontend && npm run dev`
3. If testing remote video calling, run: `.\start_https_tunnel.bat`
