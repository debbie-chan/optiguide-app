import time
from gurobipy import GRB, Model

# Define the entities involved in the distribution network
suppliers = ['supplier1', 'supplier2']
farms = ['farm1', 'farm2']
markets = ['market1', 'market2']

# Define capacities and costs associated with entities
seed_supply_capacity = {'supplier1': 1000, 'supplier2': 1500}
planting_cost = {'farm1': 20, 'farm2': 25}
storage_preservation_cost = {'market1': 10, 'market2': 15}

# Define transportation costs between suppliers and farms
transport_cost_supplier_to_farm = {
    ('supplier1', 'farm1'): 2,
    ('supplier1', 'farm2'): 3,
    ('supplier2', 'farm1'): 2,
    ('supplier2', 'farm2'): 4
}

# Define transportation costs between farms and markets
transport_cost_farm_to_market = {
    ('farm1', 'market1'): 5,
    ('farm1', 'market2'): 6,
    ('farm2', 'market1'): 4,
    ('farm2', 'market2'): 3
}

# Define market demand
market_demand = {'market1': 800, 'market2': 1200}

# Create a new optimization model
model = Model("bayer_crop_distribution")

# OPTIGUIDE DATA CODE GOES HERE

# Create decision variables for transportation from suppliers to farms and farms to markets
x = model.addVars(transport_cost_supplier_to_farm.keys(), vtype=GRB.INTEGER, name="x")
y = model.addVars(transport_cost_farm_to_market.keys(), vtype=GRB.INTEGER, name="y")

# Set the objective function to minimize overall costs
model.setObjective(
    sum(x[i] * transport_cost_supplier_to_farm[i] for i in transport_cost_supplier_to_farm.keys()) +
    sum(y[j] * transport_cost_farm_to_market[j] for j in transport_cost_farm_to_market.keys()) +
    sum(planting_cost[f] * sum(y[f, m] for m in markets) for f in farms) +
    sum(storage_preservation_cost[m] * market_demand[m] for m in markets),
    GRB.MINIMIZE)

# Ensure conservation of flow: 
# Add supply constraints limiting seed supply to farms
for s in suppliers:
    model.addConstr(sum(x[s, f] for f in farms) <= seed_supply_capacity[s], f"seed_supply_{s}")

# Add demand constraints ensuring market demand is met from farms
for m in markets:
    model.addConstr(sum(y[f, m] for f in farms) >= market_demand[m], f"market_demand_{m}")

# Optimize the model
model.optimize()
m = model

# OPTIGUIDE CONSTRAINT CODE GOES HERE

# Update and re-optimize the model
m.update()
model.optimize()

# Print the time and optimal solution status and value
print(time.ctime())
if m.status == GRB.OPTIMAL:
    print(f'Optimal cost: {m.objVal}')
else:
    print("Not solved to optimality. Optimization status:", m.status)