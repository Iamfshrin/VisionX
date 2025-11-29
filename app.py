from flask import Flask, request, render_template_string, redirect, url_for
import csv
import os

app = Flask(__name__)

CSV_FILE = "leads.csv"

LANDING_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>VisionX Academy – Bepul master klass</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary: #00bcd4;   /* logo teal */
            --primary-dark: #008ba3;
            --accent:  #ff6b3d;   /* logo orange-ish */
            --text-main: #0f172a;
            --bg-body: #020617;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background:
              radial-gradient(circle at top, #0f172a 0, #020617 48%, #020617 100%);
            color: var(--text-main);
        }
        .wrapper {
            max-width: 520px;
            margin: 0 auto;
            padding: 16px 14px 40px;
        }
        .brand-row {
            display:flex;
            align-items:center;
            gap:10px;
            margin-bottom:14px;
        }
        .brand-logo-img {
            width:44px;
            height:44px;
            border-radius:12px;
            object-fit:cover;
            background:#000;
        }
        .brand-text {
            display:flex;
            flex-direction:column;
            gap:2px;
        }
        .brand-name {
            font-weight:700;
            letter-spacing:0.06em;
            font-size:13px;
            text-transform:uppercase;
            color:#e5e7eb;
        }
        .brand-sub {
            font-size:11px;
            color:#9ca3af;
        }

        .card {
            background: linear-gradient(145deg, #020617 0%, #020617 40%, #03212a 100%);
            border-radius:26px;
            padding:22px 18px 26px;
            box-shadow:0 24px 60px rgba(0,0,0,0.7);
            position:relative;
            overflow:hidden;
            border:1px solid rgba(148,163,184,0.35);
        }
        .card::before {
            content:"";
            position:absolute;
            inset:-40%;
            background:
              radial-gradient(circle at top right, rgba(0,188,212,0.16), transparent 55%),
              radial-gradient(circle at bottom left, rgba(34,197,94,0.10), transparent 55%);
            opacity:1;
            pointer-events:none;
        }
        .card-inner { position:relative; z-index:1; }

        .badge {
            display:inline-flex;
            align-items:center;
            gap:8px;
            background:rgba(15,23,42,0.8);
            border:1px solid rgba(148,163,184,0.6);
            color:#e5e7eb;
            padding:6px 14px;
            border-radius:999px;
            font-size:12px;
            margin-bottom:14px;
        }
        .badge span.icon { font-size:16px; }

        .hero-grid {
            display:flex;
            align-items:center;
            gap:14px;
            margin-bottom:10px;
        }
        @media (max-width: 480px) {
            .hero-grid { flex-direction:column-reverse; align-items:flex-start; }
        }
        .hero-text { flex:1; }

        h1 {
            font-size:22px;
            line-height:1.25;
            margin-bottom:6px;
            color:#f9fafb;
        }
        .accent-text { color: var(--accent); }
        .subtitle {
            font-size:14px;
            color:#cbd5f5;
            margin-bottom:4px;
        }
        .tagline {
            font-size:14px;
            font-weight:600;
            color:#e5e7eb;
            margin:8px 0 6px;
        }

        .hero-photo-wrap {
            width:150px;
            height:190px;
            position:relative;
            flex-shrink:0;
        }
        .hero-bg-pill {
            position:absolute;
            inset:0;
            border-radius:36px;
            background:
              radial-gradient(circle at 0% 0%, rgba(0,188,212,0.3), transparent 55%),
              radial-gradient(circle at 100% 100%, rgba(16,185,129,0.32), transparent 55%);
            filter:blur(0.5px);
        }
        .hero-photo {
            position:absolute;
            inset:-6px -6px 0 -6px;
            background:url('/static/person.PNG') center bottom/cover no-repeat;
        }

        form { margin-top:12px; text-align:left; }
        label {
            font-size:12px;
            font-weight:600;
            display:block;
            margin-bottom:4px;
            color:#e5e7eb;
        }
        input {
            width:100%;
            padding:9px 11px;
            border-radius:12px;
            border:1px solid rgba(148,163,184,0.9);
            font-size:14px;
            margin-bottom:9px;
            background:rgba(15,23,42,0.8);
            color:#e5e7eb;
        }
        input::placeholder { color:#6b7280; }
        input:focus {
            outline:none;
            border-color: var(--primary);
            box-shadow:0 0 0 1px rgba(0,188,212,0.5);
            background:rgba(15,23,42,0.95);
        }

        .cta-btn {
            display:block;
            width:100%;
            border:none;
            cursor:pointer;
            background:linear-gradient(135deg,var(--accent),#ff914d);
            color:#fff;
            font-weight:700;
            font-size:15px;
            padding:12px 10px;
            border-radius:999px;
            box-shadow:0 16px 36px rgba(249,115,22,0.65);
            margin:10px 0 6px;
            letter-spacing:0.5px;
        }
        .cta-btn:hover { filter:brightness(1.06); }

        .privacy {
            font-size:10px;
            color:#9ca3af;
            margin-top:2px;
        }
        .section-title {
            font-weight:700;
            margin:14px 0 6px;
            font-size:15px;
            text-align:left;
            color:#e5e7eb;
        }
        ul.benefits {
            text-align:left;
            list-style:none;
            font-size:13px;
            color:#e5e7eb;
        }
        ul.benefits li {
            margin-bottom:7px;
            padding-left:24px;
            position:relative;
        }
        ul.benefits li::before {
            content:"";
            position:absolute;
            left:7px;
            top:6px;
            width:9px;
            height:9px;
            border-radius:999px;
            background:linear-gradient(135deg,var(--primary),#22c55e);
        }
        .footer-note {
            font-size:11px;
            color:#9ca3af;
            margin-top:6px;
            text-align:left;
        }
    </style>
</head>
<body>
<div class="wrapper">
    <div class="brand-row">
        <img src="/static/logo.jpg" alt="VisionX Academy" class="brand-logo-img">
        <div class="brand-text">
            <div class="brand-name">VISIONX ACADEMY</div>
            <div class="brand-sub">Smmdan kuchli sotuvgacha master klass</div>
        </div>
    </div>

    <div class="card">
        <div class="card-inner">
            <div class="badge">
                <span class="icon">🎯</span>
                <span>Bepul master klass · joylar cheklangan</span>
            </div>

            <div class="hero-grid">
                <div class="hero-text">
                    <h1>Smmdan <span class="accent-text">kuchli sotuvgacha</span> bo‘lgan yo‘lni 1 master klassda ko‘ring.</h1>
                    <p class="subtitle">Daromadingizni oshirish uchun haqiqiy natija bergan kontent va sotuv skriptlari.</p>
                </div>
                <div class="hero-photo-wrap">
                    <div class="hero-bg-pill"></div>
                    <div class="hero-photo"></div>
                </div>
            </div>

            <p class="tagline">Bepul master klassda siz:</p>
            <ul class="benefits">
                <li>Sotadigan kontent yaratish formulasini olasiz.</li>
                <li>Har qanday tovarni 3 bosqichda sotadigan AIDA texnikasini o‘rganasiz.</li>
                <li>Mavsumiy va tezkor sotuvlar uchun tayyor skriptlardan foydalanishni bilib olasiz.</li>
            </ul>

            <form method="POST" action="{{ url_for('index') }}">
                <label for="full_name">To‘liq ismingiz</label>
                <input type="text" id="full_name" name="full_name" required placeholder="Ism va familiya">

                <label for="phone">Telefon raqamingiz</label>
                <input type="tel" id="phone" name="phone" required placeholder="+998 90 123 45 67">

                <button type="submit" class="cta-btn">BEPUL RO‘YXATDAN O‘TISH »</button>
                <p class="privacy">Ma’lumotlaringiz faqat VisionX Academy master klassi bo‘yicha bog‘lanish uchun ishlatiladi.</p>
            </form>

            <p class="footer-note">Formani to‘ldirgach, keyingi sahifada Telegram kanalga qo‘shilish havolasini olasiz.</p>
        </div>
    </div>
</div>
</body>
</html>
"""

THANK_YOU_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Oxirgi qadam – VisionX Academy</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary:#00bcd4;
        }
        * { box-sizing:border-box; margin:0; padding:0; }
        body {
            font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;
            background:radial-gradient(circle at top,#0f172a 0,#020617 55%,#020617 100%);
            color:#e5e7eb;
        }
        .wrapper {
            max-width:480px;
            margin:0 auto;
            padding:40px 18px 50px;
            text-align:center;
        }
        .card {
            background:#020617;
            border-radius:24px;
            padding:28px 22px 30px;
            box-shadow:0 24px 60px rgba(15,23,42,0.9);
            border:1px solid rgba(148,163,184,0.5);
        }
        h1 { font-size:24px; margin-bottom:12px; }
        .accent { color:var(--primary); }
        p { font-size:14px; line-height:1.5; margin-bottom:14px; }
        .arrow { font-size:30px; margin:6px 0 16px; }
        .tg-btn {
            display:block;
            width:100%;
            text-decoration:none;
            text-align:center;
            background:linear-gradient(135deg,var(--primary),#38bdf8);
            color:#0b1120;
            font-weight:700;
            font-size:15px;
            padding:12px 10px;
            border-radius:999px;
            box-shadow:0 18px 40px rgba(56,189,248,0.7);
            letter-spacing:0.5px;
        }
        .tg-btn:hover { filter:brightness(1.08); }
        .note { font-size:12px; color:#9ca3af; margin-top:12px; }
    </style>
</head>
<body>
<div class="wrapper">
    <div class="card">
        <h1>Oxirgi qadam <span class="accent">qoldi!</span></h1>
        <p>Master klass sanasi, manzili va materiallari faqat Telegram kanalimizda bo‘ladi.</p>
        <p>Quyidagi tugmani bosing va <strong>VisionX Academy</strong> kanaliga qo‘shiling.</p>
        <div class="arrow">⬇️</div>
        <a class="tg-btn" href="https://t.me/visionX_academy" target="_blank">
            TELEGRAMGA OBUNA BO‘LISH
        </a>
        <p class="note">Kanalga kirganingizdan so‘ng “Join”ni bosing. Eslatma va uy vazifalar ham shu yerda bo‘ladi.</p>
    </div>
</div>
</body>
</html>
"""

def save_lead(full_name, phone):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["full_name", "phone"])
        writer.writerow([full_name, phone])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        if full_name and phone:
            save_lead(full_name, phone)
            return redirect(url_for("thank_you"))
    return render_template_string(LANDING_TEMPLATE)

@app.route("/thank-you")
def thank_you():
    return render_template_string(THANK_YOU_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)
