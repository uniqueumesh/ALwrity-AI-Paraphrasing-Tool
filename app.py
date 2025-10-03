import streamlit as st
import google.generativeai as genai
import os
import re
import html
import json
import streamlit.components.v1 as components
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Set page configuration with a custom theme to make checkboxes green
    st.set_page_config(
        page_title="AI Paraphrasing Tool",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Remove temporary theme overrides
    
    # Custom CSS styling (same as Alwrity)
    st.markdown("""
        <style>
        /* Set the primary color for checkboxes and other widgets */
        :root {
            --primary-color: #008000;
        }

        /* Reverted spacing overrides - back to default */

        ::-webkit-scrollbar-track {
        background: #e1ebf9;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }

        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }

        /* Force Streamlit checkbox to green */
        .stCheckbox [role="checkbox"] {
            box-shadow: 0 0 0 1px #008000 inset !important;
            border-color: #008000 !important;
        }
        .stCheckbox [role="checkbox"][aria-checked="true"] {
            background-color: rgba(0,128,0,0.12) !important;
            box-shadow: 0 0 0 1px #008000 inset !important;
            border-color: #008000 !important;
        }
        .stCheckbox [role="checkbox"] svg {
            color: #008000 !important;
            fill: #008000 !important;
            stroke: #008000 !important;
        }
        .stCheckbox [role="checkbox"] svg path {
            fill: #008000 !important;
            stroke: #008000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Enforce green checkbox via JS on rerenders
    components.html(f"""
    <script>
      (function() {{
        const GREEN = '#008000';
        function paint() {{
          document.querySelectorAll('.stCheckbox [role="checkbox"] svg').forEach(svg => {{
            svg.style.color = GREEN;
            svg.style.fill = GREEN;
            svg.style.stroke = GREEN;
            svg.querySelectorAll('path').forEach(p => {{
              try {{ p.setAttribute('fill', GREEN); p.setAttribute('stroke', GREEN); }} catch(e) {{}}
            }});
          }});
        }}
        const obs = new MutationObserver(paint);
        obs.observe(document.body, {{ subtree: true, childList: true, attributes: true }});
        window.addEventListener('load', paint);
        setTimeout(paint, 100);
      }})();
    </script>
    """, height=0)

    # Hide top header completely and remove reserved space
    hide_decoration_bar_style = '<style>[data-testid="stHeader"], header {display: none !important;} .stApp{padding-top:0 !important;} [data-testid="stAppViewContainer"]{padding-top:0 !important; margin-top:0 !important;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Header Section
    st.title("🔄 AI Paraphrasing Tool")

    # (BYOK removed) The app now uses a server-side key; no user API key input

    # Main Input Section (Expandable - Open by default)
    with st.expander("**PRO-TIP** - Enter your text and choose paraphrasing style for best results.", expanded=True):
        col1, col2 = st.columns([5, 5])

        with col1:
            input_text = st.text_area(
                '**📄 Enter your text to paraphrase**',
                placeholder="Type or paste your text here (maximum 800 words)...",
                help="Enter the text you want to paraphrase. Maximum 800 words allowed.",
                height=300
            )
            
            # Word count display
            word_count = count_words(input_text)
            if word_count > 0:
                if word_count > 800:
                    st.markdown(f'<p style="color: #ff6b6b; font-weight: bold;">⚠️ Word count: {word_count}/800 (exceeds limit)</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p style="color: #1976D2;">📊 Word count: {word_count}/800</p>', unsafe_allow_html=True)
            
        with col2:
            paraphrasing_style = st.selectbox(
                '🎨 Paraphrasing Style', 
                ('Balanced', 'Formal', 'Casual', 'Concise', 'Detailed'),
                index=0,
                help="Choose how you want the text to be paraphrased"
            )
            
            # Additional options
            st.markdown('<h4 style="color:#1976D2;">Additional Options</h4>', unsafe_allow_html=True)
            
            preserve_tone = st.checkbox(
                '🎯 Preserve Original Tone',
                value=True,
                help="Keep the original emotional tone of the text"
            )
            
            maintain_length = st.checkbox(
                '📏 Maintain Similar Length',
                value=True,
                help="Keep the paraphrased text similar in length to original"
            )
            
            # Paraphrase button on the right side below additional options
            st.markdown('<br>', unsafe_allow_html=True)
            paraphrase_clicked = st.button('**🔄 Paraphrase Text**', use_container_width=True)

    # Button logic moved outside the expander but still accessible
    if paraphrase_clicked:
        # Validation
        if not input_text.strip():
            st.error('**🫣 Please enter some text to paraphrase!**')
        elif word_count > 800:
            st.error('**⚠️ Text exceeds 800 words. Please shorten your text.**')
        else:
            with st.spinner("Paraphrasing your text..."):
                paraphrased_text = generate_paraphrase(
                    input_text, paraphrasing_style, None, preserve_tone, maintain_length
                )
                
                if paraphrased_text:
                    st.session_state['paraphrased_text'] = paraphrased_text
                else:
                    st.error("💥 **Failed to paraphrase text. Please try again!**")
                    if 'paraphrased_text' in st.session_state:
                        del st.session_state['paraphrased_text'] # Clear previous result on failure

    # Display the paraphrased text from session state if it exists
    if 'paraphrased_text' in st.session_state:
        st.markdown('<h4 style="margin-top:1.5rem; color:#1976D2;">✨ Paraphrased Text</h4>', unsafe_allow_html=True)
        
        paraphrased_text = st.session_state['paraphrased_text']
        # Safely escape the text for HTML display
        safe_text = html.escape(paraphrased_text)
        # Safely escape the text for JavaScript injection
        js_text = json.dumps(paraphrased_text)

        # Display the text inside a styled container
        st.markdown(f"""
        <div style="
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            color: #333;
        ">
            <pre style="
                font-family: inherit; 
                font-size: 16px;
                line-height: 1.6;
                color: inherit; 
                background: none; 
                border: none; 
                padding: 0; 
                margin: 0; 
                white-space: pre-wrap; 
                word-wrap: break-word;
            ">{safe_text}</pre>
        </div>
        """, unsafe_allow_html=True)
        
        # Implement a robust copy-to-clipboard button using components.html
        components.html(f"""
        <script>
        function copyToClipboard() {{
            const textToCopy = {js_text}; // Text is directly injected here
            navigator.clipboard.writeText(textToCopy).then(() => {{
                const copyButton = document.getElementById('copy-button');
                copyButton.innerText = 'Copied!';
                setTimeout(() => {{
                    copyButton.innerText = '📋 Copy Text';
                }}, 2000);
            }}, (err) => {{
                console.error('Failed to copy text: ', err);
                alert('Failed to copy text. Your browser might not support this feature or requires permissions.');
            }});
        }}
        </script>
        
        <button id="copy-button" onclick="copyToClipboard()" style="
            background: #1565C0;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
            transition: background-color 0.3s ease;
        ">📋 Copy Text</button>
        """, height=60)

def count_words(text):
    """Count words in the given text"""
    if not text.strip():
        return 0
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def generate_paraphrase(text, style, api_key=None, preserve_tone=True, maintain_length=True):
    """Generate paraphrased text using Gemini"""
    try:
        # Get API key
        gemini_api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            st.error("GEMINI_API_KEY is missing. Please provide it in the API Configuration section or set it in the environment.")
            return None
        
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        
        # Create prompt based on style and options
        style_prompts = {
            'Balanced': 'Paraphrase this text naturally while keeping the same meaning:',
            'Formal': 'Rewrite this text in a formal, professional tone:',
            'Casual': 'Rewrite this text in a casual, conversational style:',
            'Concise': 'Make this text shorter and more direct:',
            'Detailed': 'Expand this text with more detail:'
        }
        
        prompt = style_prompts[style]
        
        if preserve_tone:
            prompt += " Maintain the original emotional tone."
        if maintain_length:
            prompt += " Keep the length similar to the original."
        
        prompt += f"\n\n{text}"
        
        # Generate content
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        if 'quota' in str(e).lower() or 'rate limit' in str(e).lower():
            st.warning('⚠️ Gemini API rate limit or quota exceeded. Please try again later or use a different API key.')
        else:
            st.error(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    main()
