import re
import pandas as pd
import io

def redact_pii(text):
    """Redacts emails and phone numbers."""
    if not isinstance(text, str):
        return text
    
    # Email regex
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', text)
    
    # Phone regex (simple)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[REDACTED_PHONE]', text)
    
    return text

def convert_df(df, format):
    if format == "csv":
        return df.to_csv(index=False).encode('utf-8')
    elif format == "json":
        return df.to_json(orient="records").encode('utf-8')
    elif format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()
    return None
