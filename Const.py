import os


SIF_PATH = r"/home/juvenal/code_aster/code_aster_16.2.14.sif"
MAIN_DIR = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR = os.path.join(MAIN_DIR, "Template")
LIB_DIR = os.path.join(MAIN_DIR, "SectionLibrary")
DB1_PATH = os.path.join(LIB_DIR, "secpara1.json")
DB2_PATH = os.path.join(LIB_DIR, "secpara2.json")

l_sectype = (
    "Circle",
    "Tube",
    # "Concentric Tube",
    # "Cone",
    "Rectangle",
    "Hollow_Rectangle",
    "I_Section",
    "Channel",
    "Tee",
    "Angle",
    "Custom",
)

method2nom = {"MACR_CARA_POUTRE": "Aster", "Python_Package": "Python"}

sectype2numdata = {
    "Circle": 1,
    "Tube": 2,
    # "Concentric Tube": 2,
    # "Cone": 2,
    "Rectangle": 2,
    "Hollow_Rectangle": 6,
    "I_Section": 6,
    "Channel": 6,
    "Tee": 4,
    "Angle": 4,
    "Custom": 3,
}

secpara2nom = {
    "A": "Area",
    "IY": "Iyy",
    "IYZ": "Iyz",
    "IZ": "Izz",
    "JG": "Warping Constant",
    "JX": "Torsion Constant",
    "EY": "Centroid Y",
    "EZ": "Centroid Z",
}

tol_fp = 1E-7
tol_err = 5E-2