
import os
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Vireo Support Audit", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TICKETS = os.path.join(DATA_DIR, "tickets.csv")

@st.cache_data
def load_data():
    t = pd.read_csv(TICKETS)
    t["created_dt"] = pd.to_datetime(t["created_at"], errors="coerce")
    for c in ["first_response_at","resolved_at"]:
        t[c+"_dt"] = pd.to_datetime(t[c], errors="coerce")
    # Brief's stated reporting window.
    t = t[(t.created_dt >= "2025-01-01") & (t.created_dt < "2026-07-01")].copy()
    t["model_text"] = t["customer_message"].fillna("") + " " + t["agent_notes"].fillna("")
    return t

@st.cache_resource
def train_model(texts, labels):
    vec = FeatureUnion([
        ("word", TfidfVectorizer(ngram_range=(1,2), min_df=2, max_features=50000, sublinear_tf=True)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(3,5), min_df=2, max_features=50000, sublinear_tf=True))
    ])
    X = vec.fit_transform(texts)
    clf = LogisticRegression(max_iter=1000, C=3, class_weight="balanced")
    clf.fit(X, labels)
    return vec, clf

t = load_data()
vec, clf = train_model(tuple(t.model_text.tolist()), tuple(t.category.tolist()))

def predict(texts):
    X = vec.transform(texts)
    p = clf.predict_proba(X)
    idx = p.argmax(axis=1)
    return clf.classes_[idx], p.max(axis=1)

st.title("Vireo Audio — Support Ticket Audit")
st.caption("AI-assisted category cleanup + monthly volume/routing audit | Reporting window: Jan 2025–Jun 2026")

pred, conf = predict(t.model_text.tolist())
t["ai_category"] = pred
t["ai_confidence"] = conf

# Policy ownership mapping
frontline = {"chat":"Chat Frontline","email":"Email Frontline","voice":"Voice Frontline","social":"Chat Frontline"}
special = {
    "Billing & Payments":"Billing",
    "Delivery & Shipping":"Logistics",
    "Returns & Refunds":"Returns Desk",
    "Warranty & Repair":"Escalations & Warranty",
}
def owner(cat, channel):
    return special.get(cat, frontline.get(channel))
t["ai_owner"] = [owner(c,ch) for c,ch in zip(t.ai_category,t.channel)]
t["current_owner"] = [owner(c,ch) for c,ch in zip(t.category,t.channel)]

tab1, tab2, tab3 = st.tabs(["Overview", "Monthly breakdown", "Categorize a ticket"])

with tab1:
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Tickets in window", f"{len(t):,}")
    c2.metric("Existing 'Other'", f"{(t.category=='Other').mean():.1%}")
    c3.metric("AI 'Other'", f"{(t.ai_category=='Other').mean():.1%}")
    c4.metric("Low-confidence reviews", f"{(t.ai_confidence<0.60).sum():,}")

    st.subheader("Category volume: existing tag vs AI-assisted")
    cat = pd.DataFrame({"Existing tag":t.category.value_counts(), "AI category":t.ai_category.value_counts()}).fillna(0).sort_values("Existing tag",ascending=False)
    st.bar_chart(cat)

    st.subheader("Potential routing review")
    mismatch = t[t.ai_owner != t.assigned_team].copy()
    st.write(f"{len(mismatch):,} tickets ({len(mismatch)/len(t):.1%}) have an AI-inferred owner different from the first-routed team. This is a review signal, not a claim that every case is wrong.")
    st.dataframe(mismatch[["ticket_id","created_at","channel","category","ai_category","ai_confidence","assigned_team","customer_message"]].sort_values("ai_confidence").head(100), use_container_width=True)

with tab2:
    month = t.assign(month=t.created_dt.dt.to_period("M").astype(str))
    st.subheader("Monthly volume by AI category")
    mc = month.pivot_table(index="month",columns="ai_category",values="ticket_id",aggfunc="count",fill_value=0)
    st.line_chart(mc)
    st.subheader("Monthly volume by first-assigned team")
    mt = month.pivot_table(index="month",columns="assigned_team",values="ticket_id",aggfunc="count",fill_value=0)
    st.line_chart(mt)

with tab3:
    st.subheader("Classify a new ticket")
    msg = st.text_area("Customer opening message", height=150, placeholder="Example: I paid twice for order VR123456...")
    note = st.text_area("Optional closing note", height=100)
    if st.button("Categorize"):
        if not msg.strip() and not note.strip():
            st.warning("Enter a customer message or closing note.")
        else:
            pc, pp = predict([msg+" "+note])
            st.success(f"Suggested category: **{pc[0]}**")
            st.write(f"Model confidence: **{pp[0]:.0%}**")
            if pp[0] < .60:
                st.warning("Low confidence — send this ticket to human review rather than auto-routing it.")

st.divider()
st.caption("Important: the model is trained on historical category tags, so its holdout score measures agreement with the historical tagging process, not ground-truth correctness. Low-confidence and routing-mismatch cases are deliberately surfaced for review.")
