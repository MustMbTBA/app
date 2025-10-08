def load_df(file):
    """
    Robust reader for csv/tsv/txt/xlsx/parquet UploadedFile objects.
    - Auto-infers delimiter & encoding for text files.
    - Resets stream between attempts.
    - Detects XLSX content even if extension says .csv.
    - Falls back to headerless read when needed.
    """
    import pandas as pd, io, os, zipfile

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
    # Try increasingly lenient parses
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
                    # If headerless, give friendly column names
                    if header is None:
                        df.columns = [f"col_{i+1}" for i in range(df.shape[1])]
                    return df
            except Exception:
                continue

    # Final: if everything fails, surface a clear warning and return None
    try:
        _rewind()
    except Exception:
        pass
    st.warning(f"Could not read {getattr(file, 'name', 'file')}: unsupported format or empty content.")
    return None
