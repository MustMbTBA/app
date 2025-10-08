import io
import os
import zipfile
import hashlib
import pandas as pd
import streamlit as st
import re

# ---------- CONFIG ----------
COMPANY_NAME = "True Blue Analytics"
TOOL_NAME = "Easy Hasher"
LOGO_PATH = r"C:\Users\musta\Downloads\download.png"  # update if you move the file

st.set_page_config(page_title=f"{TOOL_NAME} • {COMPANY_NAME}", page_icon=None, layout="wide")

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
st.title(TOOL_NAME)
st.markdown('<div class="subtitle">Standard: minimal, one-column deduped hashes. Advanced: batch with flexible retention and defaults.</div>', unsafe_allow_html=True)

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

def hash_series(s: pd.Series, algo: str) -> pd.Series:
    f = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256, "sha512": hashlib.sha512}[algo]
    return s.astype(str).fillna("").map(lambda x: f(x.encode("utf-8")).hexdigest())

def safe_base(name: str) -> str:
    base = os.path.splitext(name)[0].strip()
    return base if base else "file"

def human_int(n): return f"{n:,}"

# ---------- Robust file loader (fixes “No columns to parse” & more) ----------
def load_df(file):
    """
    Robust reader for csv/tsv/txt/xlsx/parquet UploadedFile objects.
    - Auto-infers delimiter & encoding for text files.
    - Resets stream between attempts.
    - Detects XLSX content even if extension says .csv.
    - Falls back to headerless read when needed.
    """
    import pandas as pd

    name = (getattr(file, "name", "") or "").lower()

    # Helper to reset the file pointer safely
    def _rewind():
        try:
            file.seek(0)
        except Exception:
            pass

    # If it's actually an XLSX/ZIP container, read as Excel even if named .csv
    try:
        head = file.getvalue()[:4]  # Streamlit UploadedFile supports .getvalue()
        if head.startswith(b"PK\x03\x04"):  # ZIP magic -> likely .xlsx
            _rewind()
            return pd.read_excel(file)
    except Exception:
        pass

    # Parquet
    if name.endswith(".parquet"):
        try:
            _rewind()
            return pd.read_parquet(file, engine="pyarrow")
        except Exception:
            _rewind()
            return pd.read_parquet(file)

    # Excel
    if name.endswith((".xlsx", ".xls")):
        _rewind()
        return pd.read_excel(file)

    # Text-like (csv/tsv/txt/unknown)
    attempts = [
        dict(sep=None, engine="python", encoding="utf-8", on_bad_lines="skip"),
        dict(sep=None, engine="python", encoding="utf-8-sig", on_bad_lines="skip"),
        dict(sep=None, engine="python", encoding="latin1", on_bad_lines="skip"),
    ]
    for kw in attempts:
        try:
            _rewind()
            df = pd.read_csv(file, **kw)
            if df is not None and df.shape[1] > 0:
                return df
        except Exception:
            pass

    # Try common fixed delimiters with/without header
    for sep in [",", ";", "\t", "|"]:
        for header in [0, None]:
            try:
                _rewind()
                df = pd.read_csv(file, sep=sep, engine="python", encoding="utf-8", on_bad_lines="skip", header=header)
                if df is not None and df.shape[1] > 0:
                    if header is None:
                        df.columns = [f"col_{i+1}" for i in range(df.shape[1])]
                    return df
            except Exception:
                continue

    try:
        _rewind()
    except Exception:
        pass
    st.warning(f"Could not read {getattr(file, 'name', 'file')}: unsupported format or empty content.")
    return None

# Phone normalization helpers (used in Standard only, with auto-detect)
_digit_re = re.compile(r"\D+")
def normalize_phone_value(x: str) -> str:
    if x is None: return ""
    d = _digit_re.sub("", str(x))
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    if len(d) == 10:
        return d
    return ""

def normalize_phone_series(s: pd.Series) -> pd.Series:
    return s.astype(str).map(normalize_phone_value)

def looks_like_phone(series: pd.Series, colname: str) -> bool:
    name = (colname or "").lower()
    if any(k in name for k in ["phone", "cell", "mobile", "tel"]):
        return True
    stripped = series.astype(str).map(lambda x: _digit_re.sub("", x))
    phone_like = stripped.map(lambda d: len(d) >= 10 or (len(d) == 11 and d.startswith("1")))
    return phone_like.mean() >= 0.6  # 60% heuristic

# ======================= MAIN TABS =======================
main_tab = st.tabs(["Standard", "Advanced", "Combine"])

# ======================= STANDARD TAB ======================
with main_tab[0]:
    st.subheader("Standard")
    st.markdown("One-step hashing with minimal choices. Output is a **single `hash` column**, **deduplicated**.")

    # Defaults: MD5, minimal inputs
    std_file = st.file_uploader("Upload a file", type=["csv", "tsv", "txt", "xlsx", "xls", "parquet"], key="std_uploader")
    c1, c2 = st.columns([1,1])
    with c1:
        std_hash = st.selectbox("Hash type", ["md5", "sha1", "sha256", "sha512"], index=0, key="std_hash")  # MD5 default
    with c2:
        std_norm = st.checkbox(
            "Normalize to 10-digit phones (auto-detect)",
            value=True,
            help="Runs only if the selected column is phone-like. Emails/IDs are left as-is."
        )

    if std_file:
        df0 = load_df(std_file)
        if df0 is not None and not df0.empty:
            col = st.selectbox("Column to hash", options=list(df0.columns), index=0, key="std_col")

            # Micro-preview (fixed 10 rows)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**{std_file.name}** — showing first 10 rows")
            st.dataframe(df0.head(10), use_container_width=True, hide_index=True)

            if st.button("Hash now", type="primary", key="std_go"):
                src = df0[col]
                apply_norm = std_norm and looks_like_phone(src, col)
                if std_norm and not apply_norm:
                    st.info("Column does not look like a phone field — skipping normalization.")

                to_hash = normalize_phone_series(src) if apply_norm else src.astype(str).fillna("")
                hashed = hash_series(to_hash, std_hash)

                # Single column, dedup
                result = pd.DataFrame({"hash": hashed}).drop_duplicates().reset_index(drop=True)

                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("### Result (first 10 unique hashes)")
                st.dataframe(result.head(10), use_container_width=True, hide_index=True)

                csv_buf = io.StringIO()
                result.to_csv(csv_buf, index=False)
                st.download_button(
                    "Download hashes (CSV)",
                    data=csv_buf.getvalue().encode("utf-8"),
                    file_name=f"{safe_base(std_file.name)}_hashes.csv",
                    mime="text/csv",
                    type="primary",
                )
        else:
            st.warning("Could not read the file or it is empty.")

# ======================= ADVANCED TAB ======================
with main_tab[1]:
    st.subheader("Advanced")

    # ---- Upload first (top) ----
    files = st.file_uploader(
        "Upload file(s)",
        type=["csv", "tsv", "txt", "xlsx", "xls", "parquet"],
        accept_multiple_files=True,
        key="adv_uploader"
    )

    # State buckets
    if "outputs" not in st.session_state: st.session_state["outputs"] = {}
    if "zip_bytes" not in st.session_state: st.session_state["zip_bytes"] = None
    if "colmap" not in st.session_state: st.session_state["colmap"] = {}

    # ---- Preview / Options (same tab) ----
    st.markdown("#### Options")

    oc1, oc2, oc3 = st.columns([1,1,1])
    with oc1:
        hash_type = st.selectbox("Hash type", ["md5", "sha1", "sha256", "sha512"], index=0, key="adv_hash_type")  # MD5 default
    with oc2:
        # Multiselect default columns (from uploaded files’ columns)
        all_cols = []
        if files:
            for f in files[:20]:  # cap for performance
                df_tmp = load_df(f)
                if df_tmp is not None and not df_tmp.empty:
                    all_cols.extend(list(df_tmp.columns))
        all_cols = sorted(pd.Index(all_cols).unique().tolist()) if all_cols else []
        default_cols = st.multiselect(
            "Default columns if none selected",
            options=all_cols,
            default=all_cols[:1] if all_cols else [],
            help="Used only for files where you do not explicitly pick columns below.",
            key="adv_default_cols"
        )
    with oc3:
        add_suffix = st.text_input(
            "Suffix for added hash columns (Add mode)",
            value=f"_{hash_type}",
            help="Used when 'Keep all & add' is selected. Example: email → email_sha256",
            key="adv_suffix"
        )

    # Retention modes with your descriptions
    keep_mode = st.radio(
        "Columns to keep in output",
        [
            "Keep & replace — Replace each selected column with its hash (same name).",
            "Keep all & add — Keep file as-is and add hash column(s) using the suffix.",
            "Keep only hashed column(s) — Output just the hash column(s).",
        ],
        index=1,
        help="Choose how hashed values are written into your output.",
        key="adv_keepmode"
    )

    # Optional renaming rules
    rename_text = st.text_area(
        "Rename columns (old=new per line)",
        height=110,
        placeholder="email=primary_email\nCell=cell\nZIP=zip",
        key="adv_renames"
    )

    # ---- File previews with per-file column pickers ----
    if files:
        st.markdown("#### Preview & Column selection")
        st.info("Pick **Columns to hash** for each file. If none are picked for a file, we’ll use your **Default columns** above (when present).")

        for file in files[:12]:
            df = load_df(file)
            if df is not None and not df.empty:
                rows, cols = df.shape
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"**{file.name}**  ·  {human_int(rows)} rows × {cols} columns")

                # Build default for this file
                existing = st.session_state["colmap"].get(file.name)
                if not existing:
                    defaults_here = [c for c in st.session_state.get("adv_default_cols", []) if c in df.columns]
                    if defaults_here:
                        existing = defaults_here
                    else:
                        existing = [df.columns[0]]

                sel = st.multiselect(
                    f"Columns to hash — {file.name}",
                    options=list(df.columns),
                    default=existing,
                    key=f"adv-ms-{file.name}",
                )
                st.session_state["colmap"][file.name] = sel

                # Quick schema + head
                c1, c2 = st.columns([3, 2])
                with c1:
                    st.dataframe(df.head(15), use_container_width=True, hide_index=True)
                with c2:
                    schema = pd.DataFrame({"column": df.columns, "dtype": [str(t) for t in df.dtypes]})
                    st.dataframe(schema, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Upload files above to preview and pick columns.")

    st.markdown("---")
    # ---- Run hashing + Downloads (bottom of the same tab) ----
    run = st.button("Run hashing", type="primary", use_container_width=True, key="adv_run")

    if run:
        if not files:
            st.error("Upload at least one file.")
        else:
            renames = parse_renames(rename_text)
            zipped_buf = io.BytesIO()
            zf = zipfile.ZipFile(zipped_buf, mode="w", compression=zipfile.ZIP_DEFLATED)
            st.session_state["outputs"].clear()

            total = len(files)
            valid = 0
            progress = st.progress(0.0, text="Processing...")

            for i, file in enumerate(files, start=1):
                df = load_df(file)
                if df is None or df.empty:
                    st.warning(f"Skipped {file.name}: unsupported or empty.")
                    progress.progress(i / total, text=f"Processed {i}/{total}")
                    continue

                if renames:
                    df = df.rename(columns=renames)

                # Selected columns for this file
                sel = st.session_state["colmap"].get(file.name, [])
                sel = [c for c in sel if c in df.columns]
                if not sel:
                    defaults_here = [c for c in st.session_state.get("adv_default_cols", []) if c in df.columns]
                    if defaults_here:
                        sel = defaults_here
                    else:
                        sel = [df.columns[0]]

                keep_choice = st.session_state["adv_keepmode"]

                if keep_choice.startswith("Keep & replace"):
                    for c in sel:
                        df[c] = hash_series(df[c], hash_type)
                    out_df = df

                elif keep_choice.startswith("Keep all & add"):
                    suffix = st.session_state["adv_suffix"] or f"_{hash_type}"
                    for c in sel:
                        out_col = f"{c}{suffix}"
                        df[out_col] = hash_series(df[c], hash_type)
                    out_df = df

                else:  # Keep only hashed column(s)
                    tmp = {}
                    for c in sel:
                        out_col = f"{c}_{hash_type}"
                        tmp[out_col] = hash_series(df[c], hash_type)
                    out_df = pd.DataFrame(tmp)

                # Write individual file
                csv_buf = io.StringIO()
                out_df.to_csv(csv_buf, index=False)
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

    # Downloads
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

# ======================= COMBINE TAB (lean) ======================
with main_tab[2]:
    st.subheader("Combine (optional)")
    st.markdown("Merge multiple files into one. Useful when you truly need a single consolidated output.")

    c_files = st.file_uploader(
        "Upload file(s) to combine",
        type=["csv", "tsv", "txt", "xlsx", "xls", "parquet"],
        accept_multiple_files=True,
        key="combine_uploader"
    )
    add_source = st.checkbox("Add source filename column", value=True, help="Adds a 'source_filename' column.")
    drop_dupes = st.checkbox("Drop duplicate rows", value=True)
    c_fmt = st.selectbox("Output format", ["csv", "parquet"], index=0)
    c_name = st.text_input("Combined file name", value="combined_output.csv")
    if c_fmt == "parquet" and not c_name.lower().endswith(".parquet"):
        c_name = c_name.rsplit(".", 1)[0] + ".parquet"

    if st.button("Combine files", type="primary", key="combine_go"):
        if not c_files:
            st.error("Upload at least two files.")
        else:
            frames = []
            for f in c_files:
                df = load_df(f)
                if df is not None and not df.empty:
                    if add_source:
                        df.insert(0, "source_filename", f.name)
                    frames.append(df)
            if frames:
                combined = pd.concat(frames, axis=0, ignore_index=True, sort=False)
                if drop_dupes:
                    combined = combined.drop_duplicates()

                if c_fmt == "csv":
                    buf = io.StringIO()
                    combined.to_csv(buf, index=False)
                    data = buf.getvalue().encode("utf-8")
                    mime = "text/csv"
                else:
                    pbuf = io.BytesIO()
                    try:
                        combined.to_parquet(pbuf, engine="pyarrow", index=False)
                    except Exception:
                        combined.to_parquet(pbuf, index=False)
                    pbuf.seek(0)
                    data = pbuf.getvalue()
                    mime = "application/octet-stream"

                st.download_button(
                    f"Download {c_name}",
                    data=data,
                    file_name=c_name,
                    mime=mime,
                    type="primary",
                )
            else:
                st.error("No valid, non-empty files to combine.")

# ================ FOOTER (company name at very bottom) ================
st.markdown(f"<div class='footer'><div class='footerwrap'>{COMPANY_NAME}</div></div>", unsafe_allow_html=True)

