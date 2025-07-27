import sys
import os

# ✅ Step 1: Ensure project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# ✅ Step 2: Imports
import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv

# ✅ Step 3: Load environment variables
load_dotenv()

# ✅ Step 4: Page configuration
st.set_page_config(
    page_title="Anime Recommender",
    page_icon="🎌",
    layout="centered"
)

# ✅ Step 5: Custom styling
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #f1f1f1;
        }
        .stTextInput > div > div > input {
            background-color: #262730;
            color: white;
        }
        .recommendation-card {
            background-color: #1e222d;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }
         .intro {
            background-color: #1e222d;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Step 6: Initialize the recommendation pipeline
@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline()

pipeline = init_pipeline()

# ✅ Step 7: UI layout
st.markdown("<h1 style='text-align: center; color: #ff4c4c;'>🎌 Anime Recommender System</h1>", unsafe_allow_html=True)
st.markdown("### Tell me what kind of anime you like 👇")

query = st.text_input("Enter your anime preferences (e.g., light-hearted anime with school settings)", "")

if query:
    with st.spinner("Thinking hard..."):
        try:
            result = pipeline.recommend(query)
            
            st.markdown("### 🎯 Recommendations")
            if isinstance(result, str):
                recs = result.strip().split("\n\n")
                x=len(recs)
                for i, rec in enumerate(recs, 1):
                    if i==x:
                       st.markdown(f"""
                       <div class='intro'>
                            <h4>Conclusion</h4>
                            <p>{rec.strip()}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    elif i==1:
                     st.markdown(f"""
                        <div class='intro'>
                            <h4>Introduction</h4>
                            <p>{rec.strip()}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    else:
                     st.markdown(f"""
                        <div class='recommendation-card'>
                            <h4>✨ Recommendation</h4>
                            <p>{rec.strip()}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Unexpected response format.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
