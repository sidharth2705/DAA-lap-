import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import re, heapq, time

st.set_page_config(page_title="Dijkstra Algorithm Lab", page_icon="🧭", layout="wide")

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 10% 10%,rgba(34,211,238,.13),transparent 28%),radial-gradient(circle at 90% 10%,rgba(99,102,241,.15),transparent 28%),#070B14;color:#F8FAFC}
.block-container{max-width:1200px;padding-top:2rem}
.hero{text-align:center;padding:55px 20px 35px}.hero h1{font-size:65px;margin:0;font-weight:800;background:linear-gradient(90deg,#F8FAFC,#67E8F9,#A78BFA,#6EE7B7);-webkit-background-clip:text;-webkit-text-fill-color:transparent}.hero p{max-width:800px;margin:20px auto;color:#AAB5C7;font-size:18px;line-height:1.7}
.badge{display:inline-block;padding:7px 15px;border:1px solid rgba(103,232,249,.3);border-radius:999px;background:rgba(34,211,238,.08);color:#67E8F9;font-size:12px;font-weight:800;letter-spacing:.09em}
.glass,.card,.step{background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.11);border-radius:22px;padding:25px;box-shadow:0 18px 60px rgba(0,0,0,.18)}
.card{min-height:280px}.title{font-size:28px;font-weight:800;margin:15px 0 10px}.muted{color:#94A3B8;line-height:1.7}.formula{text-align:center;font-size:20px;padding:22px;color:#E0F2FE;background:rgba(34,211,238,.05);border:1px solid rgba(34,211,238,.16);border-radius:18px}
.metric{background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.09);border-radius:16px;padding:17px;text-align:center}.metric-value{font-size:24px;font-weight:800;color:#67E8F9}.metric-label{color:#94A3B8;font-size:12px}
.success{padding:22px;border-radius:18px;background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.25)}.warning{padding:18px;border-radius:16px;background:rgba(251,191,36,.07);border:1px solid rgba(251,191,36,.22);color:#FCD34D}.error{padding:22px;border-radius:18px;background:rgba(248,113,113,.08);border:1px solid rgba(248,113,113,.25)}
table{width:100%;border-collapse:collapse}th{color:#67E8F9;text-align:left;padding:14px;border-bottom:1px solid rgba(255,255,255,.1)}td{color:#CBD5E1;padding:14px;border-bottom:1px solid rgba(255,255,255,.06)}
div.stButton>button{width:100%;border-radius:12px;border:1px solid rgba(103,232,249,.25);background:linear-gradient(135deg,rgba(34,211,238,.16),rgba(99,102,241,.16));color:#F8FAFC;font-weight:700;min-height:46px}
textarea,input{background:rgba(255,255,255,.055)!important;color:#F8FAFC!important;border-radius:12px!important}
.footer{text-align:center;padding:40px;color:#64748B}
</style>
""", unsafe_allow_html=True)

def fw(x):
    return str(int(x)) if float(x).is_integer() else f"{x:g}"

def parse_edges(s):
    parts=[p.strip() for p in s.replace(";",",").replace("\n",",").split(",") if p.strip()]
    out=[]; seen=set()
    for p in parts:
        t=[x for x in re.split(r"\s*[-:]\s*|\s+",p) if x]
        if len(t)!=3: raise ValueError(f"Cannot read '{p}'. Use A-B-4.")
        u,v,w=t
        try:w=float(w)
        except:raise ValueError(f"Weight '{w}' is not a number.")
        if u==v: raise ValueError("Self-loops are not allowed.")
        if w<0: raise ValueError("Dijkstra requires non-negative edge weights.")
        k=tuple(sorted((u,v)))
        if k not in seen: seen.add(k); out.append((u,v,w))
    if not out: raise ValueError("Enter at least one edge.")
    return out

def build(edges):
    g=nx.Graph()
    for u,v,w in edges:g.add_edge(u,v,weight=w)
    return g

def path(prev,src,tgt):
    if tgt!=src and tgt not in prev:return []
    p=[tgt]
    while p[-1]!=src:p.append(prev[p[-1]])
    return p[::-1]

def dijkstra(g,src):
    dist={v:float("inf") for v in g}; prev={}; vis=set(); dist[src]=0
    steps=[dict(action="START",u=src,v=None,w=None,dist=dict(dist),vis=set(vis),prev=dict(prev),msg=f"Start at {src}. Set dist[{src}]=0 and all other distances to ∞.")]
    q=[(0,src)]
    while q:
        du,u=heapq.heappop(q)
        if u in vis:continue
        vis.add(u)
        steps.append(dict(action="FINALIZE",u=u,v=None,w=None,dist=dict(dist),vis=set(vis),prev=dict(prev),msg=f"{u} has the smallest tentative distance ({fw(dist[u])}), so its distance is finalized."))
        for v in sorted(g.neighbors(u),key=str):
            if v in vis:continue
            w=g[u][v]["weight"]; cand=dist[u]+w; old=dist[v]
            if cand<old:
                dist[v]=cand;prev[v]=u;heapq.heappush(q,(cand,v)); act="RELAX"
                msg=f"Relax {u} → {v}: {fw(dist[u])} + {fw(w)} = {fw(cand)}, improving dist[{v}]."
            else:
                act="CHECK";msg=f"Check {u} → {v}: {fw(dist[u])} + {fw(w)} = {fw(cand)}, not better than the current distance."
            steps.append(dict(action=act,u=u,v=v,w=w,dist=dict(dist),vis=set(vis),prev=dict(prev),msg=msg))
    return dist,prev,steps

def draw(g,dist,vis,prev,src,active=None,title=""):
    pos=nx.spring_layout(g,seed=18,k=1.25)
    pathset=set()
    # Show predecessor tree in purple; active edge cyan.
    aset=frozenset(active[:2]) if active else None
    fig=go.Figure()
    for u,v,d in g.edges(data=True):
        key=frozenset((u,v)); x0,y0=pos[u];x1,y1=pos[v]
        color="#67E8F9" if key==aset else "#A78BFA" if (prev.get(u)==v or prev.get(v)==u) else "rgba(148,163,184,.35)"
        width=6 if key==aset else 4 if color=="#A78BFA" else 2
        fig.add_trace(go.Scatter(x=[x0,x1],y=[y0,y1],mode="lines",line=dict(color=color,width=width),hoverinfo="none",showlegend=False))
        fig.add_trace(go.Scatter(x=[(x0+x1)/2],y=[(y0+y1)/2],mode="text",text=[fw(d["weight"])],textfont=dict(size=13,color="#CBD5E1"),hoverinfo="none",showlegend=False))
    xs=[];ys=[];labels=[];colors=[];sizes=[]
    for n in g:
        x,y=pos[n];xs.append(x);ys.append(y);d=dist.get(n,float("inf"));labels.append(f"{n}<br>{'∞' if d==float('inf') else fw(d)}")
        colors.append("#34D399" if n in vis else "#67E8F9" if n==src else "#818CF8");sizes.append(35 if n in vis else 38 if n==src else 29)
    fig.add_trace(go.Scatter(x=xs,y=ys,mode="markers+text",text=labels,textposition="middle center",textfont=dict(size=12,color="white"),marker=dict(size=sizes,color=colors,line=dict(width=2,color="rgba(255,255,255,.35)")),hoverinfo="none",showlegend=False))
    fig.update_layout(title=title,height=530,margin=dict(l=10,r=10,t=45,b=10),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",xaxis=dict(visible=False),yaxis=dict(visible=False),showlegend=False)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

if "page" not in st.session_state:st.session_state.page="home"
if "data" not in st.session_state:st.session_state.data=None
if "visual" not in st.session_state:st.session_state.visual=False
if "step" not in st.session_state:st.session_state.step=0

if st.session_state.page=="home":
    st.markdown('<div class="hero"><div class="badge">SINGLE SOURCE SHORTEST PATH LAB</div><h1>Dijkstra\'s Algorithm</h1><p>Find the shortest distance from one source vertex to every reachable vertex and visualize every relaxation step.</p></div>',unsafe_allow_html=True)
    st.markdown('<div class="glass"><div class="title">What is Single Source Shortest Path?</div><div class="muted">Given a source vertex, the Single Source Shortest Path problem finds the minimum-cost distance from that source to every other vertex. Dijkstra solves this efficiently when all edge weights are non-negative.</div><div class="formula">Relaxation: <b>newDist = dist[u] + weight(u,v)</b><br>If newDist &lt; dist[v], update dist[v] and predecessor[v].</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="card"><div class="badge">CORE IDEA</div><h3>🧭 Greedy Selection</h3><p class="muted">Dijkstra repeatedly chooses the unvisited vertex with the smallest tentative distance. It then relaxes every outgoing edge.</p><p>Strategy: <b>Greedy</b><br>Main operation: <b>Edge relaxation</b><br>Data structure: <b>Min-priority queue</b></p></div>',unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><div class="badge">COMPLEXITY</div><h3>⚡ Efficiency</h3><p class="muted">With an adjacency list and binary heap, the complexity is O((V+E) log V), commonly written O(E log V) for connected graphs.</p><p>Binary heap: <b>O((V+E) log V)</b><br>Simple array: <b>O(V²)</b><br>Space: <b>O(V+E)</b></p></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="glass"><div class="title">How Dijkstra Works</div><div class="muted" style="font-size:17px">1. Choose a source.<br>2. Set source distance to 0 and all others to ∞.<br>3. Select the unvisited vertex with the smallest tentative distance.<br>4. Relax its outgoing edges.<br>5. Mark it finalized.<br>6. Repeat until all reachable vertices are finalized.</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="glass"><div class="title">Important Limitation</div><div class="warning">⚠️ Dijkstra should not be used with negative edge weights. Bellman-Ford is appropriate for graphs that may contain negative weights.</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    x,y,z=st.columns([1,2,1])
    with y:
        st.markdown('<div class="card" style="text-align:center"><div style="font-size:48px">🧭</div><h2>Try Dijkstra\'s</h2><p class="muted">Enter a weighted graph, choose a source, find shortest paths, and visualize relaxation.</p></div>',unsafe_allow_html=True)
        if st.button("TRY DIJKSTRA'S →",use_container_width=True):
            st.session_state.page="play";st.rerun()
    st.markdown('<div class="footer">Dijkstra Lab • Single Source Shortest Path • Greedy Algorithms</div>',unsafe_allow_html=True)

else:
    c1,c2=st.columns([4,1])
    with c1:
        st.markdown('<div class="badge">DIJKSTRA PLAYGROUND</div><h1 style="font-size:42px">Find Shortest Paths</h1><div class="muted">Enter a weighted undirected graph and choose a source vertex.</div>',unsafe_allow_html=True)
    with c2:
        if st.button("← About"):st.session_state.page="home";st.session_state.data=None;st.rerun()
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="glass">',unsafe_allow_html=True)
    inp=st.text_area("Weighted edges",value="A-B-4, A-C-2, B-C-1, B-D-5, C-D-8, C-E-10, D-E-2, D-F-6, E-F-3",height=110)
    st.markdown('<div class="muted" style="font-size:12px">Format: <b>A-B-4, A-C-2, B-C-1</b> • Graph is undirected • weights must be non-negative.</div>',unsafe_allow_html=True)
    try:
        pe=parse_edges(inp);nodes=sorted(set([u for u,_,_ in pe]+[v for _,v,_ in pe]),key=str)
    except Exception:nodes=[]
    src=st.selectbox("Choose source vertex",nodes) if nodes else None
    p,q=st.columns(2)
    with p:find=st.button("⚡ FIND SHORTEST PATHS",use_container_width=True)
    with q:viz=st.button("▶ VISUALIZE",use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

    if find or viz:
        try:
            e=parse_edges(inp);g=build(e)
            if src is None:raise ValueError("Choose a source vertex.")
            dist,prev,steps=dijkstra(g,src)
            st.session_state.data=dict(graph=g,source=src,dist=dist,prev=prev,steps=steps)
            st.session_state.visual=viz;st.session_state.step=0
        except Exception as ex:
            st.markdown(f'<div class="error">❌ <b>Input Error</b><br><br>{ex}</div>',unsafe_allow_html=True)
    d=st.session_state.data
    if d and not st.session_state.visual:
        g=d["graph"];dist=d["dist"];prev=d["prev"];src=d["source"]
        st.markdown('<div class="title">Shortest Paths from '+src+'</div>',unsafe_allow_html=True)
        draw(g,dist,set(g),prev,src,title=f"Shortest Distances from {src}")
        vals=[(len(g), "Vertices"),(len(g.edges()),"Input Edges"),(sum(x!=float("inf") for x in dist.values()),"Reachable"),(0,"Source Distance")]
        cc=st.columns(4)
        for col,(v,l) in zip(cc,vals):
            with col:st.markdown(f'<div class="metric"><div class="metric-value">{v}</div><div class="metric-label">{l}</div></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        rows=[]
        for n in sorted(g,key=str):
            dd=dist[n];pp=path(prev,src,n)
            rows.append(f"<tr><td><b>{n}</b></td><td>{'∞' if dd==float('inf') else fw(dd)}</td><td>{' → '.join(pp) if pp else 'Unreachable'}</td></tr>")
        st.markdown(f'<div class="glass"><div class="title">Distance Table</div><table><tr><th>Vertex</th><th>Shortest Distance</th><th>Shortest Path</th></tr>{"".join(rows)}</table></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        if st.button("▶ VISUALIZE STEP BY STEP",use_container_width=True):st.session_state.visual=True;st.session_state.step=0;st.rerun()
    if d and st.session_state.visual:
        g=d["graph"];src=d["source"];steps=d["steps"];i=st.session_state.step
        st.markdown('<div class="title">🔬 Dijkstra Visualization</div><div class="muted">Follow initialization, vertex finalization, and edge relaxation one step at a time.</div>',unsafe_allow_html=True)
        if i<len(steps):
            s=steps[i];draw(g,s["dist"],s["vis"],s["prev"],src,(s["u"],s["v"],s["w"]) if s["v"] else None,title=f"Step {i+1} of {len(steps)}")
            box="success" if s["action"] in ("RELAX","FINALIZE") else "warning"
            st.markdown(f'<div class="{box}"><b>{s["action"]}</b><br><br>{s["msg"]}</div>',unsafe_allow_html=True)
            distance_parts = []
            for n, x in s["dist"].items():
                distance_parts.append(f"{n}: {'∞' if x == float('inf') else fw(x)}")
            distance_text = " • ".join(distance_parts)

            st.markdown(
                f'<div class="step"><h4>Current distances</h4>'
                f'<div class="muted">{distance_text}</div>'
                f'<hr><b>Dijkstra Rule:</b> choose the smallest tentative distance, '
                f'then relax outgoing edges.</div>',
                unsafe_allow_html=True
            )
            time.sleep(.7);st.session_state.step+=1;st.rerun()
        else:
            draw(g,d["dist"],set(g),d["prev"],src,title="Dijkstra Completed")
            st.markdown(f'<div class="success"><h2>🎯 Shortest Paths Complete</h2><div class="muted">Source: <b>{src}</b>. All reachable shortest distances have been calculated.</div></div>',unsafe_allow_html=True)
        a,b,c=st.columns(3)
        with a:
            if st.button("🔄 REPLAY",use_container_width=True):st.session_state.step=0;st.rerun()
        with b:
            if st.button("📊 VIEW OUTPUT",use_container_width=True):st.session_state.visual=False;st.rerun()
        with c:
            if st.button("← CHANGE GRAPH",use_container_width=True):st.session_state.data=None;st.session_state.visual=False;st.rerun()
    st.markdown('<div class="footer">Dijkstra Lab • Python • Streamlit • NetworkX • Plotly</div>',unsafe_allow_html=True)