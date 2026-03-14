import os
import streamlit as st
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AyuSeva — Health & Fitness Planner",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ═══ Force ALL text dark ═══ */
    html, body, [class*="css"],
    .stApp, .stApp *,
    .stMarkdown, .stMarkdown *,
    p, span, label, div, li, td, th, h1, h2, h3, h4, h5, h6, a,
    input, select, textarea, option,
    [data-testid] *, [data-baseweb] * {
        color: #2D2B3D !important;
    }

    /* ═══ Background ═══ */
    .stApp {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(160deg, #FFF0F3 0%, #FDE2E9 40%, #FFF5F7 100%) !important;
    }
    .stApp > header { background: transparent !important; }

    /* ═══ Hide Streamlit chrome ═══ */
    #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

    /* ═══ Container ═══ */
    .main .block-container {
        max-width: 1000px;
        padding: 1.5rem 2rem 3rem;
    }

    /* ═══ Headings ═══ */
    h1 { color: #E8477E !important; font-weight: 800 !important; letter-spacing: -0.03em; }
    h2 { color: #2D2B3D !important; font-weight: 700 !important; font-size: 1.4rem !important; }
    h3 { color: #E8477E !important; font-weight: 600 !important; font-size: 1.1rem !important; }

    /* ═══ ALL Input Fields (number, text, select) ═══ */
    input[type="number"],
    input[type="text"],
    input[type="email"],
    input[type="password"],
    textarea,
    .stNumberInput input,
    .stTextInput input,
    [data-baseweb="input"] input,
    [data-baseweb="base-input"] input {
        color: #2D2B3D !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #F48FB1 !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        caret-color: #E8477E !important;
    }
    input:focus, textarea:focus {
        border-color: #E8477E !important;
        box-shadow: 0 0 0 3px rgba(232,71,126,0.12) !important;
    }
    /* Number input wrapper */
    .stNumberInput > div > div {
        background: #FFFFFF !important;
        border-radius: 10px !important;
    }
    /* Number input +/- buttons */
    .stNumberInput button {
        color: #E8477E !important;
        border-color: #F48FB1 !important;
        background: #FFF5F7 !important;
    }
    .stNumberInput button:hover {
        background: #FDE2E9 !important;
    }

    /* ═══ Select boxes ═══ */
    [data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border: 1.5px solid #F48FB1 !important;
        border-radius: 10px !important;
    }
    [data-baseweb="select"] span,
    [data-baseweb="select"] div {
        color: #2D2B3D !important;
    }
    /* Dropdown menu */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    ul[role="listbox"],
    ul[role="listbox"] li {
        background: #FFFFFF !important;
        color: #2D2B3D !important;
    }
    ul[role="listbox"] li:hover {
        background: #FDE2E9 !important;
    }

    /* ═══ Labels ═══ */
    .stNumberInput label, .stSelectbox label, .stTextInput label,
    [data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] p {
        color: #6B6880 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* ═══ Buttons ═══ */
    .stButton > button {
        background: linear-gradient(135deg, #E8477E, #F06292) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.65rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 16px rgba(232,71,126,0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #D63A6E, #E8477E) !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 24px rgba(232,71,126,0.4);
        transform: translateY(-2px);
    }
    .stButton > button:active {
        transform: translateY(0);
    }
    .stButton > button span, .stButton > button p {
        color: #FFFFFF !important;
    }

    /* ═══ Expander cards ═══ */
    div[data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid rgba(232,71,126,0.12);
        border-radius: 14px;
        box-shadow: 0 2px 16px rgba(232,71,126,0.06);
        overflow: hidden;
    }
    div[data-testid="stExpander"] summary span p {
        color: #E8477E !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }

    /* ═══ Alert boxes ═══ */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        font-size: 0.9rem;
    }
    /* info */
    div[data-baseweb="notification"][kind="info"],
    .stAlert div[role="alert"][data-baseweb] {
        background: #FFF0F3 !important;
        border-left: 4px solid #E8477E !important;
    }

    /* ═══ Spinner ═══ */
    .stSpinner > div > div {
        border-top-color: #E8477E !important;
    }

    /* ═══ Divider ═══ */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #F48FB1, transparent) !important;
        margin: 1.5rem 0 !important;
    }

    /* ═══ Columns gap ═══ */
    [data-testid="stHorizontalBlock"] {
        gap: 2rem;
    }

    /* ═══ Tab bar ═══ */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [aria-selected="true"] {
        color: #E8477E !important;
        border-bottom-color: #E8477E !important;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURATION ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GROQ_API_KEY and not GOOGLE_API_KEY:
    st.error("⚠️ No API keys found! Set GROQ_API_KEY or GOOGLE_API_KEY in environment variables.")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

try:
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Error configuring Google AI: {e}")


def call_llm(prompt, system_instruction=None):
    """Try Groq first, then Gemini as fallback. Returns text or raises."""
    # 1. Try Groq (primary)
    if groq_client:
        try:
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            err_str = str(e).lower()
            if '429' in str(e) or 'rate' in err_str or 'limit' in err_str:
                pass  # Fall through to Gemini
            else:
                pass  # Fall through to Gemini

    # 2. Fallback to Gemini
    if GOOGLE_API_KEY:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        ) if system_instruction else genai.GenerativeModel(model_name="gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text

    raise Exception("All AI models unavailable. Please try again later.")

# --- HELPER FUNCTIONS ---
def display_dietary_plan(plan_content):
    with st.expander("📋 Your Personalized Dietary Plan", expanded=True):
        col1, col2 = st.columns([2.2, 1])
        with col1:
            st.markdown("### 🎯 Why This Plan Works")
            st.info("High Protein, Healthy Fats, Moderate Carbs, and Caloric Balance tailored to your profile.")
            st.markdown("### 🍽️ Meal Plan")
            st.write(plan_content)
        with col2:
            st.markdown("### ⚠️ Key Reminders")
            st.warning("💧 Stay well-hydrated throughout the day")
            st.warning("⚡ Monitor electrolytes: Na, K, Mg")
            st.warning("🥬 Get fiber from vegetables & fruits")
            st.warning("👂 Adjust portions to how you feel")

def display_fitness_plan(plan_content):
    with st.expander("💪 Your Personalized Fitness Plan", expanded=True):
        col1, col2 = st.columns([2.2, 1])
        with col1:
            st.markdown("### 🎯 Your Goals")
            st.success("Build strength, improve endurance, and maintain overall fitness")
            st.markdown("### 🏋️‍♂️ Exercise Routine")
            st.write(plan_content)
        with col2:
            st.markdown("### 💡 Pro Tips")
            st.info("📊 Track your progress weekly")
            st.info("😴 Rest properly between workouts")
            st.info("🎯 Prioritize form over weight")
            st.info("📅 Consistency is key")

# --- MAIN APP ---
def main():
    if 'dietary_plan' not in st.session_state:
        st.session_state.dietary_plan = ""
        st.session_state.fitness_plan = ""
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False

    # ─── Hero Header ───
    st.markdown("""
        <div style="text-align:center; padding: 1rem 0 0.5rem;">
            <div style="font-size:3rem; margin-bottom:0.25rem;">🩺</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; margin-bottom:0.2rem;'>AyuSeva</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#6B6880 !important; font-size:1.05rem; margin-bottom:1.5rem;'>AI-Powered Health & Fitness Planner</p>", unsafe_allow_html=True)

    st.markdown("""
        <div style='
            background: #FFFFFF;
            padding: 1rem 1.3rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border-left: 4px solid #E8477E;
            box-shadow: 0 2px 12px rgba(232,71,126,0.06);
            font-size: 0.92rem;
            line-height: 1.6;
        '>
            Get <strong style="color:#E8477E !important;">personalized dietary and fitness plans</strong>
            tailored to your goals. Our AI analyzes your unique profile to create the perfect plan.
        </div>
    """, unsafe_allow_html=True)

    # ─── Profile Section ───
    st.markdown("---")
    st.markdown("## 👤 Your Profile")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        age = st.number_input("🎂 Age", min_value=10, max_value=100, step=1, value=25, help="Enter your age")
        height = st.number_input("📏 Height (cm)", min_value=100.0, max_value=250.0, step=0.1, value=170.0)
        activity_level = st.selectbox(
            "🏃 Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
            help="Choose your typical activity level"
        )
        dietary_preferences = st.selectbox(
            "🥗 Dietary Preferences",
            options=["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"],
            help="Select your dietary preference"
        )

    with col2:
        weight = st.number_input("⚖️ Weight (kg)", min_value=20.0, max_value=300.0, step=0.1, value=70.0)
        sex = st.selectbox("⚧ Sex", options=["Male", "Female", "Other"])
        fitness_goals = st.selectbox(
            "🎯 Fitness Goals",
            options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"],
            help="What do you want to achieve?"
        )

    st.markdown("---")

    if st.button("🩺 Generate My Personalized Plan", use_container_width=True):
        with st.spinner("✨ Creating your perfect health and fitness routine..."):
            try:
                user_profile = f"""
                Age: {age}
                Weight: {weight}kg
                Height: {height}cm
                Sex: {sex}
                Activity Level: {activity_level}
                Dietary Preferences: {dietary_preferences}
                Fitness Goals: {fitness_goals}
                """

                # Dietary Plan
                dietary_system = """You are a Dietary Expert.
                    Consider the user's dietary restrictions and preferences.
                    Suggest a highly concise, bulleted meal plan for the day (breakfast, lunch, dinner, snacks).
                    Explain briefly why the plan suits the user's goals.
                    Keep responses short, precise, and practical to save reading time."""
                st.session_state.dietary_plan = call_llm(user_profile, system_instruction=dietary_system)

                # Fitness Plan
                fitness_system = """You are a Fitness Expert.
                    Provide highly concise, bulleted exercises tailored to the user's goals.
                    Include a short warm-up, main workout, and cool-down.
                    Explain briefly the benefits of each exercise.
                    Make the plan actionable, precise, and short to save reading time."""
                st.session_state.fitness_plan = call_llm(user_profile, system_instruction=fitness_system)

            except Exception as e:
                st.session_state.plans_generated = False
                st.error("❌ The app is currently under maintenance. Please try again later.")

        if st.session_state.plans_generated:
            display_dietary_plan(st.session_state.dietary_plan)
            display_fitness_plan(st.session_state.fitness_plan)

    # ─── Q&A Section ───
    if st.session_state.plans_generated:
        st.markdown("---")
        st.markdown("## ❓ Questions About Your Plan?")
        question_input = st.text_input("What would you like to know?", placeholder="e.g., Can I substitute rice with quinoa?")

        if st.button("💬 Get Answer"):
            if question_input:
                with st.spinner("🔍 Finding the best answer..."):
                    context = f"Dietary Plan: {st.session_state.dietary_plan}\n\nFitness Plan: {st.session_state.fitness_plan}"
                    full_prompt = f"Context:\n{context}\n\nUser Question: {question_input}\nAnswer as a helpful health assistant."
                    try:
                        answer = call_llm(full_prompt)
                        st.session_state.qa_pairs.append((question_input, answer))
                    except Exception as e:
                        st.error("❌ The app is currently under maintenance. Please try again later.")

        if st.session_state.qa_pairs:
            st.markdown("---")
            st.markdown("## 💬 Q&A History")
            for q, a in st.session_state.qa_pairs:
                st.markdown(f"""
                    <div style="background:rgba(232,71,126,0.06); border-left:4px solid #E8477E;
                    padding:0.7rem 1rem; border-radius:0 10px 10px 0; margin-bottom:0.4rem;">
                    <strong style="color:#E8477E !important;">Q:</strong> {q}</div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div style="background:#FFFFFF; border-left:4px solid #F48FB1;
                    padding:0.7rem 1rem; border-radius:0 10px 10px 0; margin-bottom:1rem;
                    box-shadow:0 1px 6px rgba(0,0,0,0.04);">
                    <strong style="color:#E8477E !important;">A:</strong> {a}</div>
                """, unsafe_allow_html=True)

    # ─── Footer ───
    st.markdown("""
        <div style="text-align:center; padding:1.5rem 0 1rem; color:#9E9BB0 !important;
        font-size:0.8rem; margin-top:2rem; border-top:1px solid rgba(232,71,126,0.1);">
            Crafted by Ashish Kishore 🩺
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
