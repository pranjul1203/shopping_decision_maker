import requests
def search_google_shopping(query,api_key,location="India",limit=40):
    params={"engine":"google_shopping","q":query,"location":location,"gl":"in","hl":"en","device":"desktop","api_key":api_key}
    try:
        r=requests.get("https://serpapi.com/search.json",params=params,timeout=30); r.raise_for_status(); data=r.json()
        out=[]
        for x in data.get("shopping_results",[])[:limit]:
            price=x.get("extracted_price")
            if price is None:
                raw=str(x.get("price","")).replace(",","")
                try: price=float("".join(ch for ch in raw if ch.isdigit() or ch==".")) 
                except: continue
            out.append({"title":x.get("title","Unknown product"),"price":float(price),"rating":x.get("rating"),
                        "reviews":x.get("reviews"),"source":x.get("source"),"link":x.get("product_link") or x.get("link"),
                        "snippet":x.get("snippet",""),"delivery":x.get("delivery",""),"thumbnail":x.get("thumbnail")})
        return out,None
    except Exception as e: return [],str(e)
