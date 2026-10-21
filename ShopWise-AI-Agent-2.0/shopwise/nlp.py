import re
def infer_category(text):
    t=text.lower()
    aliases={"Phone":["phone","smartphone","mobile","iphone","android"],"Laptop":["laptop","notebook","macbook"],
    "Headphones":["headphone","headphones","earbuds","earphone","tws"],"Tablet":["tablet","ipad"],
    "Smartwatch":["smartwatch"],"Camera":["camera","dslr","mirrorless"],"TV":["tv","television"],
    "Monitor":["monitor","display"],"Shoes":["shoes","sneakers"],"T-Shirt":["tshirt","t-shirt","tee"],
    "Jeans":["jeans","denim"],"Backpack":["backpack","bag"],"Speaker":["speaker","soundbar"],
    "Books":["book","books"],"Grocery":["grocery","groceries"]}
    for cat,words in aliases.items():
        if any(w in t for w in words): return cat
    return "Product"
def infer_budget(text,fallback):
    t=text.lower().replace(",",""); vals=[]
    for m in re.finditer(r'(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(lakh|lac|k)?',t):
        n=float(m.group(1)); unit=m.group(2)
        if unit in ("lakh","lac"): n*=100000
        elif unit=="k": n*=1000
        if n>=500: vals.append(n)
    return min(vals) if vals else float(fallback)
def clean_query(text):
    t=re.sub(r'₹\s*[\d,]+','',text,flags=re.I)
    t=re.sub(r'\b(?:under|below|within|max(?:imum)?|budget|rs\.?|inr)\s*[\d,.\s]*(?:lakh|lac|k)?','',t,flags=re.I)
    return re.sub(r'\s+',' ',t).strip()
