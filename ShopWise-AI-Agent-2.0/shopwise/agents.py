from shopwise.config import get_secret
from shopwise.market import search_google_shopping
from shopwise.nlp import infer_category,infer_budget,clean_query
from shopwise.scoring import score_product

class ShoppingAgent:
    def search_live(self,query,budget):
        key=get_secret("SERPAPI_KEY")
        if not key:return []
        results,_=search_google_shopping(query,key)
        return [p for p in results if p["price"]<=budget]

    def decide(self,goal,category,budget,priorities,brands):
        key=get_secret("SERPAPI_KEY")
        if not key:return {"error":"SERPAPI_KEY is not configured."}
        cat=infer_category(goal) if category=="Auto-detect" else category
        used=min(float(budget),infer_budget(goal,budget))
        q=clean_query(goal)
        activity=[{"step":"1. Understand situation","result":f"Detected {cat}; budget ceiling ₹{used:,.0f}"},
                   {"step":"2. Build search plan","result":", ".join(priorities) if priorities else "balanced value"}]
        results,error=search_google_shopping(f"{cat} {q}",key)
        if error:return {"error":f"Live market search failed: {error}"}
        activity.append({"step":"3. Search live market","result":f"Collected {len(results)} listings"})
        results=[p for p in results if p["price"]<=used]
        activity.append({"step":"4. Enforce budget","result":f"{len(results)} products remain within budget"})
        if not results:return {"error":"No live product listing was found within your budget."}
        for p in results:p["score"]=score_product(p,goal,priorities,brands)
        results.sort(key=lambda x:x["score"],reverse=True)
        activity.append({"step":"5. Evaluate trade-offs","result":"Scored relevance, ratings, reviews, priorities and brand preference"})
        rec=results[0]
        alternatives=[{"title":p["title"],"why_not":self.why_not(p,rec)} for p in results[1:4]]
        activity.append({"step":"6. Make decision","result":f"Recommended {rec['title']}"})
        return {"error":None,"category":cat,"budget":used,"products":results[:12],
                "recommendation":{**rec,"reason":f"I selected this as the strongest match for your priorities ({', '.join(priorities) if priorities else 'overall value'}). It is listed at ₹{rec['price']:,.0f}, within your ₹{used:,.0f} limit."},
                "alternatives":alternatives,"activity":activity,
                "factor_summary":f"Decision factors: {', '.join(priorities) if priorities else 'overall value, price and ratings'}."}
    def why_not(self,p,best):
        return "Cheaper, but its overall match score is lower." if p["price"]<best["price"] else "It has a lower overall match score for the stated requirements."
    def should_buy(self,url,need,budget):
        key=get_secret("SERPAPI_KEY")
        if not key:return {"error":"SERPAPI_KEY is not configured."}
        results,error=search_google_shopping(url,key)
        if error:return {"error":error}
        if not results:return {"error":"The provider could not resolve this product URL."}
        p=results[0]; price=p["price"]; rating=float(p.get("rating") or 0)
        decision="BUY"; emoji="🟢"
        checks=[{"name":"Budget","result":f"Within budget." if price<=budget else f"₹{price:,.0f} is above your ₹{budget:,.0f} limit."},
                {"name":"Rating","result":str(rating) if rating else "Not available"}]
        if price>budget: decision="AVOID"; emoji="🔴"
        elif rating and rating<4: decision="WAIT"; emoji="🟡"
        return {"error":None,"decision":decision,"decision_emoji":emoji,
                "explanation":f"At ₹{price:,.0f}, the listing {'fits' if price<=budget else 'does not fit'} your budget. The decision uses the available live listing signals and your requirements.",
                "checks":checks}
