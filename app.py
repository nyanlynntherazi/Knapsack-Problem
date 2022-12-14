import streamlit as st
import pandas as pd
from ortools.algorithms import pywrapknapsack_solver


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

    values = dataframe.Value.tolist()
    weights = dataframe.Weight.tolist()
    names = dataframe.Name.tolist()

    st.metric(label="Total Weight in Dataset",value =sum(weights))

capacities = st.number_input("""Insert Capacity 
    (Capacity Should be smaller than Total Weights in Dataset""")
st.write('The current Capacity is ', capacities)

def print_item_weight(packed_items,packed_weights,name):
    for i,j in zip(packed_items,packed_weights):
        st.write(i,name[i],j)
        
def knapsack(values, weights, capacities, name):
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    values = values
    weights = [weights]
    capacities = [capacities]

    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    total_weight = 0
    st.write('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]

    st.write('Total weight:', total_weight)
    print_item_weight(packed_items,packed_weights,name)


if st.button('Calculate'):
	knapsack(values, weights, capacities,names)
else:
	st.write("""""")
