#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
#   🎌 BLITEX ANIME BOT
#   Channel: t.me/blitexanime1
#   Bot: @BlitexPredictor11_Bot
#   Admin: @Blitex82
# ═══════════════════════════════════════════════════════════

import os, json, logging
from datetime import datetime
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# ── CONFIG ──────────────────────────────────────────────────
BOT_TOKEN  = "8652645786:AAHe78Lz70OU3Ub4vE4SPJvROo9Ggt3gsk4"
CHANNEL_ID = "@blitexanime1"
ADMIN_IDS  = [7985232177]   # Admin: @Blitex82
                             #   Get it by messaging @userinfobot
DB_FILE    = "blitex_anime_db.json"

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ── DATABASE ─────────────────────────────────────────────────
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"anime": {}, "subscribers": [], "stats": {"total_sends": 0}}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def is_admin(uid): return uid in ADMIN_IDS

# ── SEED ANIME DATA ──────────────────────────────────────────
def seed_anime():
    db = load_db()
    if db["anime"]:
        return  # already seeded

    animes = {
        "jujutsu_kaisen": {
            "name": "Jujutsu Kaisen",
            "hindi_name": "जुजुत्सु कैसेन",
            "description": "Yuji Itadori ek cursed spirit ka sharir kha leta hai aur ab wo Jujutsu sorcerer ban jaata hai.",
            "genre": "Action, Dark Fantasy",
            "status": "Ongoing",
            "seasons": 3,
            "episodes": {},
            "thumbnail": "https://upload.wikimedia.org/wikipedia/en/7/7a/Jujutsu_Kaisen_anime_key_visual.jpg",
            "rating": "⭐ 9.0/10",
            "added": "03/03/2026"
        },
        "attack_on_titan": {
            "name": "Attack on Titan",
            "hindi_name": "अटैक ऑन टाइटन",
            "description": "Insaan titanon se ladh rahe hain jo unhe kha jaate hain. Eren Yeager apni zindagi badla lene ke liye laraai karta hai.",
            "genre": "Action, Drama, Dark Fantasy",
            "status": "Completed",
            "seasons": 4,
            "episodes": {},
            "thumbnail": "https://upload.wikimedia.org/wikipedia/en/d/d6/Shingeki_no_kyojin_manga_volume_1.jpg",
            "rating": "⭐ 9.8/10",
            "added": "03/03/2026"
        },
        "demon_slayer": {
            "name": "Demon Slayer",
            "hindi_name": "डेमन स्लेयर",
            "description": "Tanjiro apni bahan Nezuko ko demon se wapas insaan banane ki koshish karta hai.",
            "genre": "Action, Supernatural",
            "status": "Ongoing",
            "seasons": 4,
            "episodes": {},
            "thumbnail": "https://upload.wikimedia.org/wikipedia/en/9/93/Demon_Slayer_-_Kimetsu_no_Yaiba%2C_volume_1.jpg",
            "rating": "⭐ 8.9/10",
            "added": "03/03/2026"
        },
        "one_piece": {
            "name": "One Piece",
            "hindi_name": "वन पीस",
            "description": "Monkey D. Luffy pirate king banna chahta hai aur legendary treasure One Piece dhundh raha hai.",
            "genre": "Adventure, Fantasy, Comedy",
            "status": "Ongoing",
            "seasons": 20,
            "episodes": {},
            "thumbnail": "https://upload.wikimedia.org/wikipedia/en/9/90/One_Piece%2C_Volume_1_Cover_%28Japanese%29.jpg",
            "rating": "⭐ 9.2/10",
            "added": "03/03/2026"
        },
        "naruto": {
            "name": "Naruto",
            "hindi_name": "नारुतो",
            "description": "Naruto Uzumaki apne gaon ka Hokage banna chahta hai. Ek aisa ladka jo sabka pyaar paana chahta hai.",
            "genre": "Action, Adventure, Comedy",
            "status": "Completed",
            "seasons": 5,
            "episodes": {},
            "thumbnail": "https://upload.wikimedia.org/wikipedia/en/9/94/NarutoCoverTankobon1.jpg",
            "rating": "⭐ 8.3/10",
            "added": "03/03/2026"
        },
        "dragon_ball_z": {
            "name": "Dragon Ball Z",
            "hindi_name": "ड्रैगन बॉल ज़ेड",
            "description": "Goku aur uske dost Earth ko evil saiyans aur aliens se bachate hain.",
            "genre": "Action, Adventure, Comedy",
            "status": "Completed",
            "seasons": 9,
            "episodes": {},
            "thumbnail": "https://upload.wikimedia.org/wikipedia/en/a/a7/Dragon_Ball_Z_volume_1.jpg",
            "rating": "⭐ 8.8/10",
            "added": "03/03/2026"
        },
        "black_clover": {
            "name": "Black Clover",
            "hindi_name": "ब्लैक क्लोवर",
            "description": "Asta jo magic ke bina paida hua, wo Wizard King banna chahta hai.",
            "genre": "Action, Fantasy, Comedy",
            "status": "Ongoing",
            "seasons": 4,
            "episodes": {},
            "thumbnail": "",
            "rating": "⭐ 8.0/10",
            "added": "03/03/2026"
        },
        "bleach": {
            "name": "Bleach",
            "hindi_name": "ब्लीच",
            "description": "Ichigo Kurosaki ek Soul Reaper ban jaata hai aur evil spirits se ladta hai.",
            "genre": "Action, Supernatural",
            "status": "Completed",
            "seasons": 16,
            "episodes": {},
            "thumbnail": "",
            "rating": "⭐ 8.1/10",
            "added": "03/03/2026"
        },
        "my_hero_academia": {
            "name": "My Hero Academia",
            "hindi_name": "माय हीरो एकेडेमिया",
            "description": "Izuku Midoriya bina superpower ke paida hua but wo greatest hero banna chahta hai.",
            "genre": "Action, Superhero",
            "status": "Completed",
            "seasons": 7,
            "episodes": {},
            "thumbnail": "",
            "rating": "⭐ 8.4/10",
            "added": "03/03/2026"
        },
        "vinland_saga": {
            "name": "Vinland Saga",
            "hindi_name": "विनलैंड सागा",
            "description": "Thorfinn apne pita ke hatyare se badla lene ke liye Vikings ke saath safar karta hai.",
            "genre": "Action, Historical, Drama",
            "status": "Ongoing",
            "seasons": 2,
            "episodes": {},
            "thumbnail": "",
            "rating": "⭐ 9.0/10",
            "added": "03/03/2026"
        }
    }
    db["anime"] = animes
    save_db(db)
    logger.info("Anime database seeded with 10 anime!")

# ── KEYBOARDS ────────────────────────────────────────────────
def main_kb(uid):
    kb = [
        [InlineKeyboardButton("🎌 Anime List", callback_data="browse_0"),
         InlineKeyboardButton("🔍 Search", callback_data="search_prompt")],
        [InlineKeyboardButton("🆕 Latest Episodes", callback_data="latest"),
         InlineKeyboardButton("🔔 Subscribe", callback_data="subscribe")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
    ]
    if is_admin(uid):
        kb.append([InlineKeyboardButton("🛡️ Admin Panel", callback_data="admin")])
    return InlineKeyboardMarkup(kb)

def back_kb(dest="main"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Back", callback_data=dest)]])

def anime_list_kb(page=0):
    db = load_db()
    keys = list(db["anime"].keys())
    per_page = 5
    start = page * per_page
    chunk = keys[start:start+per_page]
    kb = []
    for k in chunk:
        a = db["anime"][k]
        kb.append([InlineKeyboardButton(
            f"{'✅' if a['status']=='Completed' else '🔄'} {a['name']} ({a['seasons']}S)",
            callback_data=f"anime_{k}"
        )])
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"browse_{page-1}"))
    if start + per_page < len(keys):
        nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"browse_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 Home", callback_data="main")])
    return InlineKeyboardMarkup(kb)

def anime_detail_kb(anime_key):
    db = load_db()
    eps = db["anime"][anime_key].get("episodes", {})
    kb = []
    if eps:
        ep_nums = sorted(eps.keys(), key=lambda x: int(x))
        row = []
        for i, ep in enumerate(ep_nums[-10:]):  # show last 10
            row.append(InlineKeyboardButton(f"EP {ep}", callback_data=f"ep_{anime_key}_{ep}"))
            if len(row) == 4:
                kb.append(row); row = []
        if row: kb.append(row)
    kb.append([InlineKeyboardButton("◀️ Back to List", callback_data="browse_0")])
    return InlineKeyboardMarkup(kb)

def admin_kb():
    kb = [
        [InlineKeyboardButton("➕ Add Anime", callback_data="adm_add_anime"),
         InlineKeyboardButton("➕ Add Episode", callback_data="adm_add_ep")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="adm_broadcast"),
         InlineKeyboardButton("👥 Subscribers", callback_data="adm_subs")],
        [InlineKeyboardButton("🗑️ Remove Anime", callback_data="adm_remove"),
         InlineKeyboardButton("📊 Full Stats", callback_data="adm_stats")],
        [InlineKeyboardButton("🏠 Home", callback_data="main")],
    ]
    return InlineKeyboardMarkup(kb)

# ── MESSAGES ──────────────────────────────────────────────────
WELCOME = """🎌 *BLITEX ANIME* में आपका स्वागत है!

🇮🇳 *Hindi Dubbed Anime का सबसे बड़ा खजाना!*

✨ यहाँ आपको मिलेगा:
• जापानी anime हिंदी में
• हर episode की HD quality
• नए episodes की instant notification
• 10+ popular anime series

📢 हमारा Channel: @blitexanime1

नीचे से choose करें 👇"""

def anime_card(a, key):
    status_emoji = "✅" if a["status"] == "Completed" else "🔄"
    ep_count = len(a.get("episodes", {}))
    return f"""🎌 *{a['name']}*
🇮🇳 _{a.get('hindi_name', '')}_{" " if a.get('hindi_name') else ""}
{a.get('rating', '')}

📖 *कहानी:*
{a['description']}

🏷️ Genre: `{a['genre']}`
{status_emoji} Status: *{a['status']}* | 📺 Seasons: *{a['seasons']}*
🎬 Episodes Available: *{ep_count}*
📅 Added: {a['added']}

{'🎬 नीचे episode select करें 👇' if ep_count > 0 else '⏳ Episodes जल्द आएंगे! Channel join करें: @blitexanime1'}"""

# ── HANDLERS ─────────────────────────────────────────────────

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"नमस्ते *{name}* जी! 🙏\n\n" + WELCOME,
        parse_mode="Markdown",
        reply_markup=main_kb(uid)
    )

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    txt = """📚 *Commands List:*

/start - Bot शुरू करें
/list - सारे anime देखें
/search [name] - Anime ढूंढें
/latest - नए episodes
/subscribe - Alerts on/off
/stats - Bot statistics

🛡️ *Admin Commands:*
/addanime - नया anime add करें
/addep - Episode add करें
/broadcast - सबको message भेजें
/removeanime - Anime हटाएं"""
    await update.message.reply_text(txt, parse_mode="Markdown", reply_markup=back_kb("main"))

async def list_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎌 *सारे Hindi Dubbed Anime:*",
        parse_mode="Markdown",
        reply_markup=anime_list_kb(0)
    )

async def search_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text(
            "🔍 इस्तेमाल: `/search Naruto`\nया `/search attack`",
            parse_mode="Markdown"
        )
        return
    query = " ".join(ctx.args).lower()
    db = load_db()
    results = [
        (k, a) for k, a in db["anime"].items()
        if query in a["name"].lower() or query in a.get("hindi_name", "").lower()
        or query in a["genre"].lower()
    ]
    if not results:
        await update.message.reply_text(
            f"😔 '{' '.join(ctx.args)}' नहीं मिला।\n\n/list से सारे anime देखें।"
        )
        return
    kb = [[InlineKeyboardButton(f"🎌 {a['name']}", callback_data=f"anime_{k}")] for k, a in results]
    kb.append([InlineKeyboardButton("🏠 Home", callback_data="main")])
    await update.message.reply_text(
        f"🔍 *'{' '.join(ctx.args)}' के results:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    uid = q.from_user.id

    # ── Main menu
    if data == "main":
        await q.edit_message_text(WELCOME, parse_mode="Markdown", reply_markup=main_kb(uid))

    # ── Browse with pagination
    elif data.startswith("browse_"):
        page = int(data.split("_")[1])
        db = load_db()
        count = len(db["anime"])
        await q.edit_message_text(
            f"🎌 *Hindi Dubbed Anime List* ({count} anime)\n\n✅ = Completed | 🔄 = Ongoing\n\nSelect करें 👇",
            parse_mode="Markdown",
            reply_markup=anime_list_kb(page)
        )

    # ── Anime detail
    elif data.startswith("anime_"):
        key = data[6:]
        db = load_db()
        a = db["anime"].get(key)
        if not a:
            await q.edit_message_text("❌ Anime नहीं मिला।", reply_markup=back_kb("browse_0"))
            return
        await q.edit_message_text(
            anime_card(a, key),
            parse_mode="Markdown",
            reply_markup=anime_detail_kb(key)
        )

    # ── Episode
    elif data.startswith("ep_"):
        parts = data.split("_", 2)
        anime_key = parts[1]
        ep_num = parts[2]
        db = load_db()
        a = db["anime"].get(anime_key)
        ep = a["episodes"].get(ep_num) if a else None
        if not ep:
            await q.edit_message_text("❌ Episode नहीं मिला।", reply_markup=back_kb(f"anime_{anime_key}"))
            return
        # Send video
        try:
            await ctx.bot.send_video(
                chat_id=uid,
                video=ep["file_id"],
                caption=f"""🎌 *{a['name']}*
📺 Episode {ep_num}: _{ep.get('title', '')}_
🎬 Quality: {ep.get('quality','720p')}

📢 More episodes: @blitexanime1
🤖 Bot: @BlitexPredictor11_Bot""",
                parse_mode="Markdown"
            )
            await q.edit_message_text(
                f"✅ *Episode {ep_num} भेज दिया!* Check करें 👆\n\n📢 Channel: @blitexanime1",
                parse_mode="Markdown",
                reply_markup=back_kb(f"anime_{anime_key}")
            )
            # Update stats
            db2 = load_db()
            db2["stats"]["total_sends"] = db2["stats"].get("total_sends", 0) + 1
            save_db(db2)
        except Exception as e:
            await q.edit_message_text(f"❌ Error: {e}", reply_markup=back_kb(f"anime_{anime_key}"))

    # ── Latest episodes
    elif data == "latest":
        db = load_db()
        latest = []
        for k, a in db["anime"].items():
            for ep_num, ep in a.get("episodes", {}).items():
                latest.append((ep["added"], a["name"], k, ep_num, ep.get("title", "")))
        latest.sort(reverse=True)
        if not latest:
            await q.edit_message_text(
                "⏳ अभी कोई episode नहीं है।\n\nJoin करें: @blitexanime1",
                reply_markup=back_kb("main")
            )
            return
        txt = "🆕 *Latest Episodes:*\n\n"
        kb = []
        for added, aname, akey, epnum, eptitle in latest[:10]:
            txt += f"🎌 *{aname}* — EP {epnum}\n"
            kb.append([InlineKeyboardButton(f"▶️ {aname} EP{epnum}", callback_data=f"ep_{akey}_{epnum}")])
        kb.append([InlineKeyboardButton("🏠 Home", callback_data="main")])
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    # ── Subscribe
    elif data == "subscribe":
        db = load_db()
        subs = db.get("subscribers", [])
        if uid in subs:
            subs.remove(uid)
            db["subscribers"] = subs
            save_db(db)
            await q.edit_message_text(
                "🔕 *Unsubscribed!*\n\nAb aapko notifications nahi milenge.\n\nWapas subscribe karne ke liye /start karein.",
                parse_mode="Markdown", reply_markup=back_kb("main")
            )
        else:
            subs.append(uid)
            db["subscribers"] = subs
            save_db(db)
            await q.edit_message_text(
                "🔔 *Subscribed!*\n\n✅ Ab aapko naye episodes ki notification milegi!\n\n📢 Channel bhi join karein: @blitexanime1",
                parse_mode="Markdown", reply_markup=back_kb("main")
            )

    # ── Stats
    elif data == "stats":
        db = load_db()
        anime_count = len(db["anime"])
        ep_count = sum(len(a.get("episodes", {})) for a in db["anime"].values())
        subs = len(db.get("subscribers", []))
        sends = db.get("stats", {}).get("total_sends", 0)
        await q.edit_message_text(
            f"""📊 *Blitex Anime Stats:*

🎌 Total Anime: *{anime_count}*
🎬 Total Episodes: *{ep_count}*
🔔 Subscribers: *{subs}*
▶️ Total Streams: *{sends}*

📢 Channel: @blitexanime1""",
            parse_mode="Markdown", reply_markup=back_kb("main")
        )

    # ── Search prompt
    elif data == "search_prompt":
        await q.edit_message_text(
            "🔍 *Search Anime:*\n\nCommand type karein:\n`/search Naruto`\n`/search Demon`\n`/search Attack`",
            parse_mode="Markdown", reply_markup=back_kb("main")
        )

    # ── ADMIN ────────────────────────────────────────────────
    elif data == "admin":
        if not is_admin(uid):
            await q.edit_message_text("❌ Access Denied.", reply_markup=back_kb("main"))
            return
        db = load_db()
        await q.edit_message_text(
            f"🛡️ *Admin Panel*\n\nUsers: {len(db.get('subscribers',[]))}\nAnime: {len(db['anime'])}\nEpisodes: {sum(len(a.get('episodes',{})) for a in db['anime'].values())}",
            parse_mode="Markdown", reply_markup=admin_kb()
        )

    elif data == "adm_subs":
        if not is_admin(uid): return
        db = load_db()
        subs = db.get("subscribers", [])
        await q.edit_message_text(
            f"👥 *Subscribers: {len(subs)}*\n\nIDs:\n" + "\n".join(str(s) for s in subs[:20]),
            parse_mode="Markdown", reply_markup=back_kb("admin")
        )

    elif data == "adm_add_anime":
        if not is_admin(uid): return
        ctx.user_data["waiting"] = "add_anime"
        await q.edit_message_text(
            "➕ *Anime Add करें:*\n\nFormat:\n`NAME | Description | Genre | Seasons | Status`\n\nExample:\n`Sword Art Online | Kirito ek VR game mein phans jaata hai | Action,Fantasy | 3 | Ongoing`",
            parse_mode="Markdown", reply_markup=back_kb("admin")
        )

    elif data == "adm_add_ep":
        if not is_admin(uid): return
        ctx.user_data["waiting"] = "add_ep_key"
        db = load_db()
        kb = [[InlineKeyboardButton(a["name"], callback_data=f"adm_ep_{k}")] for k, a in db["anime"].items()]
        kb.append([InlineKeyboardButton("◀️ Back", callback_data="admin")])
        await q.edit_message_text("📺 *Anime select करें episode add करने के लिए:*",
                                   parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("adm_ep_"):
        if not is_admin(uid): return
        key = data[7:]
        ctx.user_data["waiting"] = "add_ep"
        ctx.user_data["ep_anime_key"] = key
        db = load_db()
        a = db["anime"][key]
        ep_count = len(a.get("episodes", {}))
        await q.edit_message_text(
            f"📺 *{a['name']}* में episode add करें:\n\nVideo file भेजें caption के साथ:\n`EP_NUMBER | Title | Quality`\n\nExample caption:\n`1 | Ryomen Sukuna | 720p`\n\n(अभी {ep_count} episodes हैं)",
            parse_mode="Markdown", reply_markup=back_kb("admin")
        )

    elif data == "adm_broadcast":
        if not is_admin(uid): return
        ctx.user_data["waiting"] = "broadcast"
        await q.edit_message_text(
            "📢 *Broadcast Message:*\n\nSabko bhejne ke liye message type karein:\n(Cancel karne ke liye /cancel)",
            parse_mode="Markdown", reply_markup=back_kb("admin")
        )

    elif data == "adm_remove":
        if not is_admin(uid): return
        db = load_db()
        kb = [[InlineKeyboardButton(f"🗑️ {a['name']}", callback_data=f"confirm_rm_{k}")] for k, a in db["anime"].items()]
        kb.append([InlineKeyboardButton("◀️ Back", callback_data="admin")])
        await q.edit_message_text("🗑️ *Kaunsa anime remove karein?*",
                                   parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("confirm_rm_"):
        if not is_admin(uid): return
        key = data[11:]
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Haan Remove Karo", callback_data=f"do_rm_{key}"),
             InlineKeyboardButton("❌ Cancel", callback_data="adm_remove")]
        ])
        db = load_db()
        await q.edit_message_text(
            f"⚠️ *{db['anime'][key]['name']}* ko remove karein?\n\nYe sare episodes bhi delete ho jaenge!",
            parse_mode="Markdown", reply_markup=kb
        )

    elif data.startswith("do_rm_"):
        if not is_admin(uid): return
        key = data[6:]
        db = load_db()
        name = db["anime"].get(key, {}).get("name", key)
        db["anime"].pop(key, None)
        save_db(db)
        await q.edit_message_text(f"✅ *{name}* remove ho gaya!", parse_mode="Markdown", reply_markup=back_kb("admin"))

    elif data == "adm_stats":
        if not is_admin(uid): return
        db = load_db()
        txt = "📊 *Full Admin Stats:*\n\n"
        for k, a in db["anime"].items():
            ep = len(a.get("episodes", {}))
            txt += f"🎌 {a['name']}: *{ep}* episodes\n"
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=back_kb("admin"))


# ── MESSAGE HANDLER (for admin inputs & video uploads) ───────
async def message_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    waiting = ctx.user_data.get("waiting")

    # ── Admin: Add Anime via text
    if waiting == "add_anime" and is_admin(uid):
        try:
            parts = [p.strip() for p in update.message.text.split("|")]
            name = parts[0]
            desc = parts[1] if len(parts) > 1 else ""
            genre = parts[2] if len(parts) > 2 else "Action"
            seasons = int(parts[3]) if len(parts) > 3 else 1
            status = parts[4] if len(parts) > 4 else "Ongoing"
            db = load_db()
            key = name.lower().replace(" ", "_").replace(":", "")
            db["anime"][key] = {
                "name": name, "hindi_name": "", "description": desc,
                "genre": genre, "status": status, "seasons": seasons,
                "episodes": {}, "thumbnail": "", "rating": "⭐ ?/10",
                "added": datetime.now().strftime("%d/%m/%Y")
            }
            save_db(db)
            ctx.user_data["waiting"] = None
            await update.message.reply_text(
                f"✅ *{name}* add ho gaya!\n\nAb episodes add karne ke liye Admin Panel → Add Episode",
                parse_mode="Markdown", reply_markup=admin_kb()
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Format galat hai: {e}\n\nFormat: `NAME | Desc | Genre | Seasons | Status`", parse_mode="Markdown")

    # ── Admin: Broadcast
    elif waiting == "broadcast" and is_admin(uid):
        msg = update.message.text
        db = load_db()
        subs = db.get("subscribers", [])
        sent, failed = 0, 0
        for sub_id in subs:
            try:
                await ctx.bot.send_message(
                    chat_id=sub_id,
                    text=f"📢 *Blitex Anime Announcement:*\n\n{msg}\n\n📢 @blitexanime1",
                    parse_mode="Markdown"
                )
                sent += 1
            except:
                failed += 1
        ctx.user_data["waiting"] = None
        await update.message.reply_text(
            f"✅ Broadcast done!\n✅ Sent: {sent}\n❌ Failed: {failed}",
            reply_markup=admin_kb()
        )

    # ── Admin: Add Episode (video file)
    elif waiting == "add_ep" and is_admin(uid) and update.message.video:
        anime_key = ctx.user_data.get("ep_anime_key")
        caption = update.message.caption or ""
        parts = [p.strip() for p in caption.split("|")]
        ep_num = parts[0] if parts else "1"
        title = parts[1] if len(parts) > 1 else f"Episode {ep_num}"
        quality = parts[2] if len(parts) > 2 else "720p"
        file_id = update.message.video.file_id

        db = load_db()
        if anime_key not in db["anime"]:
            await update.message.reply_text("❌ Anime not found!")
            return
        db["anime"][anime_key]["episodes"][ep_num] = {
            "title": title, "file_id": file_id, "quality": quality,
            "added": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        save_db(db)
        ctx.user_data["waiting"] = None
        a = db["anime"][anime_key]

        # Auto-post to channel
        try:
            await ctx.bot.send_video(
                chat_id=CHANNEL_ID,
                video=file_id,
                caption=f"""🎌 *{a['name']}* — New Episode!
━━━━━━━━━━━━━━━━━━━━
📺 *Episode {ep_num}:* _{title}_
🎬 Quality: {quality}
🇮🇳 Hindi Dubbed
━━━━━━━━━━━━━━━━━━━━
🤖 Bot se dekhein: @BlitexPredictor11_Bot
📢 Channel: @blitexanime1""",
                parse_mode="Markdown"
            )
            channel_posted = "✅ Channel pe bhi post ho gaya!"
        except Exception as e:
            channel_posted = f"⚠️ Channel post failed: {e}"

        # Notify subscribers
        subs = db.get("subscribers", [])
        notified = 0
        for sub_id in subs:
            try:
                await ctx.bot.send_message(
                    chat_id=sub_id,
                    text=f"🆕 *New Episode Alert!*\n\n🎌 *{a['name']}*\n📺 Episode {ep_num}: _{title}_\n\n▶️ Bot pe dekhein: @BlitexPredictor11_Bot",
                    parse_mode="Markdown"
                )
                notified += 1
            except:
                pass

        await update.message.reply_text(
            f"✅ *Episode {ep_num} added!*\n{channel_posted}\n🔔 {notified} subscribers notified!",
            parse_mode="Markdown", reply_markup=admin_kb()
        )

    else:
        # Regular user message - show menu
        if not update.message.video:
            await update.message.reply_text(
                "🎌 *Blitex Anime Bot*\n\n/start - Home\n/list - Anime List\n/search [name] - Search",
                parse_mode="Markdown", reply_markup=main_kb(uid)
            )

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text("❌ Cancelled.", reply_markup=main_kb(update.effective_user.id))

# ── MAIN ──────────────────────────────────────────────────────
def main():
    seed_anime()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("list", list_cmd))
    app.add_handler(CommandHandler("search", search_cmd))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, message_handler))
    logger.info("🎌 Blitex Anime Bot starting...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
