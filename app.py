from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).parent
MASTER = ROOT / "data" / "processed" / "phonepe_pulse_master.csv"
st.set_page_config(page_title="PhonePe Pulse Analytics", page_icon="📱", layout="wide")

@st.cache_data
def load_master():
    return pd.read_csv(MASTER) if MASTER.exists() else pd.DataFrame()

master = load_master()
st.title("PhonePe Pulse | India Payments Explorer")
st.caption("One consolidated master CSV · six preserved source datasets · 2018–2022")
if master.empty:
    st.error("Master file missing. Add data/processed/phonepe_pulse_master.csv from the project package.")
    st.stop()

def source(name):
    return master.loc[master.source_dataset.eq(name)].copy()

tx, au = source("aggregated_transaction"), source("aggregated_user")
mtx, mu = source("map_transaction"), source("map_user")
tt, tu = source("top_transaction"), source("top_user")

with st.sidebar:
    st.header("Filters")
    years = sorted(master.year.dropna().astype(int).unique())
    year = st.selectbox("Year", ["All"] + years)
    quarter = st.selectbox("Quarter", ["All", 1, 2, 3, 4])
    states = sorted(master.state.dropna().astype(str).unique())
    state = st.selectbox("State", ["All"] + states)
    top_n = st.selectbox("Ranking size", [5, 10, 15, 20], index=1)

def filtered(df):
    d = df.copy()
    if year != "All": d = d[d.year.eq(int(year))]
    if quarter != "All": d = d[d.quarter.eq(int(quarter))]
    if state != "All": d = d[d.state.eq(state)]
    return d

txf, auf, mtxf, muf = map(filtered, [tx, au, mtx, mu])
value = pd.to_numeric(txf.transaction_amount, errors="coerce").sum()
count = pd.to_numeric(txf.transaction_count, errors="coerce").sum()
latest = muf[["year","quarter"]].dropna().sort_values(["year","quarter"]).tail(1)
users = 0
if not latest.empty:
    y, q = latest.iloc[0]
    users = pd.to_numeric(muf.loc[muf.year.eq(y) & muf.quarter.eq(q), "registered_user_count"], errors="coerce").sum()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Transaction value", f"₹{value/1e12:.3f} tn")
c2.metric("Transaction count", f"{count/1e7:.3f} cr")
c3.metric("Registered users", f"{users/1e7:.3f} cr")
c4.metric("Average transaction value", f"₹{value/count:,.0f}" if count else "—")

tabs = st.tabs(["Executive overview","Transaction analysis","User & devices","Geography & rankings","Data quality"])
with tabs[0]:
    st.subheader("Quarterly transaction trend")
    trend = txf.groupby(["year","quarter"], as_index=False).agg(value=("transaction_amount","sum"), count=("transaction_count","sum"))
    if not trend.empty:
        trend["period"] = trend.year.astype(int).astype(str) + " Q" + trend.quarter.astype(int).astype(str)
        st.plotly_chart(px.line(trend, x="period", y="value", markers=True), use_container_width=True)
    cats = txf.groupby("transaction_type", as_index=False).transaction_amount.sum()
    if not cats.empty: st.plotly_chart(px.pie(cats, names="transaction_type", values="transaction_amount", hole=.45), use_container_width=True)
with tabs[1]:
    a,b = st.columns(2)
    cat = txf.groupby("transaction_type", as_index=False).transaction_amount.sum().sort_values("transaction_amount")
    if not cat.empty: a.plotly_chart(px.bar(cat, x="transaction_amount", y="transaction_type", orientation="h", title="Value by transaction category"), use_container_width=True)
    stx = txf.groupby("state", as_index=False).transaction_amount.sum().nlargest(top_n,"transaction_amount").sort_values("transaction_amount")
    if not stx.empty: b.plotly_chart(px.bar(stx, x="transaction_amount", y="state", orientation="h", title="Leading states"), use_container_width=True)
    st.subheader("District transaction records")
    district = mtxf.groupby(["state","district"], as_index=False).transaction_amount.sum().nlargest(top_n,"transaction_amount")
    st.dataframe(district, use_container_width=True, hide_index=True)
with tabs[2]:
    a,b = st.columns(2)
    reg = muf.groupby("state", as_index=False).registered_user_count.sum().nlargest(top_n,"registered_user_count")
    dev = auf.groupby("device_brand", as_index=False).device_user_count.sum().nlargest(12,"device_user_count")
    if not reg.empty: a.plotly_chart(px.bar(reg, x="registered_user_count", y="state", orientation="h", title="Registered users by state"), use_container_width=True)
    if not dev.empty: b.plotly_chart(px.bar(dev, x="device_user_count", y="device_brand", orientation="h", title="Device brand distribution"), use_container_width=True)
with tabs[3]:
    st.subheader("State / district transaction hierarchy")
    geo = mtxf.groupby(["state","district"], as_index=False).transaction_amount.sum()
    if not geo.empty: st.plotly_chart(px.treemap(geo, path=["state","district"], values="transaction_amount"), use_container_width=True)
    st.subheader("Top-user extract")
    st.dataframe(filtered(tu).nlargest(top_n,"registered_user_count"), use_container_width=True, hide_index=True)
    st.subheader("Top-transaction extract")
    st.dataframe(filtered(tt).nlargest(top_n,"transaction_amount"), use_container_width=True, hide_index=True)
with tabs[4]:
    inventory = master.groupby("source_dataset").size().rename("rows").reset_index()
    st.metric("Total master rows", f"{len(master):,}")
    st.metric("Source sections", master.source_dataset.nunique())
    st.dataframe(inventory, use_container_width=True, hide_index=True)
    st.download_button("Download consolidated master CSV", master.to_csv(index=False).encode(), "phonepe_pulse_master.csv", "text/csv")
    st.markdown("""
    **Methodology safeguards**
    - Master is a vertical append/union, not a side-by-side join.
    - source_dataset preserves each source identity and analytical grain.
    - Aggregated and district transaction data are not added together.
    - Registered users are snapshots; use the latest selected period, not a sum across quarters.
    - Top lists are ranking extracts, not additive totals.
    - Transaction value is not PhonePe corporate revenue.
    - Only supplied 2018–2022 data is used. No outside data or APIs are accessed.
    - No coordinates or boundary geometries are supplied; the treemap is not a choropleth.
    """)
