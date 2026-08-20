import streamlit as st
import os

from groq import Groq
from langchain_groq import ChatGroq


st.title("🔍 Groq Debugging")


# ============================================================
# 1. Check Streamlit Secret
# ============================================================

st.header("1️⃣ Checking GROQ_API_KEY")

try:
    api_key = st.secrets["GROQ_API_KEY"]

    st.success("✅ GROQ_API_KEY found in Streamlit Secrets")

    # NEVER display the complete key
    st.write("Key exists:", bool(api_key))
    st.write("Key prefix:", api_key[:7] + "..." if api_key else "None")

except Exception as e:

    st.error("❌ Could not read GROQ_API_KEY")

    st.exception(e)

    st.stop()


# ============================================================
# 2. Test Groq Client
# ============================================================

st.header("2️⃣ Testing Groq API")

try:

    client = Groq(
        api_key=api_key
    )

    st.success("✅ Groq client created successfully")

except Exception as e:

    st.error("❌ Failed to create Groq client")

    st.exception(e)

    st.stop()


# ============================================================
# 3. Get Available Models
# ============================================================

st.header("3️⃣ Checking Available Models")

try:

    models = client.models.list()

    model_names = [
        model.id
        for model in models.data
    ]

    st.success(
        f"✅ Groq returned {len(model_names)} models"
    )

    st.write(model_names)

    target_model = "llama-3.1-8b-instant"

    if target_model in model_names:

        st.success(
            f"✅ {target_model} is available"
        )

    else:

        st.error(
            f"❌ {target_model} is NOT available for this API key"
        )

except Exception as e:

    st.error("❌ Failed to retrieve Groq models")

    st.exception(e)

    st.stop()


# ============================================================
# 4. Direct Groq API Test
# ============================================================

st.header("4️⃣ Testing Direct Groq API")

try:

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence."
            }
        ],

        temperature=0

    )

    answer = response.choices[0].message.content

    st.success("✅ Direct Groq API call worked")

    st.write("Response:")
    st.write(answer)

except Exception as e:

    st.error("❌ Direct Groq API call FAILED")

    st.exception(e)


# ============================================================
# 5. Test LangChain ChatGroq
# ============================================================

st.header("5️⃣ Testing LangChain ChatGroq")

try:

    llm = ChatGroq(

        groq_api_key=api_key,

        model="llama-3.1-8b-instant",

        temperature=0,

        max_tokens=100

    )

    st.success("✅ ChatGroq object created")

    response = llm.invoke(
        "Say hello in one sentence."
    )

    st.success("✅ LangChain ChatGroq call worked")

    st.write("Response:")
    st.write(response.content)

except Exception as e:

    st.error("❌ LangChain ChatGroq call FAILED")

    st.exception(e)


# ============================================================
# 6. Environment Variable Check
# ============================================================

st.header("6️⃣ Environment Variable Check")

env_key = os.getenv("GROQ_API_KEY")

if env_key:

    st.success(
        "✅ GROQ_API_KEY also exists as environment variable"
    )

    st.write(
        "Environment key prefix:",
        env_key[:7] + "..."
    )

else:

    st.warning(
        "⚠️ GROQ_API_KEY is NOT available through os.getenv()"
    )

st.info(
    "This is okay if st.secrets works. "
    "For Streamlit Cloud, we are directly using st.secrets."
)
