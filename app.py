import json
from pathlib import Path
from urllib.parse import quote
import streamlit as st

BASE = Path(__file__).parent
DATA = BASE / "data"
PROGRESS_FILE = BASE / ".frm_academy_progress.json"

with open(DATA / "curriculum.json", encoding="utf-8") as f:
    CURRICULUM = json.load(f)
with open(DATA / "lessons.json", encoding="utf-8") as f:
    LESSONS = json.load(f)
with open(DATA / "questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

BOOK_META = {
    "Foundations of Risk Management": ("◈", "Foundations"),
    "Quantitative Analysis": ("▥", "Quantitative"),
    "Financial Markets and Products": ("◎", "Markets"),
    "Valuation and Risk Models": ("↗", "Valuation"),
}

TOTAL_CHAPTERS = sum(len(v) for v in CURRICULUM.values())


def chapter_key(book, chapter):
    return f"{book}|{chapter}"


def load_progress():
    default = {
        "xp": 780,
        "streak": 12,
        "completed_chapters": [],
        "wrong_questions": [],
        "chapter_progress": {
            chapter_key("Foundations of Risk Management", "Chapter 1: The Building Blocks of Risk Management"): 1,
            chapter_key("Quantitative Analysis", "Chapter 6: Hypothesis Testing"): 0,
        },
        "last_book": "Foundations of Risk Management",
        "last_chapter": "Chapter 1: The Building Blocks of Risk Management",
    }
    if PROGRESS_FILE.exists():
        try:
            saved = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            default.update(saved)
        except Exception:
            pass
    return default


def save_progress():
    payload = {
        "xp": st.session_state.xp,
        "streak": st.session_state.streak,
        "completed_chapters": st.session_state.completed_chapters,
        "wrong_questions": st.session_state.wrong_questions,
        "chapter_progress": st.session_state.chapter_progress,
        "last_book": st.session_state.last_book,
        "last_chapter": st.session_state.last_chapter,
    }
    try:
        PROGRESS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def init_state():
    p = load_progress()
    for k, v in p.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    if "checked" not in st.session_state:
        st.session_state.checked = {}


def q(name, default=""):
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value


def href(page, **params):
    query = [f"page={quote(page)}"]
    for k, v in params.items():
        query.append(f"{quote(str(k))}={quote(str(v))}")
    return "?" + "&".join(query)


def current_theme():
    requested = q("theme")
    if requested in ("light", "dark"):
        st.session_state.theme = requested
    return st.session_state.theme


def add_theme(url):
    sep = "&" if "?" in url else "?"
    return url + sep + f"theme={st.session_state.theme}"


def inject_css(theme):
    dark = theme == "dark"
    bg = "#0b0f14" if dark else "#f7f2eb"
    panel = "#121820" if dark else "#fffdfa"
    panel2 = "#171e27" if dark else "#f1ebe3"
    text = "#f6f4ef" if dark else "#171717"
    muted = "#9ca6b4" if dark else "#6f6b66"
    line = "rgba(255,255,255,.08)" if dark else "rgba(24,24,24,.08)"
    accent = "#7aa8ff" if dark else "#1b1f26"
    accent_text = "#08111f" if dark else "#fffaf4"
    glow = "rgba(122,168,255,.13)" if dark else "rgba(0,0,0,.035)"

    st.markdown(f"""
    <style>
      :root {{
        --bg:{bg}; --panel:{panel}; --panel2:{panel2}; --text:{text}; --muted:{muted};
        --line:{line}; --accent:{accent}; --accentText:{accent_text}; --glow:{glow};
      }}

      #MainMenu, footer, [data-testid="stHeader"], [data-testid="stToolbar"],
      [data-testid="stDecoration"], [data-testid="stStatusWidget"],
      [data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display:none !important; }}

      html, body, .stApp {{ background:var(--bg) !important; color:var(--text) !important; }}
      .stApp {{ min-height:100vh; }}
      .block-container {{
        max-width: 520px !important;
        padding: 0.75rem 1rem calc(7.4rem + env(safe-area-inset-bottom)) !important;
        margin: 0 auto !important;
      }}
      * {{ box-sizing:border-box; }}
      html, body, [class*="css"] {{
        font-family: Inter, -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", Segoe UI, sans-serif;
      }}
      h1,h2,h3,h4,p,li,label,span,div {{ color:var(--text); }}
      h1 {{ font-size:2rem !important; letter-spacing:-.035em; margin:.15rem 0 .3rem !important; }}
      h2 {{ font-size:1.55rem !important; letter-spacing:-.025em; }}
      h3 {{ font-size:1.2rem !important; }}
      p {{ line-height:1.55; }}

      .topbar {{
        display:flex; align-items:center; justify-content:space-between;
        margin:.1rem 0 1.25rem; min-height:44px;
      }}
      .brand {{ font-weight:800; font-size:1.05rem; letter-spacing:-.02em; display:flex; gap:.55rem; align-items:center; }}
      .top-actions {{ display:flex; gap:.6rem; align-items:center; }}
      .icon-btn, .pill-link {{
        text-decoration:none !important; color:var(--text) !important; border:1px solid var(--line);
        background:var(--panel); border-radius:999px; min-width:42px; height:42px;
        display:inline-flex; align-items:center; justify-content:center; box-shadow:0 8px 24px var(--glow);
      }}
      .streak-mini {{ font-size:.84rem; color:var(--muted); display:flex; align-items:center; gap:.3rem; }}

      .flame {{
        display:inline-block; filter:saturate(1.45); text-shadow:0 0 15px rgba(255,54,31,.52);
        animation: flamePop 1.25s ease-in-out 2;
      }}
      @keyframes flamePop {{
        0%,100% {{ transform:scale(1) rotate(0); }}
        30% {{ transform:scale(1.14) rotate(-5deg); }}
        60% {{ transform:scale(.98) rotate(4deg); }}
      }}

      .hero {{ margin:.3rem 0 1.25rem; }}
      .eyebrow {{ color:var(--muted); font-size:.9rem; margin-bottom:.1rem; }}
      .hero-title {{ font-size:2.35rem; font-weight:850; letter-spacing:-.05em; line-height:1.02; }}
      .hero-sub {{ color:var(--muted); font-size:1rem; margin-top:.45rem; }}

      .card {{
        background:var(--panel); border:1px solid var(--line); border-radius:24px;
        padding:1.05rem; box-shadow:0 15px 40px var(--glow); margin-bottom:.9rem;
      }}
      .card.soft {{ background:var(--panel2); box-shadow:none; }}
      .card-title {{ font-weight:780; font-size:1rem; letter-spacing:-.015em; }}
      .muted {{ color:var(--muted) !important; }}
      .big-number {{ font-size:2.1rem; font-weight:850; letter-spacing:-.05em; }}
      .tiny {{ font-size:.82rem; color:var(--muted); }}

      .progress {{ height:8px; background:color-mix(in srgb, var(--muted) 14%, transparent); border-radius:999px; overflow:hidden; margin:.7rem 0 .35rem; }}
      .progress > div {{ height:100%; border-radius:999px; background:var(--accent); }}

      .stats-row {{ display:grid; grid-template-columns:1fr 1fr; gap:.7rem; margin-top:.85rem; }}
      .stat {{ background:var(--panel2); border-radius:18px; padding:.85rem; }}
      .stat-value {{ font-size:1.25rem; font-weight:800; }}
      .stat-label {{ color:var(--muted); font-size:.8rem; margin-top:.1rem; }}

      .continue {{ display:flex; flex-direction:column; gap:.55rem; }}
      .continue-title {{ font-size:1.15rem; font-weight:800; line-height:1.25; }}
      .primary-link {{
        display:flex; text-decoration:none !important; background:var(--accent); color:var(--accentText) !important;
        border-radius:16px; padding:.85rem 1rem; font-weight:750; align-items:center; justify-content:space-between;
        margin-top:.35rem;
      }}

      .section-title {{ font-size:1.08rem; font-weight:800; margin:1.35rem 0 .7rem; }}
      .subjects {{ display:grid; grid-template-columns:1fr 1fr; gap:.7rem; }}
      .subject {{
        background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:.9rem;
        min-height:132px; display:flex; flex-direction:column; text-decoration:none !important; box-shadow:0 10px 28px var(--glow);
      }}
      .subject-icon {{ font-size:1.15rem; margin-bottom:.55rem; }}
      .subject-name {{ font-size:.9rem; line-height:1.18; font-weight:760; min-height:2.2rem; }}
      .subject-meta {{ color:var(--muted); font-size:.78rem; margin-top:auto; }}

      .bottom-nav {{
        position:fixed; z-index:9999; left:50%; transform:translateX(-50%); bottom:0;
        width:min(520px, 100%); padding:.62rem 1rem calc(.65rem + env(safe-area-inset-bottom));
        background:color-mix(in srgb, var(--bg) 92%, transparent); backdrop-filter:blur(22px);
        border-top:1px solid var(--line); display:grid; grid-template-columns:repeat(4,1fr); gap:.2rem;
      }}
      .nav-item {{ text-decoration:none !important; color:var(--muted) !important; text-align:center; font-size:.68rem; padding:.3rem .15rem; border-radius:14px; }}
      .nav-icon {{ display:block; font-size:1.15rem; line-height:1.25; margin-bottom:.15rem; }}
      .nav-item.active {{ color:var(--text) !important; background:var(--panel); }}

      .course-top {{ display:flex; gap:.7rem; align-items:center; margin-bottom:.8rem; }}
      .back {{ text-decoration:none !important; color:var(--text) !important; width:38px; height:38px; display:grid; place-items:center; border-radius:50%; background:var(--panel); border:1px solid var(--line); }}
      .course-heading {{ flex:1; }}
      .course-title {{ font-size:1.5rem; font-weight:850; letter-spacing:-.035em; line-height:1.1; }}
      .course-body {{ font-size:1.01rem; line-height:1.65; }}
      .callout {{ border-left:3px solid var(--accent); padding:.85rem 1rem; background:var(--panel2); border-radius:4px 18px 18px 4px; margin:1rem 0; }}
      .callout strong {{ display:block; margin-bottom:.3rem; }}
      .chips {{ display:flex; flex-wrap:wrap; gap:.45rem; margin-top:.85rem; }}
      .chip {{ background:var(--panel2); border-radius:999px; padding:.5rem .7rem; font-size:.8rem; }}
      .pager {{ display:grid; grid-template-columns:1fr 1.25fr; gap:.65rem; margin-top:1.1rem; }}
      .secondary-link, .next-link {{ text-decoration:none !important; border-radius:16px; padding:.85rem .8rem; text-align:center; font-weight:720; }}
      .secondary-link {{ color:var(--text) !important; border:1px solid var(--line); background:var(--panel); }}
      .next-link {{ color:var(--accentText) !important; background:var(--accent); }}

      div[data-testid="stRadio"] {{ background:transparent; }}
      div[data-testid="stRadio"] > label {{ display:none; }}
      div[data-testid="stRadio"] [role="radiogroup"] {{ gap:.65rem; }}
      div[data-testid="stRadio"] [role="radiogroup"] label {{
        background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:.85rem .8rem;
        min-height:56px; align-items:center; box-shadow:0 8px 22px var(--glow);
      }}
      div[data-testid="stButton"] button {{
        min-height:48px; border-radius:16px !important; width:100%; border:1px solid var(--line) !important;
        background:var(--accent) !important; color:var(--accentText) !important; font-weight:750 !important;
      }}
      div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {{
        border-radius:16px !important; background:var(--panel) !important; color:var(--text) !important; border:1px solid var(--line) !important;
      }}

      @media (min-width: 700px) {{
        .block-container {{ padding-top:1.2rem !important; }}
      }}
    </style>
    """, unsafe_allow_html=True)


def topbar():
    page = q("page", "home")
    toggle_theme = "dark" if st.session_state.theme == "light" else "light"
    icon = "☾" if st.session_state.theme == "light" else "☀"
    st.markdown(f"""
    <div class="topbar">
      <div class="brand"><span>◈</span> FRM Academy</div>
      <div class="top-actions">
        <div class="streak-mini"><span class="flame">🔥</span> {st.session_state.streak} j</div>
        <a class="icon-btn" href="{href(page, theme=toggle_theme)}">{icon}</a>
      </div>
    </div>
    """, unsafe_allow_html=True)


def bottom_nav(active):
    items = [
        ("home", "⌂", "Accueil"),
        ("learn", "▤", "Cours"),
        ("qcm", "✓", "QCM"),
        ("review", "↺", "À revoir"),
    ]
    html = '<nav class="bottom-nav">'
    for page, icon, label in items:
        cls = "nav-item active" if active == page else "nav-item"
        html += f'<a class="{cls}" href="{add_theme(href(page))}"><span class="nav-icon">{icon}</span>{label}</a>'
    html += '</nav>'
    st.markdown(html, unsafe_allow_html=True)


def render_progress(pct):
    pct = max(0, min(1, pct))
    st.markdown(f'<div class="progress"><div style="width:{pct*100:.0f}%"></div></div>', unsafe_allow_html=True)


def book_progress(book):
    done = sum(chapter_key(book, c) in st.session_state.completed_chapters for c in CURRICULUM[book])
    return done, len(CURRICULUM[book])


def home_page():
    topbar()
    completed = len(st.session_state.completed_chapters)
    pct = completed / TOTAL_CHAPTERS if TOTAL_CHAPTERS else 0

    st.markdown('''<div class="hero"><div class="hero-title">Bonjour Emmanuel 👋</div><div class="hero-sub">Étudie à ton rythme.</div></div>''', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Ta progression</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-number">{int(pct*100)}%</div>', unsafe_allow_html=True)
    render_progress(pct)
    st.markdown(f'<div class="tiny">{completed} / {TOTAL_CHAPTERS} chapitres complétés</div>', unsafe_allow_html=True)
    st.markdown(f'''
      <div class="stats-row">
        <div class="stat"><div class="stat-value"><span class="flame">🔥</span> {st.session_state.streak}</div><div class="stat-label">jours de série</div></div>
        <div class="stat"><div class="stat-value">✦ {st.session_state.xp}</div><div class="stat-label">XP total</div></div>
      </div>
    </div>''', unsafe_allow_html=True)

    book = st.session_state.last_book
    chapter = st.session_state.last_chapter
    key = chapter_key(book, chapter)
    lesson = LESSONS.get(key)
    step = st.session_state.chapter_progress.get(key, 0)
    total_steps = len(lesson["steps"]) if lesson else 1
    course_url = add_theme(href("course", book=book, chapter=chapter, step=step))
    st.markdown(f'''
      <div class="card continue">
        <div class="tiny">Continuer</div>
        <div class="continue-title">{chapter}</div>
        <div class="muted" style="font-size:.85rem">{book}</div>
        <div class="progress"><div style="width:{((step+1)/total_steps)*100:.0f}%"></div></div>
        <a class="primary-link" href="{course_url}"><span>Reprendre la session</span><span>→</span></a>
      </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Tes matières</div>', unsafe_allow_html=True)
    html = '<div class="subjects">'
    for book_name in CURRICULUM:
        icon, short = BOOK_META[book_name]
        done, total = book_progress(book_name)
        first = CURRICULUM[book_name][0]
        url = add_theme(href("course", book=book_name, chapter=first, step=0))
        html += f'''
          <a class="subject" href="{url}">
            <div class="subject-icon">{icon}</div>
            <div class="subject-name">{short}</div>
            <div class="subject-meta">{done} / {total} chapitres</div>
          </a>
        '''
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
    bottom_nav("home")


def learn_page():
    topbar()
    st.markdown('<div class="hero"><div class="eyebrow">Bibliothèque</div><div class="hero-title" style="font-size:2rem">Cours</div><div class="hero-sub">Choisis une matière, puis un chapitre.</div></div>', unsafe_allow_html=True)
    for book in CURRICULUM:
        icon, short = BOOK_META[book]
        st.markdown(f'<div class="section-title">{icon} {short}</div>', unsafe_allow_html=True)
        for i, chapter in enumerate(CURRICULUM[book]):
            key = chapter_key(book, chapter)
            lesson = LESSONS.get(key)
            step = st.session_state.chapter_progress.get(key, 0)
            pct = ((step + 1) / len(lesson["steps"])) if lesson else 0
            done = key in st.session_state.completed_chapters
            status = "Terminé" if done else (f"{int(pct*100)}%" if lesson else "À venir")
            url = add_theme(href("course", book=book, chapter=chapter, step=step))
            st.markdown(f'''
              <a href="{url}" style="text-decoration:none!important">
                <div class="card" style="padding:.85rem .95rem; margin-bottom:.55rem; display:flex; align-items:center; gap:.8rem;">
                  <div style="width:34px;height:34px;border-radius:12px;background:var(--panel2);display:grid;place-items:center;font-weight:800">{i+1}</div>
                  <div style="flex:1"><div style="font-weight:730;font-size:.9rem;line-height:1.25">{chapter.replace('Chapter '+str(i+1)+': ', '')}</div><div class="tiny">{status}</div></div>
                  <div class="muted">›</div>
                </div>
              </a>
            ''', unsafe_allow_html=True)
    bottom_nav("learn")


def course_page():
    book = q("book", st.session_state.last_book)
    chapter = q("chapter", st.session_state.last_chapter)
    try:
        step_idx = int(q("step", "0"))
    except ValueError:
        step_idx = 0

    st.session_state.last_book = book
    st.session_state.last_chapter = chapter
    key = chapter_key(book, chapter)
    lesson = LESSONS.get(key)
    save_progress()

    topbar()
    back_url = add_theme(href("learn"))
    st.markdown(f'''
      <div class="course-top">
        <a class="back" href="{back_url}">‹</a>
        <div class="course-heading"><div class="tiny">{BOOK_META.get(book, ('','Cours'))[1]}</div><div class="course-title">{chapter}</div></div>
      </div>
    ''', unsafe_allow_html=True)

    if not lesson:
        st.markdown('<div class="card"><div class="card-title">Contenu en préparation</div><p class="muted">Le chapitre est déjà dans le parcours, mais sa leçon interactive n’est pas encore ajoutée à cette version.</p></div>', unsafe_allow_html=True)
        bottom_nav("learn")
        return

    step_idx = max(0, min(step_idx, len(lesson["steps"]) - 1))
    step = lesson["steps"][step_idx]
    st.session_state.chapter_progress[key] = step_idx
    save_progress()

    st.markdown(f'<div class="tiny">Étape {step_idx+1} / {len(lesson["steps"])}</div>', unsafe_allow_html=True)
    render_progress((step_idx + 1) / len(lesson["steps"]))

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="eyebrow">{step["label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'## {step["title"]}')
    st.markdown(f'<div class="course-body">{step["body"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="callout"><strong>À retenir</strong>{step["takeaway"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card soft" style="margin:0"><div class="card-title">Exemple</div><div style="margin-top:.35rem;line-height:1.55">{step["example"]}</div></div>', unsafe_allow_html=True)
    chips = ''.join(f'<span class="chip">{x}</span>' for x in step["essentials"])
    st.markdown(f'<div class="chips">{chips}</div>', unsafe_allow_html=True)

    prev_idx = max(0, step_idx - 1)
    prev_url = add_theme(href("course", book=book, chapter=chapter, step=prev_idx))
    if step_idx < len(lesson["steps"]) - 1:
        next_url = add_theme(href("course", book=book, chapter=chapter, step=step_idx + 1))
        next_text = "Suivant →"
    else:
        next_url = add_theme(href("qcm", book=book, chapter=chapter, qi=0))
        next_text = "Faire le QCM →"
    prev_class = "secondary-link" if step_idx > 0 else "secondary-link"
    st.markdown(f'''
      <div class="pager">
        <a class="{prev_class}" href="{prev_url}">← Précédent</a>
        <a class="next-link" href="{next_url}">{next_text}</a>
      </div>
    </div>
    ''', unsafe_allow_html=True)
    bottom_nav("learn")


def qcm_page():
    book = q("book", st.session_state.last_book)
    chapter = q("chapter", st.session_state.last_chapter)
    pool = [x for x in QUESTIONS if x["book"] == book and x["chapter"] == chapter]
    if not pool:
        pool = [x for x in QUESTIONS if x["type"] == "qcm"]
        book = pool[0]["book"] if pool else ""
        chapter = pool[0]["chapter"] if pool else ""
    if not pool:
        topbar(); st.info("Aucun QCM pour l’instant."); bottom_nav("qcm"); return

    try:
        idx = int(q("qi", "0"))
    except ValueError:
        idx = 0
    idx = max(0, min(idx, len(pool)-1))
    item = pool[idx]

    topbar()
    st.markdown(f'<div class="eyebrow">QCM · {BOOK_META.get(book, ("","FRM"))[1]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title" style="font-size:1.65rem;line-height:1.1;margin:.25rem 0 .35rem">{chapter}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tiny">Question {idx+1} / {len(pool)}</div>', unsafe_allow_html=True)
    render_progress((idx+1)/len(pool))

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'### {item["question"]}')

    if item["type"] == "qcm":
        choice = st.radio("Réponse", item["options"], index=None, key=f"radio_{item['id']}", label_visibility="collapsed")
        checked = st.session_state.checked.get(item["id"])
        if st.button("Vérifier", key=f"check_{item['id']}"):
            if choice is None:
                st.warning("Choisis une réponse.")
            else:
                selected = item["options"].index(choice)
                ok = selected == item["answer"]
                st.session_state.checked[item["id"]] = ok
                if ok:
                    st.session_state.xp += 20
                elif item["id"] not in st.session_state.wrong_questions:
                    st.session_state.wrong_questions.append(item["id"])
                save_progress()
                st.rerun()
        if checked is not None:
            if checked:
                st.success("Bonne réponse ✓")
            else:
                st.error("Pas tout à fait.")
            st.info(item["explanation"])
            if idx < len(pool)-1:
                next_url = add_theme(href("qcm", book=book, chapter=chapter, qi=idx+1))
                label = "Question suivante →"
            else:
                key = chapter_key(book, chapter)
                if key not in st.session_state.completed_chapters:
                    st.session_state.completed_chapters.append(key)
                    st.session_state.xp += 100
                    save_progress()
                next_url = add_theme(href("home"))
                label = "Terminer ✓"
            st.markdown(f'<a class="primary-link" href="{next_url}" style="margin-top:.9rem">{label}</a>', unsafe_allow_html=True)
    else:
        st.text_area("Ta réponse", height=150)
        if st.button("Voir la réponse-type"):
            st.info(item["model_answer"])

    st.markdown('</div>', unsafe_allow_html=True)
    bottom_nav("qcm")


def review_page():
    topbar()
    st.markdown('<div class="hero"><div class="eyebrow">Révision</div><div class="hero-title" style="font-size:2rem">À revoir</div><div class="hero-sub">Tes erreurs récentes, sans surcharge.</div></div>', unsafe_allow_html=True)
    wrong = [x for x in QUESTIONS if x["id"] in st.session_state.wrong_questions]
    if not wrong:
        st.markdown('<div class="card"><div class="card-title">Rien à revoir pour l’instant.</div><div class="muted" style="margin-top:.3rem">Les questions ratées apparaîtront ici.</div></div>', unsafe_allow_html=True)
    else:
        for item in wrong:
            url = add_theme(href("qcm", book=item["book"], chapter=item["chapter"], qi=0))
            st.markdown(f'''
              <div class="card">
                <div class="tiny">{BOOK_META[item['book']][1]}</div>
                <div class="card-title" style="margin:.25rem 0">{item['question']}</div>
                <div class="muted" style="font-size:.85rem">{item.get('explanation','')}</div>
                <a class="primary-link" href="{url}" style="margin-top:.8rem">Retenter →</a>
              </div>
            ''', unsafe_allow_html=True)
    bottom_nav("review")


def main():
    st.set_page_config(page_title="FRM Academy", page_icon="🔥", layout="centered", initial_sidebar_state="collapsed")
    init_state()
    theme = current_theme()
    inject_css(theme)
    page = q("page", "home")

    if page == "home":
        home_page()
    elif page == "learn":
        learn_page()
    elif page == "course":
        course_page()
    elif page == "qcm":
        qcm_page()
    elif page == "review":
        review_page()
    else:
        home_page()


if __name__ == "__main__":
    main()
