import pandas as pd
import time
import gurobipy as gp
from gurobipy import GRB

# Define supply capacities at different locations
supply = dict({"Liverpool": 150000, "Brighton": 200000})

# Define throughput capacities at different locations
through = dict(
    {"Newcastle": 70000, "Birmingham": 50000, "London": 100000, "Exeter": 40000}
)

# Define demand from various customers
demand = dict(
    {"C1": 50000, "C2": 10000, "C3": 40000, "C4": 35000, "C5": 60000, "C6": 20000}
)

# Create a dictionary to capture shipping costs between locations and customers
    # Define costs between locations and customers
    # (Location A, Location B): Cost
    # For example: ("Liverpool", "Newcastle"): 0.5
    # This means the cost of shipping from Liverpool to Newcastle is 0.5
arcs, cost = gp.multidict(
    {
        ("Liverpool", "Newcastle"): 0.5,
        ("Liverpool", "Birmingham"): 0.5,
        ("Liverpool", "London"): 1.0,
        ("Liverpool", "Exeter"): 0.2,
        ("Liverpool", "C1"): 1.0,
        ("Liverpool", "C3"): 1.5,
        ("Liverpool", "C4"): 2.0,
        ("Liverpool", "C6"): 1.0,
        ("Brighton", "Birmingham"): 0.3,
        ("Brighton", "London"): 0.5,
        ("Brighton", "Exeter"): 0.2,
        ("Brighton", "C1"): 2.0,
        ("Newcastle", "C2"): 1.5,
        ("Newcastle", "C3"): 0.5,
        ("Newcastle", "C5"): 1.5,
        ("Newcastle", "C6"): 1.0,
        ("Birmingham", "C1"): 1.0,
        ("Birmingham", "C2"): 0.5,
        ("Birmingham", "C3"): 0.5,
        ("Birmingham", "C4"): 1.0,
        ("Birmingham", "C5"): 0.5,
        ("London", "C2"): 1.5,
        ("London", "C3"): 2.0,
        ("London", "C5"): 0.5,
        ("London", "C6"): 1.5,
        ("Exeter", "C3"): 0.2,
        ("Exeter", "C4"): 1.5,
        ("Exeter", "C5"): 0.5,
        ("Exeter", "C6"): 1.5,
    }
)

# Create a Gurobi model
model = gp.Model("SupplyNetworkDesign")

# OPTIGUIDE DATA CODE GOES HERE

# Add decision variables for flow between locations and customers
flow = model.addVars(arcs, obj=cost, name="flow")

# Production capacity limits - Ensure factories do not exceed their supply capacity
factories = supply.keys()
factory_flow = model.addConstrs(
    (
        gp.quicksum(flow.select(factory, "*")) <= supply[factory]
        for factory in factories
    ),
    name="factory",
)

# Customer demand - Ensure customer demand is met
customers = demand.keys()
customer_flow = model.addConstrs(
    (
        gp.quicksum(flow.select("*", customer)) == demand[customer]
        for customer in customers
    ),
    name="customer",
)

# Depot flow conservation - Ensure flow conservation at depots
depots = through.keys()
depot_flow = model.addConstrs(
    (
        gp.quicksum(flow.select(depot, "*")) == gp.quicksum(flow.select("*", depot))
        for depot in depots
    ),
    name="depot",
)

# Depot throughput - Ensure depots do not exceed their throughput capacities
depot_capacity = model.addConstrs(
    (gp.quicksum(flow.select("*", depot)) <= through[depot] for depot in depots),
    name="depot_capacity",
)

# Optimize the model
model.optimize()
m = model

# OPTIGUIDE CONSTRAINT CODE GOES HERE

# Update the model
m.update()
model.optimize()

# Print the time when the optimization was completed
print(time.ctime())

# If an optimal solution is found, print the flow between locations and customers
if m.status == GRB.OPTIMAL:
    product_flow = pd.DataFrame(columns=["From", "To", "Flow"])
    # print a table of flows for each arc
    for arc in arcs:
        if flow[arc].x > 1e-6:
            # Append flow information to the DataFrame
            product_flow = product_flow._append(
                {"From": arc[0], "To": arc[1], "Flow": flow[arc].x}, ignore_index=True
            )
    product_flow.index = [""] * len(product_flow)
    print(product_flow)
else:
    print("No optimal solution found")

# m.printStats()
