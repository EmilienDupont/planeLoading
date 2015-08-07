#!/usr/bin/env python

from gurobipy import *

planes = [100, 100, 100]
boxes = [34, 6, 8, 17, 16, 5, 13, 21,
        25, 31, 14, 13, 33, 9, 25, 25]

def optimize(planes, boxes, output=False):

    m = Model()

    numP = len(planes)
    numB = len(boxes)

    # Add variables
    l = {}
    for i in range(numB):
        for j in range(numP):
            l[(i,j)] = m.addVar(vtype=GRB.BINARY, name = "l" + str(i) + str(j))

    maxweight = m.addVar(lb = 0, vtype=GRB.CONTINUOUS, name = "maxweight")

    m.update()

    # Add constraints
    for i in range(numB):
        m.addConstr( quicksum( l[(i,j)] for j in range(numP)) == 1, name="c1_%d" % i)

    for j in range(numP):
        m.addConstr( quicksum( l[(i,j)]*boxes[i] for i in range(numB)) <= maxweight, name="c2_%d" % j)

    m.setObjective(maxweight, GRB.MINIMIZE)

    m.optimize()

    solution = []

    for j in range(numP):
        row = []
        for i in range(numB):
            if l[(i,j)].X > .5:
                row.append(i)
        solution.append(row)

    print solution

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
