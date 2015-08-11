#!/usr/bin/env python

from gurobipy import *

def optimize(aircrafts, packages, output=False):

    m = Model()

    numA = len(aircrafts)
    numP = len(packages)

    # Add variables
    x = {}
    for i in range(numP):
        for j in range(numA):
            x[(i,j)] = m.addVar(vtype=GRB.BINARY, name = "x" + str(i) + str(j))

    wMax = m.addVar(lb = 0, vtype=GRB.CONTINUOUS, name = "maximum_weight")

    m.update()

    # Add constraints
    for i in range(numP):
        m.addConstr( quicksum( x[(i,j)] for j in range(numA)) == 1, name="c1_%d" % i)

    for j in range(numA):
        m.addConstr( quicksum( x[(i,j)]*packages[i] for i in range(numP)) <= wMax, name="c2_%d" % j)

    m.addConstr( wMax <= min(planes), name="maxconstraint" )

    m.setObjective(wMax, GRB.MINIMIZE)

    m.optimize()

    if (m.status == 3 or m.status == 4):
        return ["infeasible"]

    solution = []

    for j in range(numA):
        row = []
        for i in range(numP):
            if x[(i,j)].X > .5:
                row.append(i)
        solution.append(row)

    return solution

def handleoptimize(jsdict):
    if 'planes' in jsdict and 'boxes' in jsdict:
        solution = optimize(jsdict['planes'], jsdict['boxes'])
        return {'solution': solution }

if __name__ == '__main__':
    import json
    jsdict = json.load(sys.stdin)
    jsdict = handleoptimize(jsdict)
    print 'Content-Type: application/json\n\n'
    print json.dumps(jsdict)
