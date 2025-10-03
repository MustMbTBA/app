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
st.markdown('<div class="subtitle">Use <b>Standard</b> for one-screen hashing with safe phone normalization, or <b>Advanced</b> for batch workflows.</div>', unsafe_allow_html=True)

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

# Phone normalization helpers
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
main_tab = st.tabs(["Standard", "Advanced"])  # <-- renamed per request

# ======================= STANDARD TAB ======================
with main_tab[0]:
    st.subheader("Standard")
    st.markdown("One-step hashing. Phone normalization is **applied only to phone-like columns** to avoid corrupting emails or IDs.")

    # defaults: MD5, preview 10
    simple_file = st.file_uploader("Upload a file", type=["csv", "tsv", "txt", "xlsx", "xls", "parquet"], key="standard_uploader")
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        simple_hash = st.selectbox("Hash type", ["md5", "sha1", "sha256", "sha512"], index=0, key="standard_hash")  # MD5 default
    with c2:
        normalize_phone_toggle = st.checkbox(
            "Normalize to 10-digit phones (recommended)",
            value=True,
            help="Only applied when the selected column is phone-like."
        )
    with c3:
        preview_rows_simple = st.slider("Preview rows", 5, 50, 10, key="standard_preview")  # default 10

    if simple_file:
        df0 = load_df(simple_file)
        if df0 is not None and not df0.empty:
            col = st.selectbox("Column to hash", options=list(df0.columns), index=0, key="standard_col")
            out_name = st.text_input("Output column name (optional if one column)", value=f"{col}_{simple_hash}", key="standard_outname")

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**{simple_file.name}**")
            st.dataframe(df0.head(preview_rows_simple), use_container_width=True, hide_index=True)

            if st.button("Hash now", type="primary", key="standard_go"):
                df = df0.copy()
                source = df[col]

                apply_norm = normalize_phone_toggle and looks_like_phone(source, col)
                if normalize_phone_toggle and not apply_norm:
                    st.info("Column does not look like a phone field — skipping normalization to protect non-phone data.")

                to_hash = normalize_phone_series(source) if apply_norm else source.astype(str).fillna("")

                # if user changed algo after default out_name was set, keep a sensible default
                if not out_name.strip():
                    out_name = f"{col}_{simple_hash}"

                df[out_name] = hash_series(to_hash, simple_hash)

                keep_cols = [col]
                if apply_norm:
                    norm_col = f"{col}_10digit"
                    df[norm_col] = normalize_phone_series(source)
                    keep_cols.append(norm_col)
                keep_cols.append(out_name)
                result = df[keep_cols]

                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("### Result preview")
                st.dataframe(result.head(preview_rows_simple), use_container_width=True, hide_index=True)

                csv_buf = io.StringIO()
                result.to_csv(csv_buf, index=False)
                st.download_button(
                    "Download hashed file (CSV)",
                    data=csv_buf.getvalue().encode("utf-8"),
                    file_name=f"{safe_base(simple_file.name)}_hashed_standard.csv",
                    mime="text/csv",
                    type="primary",
                )
        else:
            st.warning("Could not read the file or it is empty.")

# ======================= ADVANCED TAB ======================
with main_tab[1]:
    # Keep shared state buckets
    if "outputs" not in st.session_state: st.session_state["outputs"] = {}
    if "zip_bytes" not in st.session_state: st.session_state["zip_bytes"] = None
    if "combined_bytes" not in st.session_state: st.session_state["combined_bytes"] = None
    if "combined_name" not in st.session_state: st.session_state["combined_name"] = "combined_hashed.csv"
    if "colmap" not in st.session_state: st.session_state["colmap"] = {}

    adv_tabs = st.tabs(["Preview & Options", "Run & Download"])

    # -------- Tab 1: Preview & Options --------
    with adv_tabs[0]:
        st.subheader("Preview & Options")

        # Options (moved into the tab body)
        oc1, oc2, oc3 = st.columns([1,1,1])
        with oc1:
            hash_type = st.selectbox("Hash type", ["md5", "sha1", "sha256", "sha512"], index=2, key="adv_hash_type")
        with oc2:
            col_override = st.text_input("Default column if none selected", value="", placeholder="email, cell, id", key="adv_col_override")
        with oc3:
            new_col_name = st.text_input("Output column name (if hashing ONE column)", value="", placeholder="e.g., email_sha256", key="adv_newcol")

        retain_mode = st.radio("Columns to keep in output", ["Keep all columns", "Keep source + hashed only", "Keep only hashed column"], index=0, key="adv_retain")
        rename_text = st.text_area("Rename columns (old=new per line)", height=120, placeholder="email=primary_email\nCell=cell\nZIP=zip", key="adv_renames")

        st.markdown("#### Combine")
        cc1, cc2, cc3, cc4 = st.columns([1,1,1,2])
        with cc1:
            combine_files = st.checkbox("Combine all files", value=True, key="adv_combine")
        with cc2:
            add_source_col = st.checkbox("Add source filename", value=True, key="adv_addsrc")
        with cc3:
            drop_dupes = st.checkbox("Drop duplicates", value=True, key="adv_dupes")
        with cc4:
            combined_format = st.selectbox("Combined format", ["csv", "parquet"], index=0, key="adv_fmt")

        combined_name = st.text_input(
            "Combined file name",
            value=st.session_state.get("combined_name", "combined_hashed.csv"),
            key="adv_combined_name"
        )
        if st.session_state["adv_fmt"] == "parquet" and not combined_name.lower().endswith(".parquet"):
            combined_name = combined_name.rsplit(".", 1)[0] + ".parquet"

        preview_rows_adv = st.slider("Preview rows", 5, 100, 15, key="adv_preview_rows")

        files = st.file_uploader("Upload file(s)", type=["csv", "tsv", "txt", "xlsx", "xls", "parquet"], accept_multiple_files=True, key="adv_uploader")

        # Show per-file preview & column pickers
        if files:
            st.info("Choose **Columns to hash** under each file. Leave empty to use the default column above.")
            for file in files[:12]:
                df = load_df(file)
                if df is not None and not df.empty:
                    rows, cols = df.shape
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(f"**{file.name}**  ·  {human_int(rows)} rows × {cols} columns")

                    # default guess
                    default_guess = st.session_state["colmap"].get(file.name)
                    if not default_guess:
                        if st.session_state["adv_col_override"].strip() in df.columns:
                            default_guess = [st.session_state["adv_col_override"].strip()]
                        else:
                            default_guess = [df.columns[0]]

                    sel = st.multiselect(
                        f"Columns to hash — {file.name}",
                        options=list(df.columns),
                        default=default_guess,
                        key=f"adv-ms-{file.name}",
                        help="Pick one or more columns for hashing for this file."
                    )
                    st.session_state["colmap"][file.name] = sel

                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.dataframe(df.head(st.session_state["adv_preview_rows"]), use_container_width=True, hide_index=True)
                    with c2:
                        schema = pd.DataFrame({"column": df.columns, "dtype": [str(t) for t in df.dtypes]})
                        st.dataframe(schema, use_container_width=True, hide_index=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Upload files above to preview and pick columns.")

    # -------- Tab 2: Run & Download --------
    with adv_tabs[1]:
        st.subheader("Run & Download")

        # Run button
        run = st.button("Run hashing", type="primary", use_container_width=True, key="adv_run")

        if run:
            files = st.session_state.get("adv_uploader")
            if not files:
                st.error("Upload at least one file on the Preview & Options tab.")
            else:
                # Pull options from state
                hash_type = st.session_state["adv_hash_type"]
                col_override = st.session_state["adv_col_override"]
                new_col_name = st.session_state["adv_newcol"]
                retain_mode = st.session_state["adv_retain"]
                renames = parse_renames(st.session_state["adv_renames"])
                combine_files = st.session_state["adv_combine"]
                add_source_col = st.session_state["adv_addsrc"]
                drop_dupes = st.session_state["adv_dupes"]
                combined_format = st.session_state["adv_fmt"]
                combined_name = st.session_state["adv_combined_name"]

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
                    st.success(msg)
                else:
                    st.error("No outputs produced. Check column names and try again.")

        # Downloads (always visible here)
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
            st.info("Nothing to download yet—click **Run hashing** above once you’ve set options on the first tab.")

# ================ FOOTER (company name at very bottom) ================
st.markdown(f"<div class='footer'><div class='footerwrap'>{COMPANY_NAME}</div></div>", unsafe_allow_html=True)

