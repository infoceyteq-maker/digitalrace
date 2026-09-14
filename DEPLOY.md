# CEYTEQ — Deploy (Live කරන ආකාරය)

**දැනට තියෙන තත්ත්වය**

| දේ | තත්ත්වය |
|---|---|
| Code (pages 19 + backend) | ✅ push කරලා — branch `arena/01a0a0ff-digitalrace`, commit `18af648` |
| Live demo (backend + database + admin) | ✅ දැන්ම බලන්න: **https://8000-ivjfl8obmi6mzmzflsqsl.e2b.app** |
| Pull request | ✅ [PR #1](https://github.com/infoceyteq-maker/digitalrace/pull/1) — merge කරන එකයි ඉතුරු |
| GitHub Pages (www.ceyteq.linkpc.net) | ⏳ **`main` branch** එකෙන් build වෙනවා — PR එක merge කරාම ~1 මිනිත්තුවකින් auto update වෙනවා |
| Backend (database + admin) | ⏳ host එකක් ඕන (පහළ Step 2) — config files ඔක්කොම හදලා තියෙනවා |

> ⚠️ GitHub Pages එකට Python run කරන්න බෑ. ඒ නිසා **pages + database** දෙකම live කරන්න backend එකක් අවශ්‍යයි. Backend එක නැතුවත් site එක වැඩ කරනවා — contact form එක WhatsApp වලට fallback වෙනවා, Offers පිටුව built-in list එකෙන් පෙන්නනවා, admin panel එක "server offline" කියලා කියනවා (කැඩෙන්නේ නෑ).

---

## Step 1 — Public site එක live කරන්න (1 click, 1 minute)

1. Open **https://github.com/infoceyteq-maker/digitalrace/pull/1**
2. **Merge pull request** → **Confirm merge**
3. Actions tab එකේ "Build check" run එක green වෙනකම් ඉන්න (~1 min) → Pages එක auto build වෙනවා
4. **https://www.ceyteq.linkpc.net** එක open කරලා මේවා check කරන්න:
   - Home page එක English වලින්, "Digital Race" menu item එක **රතු**
   - හැම page එකේම පහළ දකුණේ **🏁 Start Digital Race** (රතු) + WhatsApp (කොළ) buttons
   - **Offers** පිටුවේ ෆ්ලයර් 10 පෙනෙනවා (කලින් කැඩිලා තිබ්බා)
   - Digital Race පිටුවේ video එක play වෙනවා
   - **Learn & Earn** පිටුව අලුතින් තියෙනවා

*(මම merge කරන්නේ නෑ — මේ session එක `arena/...` branch එකට fix කරලා තියෙන නිසා. ඔබ merge කරන එක තමයි branch rule එකට ගැලපෙන්නේ.)*

---

## Step 2 — Backend + Database live කරන්න

Backend එක **Python 3 විතරයි** ඕන (extra package නෑ). Config files repo එකේ තියෙනවා: `Dockerfile`, `docker-compose.yml`, `render.yaml`, `fly.toml`, `Procfile`.

### Environment variables

| Key | අර්ථය | උදාහරණය |
|---|---|---|
| `CEYTEQ_ADMIN_PASSWORD` | admin password (පළමු run එකේදී create වෙනවා) | `MyStrongPass2026!` |
| `CEYTEQ_ADMIN_USER` | admin username (default `admin`) | `admin` |
| `CEYTEQ_DATA_DIR` | database + uploads තියෙන තැන (**persistent volume** එකකට දෙන්න) | `/var/data` හෝ `/data` |
| `PORT` | host එක දෙන port (auto) | `10000` |

### 🅰️ Render.com (ලේසිම) — `render.yaml` තියෙනවා

1. [render.com](https://render.com) → **New** → **Blueprint** → GitHub repo එක තෝරන්න (`digitalrace`)
2. Render `render.yaml` කියවලා service එක හදනවා → **CEYTEQ_ADMIN_PASSWORD** එක type කරන්න
3. **Apply** → 2-3 මිනිත්තුවකින් `https://ceyteq-site.onrender.com` live

⚠️ Free plan එකේ **persistent disk නෑ** → redeploy එකකදී leads/flyers නැති වෙනවා. Business එකට `starter` plan (disk 1GB) එක හොඳයි. Free එකෙන් test කරන්නත් පුළුවන්.

### 🅱️ Fly.io (ලාබ, persistent volume) — `fly.toml` තියෙනවා

```bash
fly auth login
fly launch --no-deploy --copy-config          # fly.toml එකේ app name එක වෙනස් කරන්න
fly volumes create ceyteq_data -s 1
fly secrets set CEYTEQ_ADMIN_PASSWORD='MyStrongPass2026!'
fly deploy
```
`fly.toml` එකේ `CEYTEQ_DATA_DIR=/data` + volume mount එක දාලා තියෙනවා — database එක redeploy වලට ඔරොත්තු දෙනවා.

### 🅲 VPS / Dedicated server (root access තියෙනවා නම්) — තමයි හොඳම

```bash
git clone https://github.com/infoceyteq-maker/digitalrace.git /opt/ceyteq
cd /opt/ceyteq
printf 'CEYTEQ_ADMIN_PASSWORD=MyStrongPass2026!\n' > .env
docker compose up -d --build        # Dockerfile + docker-compose.yml දෙකම repo එකේ
```
Docker නැතුව run කරන්නත් පුළුවන්:

```bash
python3 server.py --init --admin-password 'MyStrongPass2026!'   # එක වරක්
python3 server.py --host 0.0.0.0 --port 8000                    # run
```
Production එකට systemd + nginx (HTTPS):

```ini
# /etc/systemd/system/ceyteq.service
[Unit]
Description=Ceyteq website + backend
After=network.target

[Service]
WorkingDirectory=/opt/ceyteq
Environment=CEYTEQ_ADMIN_PASSWORD=MyStrongPass2026!
Environment=CEYTEQ_DATA_DIR=/opt/ceyteq/data
ExecStart=/usr/bin/python3 /opt/ceyteq/server.py --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable --now ceyteq
sudo certbot --nginx -d www.ceyteq.lk -d ceyteq.lk      # free HTTPS
```
```nginx
# /etc/nginx/sites-available/ceyteq
server {
    server_name www.ceyteq.lk ceyteq.lk;
    client_max_body_size 10M;                 # flyer uploads
    location / { proxy_pass http://127.0.0.1:8000; proxy_set_header Host $host; }
}
```

### 🅳 දැනට test කරන්න විතරක් (local)

```bash
python3 server.py --init --admin-password 'test12345'
python3 server.py
# site  http://localhost:8000      admin  http://localhost:8000/admin.html
```

---

## Step 3 — Domain එක කොහොමද තියන්නේ (තෝරන්න)

**විකල්පය 1 — Pages + Backend දෙකම (ලේසි, නමුත් split)**
`www.ceyteq.linkpc.net` GitHub Pages එකේ තියෙන්න දීලා, backend එක වෙන host එකක තියන්න. ඒත් contact form/admin එක backend එකට කතා කරන්න ඕන නිසා **API base URL + CORS** එකක් ඕන — කියන්න, මම ඒක 15 මිනිත්තුවකින් හදලා දෙන්නම්.

**විකල්පය 2 — හැම දෙයක්ම backend host එකෙන් (recommend ✅)**
`www.ceyteq.lk` (හෝ `www.ceyteq.linkpc.net`) එක backend service එකට point කරන්න (Render/Fly dashboard එකේ Custom Domain → CNAME එකට host එක දෙන IP/alias එක දාන්න). එතකොට:
- pages + database + admin **එකම origin** එකේ → cookie/login ප්‍රශ්න නෑ
- GitHub Pages එක backup/staging විදියට තියන්න පුළුවන් (CNAME එක වෙනස් කරන්න ඕන නම් විතරයි)

---

## Step 4 — Live උනාට පස්සේ (5 මිනිත්තුවක වැඩ)

1. **Password එක වෙනස් කරන්න** — admin panel එකට ගිහින් login වෙන්න (`/admin.html`), පස්සේ host එකේ `CEYTEQ_ADMIN_PASSWORD` update කරලා:
   `python3 server.py --set-password admin NewPassword`
2. **`/api/health`** open කරන්න → `{"ok": true, ...}` පෙනෙන්න ඕන
3. **Offers tab** එකේ flyer එකක් upload කරලා test කරන්න, **Enquiries tab** එකේ form එකක් එවලා බලන්න
4. **Backup** — `data/ceyteq.db` කොපියක් (මේ file එකේම තමයි හැම lead + flyer එකම). දිනපතා automatic backup එකක් ඕන නම් කියන්න
5. **Robot එකට යවන්න එපා** `data/`, `.env`, `server.py` — server එකේ 403 තියෙනවා, ඒත් hosting dashboard එකේ විස්තර private තියන්න

---

## Troubleshooting

| ප්‍රශ්නය | හේතුව / විසඳුම |
|---|---|
| Admin panel එකේ "SERVER OFFLINE" | site එක static (GitHub Pages) — backend host කරලා නෑ. හෝ API domain එක වැරදි |
| Contact form එක WhatsApp එකට යනවා | backend එකට reach කරන්න බෑ (fallback එක වැඩ කරනවා). `/api/health` check කරන්න |
| Offers පිටුවේ ෆ්ලයර් පෙන්නන්නේ නෑ | `flyers/` folder + `offers.html` upload වෙලා තියෙනවද බලන්න; hard refresh (Ctrl+F5) |
| Render free එකේ data නැති වෙනවා | persistent disk ඕන (paid plan) හෝ Fly.io volume එකක් |
| Site එක update වෙන්නේ නෑ | Pages build වෙන්නේ `main` එකෙන් — PR merge කරලා Actions tab එකේ "pages build and deployment" බලන්න |
| Login එක වැඩ කරන්නේ නෑ | HTTPS තියෙන domain එකකින් login වෙන්න (cookie Secure). HTTP එකේදී browser එක cookie එක drop කරන්න පුළුවන් |

---

## Build / regenerate

```bash
python3 build_site.py        # pages 19 + flyers.html redirect එක rebuild
python3 make_flyers.py       # ෆ්ලයර් 10 අලුතින් හදන්න (pip install Pillow)
python3 server.py --reseed-flyers   # Offers list එක original 10 ට reset කරන්න
```
