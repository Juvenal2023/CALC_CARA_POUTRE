import os
from colorama import Fore, Back, Style, init
from Common import *
from Const import *
from BuildMesh import build_mesh
from PyPackage import *
from TestResu import check_result


class CALC_CARA_POUTRE:
    def __init__(self, sectype: str, secdata: list, UI: bool=False):
        if sectype not in l_sectype:
            raise TypeError(f"Invalid section type: {sectype}")
        if len(secdata) != sectype2numdata[sectype] or (sectype == "Custom" and len(secdata) > sectype2numdata[sectype]):
            raise TypeError(f"Invalid number of section datas")
        self.__m_sectype = sectype
        self.__m_secdata = secdata
        self.__m_UI = UI
        self.__m_method = "MACR_CARA_POUTRE"
        self.__m_case_dir = None

    def set_method(self, method: str):
        if method not in method2nom.keys():
            raise TypeError(f"Invalid method: {method}")
        self.__m_method = method
        if self.__m_UI:
            print(f"Switch to method: {method}")

    @property
    def method(self):
        return self.__m_method

    def run_mission(self, debug=False):
        if self.__m_sectype == "Custom":
            secdata = secdata1 = secdata2 = self.__m_secdata["Name"]
        else:
            secdata = list(map(str, self.__m_secdata))
            secdata1 = "_".join(secdata)
            secdata2 = ", ".join(secdata)
        case_nom = f"{self.__m_sectype}_{secdata1}"
        print(f"  {self.__m_sectype} :   {secdata2}  ".center(80, "-"))

        switch = False
        if self.__m_method == "MACR_CARA_POUTRE":
            if self.__m_sectype == "Custom":
                print(Fore.YELLOW + f" Warning: MACR_CARA_POUTRE method is not applicable for custom section" + Style.RESET_ALL)
                switch = True
            elif max(self.__m_secdata) / min(self.__m_secdata) > 100:
                print(Fore.YELLOW + f" Warning: Section geometries is not well define, swith to Python Package method" + Style.RESET_ALL)
                switch = True
            if switch:
                self.set_method("Python_Package")
                print(Fore.YELLOW + " Warning: Auto switching to Python Package method" + Style.RESET_ALL)

        self.__m_case_dir = os.path.join(LIB_DIR, self.__m_method, case_nom)
        if os.path.exists(self.__m_case_dir):
            print(" Section already exist, STOP !\n")
            secpara_info = read_write_file(DB1_PATH) if self.__m_method == "MACR_CARA_POUTRE" else read_write_file(DB2_PATH)
            return secpara_info[f"{self.__m_method}_{case_nom}"]
        os.makedirs(self.__m_case_dir)

        if self.__m_method == "Python_Package":
            print(f" Use Python Package to calculate section properties")
            if self.__m_sectype == "Circle":
                sect = Circle(self.__m_case_dir, self.__m_secdata[0])
            elif self.__m_sectype == "Tube":
                sect = Tube(self.__m_case_dir, self.__m_secdata[0], self.__m_secdata[1])
            elif self.__m_sectype == "Rectangle":
                sect = Rectangle(self.__m_case_dir, self.__m_secdata[0], self.__m_secdata[1])
            elif self.__m_sectype == "Hollow_Rectangle":
                sect = HollowRectangle(self.__m_case_dir, self.__m_secdata[0], self.__m_secdata[1], self.__m_secdata[2], self.__m_secdata[3], self.__m_secdata[4], self.__m_secdata[5])
            elif self.__m_sectype == "I_Section":
                sect = I(self.__m_case_dir, self.__m_secdata[0], self.__m_secdata[1], self.__m_secdata[2], self.__m_secdata[3], self.__m_secdata[4], self.__m_secdata[5])
            elif self.__m_sectype == "Channel":
                sect = Chanel(self.__m_case_dir, self.__m_secdata[0], self.__m_secdata[1], self.__m_secdata[2], self.__m_secdata[3], self.__m_secdata[4], self.__m_secdata[5])
            elif self.__m_sectype == "Tee":
                sect = Tee(self.__m_case_dir, self.__m_secdata[0], self.__m_secdata[1], self.__m_secdata[2], self.__m_secdata[3])
            elif self.__m_sectype == "Angle":
                sect = Angle(self.__m_case_dir, self.__m_secdata[0], self.__m_secdata[1], self.__m_secdata[2], self.__m_secdata[3])
            elif self.__m_sectype == "Custom":
                sect = Custom(self.__m_case_dir, self.__m_secdata["Outer"], self.__m_secdata["Inner"])
            time, secpara = sect.calc_sect_prop()

            secpara_info = read_write_file(DB2_PATH)
            secpara_info[f"Python_Package_{case_nom}"] = secpara
            read_write_file(DB2_PATH, mode="w", obj=secpara_info)
            print(f" Python Package success".ljust(40), "|", f"Used: {time:.2f}s".rjust(40))
        elif self.__m_method == "MACR_CARA_POUTRE":
            self.macr_cara_poutre()
            secpara_info = read_write_file(DB1_PATH)
            secpara = secpara_info[f"MACR_CARA_POUTRE_{case_nom}"]

        if debug and self.__m_sectype != "Custom":
            check_result(case_nom, secpara, self.__m_method)
        print("-" * 80, "\n")

    def macr_cara_poutre(self):
        print(" Use MACR_CARA_POUTRE to calculate section properties ".center(80, "-"))

        build_mesh(self.__m_case_dir, self.__m_sectype, self.__m_secdata)
        copy_files(TEMP_DIR, self.__m_case_dir, ("comm", "export"))
        export_path = os.path.join(self.__m_case_dir, "export")
        replace_keyword(export_path, "$MED$", self.__m_sectype)
        time = run_aster(export_path)

        print(f" MACR_CARA_POUTRE success".ljust(40), "|", f"Used: {time:.2f}s".rjust(40))
