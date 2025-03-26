# CALC_CARA_POUTRE

---

## Function

Calculate the **Section Properties** of **Beam**

---

## Catalogue

...

├── SectionLibrary  # Section library

│     ├── MACR_CARA_POUTRE  # Historical run cases for MACR_CARA_POUTRE method

│     ├── Python_Package  # Historical run cases for 3rd-party Python package method

│     ├── secpara1.json  # Database for MACR_CARA_POUTRE method

│     └── secpara2.json  # Database for 3rd-party Python package method

├── Template  # Template comm and export files

├── BuildMesh.py  # Call SALOME service for parametric modeling

├── Commands.py  # Main process

├── Common.py  # General function interface

├── Const.py  # Constant definition

├── Formula.py  # Section properties calculation formula  **TODO**

├── main.py  # Program entry (development environment)

├── PyPackage.py  # Call 3rd-party Python package service

└── TestResu.py  # Compare results with Ansys

```

```
