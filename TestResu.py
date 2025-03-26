from colorama import Fore, Back, Style, init
from Const import method2nom, secpara2nom, tol_fp, tol_err


def check_result(case_nom, secpara, method):
    flag = True
    for key, val in sectype2secpara[case_nom].items():
        if method == "MACR_CARA_POUTRE" and key == "IYZ":
            continue
        val_calc = secpara[key]
        err = 0 if val < tol_fp else abs((val - val_calc) / val)
        if (abs(val) < tol_fp and abs(val_calc) < tol_fp) or err < tol_err:
            continue
        if flag:
            real_method = method2nom[method]
            print(Fore.WHITE + f" Section parameter  :    Ansys   {real_method:^10}  Error(%)" + Style.RESET_ALL)
            flag = False
        key = secpara2nom[key]
        init()
        print(Fore.RED + f"{key:^20}:  {val:^10.4f}{val_calc:^10.4f}{100 * err:^10.4f}" + Style.RESET_ALL)


sectype2secpara = {
    "Circle_10": {
        "A": 313.915,
        "IY": 7837.76,
        "IYZ": -0.568e-17,
        "IZ": 7837.76,
        "JG": 0,
        "JX": 15675.5,
        "EY": -0.679e-16,
        "EZ": -0.124e-15,
    },
    "Tube_5_7": {
        "A": 75.3395,
        "IY": 1391.99,
        "IYZ": -0.746e-13,
        "IZ": 1391.99,
        "JG": 0,
        "JX": 2783.97,
        "EY": -0.943e-15,
        "EZ": 0.141e-15,
    },
    "Rectangle_1_2": {
        "A": 2,
        "IY": 0.666667,
        "IYZ": -0.347e-17,
        "IZ": 0.166667,
        "JG": 0.01987,
        "JX": 0.466431,
        "EY": 0.173e-17,
        "EZ": 0.208e-16,
    },
    "Hollow_Rectangle_4_5_0.2_0.3_0.4_0.5": {
        "A": 5.65,
        "IY": 21.4377,
        "IYZ": -0.126991,
        "IZ": 11.8907,
        "JG": 5.3577,
        "JX": 22.6142,
        "EY": 2.12699,
        "EZ": 2.62699,
    },
    "I_Section_8_7_6_0.5_0.4_0.3": {
        "A": 8.33,
        "IY": 54.5014,
        "IYZ": -0.130e-13,
        "IZ": 32.7781,
        "JG": 228.455,
        "JX": 0.541752,
        "EY": 0.260e-15,
        "EZ": 2.62983,
    },
    "Channel_4_3_5_0.3_0.5_0.4": {
        "A": 4.38,
        "IY": 16.7132,
        "IYZ": -1.05164,
        "IZ": 5.31376,
        "JG": 18.9134,
        "JX": 0.250621,
        "EY": 1.13836,
        "EZ": 2.58836,
    },
    "Tee_6_5_1_0.8": {
        "A": 9.2,
        "IY": 17.8101,
        "IYZ": 0.111e-14,
        "IZ": 18.1707,
        "JG": 2.54627,
        "JX": 2.73091,
        "EY": 0,
        "EZ": 0.869565,
    },
    "Angle_5_4_0.3_0.2": {
        "A": 2.24,
        "IY": 2.83761,
        "IYZ": -2.37857,
        "IZ": 5.98175,
        "JG": 0.099945,
        "JX": 0.054474,
        "EY": 1.60714,
        "EZ": 0.660714,
    },
    "Custom": 2,
}