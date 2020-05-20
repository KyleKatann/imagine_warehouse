import sys
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB

n=0

def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)
        selected = gp.tuplelist((i, j) for i, j in model._vars.keys() if vals[i, j] > 0.5)
        tour = subtour(selected)
        if len(tour) < n:
            model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2)) <= len(tour)-1)



def subtour(edges):
    unvisited = list(range(n))
    cycle = range(n+1)
    while unvisited:
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i, j in edges.select(current, '*') if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle

def main(N,dist):
    global n
    n=N
    m = gp.Model()
    m.setParam('OutputFlag',0)

    vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
    for i, j in vars.keys():
        vars[j, i] = vars[i, j]

    m.addConstrs(vars.sum(i, '*') == 2 for i in range(n))
    m._vars = vars
    m.Params.lazyConstraints = 1
    m.optimize(subtourelim)

    vals = m.getAttr('x', vars)
    selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)

    tour = subtour(selected)
    assert len(tour) == n

    return tour,m.objVal