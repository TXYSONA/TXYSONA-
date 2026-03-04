══════════════════════════════════════════════
   TXYSONA — Python Flask Version
   Made by Satyam Keshari
══════════════════════════════════════════════

📁 FILES:
   app.py                    → Main Python backend
   requirements.txt          → Python libraries
   templates/index.html      → TXYSONA app
   templates/admin.html      → Admin panel
   templates/admin_login.html→ Admin login page

══════════════════════════════════════════════
STEP 1 — app.py mein apni details daalo
══════════════════════════════════════════════

app.py file mein sirf yeh 3 cheezein badlo:

   JSONBIN_MASTER_KEY = 'YOUR_MASTER_KEY'   ← Apni JSONBin key
   ADMIN_USERNAME     = 'admin'              ← Admin username
   ADMIN_PASSWORD     = 'admin@txysona123'  ← Admin password

══════════════════════════════════════════════
STEP 2 — Render.com par Free Host Karo
══════════════════════════════════════════════

1. render.com par jaao → Sign Up (GitHub se)
2. "New Web Service" click karo
3. "Deploy from existing code" → files upload karo
   (ya GitHub par push karo)
4. Settings:
   - Language: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: python app.py
5. Deploy click karo → Free URL milega!

══════════════════════════════════════════════
STEP 3 — Local Test (Optional)
══════════════════════════════════════════════

Terminal mein:
   pip install -r requirements.txt
   python app.py

Browser mein:
   http://localhost:5000       → TXYSONA app
   http://localhost:5000/admin → Admin panel

══════════════════════════════════════════════
ADMIN PANEL FEATURES:
══════════════════════════════════════════════

   URL:      yoursite.com/admin
   Login:    admin / admin@txysona123

   📊 Dashboard  → Visitors & queries overview
   👁️ Visitors   → IP address ke saath!
   🔍 Queries    → Users ne kya poocha
   🔴🟢 Toggle   → App band/chalu karo
   🗑️ Clear      → Data delete karo

══════════════════════════════════════════════
KYU PYTHON VERSION SAFE HAI?
══════════════════════════════════════════════

   ✅ JSONBin key server par hai — browser mein nahi
   ✅ Admin login server par check hota hai
   ✅ Code koi copy nahi kar sakta
   ✅ IP addresses track hote hain
   ✅ Har browser par kaam karta hai

══════════════════════════════════════════════
