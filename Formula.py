import math as m


def calc_sect_prop(sect_type: int, sect_geom: dict):
    A = sect_geom["A"]
    B = sect_geom["B"]
    C = sect_geom["C"]
    D = sect_geom["D"]
    b = h = tf = tw = Asy = Asz = AY = AZ = None
    ALPHA = 0.0
    # ========== 截面属性 ==========
    # 参考网站https://calcresource.com/
    if sect_type == 1:
        d = A
        An = Ag = m.pi * d**2 / 4
        IY = IZ = Iy = Iz = m.pi * d**4 / 64
        AY = AZ = 10 / 9
        JX = m.pi * d**4 / 32
        JG = 0.0  # 圆没有翘曲常数
        Zey = Zez = m.pi * d**3 / 32
        Zpy = Zpz = d**3 / 6
        Y0 = Z0 = Yc = Zc = 0.0
        ALPHA += 90

    elif sect_type == 2:
        d = A
        t = B
        di = d - 2 * t
        Ag = m.pi * d**2 / 4
        An = m.pi * (d**2 - di**2) / 4
        IY = IZ = Iy = Iz = m.pi * (d**4 - di**4) / 64
        Asy = Asz = m.pi * d * t / 2
        AY = An / Asy  # ISO-19902直接取2.0
        AZ = An / Asz
        JX = IY * 2
        JG = 0.0  # 圆管没有翘曲常数
        Zey = Zez = m.pi * (d**4 - di**4) / (32 * d)
        Zpy = Zpz = (d**3 - di**3) / 6
        Y0 = Z0 = Yc = Zc = 0.0

    elif sect_type == 11:
        b = B
        h = A
        An = Ag = b * h
        IY = Iy = b * h**3 / 12
        IZ = Iz = h * b**3 / 12
        AY = AZ = 6 / 5
        a0 = max(b, h)
        b0 = min(b, h)
        JX = a0 * b0**3 * (1 - 0.63 * b0 / a0 + 0.052 * b0**5 / a0**5) / 3
        JG = 0.0  # 方钢没有翘曲常数
        Zey = b * h**2 / 6
        Zez = h * b**2 / 6
        Zpy = b * h**2 / 4
        Zpz = h * b**2 / 4
        Y0 = Z0 = Yc = Zc = 0.0

    elif sect_type == 12:
        b = C
        tf = D
        h = A
        tw = B
        bi = b - 2 * tw
        hi = h - 2 * tf
        Ag = b * h
        An = b * h - bi * hi
        IY = Iy = b * h**3 / 12 - bi * hi**3 / 12
        IZ = Iz = h * b**3 / 12 - hi * bi**3 / 12
        Asy = 2 * b * tf
        Asz = 2 * h * tw
        AY = An / Asy
        AZ = An / Asz
        JX = (2 * D * B * (C - D) ** 2 * (A - B) ** 2) / (C * D + A * B - D**2 - B**2)
        JG = 0.0
        Zey = 2 * IY / h
        Zez = 2 * IZ / b
        Zpy = b * h**2 / 4 - bi * hi**2 / 4
        Zpz = h * b**2 / 4 - hi * bi**2 / 4
        Y0 = Z0 = Yc = Zc = 0.0

        # Torsion Properties.pdf提出不一样的JX计算公式
        # Rc = 1.5 * tf
        # p = 2 * (h - tf + b - tw) - 2 * Rc * (4 - m.pi)
        # Ap = (h - tf) * (b - tw) - Rc**2 * (4 - m.pi)
        # JX = 4 * Ap**2 * tf / p

    elif sect_type == 13:
        b = A
        tf = B
        h = C
        tw = D
        h0 = h - tf  # 法兰质心之间的距离
        hw = h - 2 * tf
        Ag = An = 2 * b * tf + hw * tw
        IY = Iy = b * h**3 / 12 - (b - tw) * hw**3 / 12
        IZ = Iz = tf * b**3 / 6 + hw * tw**3 / 12
        Asy = 5 * b * tf / 3
        Asz = h * tw
        AY = An / Asy
        AZ = An / Asz
        JX = (2 * b * tf**3 + h0 * tw**3) / 3
        JG = IZ * h0**2 / 4
        Zey = 2 * IY / h
        Zez = 2 * IZ / b
        Zpy = b * h**2 / 4 - (b - tw) * hw**2 / 4
        Zpz = tf * b**2 / 2 + hw * tw**2 / 4
        Y0 = Z0 = Yc = Zc = 0.0

        # Formulas.pdf提出不一样的JX和JG计算公式
        # JX = 1.31 * (2 * A * B**3 + (C - 2 * B) * D**3) / 3
        # JG = b**3 * h0**2 * tf / 24

    elif sect_type == 14:
        b = B
        tf = D
        h = A
        tw = C
        bf = b - tw
        hw = h - 2 * tf
        b0 = b - tw / 2
        h0 = h - tf
        Ag = An = 2 * b * tf + hw * tw
        Yc = (hw * tw**2 / 2 + tf * b**2) / An
        Zc = h / 2
        IY = Iy = b * h**3 / 12 - bf * hw**3 / 12
        Iz = hw * tw**3 / 3 + 2 * tf * b**3 / 3
        IZ = Iz - An * Yc**2
        Asy = 5 * b * tf / 3
        Asz = h * tw
        AY = An / Asy
        AZ = An / Asz
        JX = (2 * b0 * tf**3 + h0 * tw**3) / 3
        JG = b0**3 * h0**2 * tf / 12 * (2 * h0 * tw + 3 * b0 * tf) / (h0 * tw + 6 * b0 * tf)
        Zey = 2 * IY / h
        Zez = IZ / (b - Yc)
        Zpy = b * h**2 / 4 - bf * hw**2 / 4
        if tw <= An / (2 * h):
            Zpz = tf * bf**2 / 2 + b * h * tw / 2 - h**2 * tw**2 / (8 * tf)
        else:
            Zpz = (4 * tf * b**2 * (h - tf) + tw**2 * (h**2 - 4 * tf**2) - 4 * b *tf * hw * tw) / (4 * h)
        Y0 = 3 * tf * b0**2 / (6 * b0 * tf + h0 * tw) - tw / 2 + Yc
        Z0 = 0.0

        # Formulas.pdf提出不一样的Zp和JX计算公式
        # Zpy = h**2 * tw / 4 + tf * bf * (h - tf)
        # if 2 * tf * bf <= h * tw:
        #     Zpz = bf**2 * tf / 2 - h**2 * tw**2 / 8 / tf + h * tw * (bf + tw) / 2
        # else:
        #     Zpz = tw**2 * h / 4 + tf * bf * (tw + bf - tf * bf / h)
        # JX = 1.12 * (2 * b * tf**3 + (h - 2 * tf) * tw**3) / 3

    elif sect_type == 15:  # T型钢
        b = B
        tf = D
        h = A
        tw = C
        b1 = b - tw
        hw = h - tf
        h0 = h - tf / 2
        Ag = An = b * tf + (h - tf) * tw
        Yc = b / 2
        Zc = (tw * h**2 + b1 * tf**2) / (2 * An)
        Iy = tw * h**3 / 3 + b1 * tf**3 / 3
        IY = Iy - An * Zc**2
        IZ = Iz = hw * tw**3 / 12 + tf * b**3 / 12
        Asy = 5 * b * tf / 6
        Asz = h * tw
        AY = An / Asy
        AZ = An / Asz
        JX = (b * tf**3 + h0 * tw**3) / 3
        JG = tf**3 * b**3 / 144 + tw**3 * h0**3 / 36
        Zey = IY / (h - Zc)
        Zez = 2 * IZ / b
        if tf <= An / (2 * b):
            Zpy = tw * hw**2 / 4 + b * h * tf / 2 - b**2 * tf**2 / (4 * tw)
        else:
            Zpy = tw * h**2 / 2 + b * tf**2 / 4 - h * tf * tw / 2 - hw**2 * tw**2 / (4 * b)
        Zpz = tf * b**2 / 4 + hw * tw**2 / 4
        Y0 = 0.0
        Z0 = Zc - tf / 2

        # Formulas.pdf提出不一样的JX计算公式
        # JX = 1.12 * (B * D ** 3 + (A - D) * C ** 3) / 3

    elif sect_type == 16:
        b = B
        tf = C
        h = A
        b1 = b - tf
        h1 = h - tf
        b0 = b - tf / 2
        h0 = h - tf / 2
        Ag = An = (b + h - tf) * tf
        Yc = tf / (2 * An) * (b**2 + h * tf - tf**2)
        Zc = tf / (2 * An) * (h**2 + b * tf - tf**2)
        Iy = tf * (b * tf**2 + h**3 - tf**3) / 3
        Iz = tf * (h * tf**2 + b**3 - tf**3) / 3
        Iyz = tf**2 * (b**2 + h**2 - tf**2) / 4
        Iy = Iy - An * Zc**2
        Iz = Iz - An * Yc**2
        Iyz = Iyz - An * Yc * Zc
        IY = (Iy + Iz) / 2 + m.sqrt(((Iy - Iz) / 2) ** 2 + Iyz**2)
        IZ = (Iy + Iz) / 2 - m.sqrt(((Iy - Iz) / 2) ** 2 + Iyz**2)
        Asy = 5 * tf * min(b, h) / 6
        Asz = 5 * tf * max(b, h) / 6
        AY = An / Asy
        AZ = An / Asz
        JX = (h0 + b0) * tf**3 / 3
        JG = tf**3 * (b0**3 + h0**3) / 36
        theta = m.pi / 2 if abs(Iy - Iz) < tol_fp else m.atan(-2 * Iyz / (Iy - Iz)) / 2
        Zeyy = Iy / (h - Zc)
        Zezz = Iz / (b - Yc)
        Zey = IY / ((h - Zc) * m.cos(theta) + Yc * m.sin(theta))
        Zez = IZ / ((b - Yc) * m.cos(theta) - (Zc - tf) * m.sin(theta))
        if tf <= An / 2 / b:
            Zpy = tf * (h1**2 - b**2 + 2 * b * h) / 4
        else:
            Zpy = b * tf**2 / 4 + h * tf * h1 / 2 - tf**2 * h1**2 / (4 * b)
        if tf <= An / 2 / h:
            Zpz = tf * (b1**2 - h**2 + 2 * h * b) / 4
        else:
            Zpz = h * tf**2 / 4 + b * tf * b1 / 2 - tf**2 * b1**2 / (4 * h)
        Y00 = tf / 2 - Yc
        Z00 = tf / 2 - Zc
        Y0 = Y00 * m.cos(theta) - Z00 * m.sin(theta)
        Z0 = Y00 * m.sin(theta) + Z00 * m.cos(theta)
        ALPHA += theta / m.pi * 180

    Ryy = m.sqrt(Iy / An)
    Rzz = m.sqrt(Iz / An)
    Ry = m.sqrt(IY / An)
    Rz = m.sqrt(IZ / An)

    if IY > IZ:
        Iy, Iz = Iz, Iy
        IY, IZ = IZ, IY
        Asy, Asz = Asz, Asy
        AY, AZ = AZ, AY
        Ry, Rz = Rz, Ry
        Zey, Zez = Zez, Zey
        Zpy, Zpz = Zpz, Zpy
        Yc, Zc = Zc, Yc
        Y0, Z0 = Z0, Y0
        ALPHA += 90

    sect_prop = {
        "b": b,
        "tf": tf,
        "h": h,
        "tw": tw,
        "Ag": Ag,  # 总截面积
        "A": An,  # 净截面积
        "Iy": Iy,  # 惯性矩
        "Iz": Iz,
        "IY": IY,  # 主轴惯性矩
        "IZ": IZ,
        "Asy": Asy,  # 剪切面积
        "Asz": Asz,
        "AY": AY,  # 剪切系数
        "AZ": AZ,
        "JX": JX,  # 扭转常数
        "JG": JG,  # 翘曲常数
        "ALPHA": ALPHA,  # 主惯性坐标系与原坐标系间夹角
        "Ry": Ry,  # 回转半径
        "Rz": Rz,
        "Zey": Zey,  # 弹性截面模量
        "Zez": Zez,
        "Zpy": Zpy,  # 塑性截面模量
        "Zpz": Zpz,
        "Yc": Yc,  # 重心坐标
        "Zc": Zc,
        "Y0": Y0,  # 剪切中心相对于重心的坐标
        "Z0": Z0,
    }
    return sect_prop
