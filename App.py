import io
import os
import zipfile
import hashlib
import pandas as pd
import streamlit as st
import re

# ---------- CONFIG ----------
COMPANY_NAME = "True Blue Analytics"
LOGO_PATH = r"C:\Users\musta\Downloads\download.png"  # update if you move the file

st.set_page_config(page_title=f"{COMPANY_NAME} • Batch Hasher", page_icon=None, layout="wide")

# ================ THEME / STYLES (blue) ================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

    :root{
        --bg1:#eff4ff;
        --bg2:#eaf1ff;
        --panel:#ffffff;
        --ink:#0b1a4a;
        --muted:#6e7b99;
        --line:#d9e2ff;
        --brand:#0f2a80;
        --brand-2:#2953d6;
        --brand-3:#4a74ff;
        --accent:#b7c8ff;
        --focus:#3aa0ff;
        --input-bg:#ffffff;
        --input-text:#0b1a4a;
        --placeholder:#8fa1c0;
        --input-border:#b9c8ef;
        --ring:0 0 0 3px rgba(74,116,255,.28);
    }

    *{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
    html,body,[data-testid="stAppViewContainer"]{
        background:linear-gradient(180deg,var(--bg1),var(--bg2));
        color:var(--ink);
        font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
        letter-spacing:.1px;
    }

    .block-container{padding:0 1.25rem 2rem 1.25rem;max-width:1200px}
    [data-testid="stSidebar"]{background:var(--panel);border-right:1px solid var(--line);padding-top:.75rem}

    /* ======= Top-left banner (logo only) ======= */
    .brandbar{
        position:sticky; top:0; z-index:999;
        background:#fff; border-bottom:1px solid var(--line);
        margin:0 -1.25rem .9rem -1.25rem; padding:.35rem 0;
    }
    .brandwrap{display:flex; align-items:center; gap:10px; max-width:1200px; margin:0 auto; padding:0 1.25rem; justify-content:flex-start;}
    .brandlogo{ max-height:46px; }

    /* ======= Footer with company name ======= */
    .footer{
        background:linear-gradient(135deg,var(--brand) 0%,var(--brand-2) 60%,var(--brand-3) 100%);
        color:#fff; margin:2rem -1.25rem 0 -1.25rem; border-top:1px solid var(--line);
    }
    .footerwrap{ max-width:1200px; margin:0 auto; padding:.9rem 1.25rem; font-weight:800; letter-spacing:.3px; }

    h1,h2,h3,h4,h5{ color:var(--ink); margin:0 0 .25rem 0; font-weight:700 }
    h1{font-size:2.0rem;line-height:1.16;margin-top:.25rem}
    h2{font-size:1.35rem;line-height:1.28;margin-top:.25rem}
    .subtitle{color:var(--muted);font-size:1.02rem;margin:.25rem 0 1rem 0;font-weight:500}

    label,.st-emotion-cache-1erivf3{color:var(--ink)!important;opacity:1!important;font-weight:600!important}

    input,textarea,select{
        font-size:16px!important;color:var(--input-text)!important;
        font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif!important
    }
    .stTextInput input,.stTextArea textarea{
        background:var(--input-bg)!important;color:var(--input-text)!important;border:1px solid var(--input-border)!important;border-radius:14px!important;
        box-shadow:none!important;padding:.7rem .9rem!important
    }
    .stTextInput input::placeholder,.stTextArea textarea::placeholder{color:var(--placeholder)!important;opacity:1!important}
    .stTextInput input:focus,.stTextArea textarea:focus{box-shadow:var(--ring)!important;border-color:var(--brand-3)!important;outline:none!important}

    .stSelectbox div[data-baseweb="select"]>div{
        background:var(--input-bg)!important;color:var(--input-text)!important;border:1px solid var(--input-border)!important;
        border-radius:14px!important;min-height:48px!important;padding:4px 8px!important;
        font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif!important
    }
    .stSelectbox div[data-baseweb="select"] input{color:var(--input-text)!important}
    .stSelectbox div[data-baseweb="select"] div[role="listbox"]{background:#fff!important;color:var(--input-text)!important;border:1px solid var(--line)!important}
    .stSelectbox div[data-baseweb="select"] [role="option"]{color:var(--input-text)!important}

    [data-testid="stRadio"]>label{color:var(--ink)!important}
    [data-testid="stRadio"] [role="radiogroup"] label,
    [data-testid="stRadio"] [role="radiogroup"] p,
    [data-testid="stRadio"] [role="radiogroup"] span{color:var(--ink)!important}
    [data-testid="stRadio"] [role="radiogroup"] label{border-radius:12px;padding:.35rem .6rem;font-weight:600!important}
    [data-testid="stRadio"] [role="radiogroup"] label:hover{background:#2947e214}
    [data-testid="stRadio"] [role="radiogroup"] input:focus+div,
    [data-testid="stRadio"] [role="radiogroup"] input:focus-visible+div{outline:none;box-shadow:var(--ring);border-radius:12px}

    .stTabs [data-baseweb="tab-list"]{gap:.5rem;margin-bottom:.75rem}
    .stTabs [data-baseweb="tab"]{
        background:#e6ecff;border:1px solid var(--line);border-bottom:2px solid transparent;border-radius:12px 12px 0 0;
        padding:.68rem 1rem;color:var(--ink);font-weight:650;
    }
    .stTabs [aria-selected="true"]{background:#ffffff;border-bottom:4px solid var(--brand-2)}

    .card{
        background:linear-gradient(180deg,#ffffff, #f5f7ff);
        border:1px solid var(--line);
        border-radius:18px;
        padding:1rem 1rem 1.1rem 1rem;
        box-shadow:0 14px 30px rgba(18,42,128,.08);
        margin-bottom:.9rem
    }

    .stDownloadButton button,.stButton button{
        background:linear-gradient(135deg,var(--brand) 0%,var(--brand-2) 60%,var(--brand-3) 100%)!important;color:#ffffff!important;border:none!important;border-radius:14px!important;
        padding:.85rem 1rem!important;font-weight:700!important;letter-spacing:.2px
    }
    .stDownloadButton button:hover,.stButton button:hover{filter:brightness(1.06)}
    .stAlert{border-radius:14px}

    .meta{color:var(--muted);font-size:.95rem;margin-top:.15rem}
    .kpi{display:grid;grid-template-columns:repeat(4,minmax(140px,1fr));gap:.65rem;margin:.65rem 0 .7rem 0}
    .kpi>div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:.7rem .9rem;text-align:left}
    .kpi .h{font-size:.8rem;color: var(--muted)}
    .kpi .v{font-size:1.06rem;font-weight:700;color: var(--ink)}
    .underline-accent{box-shadow:inset 0 -6px 0 var(--accent)}

    /* Sidebar headers & checkboxes */
    [data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{color:var(--ink)!important;font-weight:700!important;letter-spacing:.2px;}
    [data-testid="stSidebar"] h2{position:relative;margin-top:.25rem;margin-bottom:.35rem}
    [data-testid="stSidebar"] h2::after{content:""; position:absolute; left:0; bottom:-.35rem; width:44%; height:4px; background:var(--brand-3); border-radius:999px; opacity:.9;}
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label,[data-testid="stSidebar"] [data-testid="stCheckbox"] p,[data-testid="stSidebar"] [data-testid="stCheckbox"] span{color:var(--ink)!important;font-weight:600!important;}
    [data-testid="stSidebar"] [data-testid="stCheckbox"] input:focus + div,[data-testid="stSidebar"] [data-testid="stCheckbox"] input:focus-visible + div{box-shadow:var(--ring);border-radius:10px;}
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label:hover{background:#2947e214;border-radius:10px;padding:.15rem .25rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ================ TOP-LEFT BANNER (logo only) ================
st.markdown('<div class="brandbar"><div class="brandwrap">', unsafe_allow_html=True)
try:
    st.image(LOGO_PATH, use_container_width=False, caption=None, output_format="PNG")
except Exception:
    st.write("")
st.markdown('</div></div>', unsafe_allow_html=True)

# ================ APP TITLE =================
st.title("Batch File Hasher")
st.markdown('<div class="subtitle">Use **Simple** for one-screen hashing (with 10-digit phone normalization), or **Advanced** for batch workflows.</div>', unsafe_allow_html=True)

# ---------------- Utilities ----------------
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

def load_df(file):
    name = file.name.lower()
    try:
        if name.endswith(".csv"):
            return pd.read_csv(file)
        if name.endswith(".tsv"):
            return pd.read_csv(file, sep="\t")
        if name.endswith(".txt"):
            file.seek(0)
            try:
                return pd.read_csv(file)
            except Exception:
                file.seek(0)
                return pd.read_csv(file, sep="\t")
        if name.endswith((".xlsx", ".xls")):
            return pd.read_excel(file)
        if name.endswith(".parquet"):
            try:
                return pd.read_parquet(file, engine="pyarrow")
            except Exception:
                return pd.read_parquet(file)
    except Exception as e:
        st.warning(f"Could not read {file.name}: {e}")
    return None

def hash_series(s: pd.Series, algo: str) -> pd.Series:
    f = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256, "sha512": hashlib.sha512}[algo]
    return s.astype(str).fillna("").map(lambda x: f(x.encode("utf-8")).hexdigest())

def safe_base(name: str) -> str:
    base = os.path.splitext(name)[0].strip()
    return base if base else "file"

def human_int(n): return f"{n:,}"

# Phone normalization: strip non-digits; if 11 digits starting with '1' -> last 10; keep 10; else empty
_digit_re = re.compile(r"\D+")
def normalize_phone_value(x: str) -> str:
    if x is None: return ""
    d = _digit_re.sub("", str(x))
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    if len(d) == 10:
        return d
    return ""  # invalid -> empty

def normalize_phone_series(s: pd.Series) -> pd.Series:
    return s.astype(str).map(normalize_phone_value)

# ======================= MAIN TABS =======================
main_tab = st.tabs(["Simple", "Advanced"])

# ======================= SIMPLE TAB ======================
with main_tab[0]:
    st.subheader("Simple")
    st.markdown("One-step hashing. By default, phone numbers are normalized to **10 digits** (strip non-digits, drop leading `1` if 11 digits).")

    simple_file = st.file_uploader("Upload a file", type=["csv", "tsv", "txt", "xlsx", "xls", "parquet"], key="simple_uploader")
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        simple_hash = st.selectbox("Hash type", ["md5", "sha1", "sha256", "sha512"], index=2, key="simple_hash")
    with c2:
        normalize_phone = st.checkbox("Normalize to 10-digit phones (recommended)", value=True, help="Strips non-digits. If 11 digits and starts with 1, removes the leading 1. Others become blank.")
    with c3:
        preview_rows_simple = st.slider("Preview rows", 5, 50, 12, key="simple_preview")

    if simple_file:
        df0 = load_df(simple_file)
        if df0 is not None and not df0.empty:
            # column picker
            col = st.selectbox("Column to hash", options=list(df0.columns), index=0, key="simple_col")
            out_name = st.text_input("Output column name", value=f"{col}_{simple_hash}", key="simple_outname")

            # Show preview
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**{simple_file.name}**")
            st.dataframe(df0.head(preview_rows_simple), use_container_width=True, hide_index=True)

            # Do hashing
            if st.button("Hash now", type="primary", key="simple_go"):
                df = df0.copy()
                source = df[col]

                if normalize_phone:
                    norm_col = f"{col}_10digit"
                    df[norm_col] = normalize_phone_series(source)
                    invalid = (df[norm_col] == "").sum()
                    st.info(f"Normalized phone values → 10 digits. Invalid/other-length rows set blank: {human_int(int(invalid))}.")
                    to_hash = df[norm_col]
                else:
                    to_hash = source.astype(str).fillna("")

                df[out_name] = hash_series(to_hash, simple_hash)

                # Keep original + normalized (if applied) + hash
                keep_cols = [col]
                if normalize_phone:
                    keep_cols.append(f"{col}_10digit")
                keep_cols.append(out_name)
                result = df[keep_cols]

                # Show and provide download
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("### Result preview")
                st.dataframe(result.head(preview_rows_simple), use_container_width=True, hide_index=True)

                # Download
                csv_buf = io.StringIO()
                result.to_csv(csv_buf, index=False)
                st.download_button(
                    "Download hashed file (CSV)",
                    data=csv_buf.getvalue().encode("utf-8"),
                    file_name=f"{safe_base(simple_file.name)}_hashed_simple.csv",
                    mime="text/csv",
                    type="primary",
                )
        else:
            st.warning("Could not read the file or it is empty.")

# ======================= ADVANCED TAB ======================
with main_tab[1]:
    # ---------- SIDEBAR (Advanced) ----------
    with st.sidebar:
        st.header("Options")
        hash_type = st.selectbox("Hash type", ["md5", "sha1", "sha256", "sha512"], index=2)
        col_override = st.text_input("Default column if none selected", value="", placeholder="email, cell, id")
        new_col_name = st.text_input("Output column name (if hashing ONE column)", value="", placeholder="e.g., email_sha256")
        retain_mode = st.radio("Columns to keep in output", ["Keep all columns", "Keep source + hashed only", "Keep only hashed column"], index=0)
        rename_text = st.text_area("Rename columns (old=new per line)", height=140, placeholder="email=primary_email\nCell=cell\nZIP=zip")

        st.markdown("<h2>Combine</h2>", unsafe_allow_html=True)
        combine_files = st.checkbox("Combine all processed files into one", value=True)
        add_source_col = st.checkbox("Add source filename column", value=True, help="Adds a column named 'source_filename'.")
        drop_dupes = st.checkbox("Drop duplicate rows in combined file", value=True)
        combined_format = st.selectbox("Combined file format", ["csv", "parquet"], index=0)
        combined_name = st.text_input("Combined file name", value="combined_hashed.csv")
        if combined_format == "parquet" and not combined_name.lower().endswith(".parquet"):
            combined_name = combined_name.rsplit(".", 1)[0] + ".parquet"

        st.markdown("---")
        preview_rows = st.slider("Preview rows", 5, 100, 15)

    # ---------- File upload (Advanced) ----------
    files = st.file_uploader("Upload file(s)", type=["csv", "tsv", "txt", "xlsx", "xls", "parquet"], accept_multiple_files=True, key="adv_uploader")

    # ---------- State ----------
    if "outputs" not in st.session_state: st.session_state["outputs"] = {}
    if "zip_bytes" not in st.session_state: st.session_state["zip_bytes"] = None
    if "combined_bytes" not in st.session_state: st.session_state["combined_bytes"] = None
    if "combined_name" not in st.session_state: st.session_state["combined_name"] = combined_name
    if "colmap" not in st.session_state: st.session_state["colmap"] = {}  # per-file selected columns to hash

    # ---------- Advanced sub-tabs ----------
    tabs = st.tabs(["Process", "Preview", "Downloads"])

    with tabs[0]:
        st.subheader("Process files")
        col_a, col_b = st.columns([1, 1])
        with col_a:
            start = st.button("Run hashing", type="primary", use_container_width=True, key="adv_run")
        with col_b:
            clear = st.button("Clear results", use_container_width=True, key="adv_clear")

        if clear:
            st.session_state["outputs"].clear()
            st.session_state["zip_bytes"] = None
            st.session_state["combined_bytes"] = None
            st.session_state["colmap"].clear()
            st.info("Cleared previous results.")

        if start:
            if not files:
                st.error("Upload at least one file.")
            else:
                renames = parse_renames(rename_text)
                zipped_buf = io.BytesIO()
                zf = zipfile.ZipFile(zipped_buf, mode="w", compression=zipfile.ZIP_DEFLATED)
                st.session_state["outputs"].clear()
                st.session_state["combined_bytes"] = None
                st.session_state["combined_name"] = combined_name

                total = len(files)
                valid = 0
                combined_frames = []

                progress = st.progress(0.0, text="Processing...")
                for i, file in enumerate(files, start=1):
                    df = load_df(file)
                    if df is None or df.empty:
                        st.warning(f"Skipped {file.name}: unsupported or empty.")
                        progress.progress(i / total, text=f"Processed {i}/{total}")
                        continue

                    if renames:
                        df = df.rename(columns=renames)

                    # Per-file selected columns
                    sel = st.session_state["colmap"].get(file.name, [])
                    sel = [c for c in sel if c in df.columns]
                    if not sel:
                        target_col = col_override.strip() if col_override.strip() else df.columns[0]
                        if target_col not in df.columns:
                            st.warning(f"Skipped {file.name}: column '{target_col}' not found.")
                            progress.progress(i / total, text=f"Processed {i}/{total}")
                            continue
                        sel = [target_col]

                    # Create hash columns
                    out_cols_created = []
                    if len(sel) == 1 and new_col_name.strip():
                        out_name = new_col_name.strip()
                        df[out_name] = hash_series(df[sel[0]], hash_type)
                        out_cols_created.append(out_name)
                    else:
                        for c in sel:
                            out_name = f"{c}_{hash_type}"
                            df[out_name] = hash_series(df[c], hash_type)
                            out_cols_created.append(out_name)

                    # Retain policy
                    if retain_mode == "Keep source + hashed only":
                        keep = list(dict.fromkeys(sel + out_cols_created))
                        df = df[keep]
                    elif retain_mode == "Keep only hashed column":
                        df = df[out_cols_created]

                    # Individual file out
                    csv_buf = io.StringIO()
                    df.to_csv(csv_buf, index=False)
                    data_bytes = csv_buf.getvalue().encode("utf-8")
                    out_name = f"{safe_base(file.name)}_hashed.csv"
                    zf.writestr(out_name, data_bytes)
                    st.session_state["outputs"][out_name] = data_bytes

                    # Combined
                    df_comb = df.copy()
                    if add_source_col:
                        df_comb.insert(0, "source_filename", file.name)
                    combined_frames.append(df_comb)

                    valid += 1
                    progress.progress(i / total, text=f"Processed {i}/{total}")

                # Combined file
                if combine_files and combined_frames:
                    combined = pd.concat(combined_frames, axis=0, ignore_index=True, sort=False)
                    if drop_dupes:
                        combined = combined.drop_duplicates()
                    if combined_format == "csv":
                        cbuf = io.StringIO()
                        combined.to_csv(cbuf, index=False)
                        cbytes = cbuf.getvalue().encode("utf-8")
                    else:
                        pbuf = io.BytesIO()
                        try:
                            combined.to_parquet(pbuf, engine="pyarrow", index=False)
                        except Exception:
                            combined.to_parquet(pbuf, index=False)
                        pbuf.seek(0)
                        cbytes = pbuf.getvalue()
                    st.session_state["combined_bytes"] = cbytes
                    st.session_state["combined_name"] = combined_name
                    zf.writestr(combined_name, cbytes)

                zf.close()
                zipped_buf.seek(0)
                if st.session_state["outputs"]:
                    st.session_state["zip_bytes"] = zipped_buf.getvalue()
                    msg = f"Finished {valid} file(s)"
                    if combine_files and valid > 0:
                        msg += " • combined file ready"
                    st.success(msg + ". See Downloads tab.")
                else:
                    st.error("No outputs produced. Check column names and try again.")

    with tabs[1]:
        st.subheader("Preview")
        if files:
            st.info("Tip: choose the **Columns to hash** under each file. Leave empty to use the default column from the sidebar.")
            for file in files[:8]:
                df = load_df(file)
                if df is not None and not df.empty:
                    rows, cols = df.shape
                    mem_est = df.memory_usage(deep=True).sum()
                    kb = mem_est/1024

                    st.markdown(f'<div class="card">', unsafe_allow_html=True)
                    st.markdown(f"**{file.name}**")
                    st.markdown(f'<div class="meta">Estimated size: {kb:,.0f} KB • Shape: {human_int(rows)} × {human_int(cols)}</div>', unsafe_allow_html=True)

                    default_guess = []
                    if st.session_state.get("colmap", {}).get(file.name):
                        default_guess = st.session_state["colmap"][file.name]
                    elif (st.session_state.get("colmap") is not None) and isinstance(df.columns, pd.Index):
                        if (st.session_state.get("col_override","") or "").strip() in df.columns:
                            default_guess = [(st.session_state.get("col_override") or "").strip()]
                        else:
                            default_guess = [df.columns[0]]

                    sel = st.multiselect(
                        f"Columns to hash — {file.name}",
                        options=list(df.columns),
                        default=st.session_state["colmap"].get(file.name, default_guess),
                        key=f"ms-{file.name}",
                        help="Pick one or more columns for hashing for this file."
                    )
                    st.session_state["colmap"][file.name] = sel

                    st.markdown(
                        '<div class="kpi">'
                        f'<div><div class="h">Rows</div><div class="v underline-accent">{human_int(rows)}</div></div>'
                        f'<div><div class="h">Columns</div><div class="v underline-accent">{human_int(cols)}</div></div>'
                        f'<div><div class="h">Selected to hash</div><div class="v underline-accent">{len(sel)}</div></div>'
                        f'<div><div class="h">Null cells</div><div class="v underline-accent">{human_int(int(df.isna().sum().sum()))}</div></div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.dataframe(df.head(preview_rows), use_container_width=True, hide_index=True)
                    with c2:
                        schema = pd.DataFrame({"column": df.columns, "dtype": [str(t) for t in df.dtypes]})
                        st.dataframe(schema, use_container_width=True, hide_index=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Upload files to preview them here.")

    with tabs[2]:
        st.subheader("Downloads")
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
                if st.session_state.get("combined_bytes"):
                    st.download_button(
                        label=f"Download {st.session_state['combined_name']}",
                        data=st.session_state["combined_bytes"],
                        file_name=st.session_state["combined_name"],
                        mime=("text/csv" if st.session_state["combined_name"].endswith(".csv") else "application/octet-stream"),
                        key="dl-combined",
                        type="primary",
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
            st.info("No files yet. Process files first.")

# ================ FOOTER (company name at very bottom) ================
st.markdown(f"<div class='footer'><div class='footerwrap'>{COMPANY_NAME}</div></div>", unsafe_allow_html=True)
