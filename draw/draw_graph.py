from graph import Graph
from graph import MIN
import random
from graph import _shaps as SHAP_TYPE
import math
import time
import os
import file_io
PART_NUM = 4  # 图片数量为 PART_NUM * PART_NUM
BACK_HEIGHT = 200  # 单个零件画布的高
BACK_WIDTH = 200
BACK_AREA = BACK_HEIGHT * BACK_WIDTH
create_time = time.strftime("%Y%m%d-%H%M%S")

SAVE_PATH = "./image"

AREA_RATE = 0.1243129

def main():
    shaps = []
    total_parts = BACK_AREA
    # total_h = 0
    graph = Graph(BACK_HEIGHT, BACK_WIDTH, PART_NUM)
    p = [1, 0]
    for step in range(PART_NUM * PART_NUM):
        p[1] += 1
        if p[1] > PART_NUM:
            p[1] = 1
            p[0] += 1
        # graph.clear()
        type = random.randrange(0, int(len(SHAP_TYPE) * 1.5))
        if type >= len(SHAP_TYPE):
            type = len(SHAP_TYPE) - 1
        shap = SHAP_TYPE[type]
        part_area = random.randrange(MIN * MIN, int(total_parts))
        # total_parts -= part_area
        part = int(math.sqrt(part_area))
        # shaps.append((part, shap))
        areainfo = graph.draw((part, shap), p)

        # if not os.path.isdir(SAVE_PATH + "/" + create_time):
        #     os.mkdir(SAVE_PATH + "/" + create_time)
        # print(p)
        shaps.append(((p[0],p[1]), shap, areainfo,areainfo[0] * AREA_RATE))
    filename = SAVE_PATH + "/" + create_time + "-part.png"
    graph.save(filename)
    textfile = SAVE_PATH + "/" + create_time + "-info.txt"
    f = open(textfile, 'w')
    for shap in shaps:
        f.write(str(shap)+'\n')
    # f.write('\n')
    # for shap in shaps:
    #     f.write(str(shap[2][0])+'\n')
    f.close()

    # total_h += part
    # if total_h >= BACK_HEIGHT:
    #     for
    shaps.sort(reverse=True)
    print('*****************************shaps*****************************')
    print(shaps)


if __name__ == '__main__':
    main()
