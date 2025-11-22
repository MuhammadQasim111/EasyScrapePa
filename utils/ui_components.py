import streamlit as st
import streamlit.components.v1 as components

def visual_selector_component(html_content):
    """
    A custom component to render HTML and allow element selection.
    This is a simplified version using an iframe and JS injection.
    """
    # Escape backticks and other chars for JS string
    safe_html = html_content.replace("`", "\`").replace("${", "\${")
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; }}
            *:hover {{ outline: 2px solid #ff0000 !important; cursor: crosshair; }}
            .highlighted {{ outline: 2px solid #00ff00 !important; background-color: rgba(0, 255, 0, 0.1); }}
        </style>
    </head>
    <body>
        <div id="content">{safe_html}</div>
        <script>
            document.addEventListener('click', function(e) {{
                e.preventDefault();
                e.stopPropagation();
                
                // Remove previous highlights
                document.querySelectorAll('.highlighted').forEach(el => el.classList.remove('highlighted'));
                
                // Highlight clicked
                e.target.classList.add('highlighted');
                
                // Generate selector (simplified)
                let path = [];
                let el = e.target;
                while (el && el.id !== 'content') {{
                    let selector = el.tagName.toLowerCase();
                    if (el.id) {{
                        selector += '#' + el.id;
                        path.unshift(selector);
                        break;
                    }} else {{
                        let sib = el, nth = 1;
                        while (sib = sib.previousElementSibling) {{
                            if (sib.tagName.toLowerCase() == selector) nth++;
                        }}
                        if (nth != 1) selector += ":nth-of-type("+nth+")";
                    }}
                    path.unshift(selector);
                    el = el.parentElement;
                }}
                
                // Send back to Streamlit (simulated via console for now as full bi-directional is complex without custom component build)
                console.log("Selected:", path.join(" > "));
                // In a real custom component, we would use Streamlit.setComponentValue(path.join(" > "))
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600, scrolling=True)
    st.info("Visual Selector: Click elements in the preview above. (Note: Bi-directional communication requires a compiled component, so manually copy the selector logic for now or use browser dev tools).")

def render_dashboard_stats(history):
    total_scrapes = len(history)
    success_rate = len([h for h in history if h.get("success")]) / total_scrapes if total_scrapes > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scrapes", total_scrapes)
    col2.metric("Success Rate", f"{success_rate:.1%}")
    col3.metric("Last Run", history[0]["timestamp"][:16] if history else "N/A")
