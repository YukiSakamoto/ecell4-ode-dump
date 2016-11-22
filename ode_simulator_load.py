from ecell4.core import *
from ecell4.ode import *
from ecell4.util.decorator import *

import dumper
import dill as pickle

def singlerun1():
    L = 1e-16
    edge_length = Real3(L, L, L)
    #volume = L * L * L
    N = 60
    sp1, sp2, sp3 = Species("A"), Species("B"), Species("C")

    # Load the Model
    with open("test3.pickle", "rb") as f:
        dump_obj = pickle.load(f)
        m = dumper.load_network_model(dump_obj)
        #import ipdb; ipdb.set_trace()

    for r in m.ode_reaction_rules():
        print("# {}".format(r.as_string()))

    w = ODEWorld(edge_length)
    w.add_molecules(sp1, N)

    sim = ODESimulator(m, w)

    # obs = FixedIntervalNumberObserver(0.01, ["A", "B", "C"])
    # sim.run(10.0, obs)
    # print(obs.data())

    next_time, dt = 0.0, 0.01
    print("{}\t{}\t{}\t{}".format(
        sim.t(), w.get_value(sp1), w.get_value(sp2), w.get_value(sp3)))
    for i in xrange(1000):
        next_time += dt
        sim.step(next_time)
        print("{}\t{}\t{}\t{}".format(
            sim.t(), w.get_value(sp1), w.get_value(sp2), w.get_value(sp3)))

def singlerun2():
    L = 1e-16
    edge_length = Real3(L, L, L)
    volume = L * L * L
    N = 60
    ka, U = 0.1, 0.5
    kd = ka * volume * (1 - U) / (U * U * N)

    with reaction_rules():
        A == B + C | (lambda r, p, V, t, rr: ka * r[0],
                      lambda r, p, V, t, rr: kd / V * r[0] * r[1])

    m = get_model()

    w = ODEWorld(edge_length)
    w.add_molecules(Species("A"), N)

    sim = ODESimulator(m, w, Explicit_Euler)
    obs = FixedIntervalNumberObserver(0.01, ["A", "B", "C"])
    sim.run(20.0, obs)

    for data in obs.data():
        print("{}\t{}\t{}\t{}".format(*data))

singlerun1()
#singlerun2()
print("# done")
