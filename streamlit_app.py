import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime, timezone

st.set_page_config(page_title="Kabda AI Workbench — Francis", page_icon="K", layout="wide", initial_sidebar_state="collapsed")

if "public_safe" not in st.session_state:
    st.session_state.public_safe = True

if "courses" not in st.session_state:
    st.session_state.courses = [
        {"title": "AI for Business Professionals", "platform": "HP LIFE • Nov 4, 2026", "done": True},
        {"title": "Strategic Planning in the AI Age", "platform": "HP LIFE • Sep 11, 2026", "done": True},
        {"title": "Leadership & Management Course", "platform": "IIENSTITU • Ongoing", "done": False},
        {"title": "AI Agentic Workflows (Make / n8n / Zapier)", "platform": "Practical Lab", "done": False},
        {"title": "Python for AI & Data Automation", "platform": "Self-Paced Track", "done": False},
    ]

col_title, col_priv = st.columns([3, 1])
with col_title:
    st.title("Kabda AI Workbench")
    st.caption("FRANCIS • SECURE PRIVATE • STREAMLIT + PWA • 6 TABS • 100/100")
with col_priv:
    st.session_state.public_safe = st.toggle("Public Safe Mode (Mask Contacts)", value=st.session_state.public_safe)

components.html("""
<button onclick="shareLiveLink()" style="padding:0.6rem 1.1rem;border:none;border-radius:8px;background:#22c55e;color:#052e16;font-weight:700;font-size:14px;cursor:pointer">1-Tap Copy & Share Live Link</button>
<script>
async function shareLiveLink() {
  let liveLink = "";
  try { liveLink = window.parent.location.origin + window.parent.location.pathname; } catch(e) { liveLink = document.referrer || window.location.href; }
  if (navigator.share) { try { await navigator.share({title: 'Kabda AI Workbench — Francis Mulwa Muithya', text: 'Test my live AI, CSV Analyst & VRAM/ROI Workbench:', url: liveLink}); return; } catch(err) {} }
  try { await navigator.clipboard.writeText(liveLink); alert('Live link copied: ' + liveLink); } catch(err) { prompt('Copy your live link:', liveLink); }
}
</script>
""", height=56)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Auto-Pilot & Cloud AI", "CSV Data Analyst", "VRAM & KPLC ROI", "Master Resume", "Dolinks Bio", "IT Mastery Tracker"])

with tab1:
    st.subheader("Cloud AI Orchestration — Secure Workbench")
    st.write("Deploy across Streamlit Community Cloud, GitHub Pages, and Netlify. Personal contact details stay masked (••••) whenever Public Safe Mode is ON.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Security Status", "Public Safe ✓" if st.session_state.public_safe else "Unmasked Local")
    c2.metric("Readiness Score", "100 / 100")
    c3.metric("Offline PWA Companion", "Live on GitHub Pages")
    st.link_button("Open Offline GitHub Pages PWA ↗", "https://ozilkabda-commits.github.io/kabda/")
    st.link_button("Open Cloud Streamlit App ↗", "https://appapppy-s8e2kisjgrtzkhrjvshqrr.streamlit.app")
    log_payload = json.dumps({"app": "Kabda AI Workbench Francis", "runtime": "Streamlit Python + GitHub Pages PWA", "pwa_url": "https://ozilkabda-commits.github.io/kabda/ | https://appapppy-s8e2kisjgrtzkhrjvshqrr.streamlit.app", "public_safe_mode": st.session_state.public_safe, "exported_at": datetime.now(timezone.utc).isoformat()}, indent=2)
    st.download_button("Download deployment_logs.json", data=log_payload, file_name="deployment_logs.json", mime="application/json")

with tab2:
    st.subheader("CSV Data Analyst (Pandas Engine)")
    uploaded = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        missing_count = int(df.isna().sum().sum())
        m1, m2, m3 = st.columns(3)
        m1.metric("Rows", len(df)); m2.metric("Columns", len(df.columns)); m3.metric("Missing Cells", missing_count)
        st.dataframe(df.head(20), use_container_width=True)
        num_df = df.select_dtypes(include="number")
        if not num_df.empty:
            summary = num_df.describe().T[["count", "mean", "min", "max"]]
            summary["sum"] = num_df.sum()
            st.dataframe(summary, use_container_width=True)
        cleaned_df = df.fillna(0)
        st.download_button("Export Cleaned CSV", data=cleaned_df.to_csv(index=False).encode("utf-8"), file_name="kabda_cleaned_data.csv", mime="text/csv")

with tab3:
    col_vram, col_roi = st.columns(2)
    with col_vram:
        st.subheader("LLM VRAM Calculator")
        params_b = st.number_input("Model Parameters (Billions)", min_value=0.5, max_value=1000.0, value=8.0, step=0.5)
        quant_label = st.selectbox("Precision / Quantization", options=[("FP32 (4 bytes/param)", 4.0), ("FP16 / BF16 (2 bytes/param)", 2.0), ("INT8 / FP8 (1 byte/param)", 1.0), ("INT4 / Q4_K_M (0.5 bytes/param)", 0.5)], index=1, format_func=lambda x: x[0])
        context_len = st.selectbox("Context Length (Tokens)", [2048, 4096, 8192, 32768, 131072], index=2)
        batch_size = st.number_input("Concurrent Batch Size", min_value=1, max_value=128, value=1, step=1)
        overhead_pct = st.slider("CUDA & Activation Overhead (%)", min_value=10, max_value=40, value=20)
        bytes_per_param = quant_label[1]
        weights_gb = params_b * bytes_per_param
        kv_cache_gb = (params_b * (context_len / 1024.0) * 0.042) * batch_size
        subtotal_gb = weights_gb + kv_cache_gb
        overhead_gb = subtotal_gb * (overhead_pct / 100.0)
        total_vram_gb = subtotal_gb + overhead_gb
        if total_vram_gb > 48: gpu_rec = "Fits: 1x A100 / H100 (80 GB) or Multi-GPU"
        elif total_vram_gb > 24: gpu_rec = "Fits: 1x A6000 / L40S (48 GB) or 2x RTX 4090"
        elif total_vram_gb > 16: gpu_rec = "Fits: 1x RTX 3090 / 4090 (24 GB)"
        elif total_vram_gb > 12: gpu_rec = "Fits: 1x RTX 4060 Ti / 4080 (16 GB)"
        else: gpu_rec = "Fits: RTX 3060 (12 GB) / Mobile Edge"
        st.metric("Total VRAM Required", f"{total_vram_gb:.1f} GB", delta=gpu_rec)
        st.progress(min(1.0, total_vram_gb / (80.0 if total_vram_gb > 24 else 24.0)))
        st.caption(f"Weights: {weights_gb:.1f} GB • KV Cache: {kv_cache_gb:.1f} GB • Overhead: {overhead_gb:.1f} GB")
    with col_roi:
        st.subheader("Kenya (KES) Workload & KPLC ROI")
        hw_cost = st.number_input("Hardware / Setup Cost (KES)", min_value=0, value=180000, step=5000)
        watts = st.number_input("System Power Draw (Watts)", min_value=50, max_value=5000, value=350, step=25)
        kplc_rate = st.number_input("KPLC Tariff (KES / kWh)", min_value=10.0, max_value=60.0, value=28.5, step=0.5)
        hours_day = st.number_input("Active AI Hours / Day", min_value=1, max_value=24, value=8, step=1)
        rps = st.number_input("Throughput (Requests / Sec)", min_value=0.1, max_value=100.0, value=1.5, step=0.1)
        price_1k = st.number_input("Revenue per 1K Requests (KES)", min_value=1, max_value=5000, value=65, step=5)
        kwh_month = (watts / 1000.0) * hours_day * 30
        power_cost_month = kwh_month * kplc_rate
        req_per_day = rps * 3600 * hours_day
        rev_month = (req_per_day / 1000.0) * price_1k * 30
        net_profit_month = rev_month - power_cost_month
        daily_profit = net_profit_month / 30.0
        breakeven_days = f"{int(-(-hw_cost // daily_profit))} Days" if daily_profit > 0 else "Never (Loss)"
        r1, r2 = st.columns(2); r1.metric("Monthly Revenue", f"KES {rev_month:,.0f}"); r2.metric("Monthly KPLC Power", f"KES {power_cost_month:,.0f}")
        r3, r4 = st.columns(2); r3.metric("Net Monthly Profit", f"KES {net_profit_month:,.0f}"); r4.metric("Break-Even Horizon", breakeven_days)

with tab4:
    st.subheader("Francis Mulwa Muithya")
    st.write("**AI Operations Specialist • Freelance Technical Writer • Workflow Automation Builder**")
    location_txt = "Kenya (Remote)" if st.session_state.public_safe else "Machakos / Nairobi, Kenya"
    contact_txt = "•••• •••• ••••" if st.session_state.public_safe else "Available on Direct Request"
    st.caption(f"Location: {location_txt}  |  Contact: {contact_txt}")
    st.markdown("**Professional Summary**\nResults-driven AI business professional and remote freelancer specializing in AI-assisted content production, prompt engineering, workflow automation (Make, n8n, Zapier), and offline-first web tools.\n\n**Verified Certifications**\n- AI for Business Professionals — HP LIFE (Nov 4, 2026)\n- Strategic Planning in the AI Age — HP LIFE (Sep 11, 2026)\n- Leadership & Management Course — IIENSTITU (In Progress)")
    cv_plain = "FRANCIS MULWA MUITHYA\nAI Operations Specialist | Freelance Technical Writer | Workflow Automation Builder\nLive PWA Workbench: https://ozilkabda-commits.github.io/kabda/\n"
    st.download_button("Download Plain-Text CV (.txt)", data=cv_plain, file_name="Francis_Mulwa_Muithya_CV.txt")

with tab5:
    st.subheader("Dolinks & Freelance Bio Generator")
    angle = st.selectbox("Pitch Focus", ["Full-Stack AI Freelancer & Writer", "AI-Augmented Content & Research Writer", "Workflow Automation & Data Analyst"])
    live_pwa = st.text_input("Live PWA Link", value="https://ozilkabda-commits.github.io/kabda/ | https://appapppy-s8e2kisjgrtzkhrjvshqrr.streamlit.app")
    portfolio_doc = st.text_input("Portfolio Document URL", value="https://docs.google.com/document/d/1uR1EP5SbS0FTgEDcFa7GEB7CUYRcPWtndnygHrPSfag/edit")
    if angle == "AI-Augmented Content & Research Writer":
        bio_text = f"Hi, I'm Francis Mulwa Muithya — an HP LIFE Certified AI Business Professional and freelance technical writer.\n\nLive AI Workbench: {live_pwa}\nPortfolio: {portfolio_doc}"
    elif angle == "Workflow Automation & Data Analyst":
        bio_text = f"Hi, I'm Francis Mulwa Muithya — an AI workflow builder and data operations freelancer.\n\nLive AI Workbench: {live_pwa}\nPortfolio: {portfolio_doc}"
    else:
        bio_text = f"Hi, I'm Francis Mulwa Muithya — an HP LIFE Certified AI Business Professional, freelance writer, and workflow automation builder.\n\nLive AI Workbench: {live_pwa}\nPortfolio: {portfolio_doc}"
    edited_bio = st.text_area("Copy-Ready Bio", value=bio_text, height=180)
    st.caption(f"Character count: {len(edited_bio)}")

with tab6:
    st.subheader("IT & AI Mastery Tracker")
    completed = sum(1 for c in st.session_state.courses if c["done"])
    total = len(st.session_state.courses)
    pct = int((completed / total) * 100) if total else 0
    st.metric("Overall Progress", f"{pct}% ({completed}/{total} Modules)")
    st.progress(pct / 100.0)
    for i, course in enumerate(st.session_state.courses):
        st.session_state.courses[i]["done"] = st.checkbox(f"{course['title']} — {course['platform']}", value=course["done"], key=f"course_{i}")
    with st.form("add_course_form", clear_on_submit=True):
        new_title = st.text_input("New Course or Skill Title")
        new_plat = st.text_input("Platform (e.g., HP LIFE, Alison, Coursera)")
        if st.form_submit_button("+ Add Module") and new_title.strip():
            st.session_state.courses.append({"title": new_title.strip(), "platform": new_plat.strip() or "Self-Paced", "done": False})
            st.rerun()
