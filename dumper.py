import dill as pickle
import ecell4.ode as ode


def dump_reaction_rule(obj, filename):
    a = dumps_reaction_rule(obj)
    with open(filename, "wb") as f:
        pickle.dump(a, f) 

def dump_network_model(obj):
    if not isinstance(obj, ode.ODENetworkModel):
        raise Exception("{} is not an ODENetworkModel object".format(ojb))
    dump_obj = dict()
    dump_obj["type"] = "ODENetworkModel"
    # 1. ODEReactionRules
    rr_list = obj.ode_reaction_rules()
    dump_obj["reaction_rules"] = []
    for rr in rr_list:
        dump_obj["reaction_rules"].append(dump_reaction_rule(rr))   

    return dump_obj

def load_network_model(dump_obj):
    if not dump_obj["type"] == "ODENetworkModel":
        raise Exception("Cannot rebuild ODENetworkModel from {}".format(dump_obj))

    m = ode.ODENetworkModel()
    # 1. ODEReactionRules
    dump_rr_list = dump_obj["reaction_rules"]
    for dump_rr in dump_rr_list:
        rr = load_reaction_rule(dump_rr)
        m.add_reaction_rule(rr)
    return m

def dump_reaction_rule(obj):
    # ODEReactionRule
    #    |--- Reactants
    #    |--- Products
    #    |--- Reactants_coefficients
    #    |--- Products_coefficients
    #    |--- k (*)
    #    |--- ratelaw(*)

    if not isinstance(obj, ode.ODEReactionRule):
        raise Exception("{} is not an ODEReactionRule object".format(obj))

    dump_obj = dict()
    dump_obj["type"] = "ODEReactionRule"
    # 1. Species
    dump_obj["prod"] = obj.products()
    dump_obj["reac"] = obj.reactants()
    # 2. Coefficients
    prod_coeffs = obj.products_coefficients()
    react_coeffs= obj.reactants_coefficients()
    dump_obj["prod_coeffs"] = prod_coeffs
    dump_obj["reac_coeffs"] = react_coeffs
    
    # 3. Ratelaw or k
    dump_obj["k"] = obj.k()
    if obj.has_ratelaw():
        rl = obj.get_ratelaw()
        rl_deriv = rl.to_derivative()
        dump_obj["ratelaw"] = dump_ratelaw(rl_deriv)

    #return pickle.dumps(dump_obj)
    return dump_obj

def load_reaction_rule(dump_obj):
    if not dump_obj["type"] == "ODEReactionRule":
        raise Exception("Cannot rebuild ODEReactionRule from {}".format(dump_obj))
    rr = ode.ODEReactionRule()
    # 1. Species
    products = dump_obj["prod"]
    reactants= dump_obj["reac"]
    prod_coeffs = dump_obj["prod_coeffs"]
    react_coeffs= dump_obj["reac_coeffs"]
    for (p, c) in zip(products, prod_coeffs):
        rr.add_product(p, c)
    for (r, c) in zip(reactants, react_coeffs):
        rr.add_reactant(r, c)
    # 2. Ratelaw or K
    if dump_obj.has_key("k"):
        rr.set_k(dump_obj["k"])
    if dump_obj.has_key("ratelaw"):
        rr.set_ratelaw( load_ratelaw(dump_obj["ratelaw"]) )

    return rr
    
def dump_ratelaw(obj):
    dump_obj = dict()
    if isinstance(obj, ode.ODERatelawMassAction):
        dump_obj["type"] = "ODERatelawMassAction"
        dump_obj["k"]    = obj.get_k()
    elif isinstance(obj, ode.ODERatelawCallback):
        dump_obj["type"] = "ODERatelawCallback"
        dump_obj["name"] = obj.as_string()
        dump_obj["func"] = obj.get_callback()
    else:
        raise Exception("{} is an unknown type of ODERatelawObject".format(obj))
    return dump_obj

def load_ratelaw(dump_obj):
    if dump_obj["type"] == "ODERatelawMassAction":
        return ode.ODERatelawMassAction(dump_obj["k"])
    elif dump_obj["type"] == "ODERatelawCallback":
        return ode.ODERatelawCallback(dump_obj["func"], dump_obj["name"] )
    else:
        raise Exception("{} is an unknown type object".format(dump_obj))

