# IFOS Auto-Clustering Skeleton v1 (Explainable, hybrid semantics + usage)
# NOTE: This is a skeleton: replace stubs with real embeddings + graph community detection.

from __future__ import annotations
from typing import List, Dict, Any, Tuple
import math
import re
from collections import Counter, defaultdict

def tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-zA-Z0-9_]+", (text or "").lower()) if len(t) > 2]

def tfidf_vectors(items: List[Dict[str, Any]]) -> Tuple[List[str], List[Dict[str,float]]]:
    # Very small TF-IDF implementation for MVP (no external deps)
    docs = [tokenize((it.get("name","")+" "+it.get("description","")+" "+" ".join(it.get("tags") or []))) for it in items]
    df = Counter()
    for d in docs:
        for tok in set(d):
            df[tok] += 1
    N = max(1, len(docs))
    vocab = sorted(df.keys())
    idf = {t: math.log((N+1)/(df[t]+1))+1.0 for t in vocab}

    vecs = []
    for d in docs:
        tf = Counter(d)
        denom = max(1, sum(tf.values()))
        v = {t: (tf[t]/denom)*idf[t] for t in tf}
        vecs.append(v)
    return vocab, vecs

def cosine(a: Dict[str,float], b: Dict[str,float]) -> float:
    if not a or not b: return 0.0
    common = set(a.keys()) & set(b.keys())
    dot = sum(a[t]*b[t] for t in common)
    na = math.sqrt(sum(x*x for x in a.values()))
    nb = math.sqrt(sum(x*x for x in b.values()))
    if na == 0 or nb == 0: return 0.0
    return dot/(na*nb)

def build_similarity_graph(items: List[Dict[str, Any]], vecs: List[Dict[str,float]], usage_edges: List[Tuple[str,str,int]], sem_threshold: float=0.22) -> Dict[str, Dict[str, float]]:
    # Graph: node -> neighbor -> weight
    g = defaultdict(dict)
    # semantic edges
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            s = cosine(vecs[i], vecs[j])
            if s >= sem_threshold:
                a = items[i]["id"]; b = items[j]["id"]
                g[a][b] = max(g[a].get(b,0.0), s)
                g[b][a] = max(g[b].get(a,0.0), s)
    # usage edges (co-occurrence boosts)
    for a,b,cnt in usage_edges:
        w = min(1.0, math.log(1+cnt)/5.0)  # bounded
        g[a][b] = max(g[a].get(b,0.0), w)
        g[b][a] = max(g[b].get(a,0.0), w)
    return g

def simple_components(graph: Dict[str, Dict[str,float]], min_weight: float=0.25) -> List[List[str]]:
    # connected components on edges >= min_weight
    seen = set()
    comps = []
    for n in graph.keys():
        if n in seen: 
            continue
        stack = [n]
        comp = []
        seen.add(n)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y,w in graph.get(x,{}).items():
                if w >= min_weight and y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(comp)
    return comps

def name_cluster(items_by_id: Dict[str, Dict[str, Any]], members: List[str]) -> Tuple[str, List[str]]:
    # naive keyword extraction
    all_tokens = []
    for mid in members:
        it = items_by_id.get(mid,{})
        all_tokens += tokenize((it.get("name","")+" "+it.get("description","")))
    top = [t for t,_ in Counter(all_tokens).most_common(6)]
    name = " / ".join(top[:3]) if top else "Cluster"
    return name.title(), top

def run_pipeline(items: List[Dict[str, Any]], usage_edges: List[Tuple[str,str,int]]) -> List[Dict[str, Any]]:
    _, vecs = tfidf_vectors(items)
    g = build_similarity_graph(items, vecs, usage_edges)
    comps = simple_components(g)
    items_by_id = {it["id"]: it for it in items}
    clusters = []
    for idx, mem in enumerate(comps, start=1):
        cname, kw = name_cluster(items_by_id, mem)
        clusters.append({
            "cluster_id": f"cl.auto.{idx:03d}",
            "name": cname,
            "members": mem,
            "keywords": kw,
            "method_version": "cluster.hybrid.v1"
        })
    return clusters

if __name__ == "__main__":
    demo_items = [
        {"id":"telegram.send_message","name":"Telegram send message","description":"send notifications to telegram chat","tags":["notify","message"]},
        {"id":"email.send","name":"Email send","description":"send email alerts","tags":["notify","email"]},
        {"id":"rss.read_feed","name":"RSS read feed","description":"ingest rss feed items","tags":["ingest","rss"]},
    ]
    demo_edges = [("telegram.send_message","email.send",12), ("rss.read_feed","telegram.send_message",30)]
    print(run_pipeline(demo_items, demo_edges))
