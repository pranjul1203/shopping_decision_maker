import streamlit as st
from shopwise.database import init_db, save_search, get_history, save_snapshot, get_snapshots
from shopwise.agents import ShoppingAgent
from shopwise.config import get_secret

st.set_page_config(page_title="ShopWise AI", page_icon="🛍️", layout="wide")
init_db()
agent = ShoppingAgent()
st.markdown("""<style>
.hero{padding:24px;border-radius:18px;border:1px solid rgba(128,128,128,.25);margin-bottom:18px}
.badge{display:inline-block;padding:5px 10px;border-radius:999px;border:1px solid rgba(128,128,128,.35);font-size:12px}
.decision{padding:18px;border-radius:16px;border:1px solid rgba(128,128,128,.3);margin:10px 0}
</style>""", unsafe_allow_html=True)

st.markdown("""<div class="hero"><span class="badge">LIVE MARKET • AI DECISION AGENT</span>
<h1>🛍️ ShopWise</h1><p>Don't just find products. Decide what you should buy.</p></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")
    api_key=get_secret("SERPAPI_KEY")
    st.success("Live shopping API configured") if api_key else st.warning("Add SERPAPI_KEY to enable live search.")
    page=st.radio("Workspace",["Decision Agent","Should I Buy?","Price Tracker","History","Project Info"])

if page=="Decision Agent":
    st.subheader("Tell ShopWise your situation")
    goal=st.text_area("What are you trying to buy?",height=110,
      placeholder="I need a laptop for coding, college and occasional gaming. Budget ₹80,000. Battery and performance are important.")
    c1,c2,c3=st.columns(3)
    with c1: category=st.selectbox("Category",["Auto-detect","Phone","Laptop","Headphones","Tablet","Smartwatch","Camera","TV","Monitor","Shoes","Other"])
    with c2: budget=st.number_input("Maximum budget (₹)",min_value=500,value=50000,step=1000)
    with c3: brands=st.text_input("Preferred brands (optional)",placeholder="Samsung, OnePlus")
    priorities=st.multiselect("What matters most?",
      ["Price","Camera","Performance","Gaming","Battery","Display","Durability","Software updates","Storage","Comfort","Portability","Brand","Reviews"],
      default=["Performance","Battery"])
    if st.button("🤖 Ask ShopWise to Decide",type="primary",use_container_width=True):
        if not goal.strip(): st.error("Describe what you need first.")
        elif not api_key: st.error("Live market search needs SERPAPI_KEY. Add it to .streamlit/secrets.toml.")
        else:
            with st.spinner("Planning → searching → filtering → comparing → deciding..."):
                result=agent.decide(goal,category,budget,priorities,brands)
            if result["error"]: st.error(result["error"])
            else:
                save_search(goal,result["category"],result["budget"],result["recommendation"].get("title",""))
                st.session_state["last_result"]=result
    result=st.session_state.get("last_result")
    if result:
        st.divider(); st.subheader("🎯 ShopWise's Decision")
        rec=result["recommendation"]
        st.markdown(f'<div class="decision"><h2>🏆 {rec["title"]}</h2><h3>Why this one?</h3><p>{rec["reason"]}</p></div>',unsafe_allow_html=True)
        a,b,c,d=st.columns(4)
        a.metric("Price",f'₹{rec["price"]:,.0f}'); b.metric("Rating",str(rec.get("rating","—")))
        c.metric("Score",f'{rec["score"]:.1f}/100'); d.metric("Matches",len(result["products"]))
        if rec.get("link"): st.link_button("🛒 View live listing",rec["link"])
        st.subheader("⚖️ Why not the alternatives?")
        for alt in result["alternatives"]: st.write(f'**{alt["title"]}** — {alt["why_not"]}')
        st.subheader("🔎 Agent activity")
        for step in result["activity"]: st.write(f'**{step["step"]}** — {step["result"]}')
        st.subheader("📊 Shortlist")
        st.dataframe([{"Product":p["title"],"Price":f'₹{p["price"]:,.0f}',"Rating":p.get("rating","—"),
                       "Reviews":p.get("reviews","—"),"Score":round(p.get("score",0),1),"Seller":p.get("source","—")}
                      for p in result["products"]],use_container_width=True,hide_index=True)
        st.subheader("🧠 Decision factors"); st.write(result["factor_summary"])

elif page=="Should I Buy?":
    st.subheader("🔍 Should I Buy This?")
    url=st.text_input("Product URL",placeholder="https://...")
    need=st.text_area("Your requirements",placeholder="I need this for coding, travel and long-term use. Battery matters more than gaming.")
    budget=st.number_input("Your maximum budget (₹)",min_value=500,value=80000,step=1000)
    if st.button("Analyze Purchase",type="primary"):
        if not api_key: st.error("SERPAPI_KEY is required.")
        elif not url.startswith("http"): st.error("Enter a valid product URL.")
        else:
            with st.spinner("Analyzing current price and value..."):
                st.session_state["buy_result"]=agent.should_buy(url,need,budget)
    r=st.session_state.get("buy_result")
    if r:
        if r.get("error"): st.error(r["error"])
        else:
            st.markdown(f'<div class="decision"><h2>{r["decision_emoji"]} {r["decision"]}</h2><p>{r["explanation"]}</p></div>',unsafe_allow_html=True)
            for item in r["checks"]: st.write(f'**{item["name"]}** — {item["result"]}')

elif page=="Price Tracker":
    st.subheader("📉 Price Tracker")
    query=st.text_input("Product to track",placeholder="OnePlus 13 256GB")
    budget=st.number_input("Reference budget (₹)",min_value=500,value=60000,step=1000)
    if st.button("Track current price",type="primary"):
        if not api_key: st.error("SERPAPI_KEY is required.")
        else:
            with st.spinner("Checking live market..."):
                products=agent.search_live(query,budget)
            if products:
                p=products[0]; save_snapshot(query,p["price"],p.get("link",""))
                st.success(f'Snapshot saved: ₹{p["price"]:,.0f}')
            else: st.warning("No matching product found.")
    if query:
        snaps=get_snapshots(query)
        if snaps: st.dataframe(snaps,use_container_width=True,hide_index=True)
        else: st.info("No snapshots yet.")

elif page=="History":
    st.subheader("🧠 Memory")
    history=get_history()
    st.dataframe(history,use_container_width=True,hide_index=True) if history else st.info("No searches saved yet.")

else:
    st.subheader("About ShopWise 2.0")
    st.markdown("""**ShopWise is a Personal Shopping Decision Agent.**

The problem is not that users cannot find products. The problem is that they find too many products and do not know which one fits their situation.

**Workflow:** Understand situation → extract requirements → search live market → enforce budget → score → compare trade-offs → recommend one → explain why.

**Included:** live market search, situation-based recommendations, budget filtering, priority scoring, alternative explanations, Should I Buy, price snapshots, SQLite memory and modular agent architecture.

**Important:** live results depend on the shopping-search provider and are not literally every product on the internet.""")
