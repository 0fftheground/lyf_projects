def sub_task(cal_df):
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    cal_df['navi_distance'] = cal_df.apply(
        lambda df: geo_location_distance(df['lon0'], df['lat0'], df['lon1'], df['lat1']), axis=1)
    return cal_df.copy()


def geo_location_distance(o_X, o_Y, d_X, d_Y):
#     '''
#     根据经纬度调用高德API获取导航距离（使用距离最短策略:strategy=2）
#     :param o_X:起点经度
#     :param o_Y:起点纬度
#     :param d_X:终点经度
#     :param d_Y:终点纬度
#     :return:导航距离（km为单位）
#     '''
    k = 'c33b02b68bd7785d75ed05f0178a8e05'
    if d_X == 0 or d_Y == 0 or str(d_X).lower().strip() == 'nan':
        return 999
    origin = str(o_X) + ',' + str(o_Y)
    destination = str(d_X) + ',' + str(d_Y)

    #url = "https://restapi.amap.com/v3/direction/driving?key=%s&origin=%s&destination=%s&strategy=0&extensions=base" % (
        #k, origin, destination)

    url = "https://restapi.amap.com/v3/distance?key=%s&origins=%s&destination=%s&type=1" % (
        k, origin, destination)

    headers = {'Connection': 'close', }

    try:
        data = requests.get(url, headers=headers)
        contest = data.json()
        if contest['status'] == '1':
            # route = contest['route']
            # result = route['paths'][0]
            # out = float(result['distance']) / 1000
            result = contest['results'][0]
            out = float(result['distance']) / 1000
        else:
            print(contest['info'])
            print(d_Y)
            out = 999
    except:
        out = 999
    return out


def get_route_total_distance(store_table, store_distance_df):
    # 调用or tools, assign origin and vehicle
    manager = pywrapcp.RoutingIndexManager(store_table.shape[0],
                                           1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        #         """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        # 只计算单程线路，不计算返程，将所有目的地为仓库的距离排除计算外
        if to_node == 0:
            return 0

        #     from_node = from_index
        #     to_node = to_index
        from_code = store_table.loc[int(from_node), '门店编号']
        to_code = store_table.loc[int(to_node), '门店编号']

        #     print(from_code)
        #     print(to_code)

        if from_code > to_code:
            return store_distance_df[
                (store_distance_df['village_code_0'] == to_code) & (store_distance_df['village_code_1'] == from_code)][
                'navi_distance'].values[0]
        elif from_code < to_code:
            return store_distance_df[
                (store_distance_df['village_code_0'] == from_code) & (store_distance_df['village_code_1'] == to_code)][
                'navi_distance'].values[0]
        else:
            return 0

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    solution = routing.SolveWithParameters(search_parameters)
    total_distance = 0
    route_order = ''

    def print_solution(manager, routing, solution):
        t_d = solution.ObjectiveValue()
        r_o = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            r_o.append(store_table.loc[int(index), '门店编号'])
            index = solution.Value(routing.NextVar(index))

        return t_d, ','.join(r_o)

    if solution:
        total_distance, route_order = print_solution(manager, routing, solution)
    return total_distance, route_order

