import requests
import hashlib


def get_navi_distance(o_X, o_Y, d_X, d_Y):
    '''
    根据经纬度调用高德API获取导航距离（使用距离最短策略:strategy=2）
    :param o_X:起点经度
    :param o_Y:起点纬度
    :param d_X:终点经度
    :param d_Y:终点纬度
    :return:导航距离（m为单位）
    '''
    k = 'c33b02b68bd7785d75ed05f0178a8e05'

    try:
        float(o_X)
        float(o_Y)
        float(d_X)
        float(d_Y)
    except:
        return "inputs invalid:not a valid number!"

    if d_X == 0 or d_Y == 0 or o_X == 0 or o_Y == 0:
        return "inputs invalid:inputs contains zero points!"
    origin = str(o_X) + ',' + str(o_Y)
    destination = str(d_X) + ',' + str(d_Y)
    # 驾车导航api
    url = "https://restapi.amap.com/v3/direction/driving?key=%s&origin=%s&destination=%s&strategy=2&extensions=base" % (
        k, origin, destination)

    headers = {'Connection': 'close', }
    data = requests.get(url, headers=headers)
    contest = data.json()
    if contest['status'] == '1':
        route = contest['route']
        result = route['paths'][0]
        out = int(result['distance'])
    else:
        print(contest['info'])
        print(d_Y)
        out = get_navi_distance(o_X, o_Y, d_X, d_Y)
    return out


def verify_md5_sign(d_no, code):
    key = str(d_no) + 'abc'
    n = hashlib.new('md5')
    n.update(key.encode(encoding="utf-8"))
    if n.hexdigest() == code:
        return True
    else:
        return False
