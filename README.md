# ecell4-ode-dump

The prototype implementation of ecell4 ODENetworkModel serialization

## Requirement
* ecell4
* dill (You can install it through `pip install dill`)

## How to run

You can test this code by the follogwing commands.

    python ode_simulator.py > run_1.log
    python ode_simulator_load.py > run_2.log

Please compare the result through `vimdiff run_1.log run_2.log`.

