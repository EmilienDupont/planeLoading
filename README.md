# Cargo Plane Loading
An example of using Gurobi to solve a loading problem

![](screenshot.png?raw=true)

# Running the example

1. Start Python's webserver from the command line
    ```
    make
    ```

2. Point your browser at http://localhost:8000

3. Click on the screen to adjust the number of boxes.

4. Click "Compute" to load the planes.

# Performing an optimization

To just solve the model (without running a web server) do:

```
make test
```
