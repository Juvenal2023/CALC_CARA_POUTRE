from Commands import CALC_CARA_POUTRE

if __name__ == "__main__":
    l_runInfo = []

    # ========== 圆钢 Circle ==========
    runInfo = {
        "SectionType": "Circle",
        "SectionData": [
            10,  # 半径 Radius
        ],
    }
    l_runInfo.append(runInfo)
    # ========== 圆钢 Circle ==========

    # ========== 圆管 Tube ==========
    runInfo = {
        "SectionType": "Tube",
        "SectionData": [
            5,  # 内半径 Inner radius
            7,  # 外半径 Outer radius
        ],
    }
    l_runInfo.append(runInfo)
    # ========== 圆管 Tube ==========

    # ========== 方钢 Prismatic ==========
    runInfo = {
        "SectionType": "Rectangle",
        "SectionData": [
            1,  # 宽度 Width
            2,  # 高度 Height
        ],
    }
    l_runInfo.append(runInfo)
    # ========== 方钢 Prismatic ==========

    # ========== 空心方钢 Box ==========
    runInfo = {
        "SectionType": "Hollow_Rectangle",
        "SectionData": [
            4,  # 宽度 Width
            5,  # 高度 Height
            0.2,  # 左壁厚 Left wall thickness
            0.3,  # 右壁厚 Right wall thickness
            0.4,  # 下壁厚 Bottom wall thickness
            0.5,  # 上壁厚 Top wall thickness
        ],
    }
    l_runInfo.append(runInfo)
    # ========== 空心方钢 Box ==========

    # ========== 工字钢 Wide Flange ==========
    runInfo = {
        "SectionType": "I_Section",
        "SectionData": [
            8,  # 下宽度 Bottom width
            7,  # 上宽度 Top width
            6,  # 高度 Height
            0.5,  # 下法兰厚度 Bottom flange thickness
            0.4,  # 上法兰厚度 Top flange thickness
            0.3,  # 腹板厚度 Web thickness
        ],
    }
    l_runInfo.append(runInfo)
    # ========== 工字钢 Wide Flange ==========

    # ========== 槽钢 Channel ==========
    runInfo = {
        "SectionType": "Channel",
        "SectionData": [
            4,  # 下宽度 Bottom width
            3,  # 上宽度 Top width
            5,  # 高度 Height
            0.3,  # 下法兰厚度 Bottom flange thickness
            0.5,  # 上法兰厚度 Top flange thickness
            0.4,  # 腹板厚度 Web thickness
        ],
    }
    l_runInfo.append(runInfo)
    # ========== 槽钢 Channel ==========

    # ========== T型钢 Tee ==========
    runInfo = {
        "SectionType": "Tee",
        "SectionData": [
            6,  # 宽度 Width
            5,  # 高度 Height
            1,  # 法兰厚度 Flange thickness
            0.8,  # 腹板厚度 Web thickness
        ],
    }
    l_runInfo.append(runInfo)
    # ========== T型钢 Tee ==========

    # ========== 角钢 Angle ==========
    runInfo = {
        "SectionType": "Angle",
        "SectionData": [
            5,  # 宽度 Width
            4,  # 高度 Height
            0.3,  # 法兰厚度 Flange thickness
            0.2,  # 腹板厚度 Web thickness
        ],
    }
    l_runInfo.append(runInfo)
    # ========== 角钢 Angle ==========

    # # ========== 灌浆圆管 Concentric Tube ==========
    # runInfo = {
    #     "SectionType": 3,
    #     "SectionData": {
    #         "A": 10,  # 外直径 Outer diameter
    #         "B": None,  # 外壁厚 Outer wall thickness
    #         "C": None,  # 内直径 Inner diameter
    #         "D": None,  # 内壁厚 Inner wall thickness
    #         "E": None,
    #     },
    #     "Result_Accuracy": 2,  # 1: Coarse  |  2: Moderate  |  3: Fine
    #     "Run_Directory": r"/home/juvenal/CALC_CARA_POUTRE/auto_test/CTB",
    # }
    # l_runInfo.append(runInfo)
    # # ========== 灌浆圆管 Concentric Tube ==========

    # ========== 自定义截面 Custom ==========
    runInfo = {
        "SectionType": "Custom",
        "SectionData": {
            "Name": "Custom_1",
            "Outer": [(0, 0), (1, 0), (2, 3), (-1, 4)],
            "Inner": [(1, 1), (1.5, 3), (0, 2.5)],
        },
    }
    l_runInfo.append(runInfo)
    # ========== 角钢 Angle ==========

    for method in ("Python_Package", "MACR_CARA_POUTRE"):
        for runInfo in l_runInfo:
            cmd = CALC_CARA_POUTRE(runInfo["SectionType"], runInfo["SectionData"])
            cmd.set_method(method)
            cmd.run_mission(True)
