from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "processed"
st.set_page_config(page_title="PhonePe Pulse | Payments Explorer", page_icon="📱", layout="wide")

st.markdown("""
<style>
.block-container {padding-top:1.25rem; padding-bottom:2rem;}
[data-testid="stMetric"] {background:#17132b;border:1px solid #392e5d;padding:13px;border-radius:12px;}
[data-testid="stSidebar"] {background:#11101b;}
h1,h2,h3 {letter-spacing:-.025em;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load(name):
    p = DATA / name
    return pd.read_csv(p) if p.exists() else pd.DataFrame()

tx = load("aggregated_transaction.csv")
atop = load("top_transaction.csv")
mtx = load("map_transaction.csv")
au = load("aggregated_user.csv")
utop = load("top_user.csv")
mu = load("map_user.csv")

required = [tx, atop, mtx, au, utop, mu]
if any(d.empty for d in required):
    st.error("One or more supplied dataset files are missing from data/processed/. See README.md.")
    st.stop()

for d in required:
    for c in ("year","quarter"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    if "states" in d: d["states"] = d["states"].fillna("Unknown").astype(str)
    if "district" in d: d["district"] = d["district"].fillna("Unknown").astype(str)

st.title("PhonePe Pulse | India Payments Explorer")
st.caption("Interactive analysis of the six supplied CSV datasets · 2018–2022 · Aggregated and anonymised records")
st.info("This project uses only the six CSV files supplied with the assignment. It does not fetch or append any external data. Transaction value is payment value, not PhonePe revenue.")

years = sorted(tx.year.dropna().astype(int).unique().tolist())
states = sorted(set(tx.states) | set(mu.states))
types = sorted(tx.trans_type.dropna().astype(str).unique().tolist())
brands = sorted(au.brand.dropna().astype(str).unique().tolist())
districts = sorted(set(mtx.district.dropna().astype(str)) | set(mu.district.dropna().astype(str)))

with st.sidebar:
    st.header("Interactive filters")
    fy = st.selectbox("1 · Year", ["All"] + years)
    fq = st.selectbox("2 · Quarter", ["All", 1, 2, 3, 4])
    fs = st.selectbox("3 · State", ["All"] + states)
    fd = st.selectbox("4 · District", ["All"] + districts)
    ft = st.selectbox("5 · Transaction category", ["All"] + types)
    fb = st.selectbox("6 · Device brand", ["All"] + brands)
    metric = st.selectbox("7 · Primary measure", ["Transaction value", "Transaction count", "Registered users", "Device users"])
    growth_period = st.selectbox("8 · Growth comparison", ["YoY", "QoQ"])
    rank_n = st.selectbox("9 · Ranking size", [5, 10, 15, 20], index=1)
    geo_level = st.selectbox("10 · Geographic level", ["State", "District"])
    chart_view = st.selectbox("11 · Chart style", ["Trend", "Category mix", "Rankings"])
    st.caption("Selections filter the relevant datasets. A filter is ignored where that dimension is not present in a source file.")

def filt(df, has_type=False, has_brand=False):
    d = df.copy()
    if fy != "All": d = d[d.year == int(fy)]
    if fq != "All": d = d[d.quarter == int(fq)]
    if fs != "All": d = d[d.states == fs]
    if fd != "All" and "district" in d: d = d[d.district == fd]
    if has_type and ft != "All": d = d[d.trans_type == ft]
    if has_brand and fb != "All": d = d[d.brand == fb]
    return d

txf = filt(tx, has_type=True)
mtxf = filt(mtx)
auf = filt(au, has_brand=True)
muf = filt(mu)
tuf = filt(utop)
ttf = filt(atop)

def number(df, col):
    return pd.to_numeric(df[col], errors="coerce").fillna(0).sum() if col in df else 0

# Transactions: category aggregated dataset is the source of total value/count.
# District filters cannot be applied to this table; use map/top transaction data for district-level views.
transaction_value = number(txf, "amount")
transaction_count = number(txf, "trans_counts")

# User snapshots: show latest selected period, never sum all quarterly snapshots.
def latest_snapshot(frame, col):
    d = frame.copy()
    if d.empty: return 0, None
    if "year" in d and "quarter" in d:
        periods = d[["year","quarter"]].dropna().drop_duplicates().sort_values(["year","quarter"])
        if not periods.empty:
            y, q = periods.iloc[-1]
            d = d[(d.year == y) & (d.quarter == q)]
            return number(d, col), (int(y), int(q))
    return number(d, col), None

user_total, user_period = latest_snapshot(muf, "registered_user_counts")
device_total, _ = latest_snapshot(auf, "user_counts")

# Latest period on user map; top users are a distinct top-list extract, not additive to map.
merchant_placeholder = "Not supplied"
avg_ticket = transaction_value / transaction_count if transaction_count else 0

st.markdown("### Key performance indicators")
k1,k2,k3,k4 = st.columns(4)
k1.metric("Transaction value", f"₹{transaction_value/1e12:.3f} tn")
k2.metric("Transaction count", f"{transaction_count/1e7:.3f} cr")
k3.metric("Registered users", f"{user_total/1e7:.3f} cr", help="Latest available selected period from map_user.csv; district records summed once for that period.")
k4.metric("Average transaction value", f"₹{avg_ticket:,.0f}")

tabs = st.tabs(["Executive overview", "Transaction analysis", "User & device analysis", "Geography & rankings", "Data quality & methodology"])

with tabs[0]:
    left, right = st.columns([1.15,1])
    with left:
        st.subheader("Transaction value trend")
        trend = txf.groupby(["year","quarter"], as_index=False).agg(value=("amount","sum"), count=("trans_counts","sum"))
        if not trend.empty:
            trend["period"] = trend.year.astype(int).astype(str) + " Q" + trend.quarter.astype(int).astype(str)
            col = "value" if metric == "Transaction value" else "count"
            fig = px.line(trend, x="period", y=col, markers=True, title=f"Quarterly {metric.lower()}")
            st.plotly_chart(fig, use_container_width=True)
        else: st.warning("No transaction observations match the selected filters.")
    with right:
        st.subheader("Transaction category mix")
        cats = txf.groupby("trans_type", as_index=False).agg(value=("amount","sum"), count=("trans_counts","sum"))
        if not cats.empty:
            fig = px.pie(cats, names="trans_type", values="value", hole=.48, title="Share of transaction value")
            st.plotly_chart(fig, use_container_width=True)
        else: st.info("No category observations for this selection.")
    st.subheader("Quick interpretation")
    st.write(f"The current selection contains **{len(txf):,} category-period-state records**. KPI user count is a latest-period snapshot, not a sum across quarters.")
    st.caption("If a district is selected, transaction KPIs use district-level map_transaction records only in the geography tab; category-level transaction totals remain state/category data.")

with tabs[1]:
    st.subheader("Transaction intelligence")
    a,b = st.columns(2)
    with a:
        cat = txf.groupby("trans_type", as_index=False).agg(value=("amount","sum"))
        if not cat.empty: st.plotly_chart(px.bar(cat.sort_values("value"), x="value", y="trans_type", orientation="h", title="Value by transaction category"), use_container_width=True)
    with b:
        state_tx = txf.groupby("states", as_index=False).agg(value=("amount","sum"), count=("trans_counts","sum")).nlargest(rank_n,"value")
        if not state_tx.empty: st.plotly_chart(px.bar(state_tx.sort_values("value"), x="value", y="states", orientation="h", title=f"Top {rank_n} states by value"), use_container_width=True)
    st.subheader("Year-on-year / quarter-on-quarter growth")
    # Growth from complete quarterly state/category totals, using selected state/category scope.
    g = filt(tx, has_type=True)
    if fs != "All": g = g[g.states == fs]
    if ft != "All": g = g[g.trans_type == ft]
    if fd != "All": st.caption("District selection does not apply to aggregated category data; growth below remains at state/category grain.")
    g = g.groupby(["year","quarter"], as_index=False).agg(value=("amount","sum"), count=("trans_counts","sum")).sort_values(["year","quarter"])
    if not g.empty:
        g["period"] = g.year.astype(int).astype(str) + " Q" + g.quarter.astype(int).astype(str)
        lag = 4 if growth_period == "YoY" else 1
        g["value_growth_pct"] = g.value.pct_change(lag)*100
        g["count_growth_pct"] = g["count"].pct_change(lag)*100
        st.dataframe(g[["period","value","count","value_growth_pct","count_growth_pct"]].tail(16), use_container_width=True, hide_index=True)
        st.caption(f"{growth_period} growth compares like-for-like quarters (lag {lag}) or adjacent quarters (lag 1). First periods without a comparison are blank.")
    st.subheader("District transaction rankings")
    dtx = mtxf.groupby(["states","district"], as_index=False).agg(value=("amount","sum"), count=("trans_counts","sum")).sort_values("value",ascending=False).head(rank_n)
    st.dataframe(dtx, use_container_width=True, hide_index=True)

with tabs[2]:
    l,r = st.columns(2)
    with l:
        st.subheader("Registered users by state")
        us = muf.groupby("states",as_index=False).registered_user_counts.sum().nlargest(rank_n,"registered_user_counts")
        if not us.empty: st.plotly_chart(px.bar(us.sort_values("registered_user_counts"), x="registered_user_counts", y="states", orientation="h"), use_container_width=True)
    with r:
        st.subheader("Device brand distribution")
        dev = auf.groupby("brand",as_index=False).user_counts.sum().nlargest(12,"user_counts")
        if not dev.empty: st.plotly_chart(px.bar(dev.sort_values("user_counts"), x="user_counts", y="brand", orientation="h"), use_container_width=True)
    st.subheader("Device brand share")
    if not dev.empty:
        st.plotly_chart(px.pie(dev, names="brand", values="user_counts", hole=.5), use_container_width=True)
    st.caption("Device user counts are the values supplied in aggregated_user.csv. They should not be described as unique active users unless the source definition supports that interpretation.")

with tabs[3]:
    st.subheader("Geographic exploration")
    if geo_level == "State":
        geo = mtxf.groupby("states",as_index=False).agg(value=("amount","sum"), count=("trans_counts","sum"))
        title = "State-level transaction value"
        loc = "states"
    else:
        geo = mtxf.groupby(["states","district"],as_index=False).agg(value=("amount","sum"), count=("trans_counts","sum"))
        title = "District-level transaction value"
        loc = "district"
    if not geo.empty:
        # Hierarchical treemap is built only from supplied state/district labels; no external boundary files are used.
        if geo_level == "District":
            fig = px.treemap(geo, path=["states","district"], values="value", color="value",
                             title="Geographic hierarchy — district transaction value")
        else:
            fig = px.treemap(geo, path=["states"], values="value", color="value",
                             title="State transaction value distribution")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("This is a hierarchical geographic treemap, not a latitude/longitude map or boundary choropleth. The supplied CSVs contain names and measures, but no coordinates or polygon geometries.")
        sortcol = "value" if metric in ["Transaction value","Device users"] else "count"
        st.dataframe(geo.sort_values(sortcol,ascending=False).head(rank_n), use_container_width=True, hide_index=True)
    st.subheader("Supplied top-user dataset")
    topu = tuf.sort_values("registered_user_counts",ascending=False).head(rank_n)
    st.dataframe(topu, use_container_width=True, hide_index=True)
    st.subheader("Supplied top-transaction dataset")
    topt = ttf.sort_values("amount",ascending=False).head(rank_n)
    st.dataframe(topt, use_container_width=True, hide_index=True)

with tabs[4]:
    st.subheader("Dataset inventory")
    inventory = pd.DataFrame([
        ["aggregated_transaction.csv",len(tx),"State × year × quarter × transaction category","trans_counts, amount"],
        ["aggregated_user.csv",len(au),"State × year × quarter × device brand","user_counts, percentage"],
        ["map_transaction.csv",len(mtx),"State × year × quarter × district","trans_counts, amount"],
        ["map_user.csv",len(mu),"State × year × quarter × district","registered_user_counts"],
        ["top_transaction.csv",len(atop),"Top transaction district extract","trans_counts, amount"],
        ["top_user.csv",len(utop),"Top user district extract","registered_user_counts"],
    ],columns=["File","Rows","Grain / dimensions","Measures"])
    st.dataframe(inventory,use_container_width=True,hide_index=True)
    st.markdown("""
    **Data interpretation rules**
    - The six supplied CSVs are the exclusive data source for this dashboard.
    - Transaction value is the value of payments represented in the dataset; it is not PhonePe's corporate revenue.
    - map_transaction.csv and aggregated_transaction.csv are different grains. Do not add them together.
    - map_user.csv contains district-level registered-user observations. The KPI uses the selected latest quarter, not the sum of quarterly snapshots.
    - top_user.csv and top_transaction.csv are separate top-list extracts and should be used for ranking, not added to map totals.
    - The files cover 2018–2022 in the supplied copy. No newer periods are inferred.
    - A true geographic boundary map cannot be constructed from these CSVs alone because they contain no latitude/longitude coordinates or boundary geometries. The treemap provides an interactive state/district hierarchy without importing external geographic data.
    """)
    st.download_button("Download filtered transaction-category data", txf.to_csv(index=False).encode(), "filtered_aggregated_transaction.csv", "text/csv")
    st.download_button("Download filtered district transaction data", mtxf.to_csv(index=False).encode(), "filtered_map_transaction.csv", "text/csv")
