import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8002"

st.set_page_config(page_title="AI Fraud System", layout="wide")

st.title("🚨 AI Fraud Detection Dashboard")

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state["token"] = None


# ---------------- SIDEBAR ----------------
st.sidebar.header("🔐 Authentication")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")


# ---------------- REGISTER ----------------
if st.sidebar.button("Register"):
    try:
        res = requests.post(
            f"{API_URL}/register",
            params={"username": username, "password": password}
        )
        st.sidebar.json(res.json())
    except Exception as e:
        st.sidebar.error(str(e))


# ---------------- LOGIN ----------------
if st.sidebar.button("Login"):
    try:
        res = requests.post(
            f"{API_URL}/login",
            params={"username": username, "password": password}
        )

        if res.status_code == 200:
            st.session_state["token"] = res.json().get("access_token")
            st.sidebar.success("Login successful")
        else:
            st.sidebar.error("Login failed")

    except Exception as e:
        st.sidebar.error(str(e))


# ---------------- MAIN ----------------
col1, col2 = st.columns(2)


# ================= PREDICTION =================
with col1:
    st.subheader("🧠 Fraud Prediction")

    amount = st.number_input("Enter Transaction Amount", min_value=0)

    if st.button("Predict"):
        if not st.session_state["token"]:
            st.warning("Please login first")
        else:
            try:
                headers = {
                    "Authorization": f"Bearer {st.session_state['token']}"
                }

                res = requests.post(
                    f"{API_URL}/predict",
                    json={"amount": amount},
                    headers=headers
                )

                st.json(res.json())

            except Exception as e:
                st.error(str(e))


# ================= HISTORY =================
with col2:
    st.subheader("📊 Transaction History")

    if st.button("Load Data"):
        if not st.session_state["token"]:
            st.warning("Please login first")
        else:
            try:
                headers = {
                    "Authorization": f"Bearer {st.session_state['token']}"
                }

                res = requests.get(f"{API_URL}/history", headers=headers)

                data = res.json().get("history", [])

                df = pd.DataFrame(data)
                st.dataframe(df)

                # ---------------- CHARTS ----------------
                if not df.empty:

                    st.subheader("📈 Analytics")

                    # Pie Chart
                    fig1, ax1 = plt.subplots()
                    df["result"].value_counts().plot.pie(
                        autopct="%1.1f%%",
                        ax=ax1
                    )
                    ax1.set_ylabel("")
                    st.pyplot(fig1)

                    # Histogram
                    fig2, ax2 = plt.subplots()
                    df["amount"].plot(kind="hist", bins=10, ax=ax2)
                    st.pyplot(fig2)

            except Exception as e:
                st.error(str(e))