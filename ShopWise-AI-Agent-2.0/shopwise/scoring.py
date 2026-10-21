def score_product(p,query,priorities,preferred_brands=""):
    text=" ".join(str(p.get(k,"")) for k in ["title","snippet","source"]).lower()
    relevance=min(25,sum(3 for w in query.lower().split() if len(w)>2 and w in text))
    rating=min(20,float(p.get("rating") or 0)*4)
    try: reviews=float(p.get("reviews") or 0)
    except: reviews=0
    review_score=min(10,reviews/100)
    weights={"Price":15,"Camera":10,"Performance":10,"Gaming":10,"Battery":10,"Display":8,"Durability":8,
             "Software updates":7,"Storage":7,"Comfort":7,"Portability":7,"Brand":6,"Reviews":8}
    priority=sum(weights.get(x,5) for x in priorities if any(k in text for k in x.lower().split()))
    brand=8 if preferred_brands and any(b.strip().lower() in text for b in preferred_brands.split(",")) else 0
    return min(100,relevance+rating+review_score+priority+brand)
