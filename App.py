import io
import os
import zipfile
import hashlib
import pandas as pd
import streamlit as st
import re

# ---------- BRAND ----------
COMPANY_NAME = "True Blue Analytics"
TOOL_NAME = "Easy Hasher"
LOGO_PATH = r"IMG/signal-2025-11-05-141904.png"

st.set_page_config(page_title=f"{TOOL_NAME} • {COMPANY_NAME}", page_icon=None, layout="wide")

# ---------- THEME + DESIGNS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

    :root{
        --bg1:#eff4ff; --bg2:#eaf1ff; --panel:#ffffff;
        --ink:#141d49; --muted:#6e7b99; --line:#d9e2ff;
        --brand:#141d49; --brand-2:#141d49; --brand-3:#141d49;
        --accent:#b7c8ff; --focus:#3aa0ff;
        --input-bg:#ffffff; --input-text:#141d49; --placeholder:#8fa1c0; --input-border:#b9c8ef;
        --ring:0 0 0 3px rgba(20,29,73,.28);
    }

    *{ -webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale }
    html,body,[data-testid="stAppViewContainer"]{
        background:
          radial-gradient(1200px 800px at 90% -10%, rgba(20,29,73,.08) 0%, rgba(20,29,73,0) 60%),
          radial-gradient(900px 600px at -10% 10%, rgba(20,29,73,.06) 0%, rgba(20,29,73,0) 55%),
          linear-gradient(180deg,var(--bg1),var(--bg2));
        color:var(--ink);
        font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
        letter-spacing:.1px;
    }

    /* SIDE RAILS */
    .siderail-left, .siderail-right{
        position:fixed; top:0; bottom:0; width:16px; z-index:1000; pointer-events:none;
        background:linear-gradient(180deg, #141d49 0%, #1b2470 60%, #141d49 100%);
        box-shadow: 0 0 22px rgba(20,29,73,.40);
    }
    .siderail-left{ left:0; }
    .siderail-right{ right:0; }

    .dotgrid:before{
        content:""; position:fixed; inset:0; z-index:-1; opacity:.22; pointer-events:none;
        background-image: radial-gradient(rgba(20,29,73,.12) 1px, transparent 1px);
        background-size: 18px 18px;
        mask-image: linear-gradient(to bottom, rgba(0,0,0,.8), rgba(0,0,0,0));
    }

    .block-container{padding:0 1.25rem 2rem 1.25rem; max-width:1200px}

    .brandbar{
        position:sticky; top:0; z-index:999; background:#fff; border-bottom:1px solid var(--line);
        margin:0 -1.25rem 0.9rem -1.25rem; padding:.35rem 0 0 0; overflow:hidden;
    }
    .brandwrap{display:flex; align-items:center; gap:12px; max-width:1200px; margin:0 auto; padding:0 1.25rem; justify-content:flex-start;}
    .brandlogo{max-height:46px;}
    .brandbar:after{
        content:""; display:block; height:3px; width:120%;
        background:linear-gradient(90deg, rgba(20,29,73,.0), rgba(20,29,73,.35), rgba(20,29,73,.9), rgba(20,29,73,.35), rgba(20,29,73,.0));
        animation: slideStripe 6s linear infinite;
        transform: translateX(-10%);
    }
    @keyframes slideStripe { 0%{transform:translateX(-10%);} 100%{transform:translateX(-30%);} }

    .hero{
        display:flex; gap:16px; align-items:center; justify-content:space-between;
        background:linear-gradient(180deg,#ffffff,#f5f7ff);
        border:1px solid var(--line); border-radius:18px; padding:16px 18px;
        box-shadow:0 14px 30px rgba(20,29,73,.08); margin-bottom:12px; position:relative; overflow:hidden;
    }
    .hero:before{
        content:""; position:absolute; right:-80px; top:-80px; width:260px; height:260px; border-radius:50%;
        background: radial-gradient(closest-side, rgba(20,29,73,.08), transparent 65%);
    }
    .hero .right .badges{display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end}
    .badge{
        display:inline-flex; align-items:center; gap:6px;
        padding:.32rem .6rem; border-radius:999px; border:1px solid #dbe3ff; background:#eef2ff; color:var(--ink);
        font-size:.82rem; font-weight:600;
    }

    .stTabs [data-baseweb="tab-list"]{gap:.5rem; margin:.5rem 0 .75rem}
    .stTabs [data-baseweb="tab"]{
        background:#eef2ff; border:1px solid var(--line); border-bottom:2px solid transparent; border-radius:12px 12px 0 0;
        padding:.68rem 1rem; color:var(--ink); font-weight:650;
    }
    .stTabs [aria-selected="true"]{background:#ffffff; border-bottom:4px solid var(--brand-2)}
    .card{
        background:linear-gradient(180deg,#ffffff, #f5f7ff);
        border:1px solid var(--line); border-radius:18px; padding:1rem 1rem 1.1rem 1rem;
        box-shadow:0 14px 30px rgba(20,29,73,.08); margin-bottom:.9rem
    }

    label{color:var(--ink)!important; font-weight:600!important}
    input,textarea,select{
        font-size:16px!important; color:var(--input-text)!important; font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif!important;
    }
    .stTextInput input,.stTextArea textarea{
        background:var(--input-bg)!important; color:var(--input-text)!important; border:1px solid var(--input-border)!important; border-radius:14px!important;
        box-shadow:none!important; padding:.7rem .9rem!important
    }
    .stTextInput input::placeholder,.stTextArea textarea::placeholder{color:var(--placeholder)!important}
    .stTextInput input:focus,.stTextArea textarea:focus{box-shadow:var(--ring)!important; border-color:var(--brand-3)!important; outline:none!important}
    .stSelectbox div[data-baseweb="select"]>div{
        background:var(--input-bg)!important; color:var(--input-text)!important; border:1px solid var(--input-border)!important;
        border-radius:14px!important; min-height:48px!important; padding:4px 8px!important;
        font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif!important
    }
    [data-testid="stRadio"] [role="radiogroup"] label{border-radius:12px; padding:.35rem .6rem; font-weight:600!important}
    [data-testid="stRadio"] [role="radiogroup"] label:hover{background:rgba(20,29,73,.08)}
    [data-testid="stRadio"] [role="radiogroup"] input:focus+div{box-shadow:var(--ring); border-radius:12px}

    .stDownloadButton button,.stButton button{
        background:linear-gradient(135deg,var(--brand) 0%,var(--brand-2) 60%,var(--brand-3) 100%)!important;
        color:#ffffff!important; border:none!important; border-radius:14px!important;
        padding:.85rem 1rem!important; font-weight:700!important; letter-spacing:.2px
    }
    .stDownloadButton button:hover,.stButton button:hover{filter:brightness(1.06)}

    .gradline{height:2px; width:100%; margin:.5rem 0 1rem 0;
      background:linear-gradient(90deg, transparent, rgba(20,29,73,.65), transparent);
      border-radius:2px;}

    /* Prevent header wrapping like "E mail" */
    .stDataFrame table { letter-spacing: 0 !important; }
    .stDataFrame thead tr th div, .stDataFrame thead tr th span,
    [data-testid="stDataFrame"] [data-testid="columnHeaderName"]{
        white-space:nowrap!important; word-break:keep-all!important; hyphens:none!important;
    }

    .footer{
        background:linear-gradient(135deg,var(--brand) 0%,var(--brand-2) 60%,var(--brand-3) 100%);
        color:#fff; margin:2rem -1.25rem 0 -1.25rem; border-top:1px solid var(--line);
    }
    .footerwrap{ max-width:1200px; margin:0 auto; padding:.9rem 1.25rem; font-weight:800; letter-spacing:.3px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Side rails + background dots
st.markdown("<div class='siderail-left'></div>", unsafe_allow_html=True)
st.markdown("<div class='siderail-right'></div>", unsafe_allow_html=True)
st.markdown("<div class='dotgrid'></div>", unsafe_allow_html=True)

# ---------- BRAND BAR ----------
st.markdown('<div class="brandbar"><div class="brandwrap">', unsafe_allow_html=True)
try:
    st.image(LOGO_PATH, use_container_width=False, caption=None, output_format="PNG")
except Exception:
    st.write("")
st.markdown('</div></div>', unsafe_allow_html=True)

# ---------- HERO ----------
col_hero_l, col_hero_r = st.columns([1.25, 1])
with col_hero_l:
    st.markdown(
        f"""
        <div class="hero">
            <div>
                <h1 style="margin:.1rem 0 .15rem 0;">{TOOL_NAME}</h1>
                <div style="display:flex;gap:8px;flex-wrap:wrap;margin:.25rem 0 .6rem 0;">
                    <span class="badge">MD5 / SHA-1 / SHA-256 / SHA-512</span>
                    <span class="badge">Phone 10-digit normalize</span>
                    <span class="badge">Live preview</span>
                    <span class="badge">Combine & dedupe</span>
                </div>
                <div class="subtitle">Hash emails or phones in seconds. Clean, preview, and export — built for scale and clarity.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_hero_r:
    st.markdown(
        """
        <div class="card">
          <h2 style="margin-bottom:.4rem;">How it works</h2>
          <div class="gradline"></div>
          <ol style="margin:.3rem 0 0 1rem; padding:0; line-height:1.45;">
            <li>Upload CSV / Excel / Parquet</li>
            <li>Select column(s), choose hash & options</li>
            <li>Preview output and download</li>
          </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- HELPERS ----------
def parse_renames(txt: str):
    m = {}
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            a, b = line.split("=", 1)
            a = a.strip(); b = b.strip()
            if a and b: m[a] = b
    return m

def hash_series(s: pd.Series, algo: str) -> pd.Series:
    fn = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256, "sha512": hashlib.sha512}[algo]
    return s.astype(str).fillna("").map(lambda x: fn(x.encode("utf-8")).hexdigest())

def safe_base(name: str) -> str:
    base = os.path.splitext(name)[0].strip()
    return base if base else "file"

# ---------- ROBUST READER ----------
def load_df(file, sheet: str | int | None = None):
    """
    Safe, order-of-operations reader that never infers whitespace-delimited CSVs.
    Tries Excel/Parquet first. For text/CSV, only uses {',', '\\t', ';', '|'} — no whitespace guessing.
    """
    import io as _io
    name = (getattr(file, "name", "") or "").lower()

    def _rewind():
        try: file.seek(0)
        except Exception: pass

    def _collapse_if_single_col_data(df: pd.DataFrame) -> pd.DataFrame:
        # Keep as-is; we only collapse pathological Excel->HTML tables that pretend to be multiple columns
        return df

    # Peek header bytes
    try:
        head = file.getvalue()[:4096]
    except Exception:
        head = b""

    is_zip_like = head[:4] == b"PK\x03\x04"
    is_html_like = head.strip().lower().startswith((b'<!doctype', b'<html'))

    # --- Parquet
    if name.endswith(".parquet"):
        try:
            _rewind(); return pd.read_parquet(file, engine="pyarrow")
        except Exception:
            _rewind(); return pd.read_parquet(file)

    # --- Excel
    if name.endswith(".xlsb"):
        try:
            _rewind()
            return pd.read_excel(file, engine="pyxlsb", sheet_name=sheet if sheet is not None else 0)
        except Exception:
            pass

    if name.endswith((".xlsx", ".xlsm")) or is_zip_like:
        _rewind()
        data = _io.BytesIO(file.read())
        try:
            return pd.read_excel(data, engine="openpyxl", sheet_name=sheet if sheet is not None else 0)
        except Exception:
            try:
                data.seek(0)
                df = pd.read_excel(data, engine="openpyxl", sheet_name=sheet if sheet is not None else 0, header=None)
                if df is not None and df.shape[1] > 0:
                    df.columns = [f"col_{i+1}" for i in range(df.shape[1])]
                    return df
            except Exception:
                pass

    if name.endswith(".xls") or is_html_like:
        # Try legacy Excel
        try:
            _rewind()
            bio = _io.BytesIO(file.read())
            return pd.read_excel(bio, engine="xlrd", sheet_name=sheet if sheet is not None else 0)
        except Exception:
            # Try HTML table fallback
            if is_html_like or b"<table" in head.lower():
                try:
                    _rewind()
                    html_bytes = file.read()
                    tables = pd.read_html(_io.BytesIO(html_bytes))
                    if tables:
                        return _collapse_if_single_col_data(tables[0])
                except Exception:
                    pass
            # Fall back to CSV attempts (NO whitespace delimiter)
            for sep in [",", "\t", ";", "|"]:
                for header in [0, None]:
                    try:
                        _rewind()
                        df = pd.read_csv(file, sep=sep, engine="python", encoding="utf-8",
                                         on_bad_lines="skip", header=header, dtype=str, keep_default_na=False)
                        if df is not None and df.shape[1] > 0:
                            if header is None:
                                df.columns = [f"col_{i+1}" for i in range(df.shape[1])]
                            return df
                    except Exception:
                        continue
            st.error("`.xls` detected but could not be parsed. Pin xlrd==1.2.0 or resave as .xlsx/.csv.")
            return None

    # --- CSV/TXT (SAFE CSV READ — no whitespace splitting)
    for sep in [",", "\t", ";", "|"]:
        try:
            _rewind()
            df = pd.read_csv(file, sep=sep, engine="python", encoding="utf-8",
                             on_bad_lines="skip", header=0, dtype=str, keep_default_na=False)
            if df is not None and df.shape[1] > 0:
                return df
        except Exception:
            pass

    # Retry with header=None (still only with safe seps)
    for sep in [",", "\t", ";", "|"]:
        try:
            _rewind()
            df = pd.read_csv(file, sep=sep, engine="python", encoding="utf-8",
                             on_bad_lines="skip", header=None, dtype=str, keep_default_na=False)
            if df is not None and df.shape[1] > 0:
                df.columns = [f"col_{i+1}" for i in range(df.shape[1])]
                return df
        except Exception:
            pass

    _rewind()
    st.warning(f"Could not read {getattr(file, 'name', 'file')}: unsupported or corrupted content.")
    return None

# Track Excel sheet choice
if "sheets_map" not in st.session_state:
    st.session_state["sheets_map"] = {}

def pick_sheet(uploaded_file):
    import io as _io
    try:
        uploaded_file.seek(0)
        bio = _io.BytesIO(uploaded_file.read())
        xls = pd.ExcelFile(bio, engine="openpyxl")
        if len(xls.sheet_names) > 1:
            default = st.session_state["sheets_map"].get(uploaded_file.name, xls.sheet_names[0])
            choice = st.selectbox(
                f"Sheet — {uploaded_file.name}",
                options=xls.sheet_names,
                index=xls.sheet_names.index(default) if default in xls.sheet_names else 0,
                key=f"sheet-{uploaded_file.name}"
            )
            st.session_state["sheets_map"][uploaded_file.name] = choice
            return choice
        st.session_state["sheets_map"][uploaded_file.name] = xls.sheet_names[0]
        return xls.sheet_names[0]
    except Exception:
        return None

# ---------- PHONE NORMALIZATION ----------
_digit_re = re.compile(r"\D+")

def normalize_phone_value(x):
    s = "" if x is None else str(x)
    d = _digit_re.sub("", s)
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    elif len(d) > 10:
        d = d[-10:]
    if len(d) == 10:
        return d
    return ""

def looks_like_phone(series: pd.Series, colname: str) -> bool:
    name = (colname or "").lower()
    if any(k in name for k in ["phone","cell","mobile","tel"]):
        return True
    stripped = series.astype(str).map(lambda x: _digit_re.sub("", x))
    return (stripped.map(len) >= 10).mean() >= 0.6

def series_for_hash(series: pd.Series, normalize_enabled: bool, colname: str) -> pd.Series:
    s = series.astype(str).fillna("")
    if not normalize_enabled or not looks_like_phone(series, colname):
        return s
    n = s.map(normalize_phone_value)
    return n.mask(n.eq(""), s)

# ---------- APP ----------
main_tab = st.tabs(["Standard", "Advanced", "Combine"])

# ----- STANDARD -----
with main_tab[0]:
    st.subheader("Standard")
    st.markdown("One-step hashing. Output is a **single `hash` column**, **deduplicated**.")
    st.markdown("<div class='gradline'></div>", unsafe_allow_html=True)
    std_file = st.file_uploader("Upload a file", type=["csv","tsv","txt","xlsx","xls","xlsb","parquet"], key="std_uploader")
    c1, c2 = st.columns([1,1])
    with c1:
        std_hash = st.selectbox("Hash type", ["md5","sha1","sha256","sha512"], index=0, key="std_hash")
    with c2:
        std_norm = st.checkbox("Normalize to 10-digit phones (auto-detect)", value=True)
    if std_file:
        sheet = pick_sheet(std_file)
        with st.spinner("Reading file..."):
            df0 = load_df(std_file, sheet=sheet)
        if df0 is not None and not df0.empty:
            col = st.selectbox("Column to hash", options=list(df0.columns), index=0, key="std_col")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            r, c = df0.shape
            st.caption(f"Preview shape: {r:,} × {c}")
            st.dataframe(df0.head(10), use_container_width=True, hide_index=True)
            if st.button("Hash now", type="primary", key="std_go"):
                with st.spinner("Hashing..."):
                    to_hash = series_for_hash(df0[col], std_norm, col)
                    hashed = hash_series(to_hash, std_hash)
                    result = pd.DataFrame({"hash": hashed}).drop_duplicates().reset_index(drop=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("### Result (first 10 unique hashes)")
                st.dataframe(result.head(10), use_container_width=True, hide_index=True)
                csv_buf = io.StringIO(); result.to_csv(csv_buf, index=False)
                st.download_button(
                    "Download hashes (CSV)",
                    data=csv_buf.getvalue().encode("utf-8"),
                    file_name=f"{safe_base(std_file.name)}_hashes.csv",
                    mime="text/csv",
                    type="primary",
                )
        else:
            st.warning("Could not read the file or it is empty.")

# ----- ADVANCED -----
with main_tab[1]:
    st.subheader("Advanced")
    st.markdown("<div class='gradline'></div>", unsafe_allow_html=True)
    files = st.file_uploader("Upload file(s)", type=["csv","tsv","txt","xlsx","xls","xlsb","parquet"], accept_multiple_files=True, key="adv_uploader")
    if "outputs" not in st.session_state: st.session_state["outputs"] = {}
    if "zip_bytes" not in st.session_state: st.session_state["zip_bytes"] = None

    # Use a form so typing in options doesn't trigger reruns until Apply
    with st.form("adv_options_form", clear_on_submit=False):
        oc1, oc2, oc3 = st.columns([1,1,1])
        with oc1:
            adv_hash = st.selectbox("Hash type", ["md5","sha1","sha256","sha512"], index=0, key="adv_hash_type")
        with oc2:
            all_cols = []
            if files:
                for f in files[:20]:
                    sheet = st.session_state["sheets_map"].get(f.name) or pick_sheet(f)
                    tmp = load_df(f, sheet=sheet)
                    if tmp is not None and not tmp.empty:
                        all_cols.extend(list(tmp.columns))
            all_cols = sorted(pd.Index(all_cols).unique().tolist()) if all_cols else []
            cols_to_hash = st.multiselect("Columns to hash", options=all_cols, default=all_cols[:1] if all_cols else [], key="adv_cols_to_hash")
        with oc3:
            suffix = st.text_input("Suffix for added hash columns (Add mode)", value=f"_{st.session_state.get('adv_hash_type','md5')}", key="adv_suffix")
        adv_norm = st.checkbox("Normalize to 10-digit phones (auto-detect per selected column)", value=True, key="adv_norm_chk")
        keep_mode = st.radio(
            "Columns to keep in output",
            [
                "Keep & replace — Replace each selected column with its hash (same name).",
                "Keep all & add — Keep file as-is and add hash column(s) using the suffix.",
                "Keep only hashed column(s) — Output just the hash column(s).",
            ],
            index=0,  # default Keep & replace
            key="adv_keepmode"
        )
        rename_on = st.checkbox("Manually rename columns", value=False, key="adv_rename_on")
        rename_text = ""
        if rename_on:
            rename_text = st.text_area("Rename columns (old=new per line)", height=110, placeholder="email=primary_email\nCell=cell\nZIP=zip", key="adv_renames")
        apply = st.form_submit_button("Apply options")

    if apply or "adv_opts" not in st.session_state:
        st.session_state["adv_opts"] = dict(
            adv_hash=st.session_state.get("adv_hash_type","md5"),
            cols_to_hash=st.session_state.get("adv_cols_to_hash",[]),
            suffix=st.session_state.get("adv_suffix","_md5"),
            adv_norm=st.session_state.get("adv_norm_chk",True),
            keep_mode=st.session_state.get("adv_keepmode"),
            rename_on=st.session_state.get("adv_rename_on",False),
            rename_text=st.session_state.get("adv_renames","") if st.session_state.get("adv_rename_on",False) else ""
        )

    opts = st.session_state["adv_opts"]

    if files:
        st.markdown("#### Preview (shows final output structure)")
        for file in files[:10]:
            sheet = st.session_state["sheets_map"].get(file.name) or pick_sheet(file)
            with st.spinner(f"Reading {file.name}..."):
                df = load_df(file, sheet=sheet)
            if df is not None and not df.empty:
                if opts["rename_on"] and opts["rename_text"].strip():
                    df = df.rename(columns=parse_renames(opts["rename_text"]))
                sel = [c for c in opts["cols_to_hash"] if c in df.columns]
                if not sel and len(df.columns) > 0:
                    sel = [df.columns[0]]
                if opts["keep_mode"].startswith("Keep & replace"):
                    out_df = df.copy()
                    for c in sel:
                        to_hash = series_for_hash(out_df[c], opts["adv_norm"], c)
                        out_df[c] = hash_series(to_hash, opts["adv_hash"])
                elif opts["keep_mode"].startswith("Keep all & add"):
                    out_df = df.copy()
                    sfx = opts["suffix"] or f"_{opts['adv_hash']}"
                    for c in sel:
                        to_hash = series_for_hash(out_df[c], opts["adv_norm"], c)
                        out_df[f"{c}{sfx}"] = hash_series(to_hash, opts["adv_hash"])
                else:
                    cols = {}
                    for c in sel:
                        to_hash = series_for_hash(df[c], opts["adv_norm"], c)
                        cols[f"{c}_{opts['adv_hash']}"] = hash_series(to_hash, opts["adv_hash"])
                    out_df = pd.DataFrame(cols)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                r, ccount = out_df.shape
                st.caption(f"{file.name} — previewing first 15 rows · shape: {r:,} × {ccount}")
                st.dataframe(out_df.head(15), use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Upload files above, set options, then review the live preview here.")

    st.markdown("---")
    run = st.button("Run hashing", type="primary", use_container_width=True, key="adv_run")
    if run:
        if not files:
            st.error("Upload at least one file.")
        else:
            with st.spinner("Hashing files..."):
                zipped_buf = io.BytesIO()
                zf = zipfile.ZipFile(zipped_buf, mode="w", compression=zipfile.ZIP_DEFLATED)
                st.session_state["outputs"].clear()
                total = len(files); valid = 0
                progress = st.progress(0.0, text="Processing...")
                renames = parse_renames(opts["rename_text"]) if (opts["rename_on"] and opts["rename_text"].strip()) else {}
                for i, file in enumerate(files, start=1):
                    sheet = st.session_state["sheets_map"].get(file.name) or pick_sheet(file)
                    df = load_df(file, sheet=sheet)
                    if df is None or df.empty:
                        st.warning(f"Skipped {file.name}: unsupported or empty.")
                        progress.progress(i / total, text=f"Processed {i}/{total}")
                        continue
                    if renames:
                        df = df.rename(columns=renames)
                    sel = [c for c in opts["cols_to_hash"] if c in df.columns]
                    if not sel:
                        sel = [df.columns[0]]
                    if opts["keep_mode"].startswith("Keep & replace"):
                        out_df = df.copy()
                        for c in sel:
                            to_hash = series_for_hash(out_df[c], opts["adv_norm"], c)
                            out_df[c] = hash_series(to_hash, opts["adv_hash"])
                    elif opts["keep_mode"].startswith("Keep all & add"):
                        out_df = df.copy()
                        sfx = opts["suffix"] or f"_{opts['adv_hash']}"
                        for c in sel:
                            to_hash = series_for_hash(out_df[c], opts["adv_norm"], c)
                            out_df[f"{c}{sfx}"] = hash_series(to_hash, opts["adv_hash"])
                    else:
                        cols = {}
                        for c in sel:
                            to_hash = series_for_hash(df[c], opts["adv_norm"], c)
                            cols[f"{c}_{opts['adv_hash']}"] = hash_series(to_hash, opts["adv_hash"])
                        out_df = pd.DataFrame(cols)
                    csv_buf = io.StringIO(); out_df.to_csv(csv_buf, index=False)
                    data_bytes = csv_buf.getvalue().encode("utf-8")
                    out_name = f"{safe_base(file.name)}_hashed.csv"
                    zf.writestr(out_name, data_bytes)
                    st.session_state["outputs"][out_name] = data_bytes
                    valid += 1
                    progress.progress(i / total, text=f"Processed {i}/{total}")
                zf.close()
                zipped_buf.seek(0)
                if st.session_state["outputs"]:
                    st.session_state["zip_bytes"] = zipped_buf.getvalue()
                    st.success(f"Finished {valid} file(s). Scroll down to download.")
                else:
                    st.error("No outputs produced. Check column names and try again.")
    st.markdown("### Downloads")
    if st.session_state.get("outputs"):
        left, right = st.columns([2, 1])
        with left:
            for name, data_bytes in st.session_state["outputs"].items():
                st.download_button(
                    label=f"Download {name}",
                    data=data_bytes,
                    file_name=name,
                    mime="text/csv",
                    key=f"dl-{name}",
                    use_container_width=True,
                )
        with right:
            if st.session_state.get("zip_bytes"):
                st.download_button(
                    label="Download all as ZIP",
                    data=st.session_state["zip_bytes"],
                    file_name="hashed_outputs.zip",
                    mime="application/zip",
                    key="dl-zip",
                    type="primary",
                    use_container_width=True,
                )
    else:
        st.info("Nothing to download yet—run hashing above once you’ve set options and previews.")

# ----- COMBINE -----
with main_tab[2]:
    st.subheader("Combine (optional)")
    st.markdown("<div class='gradline'></div>", unsafe_allow_html=True)
    st.markdown("Merge multiple files into one. Defaults: **drop duplicate rows** ON, **source filename** OFF.")
    c_files = st.file_uploader("Upload file(s) to combine", type=["csv","tsv","txt","xlsx","xls","xlsb","parquet"], accept_multiple_files=True, key="combine_uploader")
    drop_dupes = st.checkbox("Drop duplicate rows", value=True)
    add_source = st.checkbox("Add source filename column", value=False, help="Adds a 'source_filename' column.")
    c_fmt = st.selectbox("Output format", ["csv","parquet"], index=0)
    c_name = st.text_input("Combined file name", value="combined_output.csv")
    if c_fmt == "parquet" and not c_name.lower().endswith(".parquet"):
        c_name = c_name.rsplit(".", 1)[0] + ".parquet"

    def _coerce_to_single_hash(df: pd.DataFrame) -> pd.DataFrame:
        if add_source:
            return df
        if "hash" in df.columns:
            return df[["hash"]].copy()
        if df.shape[1] == 1:
            d2 = df.copy(); d2.columns = ["hash"]; return d2
        d2 = df.drop(columns=[c for c in df.columns if df[c].isna().all()], errors="ignore")
        first = d2.columns[0]
        return d2[[first]].rename(columns={first: "hash"})

    if st.button("Combine files", type="primary", key="combine_go"):
        if not c_files:
            st.error("Upload at least two files.")
        else:
            frames = []
            for f in c_files:
                sheet = st.session_state["sheets_map"].get(f.name) or pick_sheet(f)
                with st.spinner(f"Reading {f.name}..."):
                    df = load_df(f, sheet=sheet)
                if df is not None and not df.empty:
                    df_std = _coerce_to_single_hash(df)
                    if add_source and "source_filename" not in df_std.columns:
                        df_std.insert(0, "source_filename", f.name)
                    frames.append(df_std)
            if frames:
                combined = pd.concat(frames, axis=0, ignore_index=True, sort=False)
                if drop_dupes:
                    combined = combined.drop_duplicates()
                if c_fmt == "csv":
                    buf = io.StringIO(); combined.to_csv(buf, index=False)
                    data = buf.getvalue().encode("utf-8"); mime = "text/csv"
                else:
                    pbuf = io.BytesIO()
                    try:
                        combined.to_parquet(pbuf, engine="pyarrow", index=False)
                    except Exception:
                        combined.to_parquet(pbuf, index=False)
                    pbuf.seek(0); data = pbuf.getvalue(); mime = "application/octet-stream"
                st.download_button(f"Download {c_name}", data=data, file_name=c_name, mime=mime, type="primary")
            else:
                st.error("No valid, non-empty files to combine.")

# ---------- FOOTER ----------
st.markdown(f"<div class='footer'><div class='footerwrap'>{COMPANY_NAME}</div></div>", unsafe_allow_html=True)



