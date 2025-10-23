import io
import os
import zipfile
import hashlib
import pandas as pd
import streamlit as st
import re
import importlib.util

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
        --bg1:#eff4ff; --bg2:#eaf1ff; --panel:#ffffff;
        --ink:#061d4c; --muted:#6e7b99; --line:#d9e2ff;
        --brand:#061d4c; --brand-2:#061d4c; --brand-3:#061d4c;
        --accent:#b7c8ff; --focus:#3aa0ff;
        --input-bg:#ffffff; --input-text:#061d4c;
        --placeholder:#8fa1c0; --input-border:#b9c8ef;
        --ring:0 0 0 3px rgba(6,29,76,.28);
    }
    *{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
    html,body,[data-testid="stAppViewContainer"]{
        background:linear-gradient(180deg,var(--bg1),var(--bg2));
        color:var(--ink);
        font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; letter-spacing:.1px;
    }
    .block-container{padding:0 1.25rem 2rem 1.25rem;max-width:1200px}
    [data-testid="stSidebar"]{background:var(--panel);border-right:1px solid var(--line);padding-top:.75rem}
    .brandbar{position:sticky;top:0;z-index:999;background:#fff;border-bottom:1px solid var(--line);margin:0 -1.25rem .9rem -1.25rem;padding:.35rem 0;}
    .brandwrap{display:flex;align-items:center;gap:10px;max-width:1200px;margin:0 auto;padding:0 1.25rem;justify-content:flex-start;}
    .footer{background:linear-gradient(135deg,var(--brand) 0%,var(--brand-2) 60%,var(--brand-3) 100%);color:#fff;margin:2rem -1.25rem 0 -1.25rem;border-top:1px solid var(--line);}
    .footerwrap{max-width:1200px;margin:0 auto;padding:.9rem 1.25rem;font-weight:800;letter-spacing:.3px;}
    h1,h2,h3,h4,h5{color:var(--ink);margin:0 0 .25rem 0;font-weight:700}
    h1{font-size:2.0rem;line-height:1.16;margin-top:.25rem}
    h2{font-size:1.35rem;line-height:1.28;margin-top:.25rem}
    .subtitle{color:var(--muted);font-size:1.02rem;margin:.25rem 0 1rem 0;font-weight:500}
    label{color:var(--ink)!important;font-weight:600!important}
    input,textarea,select{font-size:16px!important;color:var(--input-text)!important;font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif!important}
    .stTextInput input,.stTextArea textarea{background:var(--input-bg)!important;color:var(--input-text)!important;border:1px solid var(--input-border)!important;border-radius:14px!important;box-shadow:none!important;padding:.7rem .9rem!important}
    .stTextInput input::placeholder,.stTextArea textarea::placeholder{color:var(--placeholder)!important}
    .stTextInput input:focus,.stTextArea textarea:focus{box-shadow:var(--ring)!important;border-color:var(--brand-3)!important;outline:none!important}
    .stSelectbox div[data-baseweb="select"]>div{background:var(--input-bg)!important;color:var(--input-text)!important;border:1px solid var(--input-border)!important;border-radius:14px!important;min-height:48px!important;padding:4px 8px!important}
    [data-testid="stRadio"] [role="radiogroup"] label{border-radius:12px;padding:.35rem .6rem;font-weight:600!important}
    .stTabs [data-baseweb="tab-list"]{gap:.5rem;margin-bottom:.75rem}
    .stTabs [data-baseweb="tab"]{background:#e6ecff;border:1px solid var(--line);border-bottom:2px solid transparent;border-radius:12px 12px 0 0;padding:.68rem 1rem;color:var(--ink);font-weight:650;}
    .stTabs [aria-selected="true"]{background:#ffffff;border-bottom:4px solid var(--brand-2)}
    .card{background:linear-gradient(180deg,#ffffff,#f5f7ff);border:1px solid var(--line);border-radius:18px;padding:1rem 1rem 1.1rem 1rem;box-shadow:0 14px 30px rgba(6,29,76,.08);margin-bottom:.9rem}
    .stDownloadButton button,.stButton button{background:linear-gradient(135deg,var(--brand) 0%,var(--brand-2) 60%,var(--brand-3) 100%)!important;color:#ffffff!important;border:none!important;border-radius:14px!important;padding:.85rem 1rem!important;font-weight:700!important;letter-spacing:.2px}
    .stAlert{border-radius:14px}
    /* no split headers like 'E mail' */
    .stDataFrame table{letter-spacing:0!important}
    .stDataFrame thead tr th div,[data-testid="stDataFrame"] [data-testid="columnHeaderName"]{white-space:nowrap!important;word-break:keep-all!important;hyphens:none!important}
    </style>
    """,
    unsafe_allow_html=True,
)

# ================ TOP-LEFT BANNER (logo) ================
st.markdown('<div class="brandbar"><div class="brandwrap">', unsafe_allow_html=True)
try:
    st.image(LOGO_PATH, use_container_width=False, caption=None, output_format="PNG")
except Exception:
    st.write("")
st.markdown('</div></div>', unsafe_allow_html=True)

# ================ APP TITLE =================
st.title(TOOL_NAME)
st.markdown('<div class="subtitle">Standard: minimal, one-column deduped hashes. Advanced: per-file column selection with live output preview.</div>', unsafe_allow_html=True)

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

def _has(mod: str) -> bool:
    return importlib.util.find_spec(mod) is not None

# ---------- robust Excel & text loader ----------
def _collapse_if_single_col_data(df: pd.DataFrame) -> pd.DataFrame:
    """Tidy up sheets that are effectively single-column."""
    import re
    cols_all_na = [c for c in df.columns if df[c].isna().all()]
    if cols_all_na: df = df.drop(columns=cols_all_na)
    if df.shape[1] == 1:
        c = df.columns[0]
        if re.match(r"^Unnamed", str(c), flags=re.I):
            df = df.rename(columns={c: "col_1"})
        return df
    non_empty_counts = df.notna().sum()
    top_col = non_empty_counts.idxmax()
    if (non_empty_counts[top_col] > 0) and (
        (non_empty_counts[top_col] >= non_empty_counts.sum() * 0.8)
        or (non_empty_counts[top_col] >= len(df) * 0.9)
    ):
        tmp = df[[top_col]].copy()
        if re.match(r"^Unnamed", str(top_col), flags=re.I):
            tmp = tmp.rename(columns={top_col: "col_1"})
        return tmp
    return df

def load_df(file):
    """
    Read csv/tsv/txt/xlsx/xls/xlsb/parquet.
    - For Excel: force engine by extension, use dtype=str to avoid mojibake.
    - Never fall back to CSV for Excel.
    """
    import pandas as pd, io

    name = (getattr(file, "name", "") or "").lower()

    def _rewind():
        try: file.seek(0)
        except Exception: pass

    # sniff leading bytes (ZIP magic for xlsx)
    head = b""
    try: head = file.getvalue()[:4]
    except Exception: pass

    # PARQUET
    if name.endswith(".parquet"):
        for eng in ("pyarrow", None):
            try:
                _rewind()
                return pd.read_parquet(file, engine=eng)
            except Exception:
                continue

    # Excel helpers (engine by ext)
    def _read_xlsx(bytes_data: bytes):
        if not _has("openpyxl"):
            return "__NO_XLSX__"
        bio = io.BytesIO(bytes_data)
        try:
            # dtype=str supported by openpyxl
            df = pd.read_excel(bio, engine="openpyxl", dtype=str)
            return _collapse_if_single_col_data(df)
        except Exception:
            return None

    def _read_xls(bytes_data: bytes):
        if not _has("xlrd"):
            return "__NO_XLS__"
        bio = io.BytesIO(bytes_data)
        try:
            # xlrd dtype=str is honored in older versions; pin xlrd==1.2.0
            df = pd.read_excel(bio, engine="xlrd", dtype=str)
            # ensure strings
            df = df.apply(lambda col: col.astype(str) if col.dtype.kind not in "OUS" else col)
            return _collapse_if_single_col_data(df)
        except Exception:
            return None

    def _read_xlsb(bytes_data: bytes):
        if not _has("pyxlsb"):
            return "__NO_XLSB__"
        bio = io.BytesIO(bytes_data)
        try:
            df = pd.read_excel(bio, engine="pyxlsb")  # dtype not supported; coerce after
            df = df.apply(lambda col: col.astype(str))
            return _collapse_if_single_col_data(df)
        except Exception:
            return None

    is_zip = head.startswith(b"PK\x03\x04")
    # Misnamed .xlsx or real .xlsx
    if is_zip or name.endswith(".xlsx"):
        _rewind(); data = file.getvalue()
        res = _read_xlsx(data)
        if res == "__NO_XLSX__":
            st.error("`.xlsx` file detected, but **openpyxl** is not installed. Add `openpyxl` to requirements.txt.")
            return None
        if res is None:
            st.error("`.xlsx` file detected but could not be read with openpyxl.")
            return None
        return res

    if name.endswith(".xls"):
        _rewind(); data = file.getvalue()
        res = _read_xls(data)
        if res == "__NO_XLS__":
            st.error("`.xls` file detected, but **xlrd==1.2.0** is required. Add `xlrd==1.2.0` to requirements.txt.")
            return None
        if res is None:
            st.error("`.xls` file detected but could not be read with xlrd.")
            return None
        return res

    if name.endswith(".xlsb"):
        _rewind(); data = file.getvalue()
        res = _read_xlsb(data)
        if res == "__NO_XLSB__":
            st.error("`.xlsb` file detected, but **pyxlsb** is not installed. Add `pyxlsb` to requirements.txt.")
            return None
        if res is None:
            st.error("`.xlsb` file detected but could not be read with pyxlsb.")
            return None
        return res

    # TEXT-LIKE
    attempts = [
        dict(sep=None, engine="python", encoding="utf-8", on_bad_lines="skip"),
        dict(sep=None, engine="python", encoding="utf-8-sig", on_bad_lines="skip"),
        dict(sep=None, engine="python", encoding="latin1", on_bad_lines="skip"),
    ]
    for kw in attempts:
        try:
            _rewind(); df = pd.read_csv(file, **kw)
            if df is not None and df.shape[1] > 0: return df
        except Exception:
            pass

    for sep in [",", ";", "\t", "|"]:
        for header in [0, None]:
            try:
                _rewind()
                df = pd.read_csv(file, sep=sep, engine="python", encoding="utf-8", on_bad_lines="skip", header=header)
                if df is not None and df.shape[1] > 0:
                    if header is None: df.columns = [f"col_{i+1}" for i in range(df.shape[1])]
                    return df
            except Exception:
                continue

    st.warning(f"Could not read {getattr(file, 'name', 'file')}: unsupported or empty.")
    return None

# Phone normalization
_digit_re = re.compile(r"\D+")
def normalize_phone_value(x: str) -> str:
    if x is None: return ""
    d = _digit_re.sub("", str(x))
    if len(d) == 11 and d.startswith("1"): d = d[1:]
    if len(d) == 10: return d
    return ""

def normalize_phone_series(s: pd.Series) -> pd.Series:
    return s.astype(str).map(normalize_phone_value)

def looks_like_phone(series: pd.Series, colname: str) -> bool:
    name = (colname or "").lower()
    if any(k in name for k in ["phone", "cell", "mobile", "tel"]): return True
    stripped = series.astype(str).map(lambda x: _digit_re.sub("", x))
    phone_like = stripped.map(lambda d: len(d) >= 10 or (len(d) == 11 and d.startswith("1")))
    return phone_like.mean() >= 0.6

# ======================= MAIN TABS =======================
main_tab = st.tabs(["Standard", "Advanced", "Combine"])

# ======================= STANDARD TAB ======================
with main_tab[0]:
    st.subheader("Standard")
    st.markdown("One-step hashing with minimal choices. Output is a **single `hash` column**, **deduplicated**.")
    std_file = st.file_uploader("Upload a file", type=["csv","tsv","txt","xlsx","xls","xlsb","parquet"], key="std_uploader")
    c1, c2 = st.columns([1,1])
    with c1:
        std_hash = st.selectbox("Hash type", ["md5","sha1","sha256","sha512"], index=0)
    with c2:
        std_norm = st.checkbox("Normalize to 10-digit phones (auto-detect)", value=True)

    if std_file:
        df0 = load_df(std_file)
        if df0 is not None and not df0.empty:
            col = st.selectbox("Column to hash", options=list(df0.columns), index=0)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            rows, cols = df0.shape; st.caption(f"Preview shape: {rows:,} × {cols}")
            st.dataframe(df0.head(10), use_container_width=True, hide_index=True)
            if st.button("Hash now", type="primary", key="std_go"):
                src = df0[col]
                to_hash = normalize_phone_series(src) if (std_norm and looks_like_phone(src, col)) else src.astype(str).fillna("")
                result = pd.DataFrame({"hash": hash_series(to_hash, std_hash)}).drop_duplicates().reset_index(drop=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("### Result (first 10 unique hashes)")
                st.dataframe(result.head(10), use_container_width=True, hide_index=True)
                csv_buf = io.StringIO(); result.to_csv(csv_buf, index=False)
                st.download_button("Download hashes (CSV)", data=csv_buf.getvalue().encode("utf-8"),
                                   file_name=f"{safe_base(std_file.name)}_hashes.csv", mime="text/csv", type="primary")
        else:
            st.warning("Could not read the file or it is empty.")

# ======================= ADVANCED TAB (per-file selection) ======================
with main_tab[1]:
    st.subheader("Advanced")
    files = st.file_uploader("Upload file(s)", type=["csv","tsv","txt","xlsx","xls","xlsb","parquet"], accept_multiple_files=True, key="adv_uploader")

    if "outputs" not in st.session_state: st.session_state["outputs"] = {}
    if "zip_bytes" not in st.session_state: st.session_state["zip_bytes"] = None
    if "colmap" not in st.session_state: st.session_state["colmap"] = {}

    st.markdown("#### Options")
    oc1, oc2, oc3 = st.columns([1,1,1])
    with oc1:
        adv_hash = st.selectbox("Hash type", ["md5","sha1","sha256","sha512"], index=0, key="adv_hash_type")
    with oc2:
        suffix = st.text_input("Suffix for added hash columns (Add mode)", value=f"_{adv_hash}", key="adv_suffix")
    with oc3:
        adv_norm = st.checkbox("Normalize to 10-digit phones", value=True,
                               help="Applied per selected column when it looks like a phone field.")

    keep_mode = st.radio(
        "Columns to keep in output",
        [
            "Keep & replace — Replace each selected column with its hash (same name).",
            "Keep all & add — Keep file as-is and add hash column(s) using the suffix.",
            "Keep only hashed column(s) — Output just the hash column(s).",
        ], index=1, key="adv_keepmode"
    )

    rename_on = st.checkbox("Manually rename columns", value=False)
    rename_text = ""
    if rename_on:
        rename_text = st.text_area("Rename columns (old=new per line)", height=110,
                                   placeholder="email=primary_email\nCell=cell\nZIP=zip", key="adv_renames")

    # ----- Per-file PREVIEW & selection -----
    if files:
        st.markdown("#### Preview & choose columns (per file)")
        for file in files[:12]:
            df = load_df(file)
            if df is not None and not df.empty:
                if rename_on and rename_text.strip():
                    df = df.rename(columns=parse_renames(rename_text))

                default_sel = st.session_state["colmap"].get(file.name)
                if not default_sel:
                    default_sel = [df.columns[0]]
                sel = st.multiselect(f"Columns to hash — {file.name}", options=list(df.columns),
                                     default=[c for c in default_sel if c in df.columns],
                                     key=f"adv-ms-{file.name}")
                st.session_state["colmap"][file.name] = sel

                # Build live output preview for this file
                if keep_mode.startswith("Keep & replace"):
                    out_df = df.copy()
                    for c in sel:
                        series = out_df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        out_df[c] = hash_series(to_hash, adv_hash)

                elif keep_mode.startswith("Keep all & add"):
                    out_df = df.copy()
                    sfx = suffix or f"_{adv_hash}"
                    for c in sel:
                        series = out_df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        out_df[f"{c}{sfx}"] = hash_series(to_hash, adv_hash)

                else:  # Keep only hashed column(s)
                    cols = {}
                    for c in sel:
                        series = df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        cols[f"{c}_{adv_hash}"] = hash_series(to_hash, adv_hash)
                    out_df = pd.DataFrame(cols)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                rows, cols = out_df.shape; st.caption(f"{file.name} — previewing first 15 rows · shape: {rows:,} × {cols}")
                st.dataframe(out_df.head(15), use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Upload files above to choose columns and see per-file previews.")

    st.markdown("---")
    run = st.button("Run hashing", type="primary", use_container_width=True, key="adv_run")
    if run:
        if not files:
            st.error("Upload at least one file.")
        else:
            zipped_buf = io.BytesIO(); zf = zipfile.ZipFile(zipped_buf, mode="w", compression=zipfile.ZIP_DEFLATED)
            st.session_state["outputs"].clear()
            total = len(files); valid = 0
            progress = st.progress(0.0, text="Processing...")

            renames = parse_renames(rename_text) if (rename_on and rename_text.strip()) else {}

            for i, file in enumerate(files, start=1):
                df = load_df(file)
                if df is None or df.empty:
                    st.warning(f"Skipped {file.name}: unsupported or empty.")
                    progress.progress(i/total, text=f"Processed {i}/{total}"); continue

                if renames: df = df.rename(columns=renames)

                sel = st.session_state["colmap"].get(file.name, [])
                sel = [c for c in sel if c in df.columns] or [df.columns[0]]

                if keep_mode.startswith("Keep & replace"):
                    out_df = df.copy()
                    for c in sel:
                        series = out_df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        out_df[c] = hash_series(to_hash, adv_hash)

                elif keep_mode.startswith("Keep all & add"):
                    out_df = df.copy()
                    sfx = suffix or f"_{adv_hash}"
                    for c in sel:
                        series = out_df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        out_df[f"{c}{sfx}"] = hash_series(to_hash, adv_hash)

                else:
                    cols = {}
                    for c in sel:
                        series = df[c]
                        to_hash = normalize_phone_series(series) if (adv_norm and looks_like_phone(series, c)) else series.astype(str).fillna("")
                        cols[f"{c}_{adv_hash}"] = hash_series(to_hash, adv_hash)
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
                st.download_button(label=f"Download {name}", data=data_bytes, file_name=name, mime="text/csv",
                                   key=f"dl-{name}", use_container_width=True)
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
    c_files = st.file_uploader("Upload file(s) to combine", type=["csv","tsv","txt","xlsx","xls","xlsb","parquet"],
                               accept_multiple_files=True, key="combine_uploader")
    drop_dupes = st.checkbox("Drop duplicate rows", value=True)
    add_source = st.checkbox("Add source filename column", value=False, help="Adds a 'source_filename' column.")
    c_fmt = st.selectbox("Output format", ["csv","parquet"], index=0)
    c_name = st.text_input("Combined file name", value="combined_output.csv")
    if c_fmt == "parquet" and not c_name.lower().endswith(".parquet"):
        c_name = c_name.rsplit(".", 1)[0] + ".parquet"

    def _coerce_to_single_hash(df: pd.DataFrame) -> pd.DataFrame:
        if add_source: return df
        if "hash" in df.columns: return df[["hash"]].copy()
        if df.shape[1] == 1: df2 = df.copy(); df2.columns = ["hash"]; return df2
        first = df.columns[0]
        if re.match(r"^Unnamed", str(first), flags=re.I): return df[[first]].rename(columns={first:"hash"})
        return df[[first]].rename(columns={first:"hash"})

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
                    try:
                        combined.to_parquet(pbuf, engine="pyarrow", index=False)
                    except Exception:
                        combined.to_parquet(pbuf, index=False)
                    pbuf.seek(0); data = pbuf.getvalue(); mime = "application/octet-stream"
                st.download_button(f"Download {c_name}", data=data, file_name=c_name, mime=mime, type="primary")
            else:
                st.error("No valid, non-empty files to combine.")

# ================ FOOTER =================
st.markdown(f"<div class='footer'><div class='footerwrap'>{COMPANY_NAME}</div></div>", unsafe_allow_html=True)
