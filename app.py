import json
from pathlib import Path
import streamlit as st

BASE = Path(__file__).parent
DATA = BASE / "data"
PROGRESS_FILE = BASE / ".frm_academy_progress.json"

BOOK_META = {
    "Foundations of Risk Management": {"icon": "🛡️", "short": "Foundations"},
    "Quantitative Analysis": {"icon": "📊", "short": "Quantitative"},
    "Financial Markets and Products": {"icon": "🪙", "short": "Markets"},
    "Valuation and Risk Models": {"icon": "📈", "short": "Valuation"},
}

with open(DATA / "curriculum.json", encoding="utf-8") as f:
    CURRICULUM = json.load(f)
with open(DATA / "lessons.json", encoding="utf-8") as f:
    LESSONS = json.load(f)
with open(DATA / "questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

TOTAL_CHAPTERS = sum(len(v) for v in CURRICULUM.values())


def chapter_key(book, chapter):
    return f"{book}|{chapter}"


def load_progress():
    default = {
        "xp": 780,
        "streak": 12,
        "theme": "light",
        "completed_chapters": [],
        "wrong_questions": [],
        "chapter_progress": {
            chapter_key("Foundations of Risk Management", "Chapter 1: The Building Blocks of Risk Management"): 2,
            chapter_key("Quantitative Analysis", "Chapter 6: Hypothesis Testing"): 1,
        },
        "last_book": "Quantitative Analysis",
        "last_chapter": "Chapter 6: Hypothesis Testing",
        "current_question_index": 0,
        "question_answers": {},
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
        "theme": st.session_state.theme,
        "completed_chapters": st.session_state.completed_chapters,
        "wrong_questions": st.session_state.wrong_questions,
        "chapter_progress": st.session_state.chapter_progress,
        "last_book": st.session_state.last_book,
        "last_chapter": st.session_state.last_chapter,
        "current_question_index": st.session_state.current_question_index,
        "question_answers": st.session_state.question_answers,
    }
    PROGRESS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def init_state():
    progress = load_progress()
    for key, value in progress.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if "page" not in st.session_state:
        st.session_state.page = "Accueil"


def inject_css(theme: str):
    if theme == "dark":
        vars_css = """
        --bg: #0b0f14;
        --panel: rgba(17, 23, 31, 0.86);
        --panel-2: rgba(22, 29, 38, 0.9);
        --line: rgba(255,255,255,0.08);
        --text: #f6f4ef;
        --muted: #abb3c0;
        --accent: #78a8ff;
        --accent-soft: #1b2740;
        --warm: #f2e8dc;
        --beige: #d6c3a9;
        --shadow: 0 18px 40px rgba(0,0,0,0.28);
        --good: #90d0a4;
        --bad: #ff8f8f;
        """
        background = "background: radial-gradient(circle at top left, rgba(25,45,85,.35), transparent 26%), #0b0f14;"
    else:
        vars_css = """
        --bg: #f6f1ea;
        --panel: rgba(255,255,255,0.76);
        --panel-2: rgba(255,251,246,0.88);
        --line: rgba(20,20,20,0.08);
        --text: #171717;
        --muted: #6d6a65;
        --accent: #1b2430;
        --accent-soft: #ece5db;
        --warm: #fffaf4;
        --beige: #baa58d;
        --shadow: 0 16px 36px rgba(35,35,35,0.06);
        --good: #6da77c;
        --bad: #b25c5c;
        """
        background = "background: linear-gradient(180deg, #faf7f2 0%, #f4efe8 100%);"

    st.markdown(
        f"""
        <style>
        .stApp {{
            {background}
            color: var(--text);
        }}
        :root {{ {vars_css} }}
        html, body, [class*="css"]  {{ font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
        .block-container {{ padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1220px; }}
        [data-testid="stSidebar"] {{ background: transparent; border-right: 1px solid var(--line); }}
        [data-testid="stSidebar"] > div:first-child {{ padding-top: 1rem; }}
        h1,h2,h3,h4, p, li, label, div {{ color: var(--text); }}
        .muted {{ color: var(--muted); }}
        .fa-panel {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 1.25rem 1.4rem;
            box-shadow: var(--shadow);
            backdrop-filter: blur(10px);
        }}
        .fa-card {{
            background: var(--panel-2);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1rem 1.15rem;
            box-shadow: var(--shadow);
            height: 100%;
        }}
        .fa-mini {{ font-size: .92rem; color: var(--muted); }}
        .fa-title {{ font-weight: 700; font-size: 1.1rem; margin-bottom: .15rem; }}
        .fa-hero {{ font-size: 3rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: .15rem; }}
        .fa-progress-wrap {{ height: 10px; background: rgba(150,150,150,.16); border-radius: 999px; overflow: hidden; margin: .6rem 0 .45rem; }}
        .fa-progress-bar {{ height: 100%; background: linear-gradient(90deg, var(--beige), var(--accent)); border-radius: 999px; }}
        .fa-chip {{ display:inline-flex; align-items:center; gap:.5rem; border:1px solid var(--line); border-radius:999px; padding:.5rem .8rem; background: rgba(255,255,255,.02); }}
        .fa-flame {{ display:inline-block; font-size: 1.35rem; color:#ff4d2d; text-shadow: 0 0 16px rgba(255,68,0,.45); animation: flameGlow 1.8s ease-in-out 2; }}
        @keyframes flameGlow {{ 0% {{ transform: scale(1); opacity:.88; }} 25% {{ transform: scale(1.08) rotate(-4deg); opacity:1; }} 50% {{ transform: scale(.98) rotate(3deg); }} 75% {{ transform: scale(1.08) rotate(-2deg); }} 100% {{ transform: scale(1); opacity:.92; }} }}
        .fa-subtle-quote {{ font-size: .9rem; color: var(--muted); text-align:right; line-height:1.5; }}
        .fa-section-title {{ font-size: 1.7rem; font-weight: 750; margin-bottom: .2rem; }}
        .fa-step-badge {{ font-size: .82rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }}
        .fa-list li {{ margin-bottom: .45rem; }}
        .metric-box {{ text-align:center; padding: .7rem .5rem; }}
        .metric-big {{ font-size: 1.9rem; font-weight: 800; }}
        .metric-label {{ color: var(--muted); font-size: .92rem; }}
        .chapter-plan-item {{ padding: .5rem 0; border-bottom: 1px dashed var(--line); font-size: .95rem; }}
        .chapter-plan-item:last-child {{ border-bottom: none; }}
        .soft-kicker {{ color: var(--muted); font-size: 1rem; margin-top:-.1rem; }}
        div[data-testid="stButton"] > button {{
            border-radius: 14px !important;
            padding: .65rem 1rem !important;
            border: 1px solid var(--line) !important;
            background: var(--accent) !important;
            color: {('#f8f6f1' if theme=='dark' else '#fbf7f2')} !important;
            box-shadow: none !important;
        }}
        div[data-testid="stButton"] > button[kind="secondary"] {{
            background: transparent !important;
            color: var(--text) !important;
        }}
        div[data-testid="stRadio"] label, div[data-testid="stCheckbox"] label {{ color: var(--text) !important; }}
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {{
            border-radius: 16px !important; border: 1px solid var(--line) !important; background: var(--panel-2) !important; color: var(--text) !important;
        }}
        .stProgress > div > div > div > div {{ background-color: var(--accent) !important; }}
        .fa-divider {{ height: 1px; background: var(--line); margin: .6rem 0 0; }}
        .small-space {{ height: .55rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def overall_progress():
    completed = len(st.session_state.completed_chapters)
    return completed, TOTAL_CHAPTERS, (completed / TOTAL_CHAPTERS if TOTAL_CHAPTERS else 0)


def progress_for_book(book):
    chapters = CURRICULUM[book]
    completed = sum(chapter_key(book, c) in st.session_state.completed_chapters for c in chapters)
    return completed, len(chapters)


def get_current_lesson():
    book = st.session_state.last_book
    chapter = st.session_state.last_chapter
    key = chapter_key(book, chapter)
    lesson = LESSONS.get(key)
    if not lesson:
        return book, chapter, None, 0
    step_index = st.session_state.chapter_progress.get(key, 0)
    step_index = min(step_index, len(lesson["steps"]) - 1)
    return book, chapter, lesson, step_index


def set_current(book, chapter):
    st.session_state.last_book = book
    st.session_state.last_chapter = chapter
    st.session_state.page = "Cours"
    save_progress()


def get_question_pool(book=None, chapter=None):
    pool = QUESTIONS
    if book:
        pool = [q for q in pool if q["book"] == book]
    if chapter:
        pool = [q for q in pool if q["chapter"] == chapter]
    return pool


def render_progress_bar(value: float):
    width = max(0, min(100, int(value * 100)))
    st.markdown(
        f'<div class="fa-progress-wrap"><div class="fa-progress-bar" style="width:{width}%"></div></div>',
        unsafe_allow_html=True,
    )


def nav_sidebar():
    with st.sidebar:
        st.markdown("## 🎓 FRM Academy")
        pages = ["Accueil", "Cours", "QCM", "À revoir"]
        current = pages.index(st.session_state.page) if st.session_state.page in pages else 0
        picked = st.radio("Navigation", pages, index=current, label_visibility="collapsed")
        st.session_state.page = picked
        st.markdown("---")
        old_theme = st.session_state.theme
        theme_choice = st.toggle("Mode sombre", value=(st.session_state.theme == "dark"))
        st.session_state.theme = "dark" if theme_choice else "light"
        st.markdown(
            f"<div class='fa-panel' style='padding:.9rem 1rem;'>"
            f"<div class='fa-title'>Streak <span class='fa-flame'>🔥</span></div>"
            f"<div class='metric-big'>{st.session_state.streak} jours</div>"
            f"<div class='metric-label'>{st.session_state.xp} XP total</div></div>",
            unsafe_allow_html=True,
        )
        st.caption("FRM Academy — V0.2")
        save_progress()
        if old_theme != st.session_state.theme:
            st.rerun()


def dashboard_page():
    completed, total, progress = overall_progress()
    book, chapter, lesson, step_index = get_current_lesson()
    if lesson:
        total_steps = len(lesson["steps"])
    else:
        total_steps = 1

    search = st.text_input("", placeholder="Rechercher un chapitre, un concept…", label_visibility="collapsed")
    if search:
        search_lower = search.lower()
        hits = []
        for b, chapters in CURRICULUM.items():
            for ch in chapters:
                if search_lower in ch.lower() or search_lower in b.lower():
                    hits.append((b, ch))
        if hits:
            st.markdown("<div class='fa-panel'><div class='fa-title'>Résultats</div>", unsafe_allow_html=True)
            for idx, (b, ch) in enumerate(hits[:6]):
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.write(f"**{b}** — {ch}")
                with c2:
                    if st.button("Ouvrir", key=f"search_{idx}"):
                        set_current(b, ch)
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")

    st.markdown("<div class='fa-hero'>Bonjour Emmanuel 👋</div>", unsafe_allow_html=True)
    st.markdown("<div class='soft-kicker'>Étudie à ton rythme.</div>", unsafe_allow_html=True)
    st.write("")

    left, right = st.columns([3, 1.4])
    with left:
        st.markdown("<div class='fa-panel'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2.2, 1, 1])
        with c1:
            st.markdown("<div class='fa-title'>Ta progression globale</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-big'>{int(progress*100)}%</div>", unsafe_allow_html=True)
            render_progress_bar(progress)
            st.markdown(f"<div class='metric-label'>{completed} / {total} chapitres complétés</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-box'><div class='fa-flame'>🔥</div><div class='metric-big' style='font-size:1.6rem'>{st.session_state.streak}</div><div class='metric-label'>jours de série</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-box'><div style='font-size:1.5rem'>✦</div><div class='metric-big' style='font-size:1.6rem'>{st.session_state.xp}</div><div class='metric-label'>XP total</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='fa-subtle-quote'>\"A little progress each day adds up to big results.\"</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='fa-panel'>", unsafe_allow_html=True)
    c1, c2 = st.columns([4, 1.4])
    with c1:
        st.markdown("<div class='fa-title'>Continue la session</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fa-mini'>{book}</div>", unsafe_allow_html=True)
        st.markdown(f"### {chapter}")
        if lesson:
            render_progress_bar((step_index + 1) / total_steps)
            st.markdown(f"<div class='metric-label'>{step_index + 1} / {total_steps} étapes</div>", unsafe_allow_html=True)
    with c2:
        st.write("")
        st.write("")
        if st.button("Continuer →", key="continue_dashboard"):
            st.session_state.page = "Cours"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='fa-title'>Tes matières</div>", unsafe_allow_html=True)
    cols_top = st.columns(2)
    books = list(CURRICULUM.keys())
    for i, book_name in enumerate(books):
        done, totalb = progress_for_book(book_name)
        col = cols_top[i % 2]
        with col:
            st.markdown("<div class='fa-card'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:1.4rem'>{BOOK_META[book_name]['icon']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fa-title'>{book_name}</div>", unsafe_allow_html=True)
            render_progress_bar(done / totalb if totalb else 0)
            st.markdown(f"<div class='metric-label'>{done} / {totalb} chapitres</div>", unsafe_allow_html=True)
            if st.button("Ouvrir", key=f"open_book_{i}"):
                set_current(book_name, CURRICULUM[book_name][0])
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


def course_page():
    book, chapter, lesson, step_index = get_current_lesson()
    if not lesson:
        st.title(chapter)
        st.info("Le contenu détaillé pour ce chapitre sera ajouté progressivement.")
        return

    steps = lesson["steps"]
    step = steps[step_index]

    st.caption(f"Cours  ›  {book}")
    top_left, top_right = st.columns([4, 1.2])
    with top_left:
        st.markdown(f"<div class='fa-section-title'>{chapter}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='soft-kicker'>{lesson['subtitle']}</div>", unsafe_allow_html=True)
    with top_right:
        st.markdown(f"<div class='fa-chip'><span class='fa-flame'>🔥</span><strong>{st.session_state.streak} jours</strong></div>", unsafe_allow_html=True)

    render_progress_bar((step_index + 1) / len(steps))
    st.markdown(f"<div class='metric-label'>Étape {step_index + 1} / {len(steps)}</div>", unsafe_allow_html=True)
    st.write("")

    main, side = st.columns([3, 1.25])
    with main:
        st.markdown("<div class='fa-panel'>", unsafe_allow_html=True)
        st.markdown(f"<div class='fa-step-badge'>{step['label']}</div>", unsafe_allow_html=True)
        st.markdown(f"## {step['title']}")
        st.write(step["body"])
        st.write("")
        st.markdown("<div class='fa-card'>", unsafe_allow_html=True)
        st.markdown("**À retenir**")
        st.write(step["takeaway"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div class='fa-card'>", unsafe_allow_html=True)
        st.markdown("**Exemple**")
        st.write(step["example"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("**Points essentiels**")
        for item in step["essentials"]:
            st.markdown(f"- {item}")
        st.write("")
        b1, b2, b3 = st.columns([1, 1, 1])
        with b1:
            if st.button("← Précédent", disabled=(step_index == 0), key="prev_step"):
                st.session_state.chapter_progress[chapter_key(book, chapter)] = max(0, step_index - 1)
                save_progress()
                st.rerun()
        with b2:
            if st.button("Demander à l’IA", key="ask_ai"):
                st.info(f"Prompt prêt : Explique-moi {step['title']} dans le chapitre {chapter} ({book}).")
        with b3:
            label = "Terminer le chapitre" if step_index == len(steps) - 1 else "Suivant →"
            if st.button(label, key="next_step"):
                if step_index < len(steps) - 1:
                    st.session_state.chapter_progress[chapter_key(book, chapter)] = step_index + 1
                else:
                    ck = chapter_key(book, chapter)
                    if ck not in st.session_state.completed_chapters:
                        st.session_state.completed_chapters.append(ck)
                        st.session_state.xp += 100
                    st.session_state.page = "QCM"
                    st.session_state.current_question_index = 0
                save_progress()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with side:
        st.markdown("<div class='fa-card'>", unsafe_allow_html=True)
        st.markdown("**Plan du chapitre**")
        for i, s in enumerate(steps, start=1):
            marker = "●" if i - 1 == step_index else "○"
            st.markdown(f"<div class='chapter-plan-item'>{marker} {i}. {s['title']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='fa-card'>", unsafe_allow_html=True)
        st.markdown("**Ressources**")
        st.markdown("- Résumé de chapitre")
        st.markdown("- Formules clés")
        st.markdown("- Exercice supplémentaire")
        st.markdown("</div>", unsafe_allow_html=True)


def qcm_page():
    book = st.session_state.last_book
    chapter = st.session_state.last_chapter
    pool = get_question_pool(book, chapter)
    if not pool:
        st.title("QCM")
        st.info("Aucun QCM n’est encore disponible pour ce chapitre.")
        return

    idx = min(st.session_state.current_question_index, len(pool) - 1)
    q = pool[idx]
    st.caption(f"QCM  ›  {book}")
    top_left, top_right = st.columns([4, 1.5])
    with top_left:
        st.markdown(f"<div class='fa-section-title'>{chapter}</div>", unsafe_allow_html=True)
        st.markdown("<div class='soft-kicker'>Teste tes connaissances et progresse chapitre par chapitre.</div>", unsafe_allow_html=True)
    with top_right:
        st.markdown(
            f"<div class='fa-panel' style='padding:.85rem 1rem;'><div style='display:flex; justify-content:space-between;'>"
            f"<div><span class='fa-flame'>🔥</span> <strong>{st.session_state.streak} jours</strong></div>"
            f"<div><strong>{st.session_state.xp}</strong> XP</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='fa-panel'>", unsafe_allow_html=True)
    st.markdown(f"**Question {idx + 1} / {len(pool)}**")
    render_progress_bar((idx + 1) / len(pool))
    st.write("")
    st.markdown(f"### {q['question']}")

    answer_key = f"ans_{q['id']}"
    previous_choice = st.session_state.question_answers.get(q['id'])

    if q["type"] == "qcm":
        choice = st.radio("", q["options"], index=(q["options"].index(previous_choice) if previous_choice in q["options"] else None), key=answer_key, label_visibility="collapsed")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c3:
            if st.button("Vérifier →", key=f"check_{q['id']}"):
                if choice is None:
                    st.warning("Choisis une réponse.")
                else:
                    st.session_state.question_answers[q['id']] = choice
                    selected = q["options"].index(choice)
                    if selected == q["answer"]:
                        st.success("Bonne réponse ✅")
                        st.session_state.xp += 20
                    else:
                        st.error("Incorrect")
                        if q['id'] not in st.session_state.wrong_questions:
                            st.session_state.wrong_questions.append(q['id'])
                    st.info(q["explanation"])
                    save_progress()
        with c2:
            next_label = "Terminer" if idx == len(pool) - 1 else "Passer"
            if st.button(next_label, key=f"nextq_{q['id']}"):
                if idx < len(pool) - 1:
                    st.session_state.current_question_index = idx + 1
                else:
                    st.session_state.page = "Accueil"
                save_progress()
                st.rerun()
    else:
        txt = st.text_area("Ta réponse", height=160, key=answer_key)
        if st.button("Voir une réponse-type", key=f"free_{q['id']}"):
            st.info(q["model_answer"])
            if idx < len(pool) - 1:
                st.session_state.current_question_index = idx + 1
            save_progress()

    st.markdown("</div>", unsafe_allow_html=True)


def review_page():
    st.markdown("<div class='fa-section-title'>À revoir</div>", unsafe_allow_html=True)
    st.markdown("<div class='soft-kicker'>Retrouve rapidement les questions qui t’ont posé problème.</div>", unsafe_allow_html=True)
    wrong_ids = st.session_state.wrong_questions
    if not wrong_ids:
        st.success("Aucune erreur enregistrée pour l’instant.")
        return

    for q in [q for q in QUESTIONS if q["id"] in wrong_ids]:
        st.markdown("<div class='fa-card'>", unsafe_allow_html=True)
        st.markdown(f"**{q['book']}**")
        st.markdown(f"*{q['chapter']}*")
        st.write(q["question"])
        if q["type"] == "qcm":
            st.markdown("- " + "\n- ".join(q["options"]))
            st.info(q["explanation"])
        else:
            st.info(q["model_answer"])
        if st.button("Retenter ce chapitre", key=f"retry_{q['id']}"):
            set_current(q["book"], q["chapter"])
            st.session_state.page = "QCM"
            st.session_state.current_question_index = 0
            save_progress()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")


def main():
    st.set_page_config(page_title="FRM Academy", page_icon="🎓", layout="wide")
    init_state()
    nav_sidebar()
    inject_css(st.session_state.theme)

    if st.session_state.page == "Accueil":
        dashboard_page()
    elif st.session_state.page == "Cours":
        course_page()
    elif st.session_state.page == "QCM":
        qcm_page()
    else:
        review_page()

    save_progress()


if __name__ == "__main__":
    main()
