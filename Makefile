all:
	./SimpleServer.py

test:
	./planeLoading.py

clean:
	-rm gurobi.log *.pyc *.lp
