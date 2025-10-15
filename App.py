import io
import os
import zipfile
import hashlib
import pandas as pd
import streamlit as st
import re
import numpy as np

# ---------- CONFIG ----------
COMPANY_NAME = "True Blue Analytics"
TOOL_NAME = "Easy Hasher"
LOGO_PATH = r"C:\Users\musta\Downloads\download.png"  # update if needed

st.set_page_config(page_title=f"{TOOL_NAME} • {COMPANY_NAME}", page_icon=None, layout="wide")

# ================ THEME / STYLES (brand = #061d4c) ================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

    :root{
        --bg1:#eff4ff;
        --bg2:#eaf1ff;
        --panel:#ffffff;
        --ink:#061d4c;
        --muted:#6e7b99;
        --line:#d9e2ff;

        --brand:#061d4c; --brand-2:#061d4c; --brand-3:#061d4c;

        --accent:#b7c8ff; --focus:#3aa0ff;

        --input-bg:#ffffff; --input-text:#061d4c; --placeholder:#8fa1c0; --input-border:#b9c8ef;
        --ring:0 0 0 3px rgba(6,29,76,.28);
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

    /* top-left banner */
    .brandbar{position:sticky; top:0; z-index:999; background:#fff; border-bottom:1px solid var(--line);
              margin:0 -1.25rem .9rem -1.25rem; padding:.35rem 0;}
    .brandwrap{display:flex; align-items:center; gap:10px; max-width:1200px; margin:0 auto; padding:0 1.25rem;}

    /* footer */
    .footer{background:linear-gradient(135deg,var(--brand),var(--brand-2) 60%,var(--brand-3)); color:#fff;
            margin:2rem -1.25rem 0 -1.25rem; border-top:1px solid var(--line);}
    .footerwrap{ max-width:1200px; margin:0 auto; padding:.9rem 1.25rem; font-weight:800; letter-spacing:.3px;}

    h1,h2,h3,h4,h5{ color:var(--ink); margin:0 0 .25rem 0; font-weight:700 }
    h1{font-size:2.0rem;line-height:1.16;margin-top:.25rem}
    h2{font-size:1.35rem;line-height:1.28;margin-top:.25rem}
    .subtitle{color:var(--muted);font-size:1.02rem;margin:.25rem 0 1rem 0;font-weight:500}
    label{color:var(--ink)!important;font-weight:600!important}

    input,textarea,select{font-size:16px!important;color:var(--input-text)!important;
        font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif!important}
    .stTextInput input,.stTextArea textarea{
        background:var(--input-bg)!important;color:var(--input-text)!important;border:1px solid var(--input-border)!important;
        border-radius:14px!important; box-shadow:none!important; padding:.7rem .9rem!important}
    .stTextInput input::placeholder,.stTextArea textarea::placeholder{color:var(--placeholder)!important}
    .stTextInput input:focus,.stTextArea textarea:focus{box-shadow:var(--ring)!important;border-color:var(--brand-3)!important;outline:none!important}

    .stSelectbox div[data-baseweb="select"]>div{
        background:var(--input-bg)!important;color:var(--input-text)!important;border:1px solid var(--input-border)!important;
        border-radius:14px!important;min-height:48px!important;padding:4px 8px!important;
        font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif!important}

    [data-testid="stRadio"] [role="radiogroup"] label{border-radius:12px;padding:.35rem .6rem;font-weight:600!important}
    [data-testid="stRadio"] [role="radiogroup"] label:hover{background:rgba(6,29,76,.08)}
    [data-testid="stRadio"] [role="radiogroup"] input:focus+div{box-shadow:var(--ring);border-radius:12px}

    .stTabs [data-baseweb="tab-list"]{gap:.5rem;margin-bottom:.75rem}
    .stTabs [data-baseweb="tab"]{
        background:#e6ecff;border:1px solid var(--line);border-bottom:2px solid transparent;border-radius:12px 12px 0 0;
        padding:.68rem 1rem;color:var(--ink);font-weight:650;}
    .stTabs [aria-selected="true"]{background:#ffffff;border-bottom:4px solid var(--brand-2)}

    .card{
        background:linear-gradient(180deg,#ffffff,#f5f7ff); border:1px solid var(--line);
        border-radius:18px; padding:1rem 1rem 1.1rem 1rem; box-shadow:0 14px 30px rgba(6,29,76,.08);
        margin-bottom:.9rem}

    .stDownloadButton button,.stButton button{
        background:linear-gradient(135deg,var(--brand),var(--brand-2) 60%,var(--brand-3))!important;color:#ffffff!important;border:none!important;border-radius:14px!important;
        padding:.85rem 1rem!important;font-weight:700!important;letter-spacing:.2px}
    .stDownloadButton button:hover,.stButton button:hover{filter:brightness(1.06)}
    .stAlert{border-radius:14px}

    /* prevent column header wrapping 'E mail' */
    .stDataFrame table { letter-spacing:0 !important; }
    .stDataFrame thead tr th div,
    .stDataFrame thead tr th span,
    [data-testid="stDataFrame"] [data-testid="columnHeaderName"]{
      white-space:nowrap !important; word-break:keep-all !important; hyphens:none !important;
    }
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
st.markdown('<div class="subtitle">Standard: minimal, one-column deduped hashes. Advanced: batch with flexible preview that shows final output.</div>', unsafe_allow_html=True)

# ---------------- Utilities ----------------
def parse_renames(txt: str):
    m = {}
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        if "=" in line:
            a, b = line.split("=", 1)
            a = a.strip(); b = b.strip()
            if a and b: m[a] = b
    return m

def hash_series(s: pd.Series, algo: str, uppercase: bool = False) -> pd.Series:
    f = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256, "sha512": hashlib.sha512}[algo]
    out = s.astype(str).fillna("").map(lambda x: f(x.encode("utf-8")).hexdigest())
    return out.str.upper() if uppercase else out

def safe_base(name: str) -> str:
    base = os.path.splitext(name)[0].strip()
    return base if base else "file"

def human_int(n): return f"{n:,}"

# ---------- Robust file loader with anti-over-split ----------
def load_df(file):
    """
    Robust reader for csv/tsv/txt/xlsx/parquet UploadedFile objects.
    Anti-over-split: collapses accidental multi-column reads (e.g., 'E' + 'ail')
    even when extra cols contain tokens like 'None', 'null', '' etc.
    """
    name = (getattr(file, "name", "") or "").lower()

    def _rewind():
        try: file.seek(0)
        except Exception: pass

    NULL_TOKENS = {"", "none", "null", "na", "n/a", "nan", "nil", "(null)", "-"}

    def _effective_notnull_count(s: pd.Series) -> int:
        s2 = s.astype(str).str.strip()
        s2 = s2.replace(r"^\s*$", np.nan, regex=True)
        s2 = s2.str.lower().replace(list(NULL_TOKENS), np.nan)
        return s2.notna().sum()

    def _collapse_if_single_col_data(df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.shape[1] <= 1: return df
        rows = len(df)
        if rows == 0: return df
        nn = df.apply(_effective_notnull_count)
        top_col = nn.idxmax(); top_cnt = nn.loc[top_col]
        others_nonzero = int((nn.drop(index=top_col) > max(1, int(0.01*rows))).sum())
        top_ratio = top_cnt / max(rows,1)
        if top_ratio >= 0.90 and others_nonzero == 0:
            joined_name = "".join([str(c) for c in df.columns if str(c).strip()])
            new_name = joined_name if 1 <= len(joined_name) <= 40 else str(top_col)
            return pd.DataFrame({new_name: df[top_col]})
        return df

    # Misnamed Excel (ZIP header)
    try:
        head = file.getvalue()[:4]
        if head.startswith(b"PK\x03\x04"):
            _rewind(); df = pd.read_excel(file); return _collapse_if_single_col_data(df)
    except Exception:
        pass

    # Parquet
    if name.endswith(".parquet"):
        try:
            _rewind(); return pd.read_parquet(file, engine="pyarrow")
        except Exception:
            _rewind(); return pd.read_parquet(file)

    # Excel
    if name.endswith((".xlsx", ".xls")):
        _rewind(); df = pd.read_excel(file); return _collapse_if_single_col_data(df)

    # Text-like autodetects
    attempts = [
        dict(sep=None, engine="python", encoding="utf-8", on_bad_lines="skip"),
        dict(sep=None, engine="python", encoding="utf-8-sig", on_bad_lines="skip"),
        dict(sep=None, engine="python", encoding="latin1", on_bad_lines="skip"),
    ]
    for kw in attempts:
        try:
            _rewind(); df = pd.read_csv(file, **kw)
            if df is not None and df.shape[1] > 0: return _collapse_if_single_col_data(df)
        except Exception: pass

    # Fixed delimiters
    for sep in [",", ";", "\t", "|"]:
        for header in [0, None]:
            try:
                _rewind()
                df = pd.read_csv(file, sep=sep, engine="python", encoding="utf-8", on_bad_lines="skip", header=header)
                if df is not None and df.shape[1] > 0:
                    if header is None: df.columns = [f"col_{i+1}" for i in range(df.shape[1])]
                    return _collapse_if_single_col_data(df)
            except Exception:
                continue

    try: _rewind()
    except Exception: pass
    st.warning(f"Could not read {getattr(file, 'name', 'file')}: unsupported format or empty content.")
    return None

# Phone normalization helpers
_digit_re = re.compile(r"\D+")
def normalize_phone_value(x: str) -> str:
    if x is None: return ""
    d = _digit_re.sub("", str(x))
    if len(d) == 11 and d.startswith("1"): d = d[1:]
    return d if len(d) == 10 else ""

def normalize_phone_series(s: pd.Series) -> pd.Series:
    return s.astype(str).map(normalize_phone_value)

def looks_like_phone(series: pd.Series, colname: str) -> bool:
    name = (colname or "").lower()
    if any(k in name for k in ["phone","cell","mobile","tel"]): return True
    stripped = series.astype(str).map(lambda x: _digit_re.sub("", x))
    phone_like = stripped.map(lambda d: len(d) >= 10 or (len(d) == 11 and d.startswith("1")))
    return phone_like.mean() >= 0.6

# ======================= MAIN TABS =======================
main_tab = st.tabs(["Standard", "Advanced", "Combine"])

# ======================= STANDARD TAB ======================
with main_tab[0]:
    st.subheader("Standard")
    st.markdown("One-step hashing with minimal choices. Output is a **single `hash` column**, **deduplicated**.")

    std_file = st.file_uploader("Upload a file", type=["csv","tsv","txt","xlsx","xls","parquet"], key="std_uploader")
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        std_hash = st.selectbox("Hash type", ["md5","sha1","sha256","sha512"], index=0, key="std_hash")
    with c2:
        std_norm = st.checkbox("Normalize to 10-digit phones (auto-detect)", value=True,
                               help="Runs only if the selected column is phone-like. Emails/IDs are left as-is.")
    with c3:
        std_upper = st.checkbox("Uppercase hashes (A–F)", value=False)

    if std_file:
        df0 = load_df(std_file)
        if df0 is not None and not df0.empty:
            col = st.selectbox("Column to hash", options=list(df0.columns), index=0, key="std_col")

            st.markdown('<div class="card">', unsafe_allow_html=True)
            rows, cols = df0.shape
            st.caption(f"Source preview shape: {rows:,} × {cols}")
            st.dataframe(df0.head(10), use_container_width=True, hide_index=True)

            if st.button("Hash now", type="primary", key="std_go"):
                src = df0[col]
                apply_norm = std_norm and looks_like_phone(src, col)
                if std_norm and not apply_norm:
                    st.info("Column does not look like a phone field — skipping normalization.")
                to_hash = normalize_phone_series(src) if apply_norm else src.astype(str).fillna("")
                hashed = hash_series(to_hash, std_hash, uppercase=std_upper)
                result = pd.DataFrame({"hash": hashed}).drop_duplicates().reset_index(drop=True)

                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("### Result (first 10 unique hashes)")
                r_rows, r_cols = result.shape
                st.caption(f"Result shape: {r_rows:,} × {r_cols}")
                st.dataframe(result.head(10), use_container_width=True, hide_index=True)

                csv_buf = io.StringIO(); result.to_csv(csv_buf, index=False)
                st.download_button("Download hashes (CSV)", data=csv_buf.getvalue().encode("utf-8"),
                                   file_name=f"{safe_base(std_file.name)}_hashes.csv", mime="text/csv", type="primary")
        else:
            st.warning("Could not read the file or it is empty.")

# ======================= ADVANCED TAB ======================
with main_tab[1]:
    st.subheader("Advanced")

    # Upload at top
    files = st.file_uploader("Upload file(s)", type=["csv","tsv","txt","xlsx","xls","parquet"],
                             accept_multiple_files=True, key="adv_uploader")

    if "outputs" not in st.session_state: st.session_state["outputs"] = {}
    if "zip_bytes" not in st.session_state: st.session_state["zip_bytes"] = None

    st.markdown("#### Options")
    oc1, oc2, oc3 = st.columns([1,1,1])
    with oc1:
        adv_hash = st.selectbox("Hash type", ["md5","sha1","sha256","sha512"], index=0, key="adv_hash_type")
    with oc2:
        # global columns to hash
        all_cols = []
        if files:
            for f in files[:20]:
                df_tmp = load_df(f)
                if df_tmp is not None and not df_tmp.empty:
                    all_cols.extend(list(df_tmp.columns))
        all_cols = sorted(pd.Index(all_cols).unique().tolist()) if all_cols else []
        cols_to_hash = st.multiselect("Columns to hash", options=all_cols,
                                      default=all_cols[:1] if all_cols else [],
                                      help="These columns will be hashed in each file if present.",
                                      key="adv_cols_to_hash")
    with oc3:
        suffix = st.text_input("Suffix for added hash columns (Add mode)", value=f"_{adv_hash}",
                               help="Used only for 'Keep all & add'. Example: email → email_sha256",
                               key="adv_suffix")

    adv_norm  = st.checkbox("Normalize to 10-digit phones (auto-detect per selected column)", value=True)
    adv_upper = st.checkbox("Uppercase hashes (A–F)", value=False)

    keep_mode = st.radio("Columns to keep in output", [
        "Keep & replace — Replace each selected column with its hash (same name).",
        "Keep all & add — Keep file as-is and add hash column(s) using the suffix.",
        "Keep only hashed column(s) — Output just the hash column(s).",
    ], index=1, key="adv_keepmode")

    rename_on = st.checkbox("Manually rename columns", value=False)
    rename_text = ""
    if rename_on:
        rename_text = st.text_area("Rename columns (old=new per line)", height=110,
                                   placeholder="email=primary_email\nCell=cell\nZIP=zip", key="adv_renames")

    # ----- PREVIEW of FINAL OUTPUT (per file) -----
    if files:
        st.markdown("#### Preview (shows final output structure)")
        for file in files[:10]:
            df = load_df(file)
            if df is not None and not df.empty:
                if rename_on and rename_text.strip():
                    df = df.rename(columns=parse_renames(rename_text))

                sel = [c for c in cols_to_hash if c in df.columns]
                if not sel and len(df.columns) > 0: sel = [df.columns[0]]

                if keep_mode.startswith("Keep & replace"):
                    out_df = df.copy()
                    for c in sel:
                        series = out_df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        out_df[c] = hash_series(to_hash, adv_hash, uppercase=adv_upper)

                elif keep_mode.startswith("Keep all & add"):
                    out_df = df.copy()
                    sfx = suffix or f"_{adv_hash}"
                    for c in sel:
                        series = out_df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        out_df[f"{c}{sfx}"] = hash_series(to_hash, adv_hash, uppercase=adv_upper)

                else:  # Keep only hashed column(s)
                    cols = {}
                    for c in sel:
                        series = df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        cols[f"{c}_{adv_hash}"] = hash_series(to_hash, adv_hash, uppercase=adv_upper)
                    out_df = pd.DataFrame(cols)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                o_rows, o_cols = out_df.shape
                st.caption(f"{file.name} — preview shape: {o_rows:,} × {o_cols}")
                st.dataframe(out_df.head(15), use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Upload files above, pick **Columns to hash**, then review the live preview here.")

    st.markdown("---")
    run = st.button("Run hashing", type="primary", use_container_width=True, key="adv_run")

    if run:
        if not files:
            st.error("Upload at least one file.")
        else:
            zipped_buf = io.BytesIO()
            zf = zipfile.ZipFile(zipped_buf, mode="w", compression=zipfile.ZIP_DEFLATED)
            st.session_state["outputs"].clear()

            total = len(files); valid = 0
            progress = st.progress(0.0, text="Processing...")

            renames = parse_renames(rename_text) if (rename_on and rename_text.strip()) else {}

            for i, file in enumerate(files, start=1):
                df = load_df(file)
                if df is None or df.empty:
                    st.warning(f"Skipped {file.name}: unsupported or empty.")
                    progress.progress(i/total, text=f"Processed {i}/{total}")
                    continue

                if renames: df = df.rename(columns=renames)

                sel = [c for c in cols_to_hash if c in df.columns]
                if not sel: sel = [df.columns[0]]

                if keep_mode.startswith("Keep & replace"):
                    out_df = df.copy()
                    for c in sel:
                        series = out_df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        out_df[c] = hash_series(to_hash, adv_hash, uppercase=adv_upper)

                elif keep_mode.startswith("Keep all & add"):
                    out_df = df.copy()
                    sfx = suffix or f"_{adv_hash}"
                    for c in sel:
                        series = out_df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        out_df[f"{c}{sfx}"] = hash_series(to_hash, adv_hash, uppercase=adv_upper)

                else:  # Keep only hashed column(s)
                    cols = {}
                    for c in sel:
                        series = df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        cols[f"{c}_{adv_hash}"] = hash_series(to_hash, adv_hash, uppercase=adv_upper)
                    out_df = pd.DataFrame(cols)

                csv_buf = io.StringIO(); out_df.to_csv(csv_buf, index=False)
                data_bytes = csv_buf.getvalue().encode("utf-8")
                out_name = f"{safe_base(file.name)}_hashed.csv"
                zf.writestr(out_name, data_bytes)
                st.session_state["outputs"][out_name] = data_bytes

                valid += 1
                progress.progress(i/total, text=f"Processed {i}/{total}")

            zf.close(); zipped_buf.seek(0)
            if st.session_state["outputs"]:
                st.session_state["zip_bytes"] = zipped_buf.getvalue()
                st.success(f"Finished {valid} file(s). Scroll down to download.")
            else:
                st.error("No outputs produced. Check column names and try again.")

    st.markdown("### Downloads")
    if st.session_state.get("outputs"):
        left, right = st.columns([2,1])
        with left:
            for name, data_bytes in st.session_state["outputs"].items():
                st.download_button(label=f"Download {name}", data=data_bytes, file_name=name,
                                   mime="text/csv", key=f"dl-{name}", use_container_width=True)
        with right:
            if st.session_state.get("zip_bytes"):
                st.download_button(label="Download all as ZIP", data=st.session_state["zip_bytes"],
                                   file_name="hashed_outputs.zip", mime="application/zip",
                                   key="dl-zip", type="primary", use_container_width=True)
    else:
        st.info("Nothing to download yet—run hashing above once you’ve set options and previews.")

# ======================= COMBINE TAB ======================
with main_tab[2]:
    st.subheader("Combine (optional)")
    st.markdown("Merge multiple files into one. Defaults: **drop duplicate rows** ON, **source filename** OFF.")

    c_files = st.file_uploader("Upload file(s) to combine", type=["csv","tsv","txt","xlsx","xls","parquet"],
                               accept_multiple_files=True, key="combine_uploader")
    drop_dupes = st.checkbox("Drop duplicate rows", value=True)
    add_source = st.checkbox("Add source filename column", value=False, help="Adds a 'source_filename' column.")

    c_fmt  = st.selectbox("Output format", ["csv","parquet"], index=0)
    c_name = st.text_input("Combined file name", value="combined_output.csv")
    if c_fmt == "parquet" and not c_name.lower().endswith(".parquet"):
        c_name = c_name.rsplit(".", 1)[0] + ".parquet"

    def _coerce_to_single_hash(df: pd.DataFrame) -> pd.DataFrame:
        """Standardize to one 'hash' column when possible (unless add_source is True)."""
        if add_source: return df
        if "hash" in df.columns: return df[["hash"]].copy()
        if df.shape[1] == 1:
            df2 = df.copy(); df2.columns = ["hash"]; return df2
        df2 = df.drop(columns=[c for c in df.columns if df[c].isna().all()]) if df.shape[1] else df
        first = df2.columns[0]; return df2[[first]].rename(columns={first:"hash"})

    if st.button("Combine files", type="primary", key="combine_go"):
        if not c_files:
            st.error("Upload at least two files.")
        else:
            frames = []
            for f in c_files:
                df = load_df(f)
                if df is not None and not df.empty:
                    df_std = _coerce_to_single_hash(df)
                    if add_source and "source_filename" not in df_std.columns:
                        df_std.insert(0, "source_filename", f.name)
                    frames.append(df_std)

            if frames:
                combined = pd.concat(frames, axis=0, ignore_index=True, sort=False)
                if drop_dupes: combined = combined.drop_duplicates()

                if c_fmt == "csv":
                    buf = io.StringIO(); combined.to_csv(buf, index=False)
                    data = buf.getvalue().encode("utf-8"); mime = "text/csv"
                else:
                    pbuf = io.BytesIO()
                    try: combined.to_parquet(pbuf, engine="pyarrow", index=False)
                    except Exception: combined.to_parquet(pbuf, index=False)
                    pbuf.seek(0); data = pbuf.getvalue(); mime = "application/octet-stream"

                st.download_button(f"Download {c_name}", data=data, file_name=c_name, mime=mime, type="primary")
            else:
                st.error("No valid, non-empty files to combine.")

# ================ FOOTER (company name at very bottom) ================
st.markdown(f"<div class='footer'><div class='footerwrap'>{COMPANY_NAME}</div></div>", unsafe_allow_html=True)

