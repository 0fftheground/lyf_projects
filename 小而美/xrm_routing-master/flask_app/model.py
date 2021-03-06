import json
import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from utils import get_navi_distance


def get_route_json(json_data):
    '''

    :param request_data:
    :return:
    '''
    # init model input data
    node_list = json_data['nodeList']
    points_len = len(node_list)
    distance_matrix = np.zeros((points_len, points_len), dtype=np.int)
    for row in range(points_len):
        for col in range(row + 1, points_len):
            X_0, Y_0, X_1, Y_1 = node_list[row]['longitude'], node_list[row]['latitude'], node_list[col]['longitude'], \
                                 node_list[col]['latitude']
            try:
                distance_matrix[row, col] = get_navi_distance(X_0, Y_0, X_1, Y_1)
            except:
                return 0, 'Inputs invalid:inputs contain zero point!'

    distance_matrix_1 = distance_matrix + distance_matrix.T
    distance_matrix_1[:, 0] = 0

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix_1),
                                           1, 0)

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix_1[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return 1, print_solution(json_data, manager, routing, solution)
    else:
        return 0, "Calculation failed with ortools error."


def print_solution(json_data, manager, routing, solution):
    #     ??????json??????
    out_dict = {"sign": json_data['sign'],
                "deliveryNo": json_data['deliveryNo']}
    node_list = json_data['nodeList']
    out_node_list = []
    distance_list = []
    # "totalMileage": int(solution.ObjectiveValue()) / 1000,
    index = routing.Start(0)
    count = 1
    while not routing.IsEnd(index):
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        if routing.IsEnd(index):
            break
        node_dict = {"nodeNo": node_list[manager.IndexToNode(index)]['nodeNo'], "sort": count}
        # float('%.2f' % a)
        node_dict["mileage"] = float('%.2f' % (float(routing.GetArcCostForVehicle(previous_index, index, 0)) / 1000))
        distance_list.append(node_dict["mileage"])
        out_node_list.append(node_dict)
        count += 1

    out_dict['nodeList'] = out_node_list
    out_dict['totalMileage'] = float('%.2f' % (np.sum(distance_list)))
    return json.dumps(out_dict)
