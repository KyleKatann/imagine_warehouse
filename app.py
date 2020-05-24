import streamlit as st
import pandas as pd
import networkx as nx
import random as rd
import tsp

'''
# imagine warehouse
## 問題設定
ある倉庫があります、それを35点のグラフで表現します。\n
その倉庫にはA～fで表現された商品棚があります。\n
そして、ピッキング指示書として、ランダムなA～fの組み合わせのクエリが与えられます。\n
この時、15番の点から出発してA～fのクエリの点を全て通り、15番の点に戻る最短距離のルートを表示してください。
'''

st.image("./problem.png")


dfnode=pd.read_excel("./warehouse_node.xlsx").fillna("")
dfroot=pd.read_excel("warehouse_root.xlsx").values.tolist()
dwii  ={name:node for name,node in pd.read_excel("where_is_inventry.xlsx").values.tolist()}
subroot={(start,end):root.split(",")for start,end,cost,root in dfroot}
inventry=[name for name in dwii.keys() if name!="start"]

def makequery():
    l=[]
    for i in range(10):
        num=rd.randint(1,10)
        l.append("start,"+",".join( sorted(set(inventry[rd.randint(0,len(inventry)-1)]for i in range(num))) ))
    return l

for q in makequery():
    st.write(q)

    q=set([dwii[name]for name in q.split(",")])
    n=len(q)
    oldtonew={node:newnode for newnode,node in enumerate(q)}
    newtoold={newnode:node for node,newnode in oldtonew.items()}
    dist = {(oldtonew[start],oldtonew[end]):cost for start,end,cost,root in dfroot if start in q and end in q}

    cost,root=tsp.tsp(range(n),dist=dist)
    st.write("最短距離:"+str(int(cost))+"m")

    root=[newtoold[i] for i in root]

    G=nx.DiGraph()
    G.add_nodes_from([str(i)for i in dfnode["node_number"]])
    for i in range(-1,len(root)-1):
        sr=subroot[(root[i],root[i+1])]
        for j in range(len(sr)-1):
            G.add_edge(sr[j],sr[j+1])
    
    pos={str(num):(x,-y) for num,x,y in zip(dfnode["node_number"],dfnode["point_x"],dfnode["point_y"])}
    nx.draw_networkx(G, pos=pos, node_color="c")
    st.pyplot()