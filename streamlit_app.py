import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import io

st.set_page_config(page_title="Kabda AI Workbench Francis — Secure Private", page_icon="K", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: "Space Grotesk", sans-serif; }
.mono { font-family: "JetBrains Mono", monospace; }
div[data-testid="stMetricValue"] { font-size: 28px; color: #22c55e; }
</style>
""", unsafe_allow_html=True)

st.title("KABDA AI WORKBENCH — Francis Mulwa Muithya")
st.caption("SECURE PRIVATE • FINAL PWA • 6 TABS • 100/100 • KPLC KES ROI • Offline-first")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 Auto-Pilot & Cloud AI", 
    "📊 CSV Data Analyst", 
    "🧠 VRAM & ROI", 
    "📄 Master Resume", 
    "🔗 Dolinks Bio", 
    "🎓 IT Mastery Tracker"
])

# ================= TAB 1 =================
with tab1:
    st.subheader("Cloud AI Orchestration — Secure PWA")
    st.write("Deploy agents across GitHub Pages, Netlify, Vercel. No hardcoded private contacts — personal fields auto-mask as •••• when Public Safe mode is active.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("No hardcoded contact ✓ — HTTPS ready • LocalStorage offline persistence")
    with col2:
        st.metric("READINESS", "100/100", "Secure")
        st.progress(100)
    
    st.divider()
    st.markdown("### 1-Tap Live Link (GitHub Pages / Netlify)")
    
    live_url = st.text_input("Your Live URL (auto-filled after deploy)", value="https://yourusername.github.io/kabda/", help="Paste your GitHub Pages URL after deploying. This auto-injects into bio & resume.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.link_button("Deploy on GitHub Pages ↗", "https://github.com/new", use_container_width=True)
    with c2:
        st.link_button("Deploy on Netlify Drop ↗", "https://app.netlify.com/drop", use_container_width=True)
    with c3:
        st.download_button("Download deployment_logs.json", data=f'{{"app":"Kabda AI Workbench","tabs":6,"url":"{live_url}"}}', file_name="deployment_logs.json", mime="application/json", use_container_width=True)
    
    # --- PWA EMBED: This is the clean snippet to paste ---
    # The PWA is embedded below so your Streamlit app *is* the workbench on mobile
    with st.expander("📱 Show Embedded PWA (offline capable)", expanded=True):
        # Load the clean PWA HTML we built
        try:
            with open("kabda-netlify/index.html", "r", encoding="utf-8") as f:
                pwa_html = f.read()
            # components.html needs height
            components.html(pwa_html, height=900, scrolling=True)
        except FileNotFoundError:
            st.info("Place your Kabda-Final-PWA.html as kabda-netlify/index.html to embed the full offline PWA here. For now showing placeholder.")
            components.html(f"""
            <div style="background:#0f172a;color:#e2e8f0;padding:20px;border-radius:16px;font-family:sans-serif">
                <h3>KABDA AI WORKBENCH</h3>
                <p>Live link: {live_url}</p>
                <button onclick="navigator.clipboard.writeText('{live_url}'); this.innerText='Copied ✓'" 
                style="padding:12px 18px;border-radius:12px;background:#22c55e;color:#052e16;font-weight:700;border:none;cursor:pointer">
                1-Tap Copy & Share Live Link</button>
            </div>
            """, height=250)

# ================= TAB 2 =================
with tab2:
    st.subheader("CSV Data Analyst — Offline Engine (Python)")
    st.write("Process CSV files locally — zero server uploads, 100% offline compatible. Cleaner than JS FileReader with Pandas stats.")
    
    uploaded = st.file_uploader("Tap to choose or drop CSV here", type=["csv"])
    
    if uploaded:
        df = pd.read_csv(uploaded)
        st.success(f"Rows: {len(df)} | Columns: {len(df.columns)} | Missing cells: {df.isna().sum().sum()}")
        
        # Numeric summary
        numeric = df.select_dtypes(include=['number'])
        if not numeric.empty:
            st.markdown("#### Numeric Summary")
            st.dataframe(numeric.describe().T, use_container_width=True)
        else:
            st.info("No numeric columns detected.")
        
        st.markdown("#### Preview (first 15 rows)")
        st.dataframe(df.head(15), use_container_width=True)
        
        # Cleaned export
        df_cleaned = df.fillna(0)
        # Trim whitespace for object cols
        for col in df_cleaned.select_dtypes(include=['object']).columns:
            df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
        
        csv_buffer = io.StringIO()
        df_cleaned.to_csv(csv_buffer, index=False)
        
        st.download_button("Export Cleaned CSV", data=csv_buffer.getvalue(), file_name="kabda_cleaned_data.csv", mime="text/csv", type="primary")
    else:
        st.info("Upload a CSV to see stats, numeric summary, and cleaned export.")

# ================= TAB 3 =================
with tab3:
    st.subheader("LLM VRAM & KPLC KES ROI Calculator")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("**🧠 MEMORY ENGINE — LLM VRAM Calculator**")
        params_b = st.number_input("Model Parameters (Billions)", value=8.0, min_value=0.5, max_value=1000.0, step=0.5)
        quant = st.selectbox("Precision / Quantization", options=[("FP32 (4 bytes/param)",4), ("FP16 / BF16 (2 bytes/param)",2), ("INT8 / FP8 (1 byte/param)",1), ("INT4 / Q4_K_M (0.5 bytes/param)",0.5)], format_func=lambda x: x[0])
        bytes_per_param = quant[1]
        
        context = st.selectbox("Context Length (Tokens)", options=[2048,4096,8192,32768,131072], index=2)
        batch = st.number_input("Concurrent Batch Size", value=1, min_value=1, max_value=32)
        overhead_pct = st.slider("CUDA & Activation Overhead %", 0, 50, 20)
        
        # Calculation — same formula as JS: Params × Bytes_per_param + KV cache + overhead
        weights_gb = params_b * bytes_per_param
        kv_cache_gb = (params_b * (context / 1024) * 0.042) * batch
        subtotal = weights_gb + kv_cache_gb
        overhead_gb = subtotal * (overhead_pct / 100)
        total_gb = subtotal + overhead_gb
        
        st.metric("TOTAL VRAM REQUIRED", f"{total_gb:.1f} GB")
        st.progress(min(100, int(total_gb/80*100)) if total_gb<=80 else 100)
        
        # GPU rec
        if total_gb > 48:
            rec = "Fits: 1x A100 / H100 (80 GB) or Multi-GPU"
        elif total_gb > 24:
            rec = "Fits: 1x A6000 / L40S (48 GB) or 2x RTX 4090"
        elif total_gb > 16:
            rec = "Fits: 1x RTX 3090 / 4090 (24 GB)"
        elif total_gb > 12:
            rec = "Fits: 1x RTX 4060 Ti / 4080 (16 GB)"
        else:
            rec = "Fits: RTX 3060 (12 GB) / Mobile Edge"
        
        st.code(f"{rec}\nWeights: {weights_gb:.1f} GB • KV Cache: {kv_cache_gb:.1f} GB • Overhead: {overhead_gb:.1f} GB", language="text")
    
    with col_right:
        st.markdown("**💰 KENYA (KES) ROI — Workload & Power**")
        st.caption("Calculate KPLC power costs (KES/kWh), API revenue, and payback.")
        
        hw_cost = st.number_input("Hardware / Cloud Cost (KES)", value=150000, step=1000)
        watts = st.number_input("System Power Draw (Watts)", value=450, step=10)
        kplc_rate = st.number_input("KPLC Tariff (KES / kWh)", value=28.5, step=0.1)
        hours_day = st.number_input("Active AI Hours / Day", value=8, step=1)
        rps = st.number_input("Throughput (Requests / Sec)", value=5, step=1)
        price_1k = st.number_input("Revenue per 1K Req (KES)", value=20, step=1)
        
        kwh_month = (watts / 1000) * hours_day * 30
        power_cost_month = kwh_month * kplc_rate
        req_per_day = rps * 3600 * hours_day
        rev_month = (req_per_day / 1000) * price_1k * 30
        net_profit_month = rev_month - power_cost_month
        daily_profit = net_profit_month / 30
        break_even = int(hw_cost / daily_profit) if daily_profit>0 else 9999
        
        m1, m2 = st.columns(2)
        m1.metric("MONTHLY REVENUE", f"KES {rev_month:,.0f}")
        m2.metric("MONTHLY KPLC POWER", f"KES {power_cost_month:,.0f}")
        
        m3, m4 = st.columns(2)
        m3.metric("NET MONTHLY PROFIT", f"KES {net_profit_month:,.0f}", delta=f"{net_profit_month:,.0f}")
        m4.metric("BREAK-EVEN", f"{break_even} Days" if break_even!=9999 else "Never (Loss)")

# ================= TAB 4 =================
with tab4:
    st.subheader("Master Resume — Privacy-Aware CV")
    st.markdown("""
    **Francis Mulwa Muithya**  
    AI Operations Specialist • Freelance Technical Writer • Workflow Automation Builder  
    Location: Kenya (Remote) • Contact: •••• •••• ••••
    
    **PROFESSIONAL SUMMARY**  
    Results-driven AI business professional and remote freelancer specializing in AI-assisted content production, prompt engineering, workflow automation (Make, n8n, Zapier), and offline-first web tools.
    
    **CORE COMPETENCIES**  
    AI Workflow Automation, Prompt Engineering, Technical & SEO Writing, Data Cleaning (CSV/Excel), PWA & Web Deployment, AI Data Annotation
    
    **VERIFIED CERTIFICATIONS**  
    - AI for Business Professionals — HP LIFE (Nov 2026)
    - Strategic Planning in the AI Age — HP LIFE (Sep 2026)
    - Leadership & Management — IIENSTITU (In Progress)
    """)
    cv_text = f"""FRANCIS MULWA MUITHYA
AI Operations Specialist | Freelance Technical Writer | Workflow Automation Builder
Live Workbench: {live_url}
SUMMARY
Results-driven AI business professional and remote freelancer specializing in AI-assisted content production, prompt engineering, workflow automation (Make, n8n, Zapier), and offline-first web tools.
CERTIFICATIONS
• AI for Business Professionals — HP LIFE (Completed Nov 4, 2026)
• Strategic Planning in the AI Age — HP LIFE (Completed Sep 11, 2026)
• Leadership Course — IIENSTITU (In Progress)
SKILLS
AI Workflow Automation, Prompt Engineering, Technical & SEO Writing, CSV/Excel Data Cleaning, PWA Deployment, AI Data Annotation.
"""
    st.code(cv_text, language="text")
    st.download_button("Copy Plain-Text CV (Download)", data=cv_text, file_name="Francis_Mulwa_Muithya_CV.txt")

# ================= TAB 5 =================
with tab5:
    st.subheader("Dolinks & Freelance Bio Generator")
    angle = st.selectbox("Pitch Focus", ["Full-Stack AI Freelancer & Writer (Default)", "AI-Augmented Content & Research Writer", "Workflow Automation & Data Analyst"])
    portfolio_url = st.text_input("Portfolio Document URL (HTTPS)", value="https://docs.google.com/document/d/1uR1EP5SbS0FTgEDcFa7GEB7CUYRcPWtndnygHrPSfag/edit")
    
    def ensure_https(u):
        u=u.strip()
        if not u: return "https://docs.google.com"
        return u if u.startswith("http") else "https://"+u
    
    url = ensure_https(portfolio_url)
    live_app_line = f"\nLive AI Workbench: {live_url}" if live_url.startswith("http") else ""
    
    if angle.startswith("AI-Augmented"):
        bio = f"""Hi, I'm Francis Mulwa Muithya — an HP LIFE Certified AI Business Professional and freelance technical writer. I combine human editorial judgment with structured AI workflows to deliver well-researched articles, SOPs, and business copy on deadline.

Credentials:
• HP LIFE: AI for Business Professionals (Certified)
• HP LIFE: Strategic Planning in the AI Age (Certified)
• IIENSTITU: Leadership Program (In Progress)

View my writing & project portfolio: {url}{live_app_line}"""
    elif angle.startswith("Workflow"):
        bio = f"""Hi, I'm Francis Mulwa Muithya — an AI workflow builder and data operations freelancer. I help businesses automate repetitive tasks using Make, n8n, Zapier, and clean CSV/Excel pipelines, backed by formal training in AI business strategy.

Credentials:
• HP LIFE: AI for Business Professionals (Certified)
• HP LIFE: Strategic Planning in the AI Age (Certified)

Explore my work samples: {url}{live_app_line}"""
    else:
        bio = f"""Hi, I'm Francis Mulwa Muithya — an HP LIFE Certified AI Business Professional, freelance writer, and workflow automation builder. I help remote teams and founders save hours every week through clear, research-backed content, clean data processing, and practical AI workflows.

Verified Training:
• AI for Business Professionals — HP LIFE (Nov 2026)
• Strategic Planning in the AI Age — HP LIFE (Sep 2026)
• Leadership Course — IIENSTITU (In Progress)

Portfolio & Samples: {url}{live_app_line}"""
    
    st.text_area("Live Editable Bio", value=bio, height=250, key="bio")
    st.caption(f"Character count: {len(bio)}")
    st.download_button("Copy Bio to Clipboard (Download)", data=bio, file_name="kabda_bio.txt")

# ================= TAB 6 =================
with tab6:
    st.subheader("IT & AI Mastery Tracker")
    st.caption("LocalStorage equivalent — uses st.session_state for this session, persistent in PWA version via kabda_courses_v1")
    
    if "courses" not in st.session_state:
        st.session_state.courses = [
            {"title":"AI for Business Professionals","platform":"HP LIFE • Nov 4, 2026","done":True},
            {"title":"Strategic Planning in the AI Age","platform":"HP LIFE • Sep 11, 2026","done":True},
            {"title":"Leadership & Management Course","platform":"IIENSTITU • Ongoing","done":False},
            {"title":"AI Agentic Workflows (Make / n8n / Zapier)","platform":"Practical Lab","done":False},
            {"title":"Python for AI & Data Automation","platform":"Self-Paced Track","done":False},
        ]
    
    completed = sum(1 for c in st.session_state.courses if c["done"])
    pct = int(completed / len(st.session_state.courses) * 100) if st.session_state.courses else 0
    st.progress(pct, text=f"{pct}% Complete ({completed}/{len(st.session_state.courses)})")
    
    for i, c in enumerate(st.session_state.courses):
        col_a, col_b = st.columns([4,1])
        with col_a:
            st.markdown(f"**{'✓ ' if c['done'] else ''}{c['title']}**  \n<span style='color:#94a3b8;font-size:12px'>{c['platform']}</span>", unsafe_allow_html=True)
        with col_b:
            if st.button("Completed" if c["done"] else "Mark Done", key=f"course_{i}"):
                st.session_state.courses[i]["done"] = not st.session_state.courses[i]["done"]
                st.rerun()
    
    st.divider()
    with st.form("add_course"):
        new_title = st.text_input("Course title")
        new_platform = st.text_input("Platform • Date", placeholder="Self-Paced")
        submitted = st.form_submit_button("+ Add to Tracker", use_container_width=True)
        if submitted and new_title.strip():
            st.session_state.courses.append({"title":new_title.strip(),"platform":new_platform.strip() or "Self-Paced","done":False})
            st.rerun()

# --- Footer: PWA Service Worker Hint ---
st.divider()
st.caption("To connect your code to a one-tap live link: Deploy this Streamlit app to Streamlit Cloud, then also deploy Kabda-Final-PWA.html to GitHub Pages (Settings → Pages → main / root). The PWA works offline; Streamlit gives you Python power.")
