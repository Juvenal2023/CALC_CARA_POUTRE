import os
from time import time


def build_mesh(case_dir, sectype, secdata):
    # Start SALOME
    import salome

    salome.salome_init()
    import salome_notebook

    notebook = salome_notebook.NoteBook()

    import SALOMEDS

    import GEOM
    from salome.geom import geomBuilder

    import SMESH
    from salome.smesh import smeshBuilder

    geompy = geomBuilder.New()
    smesh = smeshBuilder.New()

    # all start
    geom_start = time()

    ###
    ### GEOM component
    ###
    # turn off auto-rendering
    geompy.addToStudyAuto(maxNbSubShapes=0)
    O = geompy.MakeVertex(0, 0, 0)
    OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
    OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
    OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

    if sectype == "Circle":
        R = secdata[0]
        Divided_Cylinder_1 = geompy.MakeDividedCylinder(R, R, GEOM.SQUARE)
        Group_1 = geompy.CreateGroup(Divided_Cylinder_1, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Group_1, [56, 80, 100, 32, 94])
        Group_2 = geompy.CreateGroup(Divided_Cylinder_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Group_2, [43, 88, 19, 67])
        Section_1 = geompy.MakePartition([Group_1], [Group_2], [], [], geompy.ShapeType["FACE"], 0, [], 0)
        geompy.addToStudy( Divided_Cylinder_1, "Divided Cylinder_1" )
        geompy.addToStudyInFather( Divided_Cylinder_1, Group_1, "Section_1" )
        geompy.addToStudyInFather( Divided_Cylinder_1, Group_2, "Outer_Lines_1" )
        [Elems_1, Outer_Lines_1] = geompy.RestoreGivenSubShapes(Section_1, [Group_1, Group_2], GEOM.FSM_GetInPlaceByHistory, False, False)
        [Elems_1, Outer_Lines_1] = geompy.GetExistingSubObjects(Section_1, False)
        Rnd_Node_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["VERTEX"])
        geompy.UnionIDs(Rnd_Node_1, [6])
        local_length = R / 10

    elif sectype == "Tube":
        RI, RO = secdata[0], secdata[1]
        Disk_1 = geompy.MakeDiskR(RO, 1)
        Disk_2 = geompy.MakeDiskR(RI, 1)
        Section_1 = geompy.MakeCutList(Disk_1, [Disk_2], True)
        Elems_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Elems_1, [1])
        Outer_Lines_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Outer_Lines_1, [3])
        Inner_Lines_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Inner_Lines_1, [6])
        Rnd_Node_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["VERTEX"])
        geompy.UnionIDs(Rnd_Node_1, [7])
        [Elems_1, Outer_Lines_1, Inner_Lines_1, Rnd_Node_1] = geompy.GetExistingSubObjects(Section_1, False)
        local_length = (RO - RI) / 4

    elif sectype == "Rectangle":
        B, H = secdata[0], secdata[1]
        Vertex_1 = geompy.MakeVertex(0, 0, 0)
        Vertex_2 = geompy.MakeVertex(B, 0, 0)
        Vertex_3 = geompy.MakeVertex(B, H, 0)
        Vertex_4 = geompy.MakeVertex(0, H, 0)
        Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
        Line_2 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_3)
        Line_3 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_4)
        Line_4 = geompy.MakeLineTwoPnt(Vertex_4, Vertex_1)
        Face_1 = geompy.MakeFaceWires([Line_1, Line_2, Line_3, Line_4], 1)
        Section_1 = geompy.MakePartition([Face_1], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)
        Outer_Lines_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Outer_Lines_1, [3, 6, 8, 10])
        Elems_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Elems_1, [1])
        Rnd_Node_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["VERTEX"])
        geompy.UnionIDs(Rnd_Node_1, [5])
        geompy.DifferenceIDs(Rnd_Node_1, [5])
        geompy.UnionIDs(Rnd_Node_1, [4])
        [Outer_Lines_1, Elems_1, Rnd_Node_1] = geompy.GetExistingSubObjects(Section_1, False)
        local_length = min(B, H) / 4

    elif sectype == "Hollow_Rectangle":
        W1, W2, t1, t2, t3, t4 = secdata[:6]
        Vertex_1 = geompy.MakeVertex(       0,       0, 0)
        Vertex_2 = geompy.MakeVertex(      t1,       0, 0)
        Vertex_3 = geompy.MakeVertex( W1 - t2,       0, 0)
        Vertex_4 = geompy.MakeVertex(      W1,       0, 0)
        Vertex_5 = geompy.MakeVertex(       0,      t3, 0)
        Vertex_6 = geompy.MakeVertex(      t1,      t3, 0)
        Vertex_7 = geompy.MakeVertex( W1 - t2,      t3, 0)
        Vertex_8 = geompy.MakeVertex(      W1,      t3, 0)
        Vertex_9 = geompy.MakeVertex(       0, W2 - t4, 0)
        Vertex_10 = geompy.MakeVertex(     t1, W2 - t4, 0)
        Vertex_11 = geompy.MakeVertex(W1 - t2, W2 - t4, 0)
        Vertex_12 = geompy.MakeVertex(     W1, W2 - t4, 0)
        Vertex_13 = geompy.MakeVertex(      0,      W2, 0)
        Vertex_14 = geompy.MakeVertex(     t1,      W2, 0)
        Vertex_15 = geompy.MakeVertex(W1 - t2,      W2, 0)
        Vertex_16 = geompy.MakeVertex(     W1,      W2, 0)
        Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
        Line_2 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_3)
        Line_3 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_4)
        Line_4 = geompy.MakeLineTwoPnt(Vertex_4, Vertex_8)
        Line_5 = geompy.MakeLineTwoPnt(Vertex_8, Vertex_7)
        Line_6 = geompy.MakeLineTwoPnt(Vertex_7, Vertex_6)
        Line_7 = geompy.MakeLineTwoPnt(Vertex_6, Vertex_5)
        Line_8 = geompy.MakeLineTwoPnt(Vertex_5, Vertex_1)
        Line_9 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_6)
        Line_10 = geompy.MakeLineTwoPnt(Vertex_6, Vertex_10)
        Line_11 = geompy.MakeLineTwoPnt(Vertex_10, Vertex_11)
        Line_12 = geompy.MakeLineTwoPnt(Vertex_11, Vertex_12)
        Line_13 = geompy.MakeLineTwoPnt(Vertex_12, Vertex_16)
        Line_14 = geompy.MakeLineTwoPnt(Vertex_16, Vertex_15)
        Line_15 = geompy.MakeLineTwoPnt(Vertex_15, Vertex_14)
        Line_16 = geompy.MakeLineTwoPnt(Vertex_14, Vertex_13)
        Line_17 = geompy.MakeLineTwoPnt(Vertex_13, Vertex_9)
        Line_18 = geompy.MakeLineTwoPnt(Vertex_9, Vertex_10)
        Line_19 = geompy.MakeLineTwoPnt(Vertex_10, Vertex_14)
        Line_20 = geompy.MakeLineTwoPnt(Vertex_5, Vertex_9)
        Line_21 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_7)
        Line_22 = geompy.MakeLineTwoPnt(Vertex_7, Vertex_11)
        Line_23 = geompy.MakeLineTwoPnt(Vertex_11, Vertex_15)
        Line_24 = geompy.MakeLineTwoPnt(Vertex_12, Vertex_8)
        Face_1 = geompy.MakeFaceWires([Line_1, Line_7, Line_8, Line_9], 1)
        Face_2 = geompy.MakeFaceWires([Line_16, Line_17, Line_18, Line_19], 1)
        Face_3 = geompy.MakeFaceWires([Line_12, Line_13, Line_14, Line_23], 1)
        Face_4 = geompy.MakeFaceWires([Line_3, Line_4, Line_5, Line_21], 1)
        Face_5 = geompy.MakeFaceWires([Line_7, Line_10, Line_18, Line_20], 1)
        Face_6 = geompy.MakeFaceWires([Line_11, Line_15, Line_19, Line_23], 1)
        Face_7 = geompy.MakeFaceWires([Line_5, Line_12, Line_22, Line_24], 1)
        Face_8 = geompy.MakeFaceWires([Line_2, Line_6, Line_9, Line_21], 1)
        Section_1 = geompy.MakePartition([Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7, Face_8], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)
        Rnd_Node_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["VERTEX"])
        geompy.UnionIDs(Rnd_Node_1, [5])
        Elems_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Elems_1, [2, 12, 22, 32, 42, 46, 50, 54])
        Outer_Lines_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Outer_Lines_1, [4, 11, 14, 17, 27, 29, 34, 37, 44, 49, 53, 56])
        [Rnd_Node_1, Elems_1, Outer_Lines_1] = geompy.GetExistingSubObjects(Section_1, False)
        Inner_Lines_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Inner_Lines_1, [45, 48, 52, 57])
        [Rnd_Node_1, Elems_1, Outer_Lines_1, Inner_Lines_1] = geompy.GetExistingSubObjects(Section_1, False)
        local_length = min(t1, t2, t3, t4) / 4

    elif sectype == "I_Section":
        W1, W2, W3, t1, t2, t3 = secdata[:6]
        Vertex_1 = geompy.MakeVertex(  t3 / 2,       0, 0)
        Vertex_2 = geompy.MakeVertex(  W1 / 2,       0, 0)
        Vertex_3 = geompy.MakeVertex(  W1 / 2,      t1, 0)
        Vertex_4 = geompy.MakeVertex(  t3 / 2,      t1, 0)
        Vertex_5 = geompy.MakeVertex( -t3 / 2,       0, 0)
        Vertex_6 = geompy.MakeVertex( -W1 / 2,       0, 0)
        Vertex_7 = geompy.MakeVertex( -W1 / 2,      t1, 0)
        Vertex_8 = geompy.MakeVertex( -t3 / 2,      t1, 0)
        Vertex_9 = geompy.MakeVertex(  t3 / 2, W3 - t2, 0)
        Vertex_10 = geompy.MakeVertex( W2 / 2, W3 - t2, 0)
        Vertex_11 = geompy.MakeVertex( W2 / 2,      W3, 0)
        Vertex_12 = geompy.MakeVertex( t3 / 2,      W3, 0)
        Vertex_13 = geompy.MakeVertex(-t3 / 2, W3 - t2, 0)
        Vertex_14 = geompy.MakeVertex(-W2 / 2, W3 - t2, 0)
        Vertex_15 = geompy.MakeVertex(-W2 / 2,      W3, 0)
        Vertex_16 = geompy.MakeVertex(-t3 / 2,      W3, 0)
        Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
        Line_2 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_3)
        Line_3 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_4)
        Line_4 = geompy.MakeLineTwoPnt(Vertex_4, Vertex_9)
        Line_5 = geompy.MakeLineTwoPnt(Vertex_9, Vertex_10)
        Line_6 = geompy.MakeLineTwoPnt(Vertex_10, Vertex_11)
        Line_7 = geompy.MakeLineTwoPnt(Vertex_11, Vertex_12)
        Line_8 = geompy.MakeLineTwoPnt(Vertex_12, Vertex_16)
        Line_9 = geompy.MakeLineTwoPnt(Vertex_16, Vertex_15)
        Line_10 = geompy.MakeLineTwoPnt(Vertex_15, Vertex_14)
        Line_11 = geompy.MakeLineTwoPnt(Vertex_14, Vertex_13)
        Line_12 = geompy.MakeLineTwoPnt(Vertex_13, Vertex_8)
        Line_13 = geompy.MakeLineTwoPnt(Vertex_8, Vertex_7)
        Line_14 = geompy.MakeLineTwoPnt(Vertex_7, Vertex_6)
        Line_15 = geompy.MakeLineTwoPnt(Vertex_6, Vertex_5)
        Line_16 = geompy.MakeLineTwoPnt(Vertex_5, Vertex_1)
        Line_17 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_4)
        Line_18 = geompy.MakeLineTwoPnt(Vertex_4, Vertex_8)
        Line_19 = geompy.MakeLineTwoPnt(Vertex_8, Vertex_5)
        Line_20 = geompy.MakeLineTwoPnt(Vertex_13, Vertex_9)
        Line_21 = geompy.MakeLineTwoPnt(Vertex_9, Vertex_12)
        Line_22 = geompy.MakeLineTwoPnt(Vertex_16, Vertex_13)
        Face_1 = geompy.MakeFaceWires([Line_9, Line_10, Line_11, Line_22], 1)
        Face_2 = geompy.MakeFaceWires([Line_22, Line_20, Line_21, Line_8], 1)
        Face_3 = geompy.MakeFaceWires([Line_21, Line_5, Line_6, Line_7], 1)
        Face_4 = geompy.MakeFaceWires([Line_20, Line_12, Line_18, Line_4], 1)
        Face_5 = geompy.MakeFaceWires([Line_13, Line_14, Line_15, Line_19], 1)
        Face_6 = geompy.MakeFaceWires([Line_18, Line_19, Line_16, Line_17], 1)
        Face_7 = geompy.MakeFaceWires([Line_1, Line_2, Line_3, Line_17], 1)
        Section_1 = geompy.MakePartition([Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)
        Elems_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Elems_1, [2, 12, 19, 26, 33, 42, 47])
        Rnd_Node_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["VERTEX"])
        geompy.UnionIDs(Rnd_Node_1, [5])
        Outer_Lines_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Outer_Lines_1, [4, 7, 9, 28, 32, 35, 37, 53, 18, 21, 23, 25, 39, 44, 49, 51])
        [Elems_1, Rnd_Node_1, Outer_Lines_1] = geompy.GetExistingSubObjects(Section_1, False)
        local_length = min(t1, t2, t3) / 4

    elif sectype == "Channel":
        W1, W2, W3, t1, t2, t3 = secdata[:6]
        Vertex_1 = geompy.MakeVertex(  0,       0, 0)
        Vertex_2 = geompy.MakeVertex( t3,       0, 0)
        Vertex_3 = geompy.MakeVertex( W1,       0, 0)
        Vertex_4 = geompy.MakeVertex(  0,      t1, 0)
        Vertex_5 = geompy.MakeVertex( t3,      t1, 0)
        Vertex_6 = geompy.MakeVertex( W1,      t1, 0)
        Vertex_7 = geompy.MakeVertex(  0, W3 - t2, 0)
        Vertex_8 = geompy.MakeVertex( t3, W3 - t2, 0)
        Vertex_9 = geompy.MakeVertex( W2, W3 - t2, 0)
        Vertex_10 = geompy.MakeVertex( 0,      W3, 0)
        Vertex_11 = geompy.MakeVertex(t3,      W3, 0)
        Vertex_12 = geompy.MakeVertex(W2,      W3, 0)
        Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
        Line_2 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_3)
        Line_3 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_6)
        Line_4 = geompy.MakeLineTwoPnt(Vertex_6, Vertex_5)
        Line_5 = geompy.MakeLineTwoPnt(Vertex_5, Vertex_4)
        Line_6 = geompy.MakeLineTwoPnt(Vertex_4, Vertex_1)
        Line_7 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_5)
        Line_8 = geompy.MakeLineTwoPnt(Vertex_5, Vertex_8)
        Line_9 = geompy.MakeLineTwoPnt(Vertex_8, Vertex_9)
        Line_10 = geompy.MakeLineTwoPnt(Vertex_9, Vertex_12)
        Line_11 = geompy.MakeLineTwoPnt(Vertex_12, Vertex_11)
        Line_12 = geompy.MakeLineTwoPnt(Vertex_11, Vertex_10)
        Line_13 = geompy.MakeLineTwoPnt(Vertex_10, Vertex_7)
        Line_14 = geompy.MakeLineTwoPnt(Vertex_7, Vertex_8)
        Line_15 = geompy.MakeLineTwoPnt(Vertex_8, Vertex_11)
        Line_16 = geompy.MakeLineTwoPnt(Vertex_4, Vertex_7)
        Face_1 = geompy.MakeFaceWires([Line_1, Line_5, Line_6, Line_7], 1)
        Face_2 = geompy.MakeFaceWires([Line_12, Line_13, Line_14, Line_15], 1)
        Face_3 = geompy.MakeFaceWires([Line_2, Line_3, Line_4, Line_7], 1)
        Face_4 = geompy.MakeFaceWires([Line_5, Line_8, Line_14, Line_16], 1)
        Face_5 = geompy.MakeFaceWires([Line_9, Line_10, Line_11, Line_15], 1)
        Section_1 = geompy.MakePartition([Face_1, Face_2, Face_3, Face_4, Face_5], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)
        Elems_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Elems_1, [2, 12, 22, 29, 33])
        Outer_Lines_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Outer_Lines_1, [4, 11, 14, 17, 24, 26, 28, 31, 32, 35, 37, 39])
        Rnd_Node_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["VERTEX"])
        geompy.UnionIDs(Rnd_Node_1, [5])
        [Elems_1, Outer_Lines_1, Rnd_Node_1] = geompy.GetExistingSubObjects(Section_1, False)
        local_length = min(t1, t2, t3) / 4

    elif sectype == "Tee":
        W1, W2, t1, t2 = secdata[:4]
        Vertex_1 = geompy.MakeVertex(             0,  0, 0)
        Vertex_2 = geompy.MakeVertex( (W1 - t2) / 2,  0, 0)
        Vertex_3 = geompy.MakeVertex( (W1 + t2) / 2,  0, 0)
        Vertex_4 = geompy.MakeVertex(            W1,  0, 0)
        Vertex_5 = geompy.MakeVertex(             0, t1, 0)
        Vertex_6 = geompy.MakeVertex( (W1 - t2) / 2, t1, 0)
        Vertex_7 = geompy.MakeVertex( (W1 + t2) / 2, t1, 0)
        Vertex_8 = geompy.MakeVertex(            W1, t1, 0)
        Vertex_9 = geompy.MakeVertex( (W1 - t2) / 2, W2, 0)
        Vertex_10 = geompy.MakeVertex((W1 + t2) / 2, W2, 0)
        Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
        Line_2 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_3)
        Line_3 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_4)
        Line_4 = geompy.MakeLineTwoPnt(Vertex_4, Vertex_8)
        Line_5 = geompy.MakeLineTwoPnt(Vertex_8, Vertex_7)
        Line_6 = geompy.MakeLineTwoPnt(Vertex_7, Vertex_6)
        Line_7 = geompy.MakeLineTwoPnt(Vertex_6, Vertex_5)
        Line_8 = geompy.MakeLineTwoPnt(Vertex_5, Vertex_1)
        Line_9 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_6)
        Line_10 = geompy.MakeLineTwoPnt(Vertex_6, Vertex_9)
        Line_11 = geompy.MakeLineTwoPnt(Vertex_9, Vertex_10)
        Line_12 = geompy.MakeLineTwoPnt(Vertex_10, Vertex_7)
        Line_13 = geompy.MakeLineTwoPnt(Vertex_7, Vertex_3)
        Face_1 = geompy.MakeFaceWires([Line_1, Line_7, Line_8, Line_9], 1)
        Face_2 = geompy.MakeFaceWires([Line_6, Line_10, Line_11, Line_12], 1)
        Face_3 = geompy.MakeFaceWires([Line_3, Line_4, Line_5, Line_13], 1)
        Face_4 = geompy.MakeFaceWires([Line_2, Line_6, Line_9, Line_13], 1)
        Section_1 = geompy.MakePartition([Face_1, Face_2, Face_3, Face_4], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)
        Elems_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Elems_1, [2, 12, 21, 30])
        Rnd_Node_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["VERTEX"])
        geompy.UnionIDs(Rnd_Node_1, [5])
        Outer_Lines_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Outer_Lines_1, [4, 9, 11, 16, 18, 20, 23, 26, 28, 32])
        [Elems_1, Rnd_Node_1, Outer_Lines_1] = geompy.GetExistingSubObjects(Section_1, False)
        local_length = min(t1, t2) / 4

    elif sectype == "Angle":
        W1, W2, t1, t2 = secdata[:4]
        Vertex_1 = geompy.MakeVertex(0, 0, 0)
        Vertex_2 = geompy.MakeVertex(t2, 0, 0)
        Vertex_3 = geompy.MakeVertex(W1, 0, 0)
        Vertex_4 = geompy.MakeVertex(0, t1, 0)
        Vertex_5 = geompy.MakeVertex(t2, t1, 0)
        Vertex_6 = geompy.MakeVertex(W1, t1, 0)
        Vertex_7 = geompy.MakeVertex(0, W2, 0)
        Vertex_8 = geompy.MakeVertex(t2, W2, 0)
        Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
        Line_2 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_3)
        Line_3 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_6)
        Line_4 = geompy.MakeLineTwoPnt(Vertex_6, Vertex_5)
        Line_5 = geompy.MakeLineTwoPnt(Vertex_5, Vertex_4)
        Line_6 = geompy.MakeLineTwoPnt(Vertex_4, Vertex_1)
        Line_7 = geompy.MakeLineTwoPnt(Vertex_2, Vertex_5)
        Line_8 = geompy.MakeLineTwoPnt(Vertex_5, Vertex_8)
        Line_9 = geompy.MakeLineTwoPnt(Vertex_8, Vertex_7)
        Line_10 = geompy.MakeLineTwoPnt(Vertex_7, Vertex_4)
        Face_1 = geompy.MakeFaceWires([Line_1, Line_5, Line_6, Line_7], 1)
        Face_2 = geompy.MakeFaceWires([Line_2, Line_3, Line_4, Line_7], 1)
        Face_3 = geompy.MakeFaceWires([Line_5, Line_8, Line_9, Line_10], 1)
        Section_1 = geompy.MakePartition([Face_1, Face_2, Face_3], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)
        Outer_Lines_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Outer_Lines_1, [4, 11, 14, 16, 18, 21, 23, 25])
        Elems_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Elems_1, [2, 12, 19])
        Rnd_Node_1 = geompy.CreateGroup(Section_1, geompy.ShapeType["VERTEX"])
        geompy.UnionIDs(Rnd_Node_1, [5])
        [Outer_Lines_1, Elems_1, Rnd_Node_1] = geompy.GetExistingSubObjects(Section_1, False)
        local_length = min(t1, t2) / 4

    geom_end = time()


    ###
    ### SMESH component
    ###
    Mesh_1 = smesh.Mesh(Section_1)
    if sectype == "Tube":
        Mesh_1.Quadrangle(algo=smeshBuilder.QUAD_MA_PROJ)
    else:
        Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
    Regular_1D = Mesh_1.Segment()
    Regular_1D.LocalLength(local_length, None, 1e-07)
    Mesh_1.GroupOnGeom(Outer_Lines_1, "Outer_Lines_1", SMESH.EDGE)
    if sectype in ("Tube", "Hollow_Rectangle"):
        Mesh_1.GroupOnGeom(Inner_Lines_1, "Inner_Lines_1", SMESH.EDGE)
    Mesh_1.GroupOnGeom(Rnd_Node_1, "Rnd_Node_1", SMESH.NODE)
    isDone = Mesh_1.Compute()
    Mesh_1.GetGroups()
    smesh.SetName(Mesh_1, sectype)

    med_path = os.path.join(case_dir, f"{sectype}.med")
    try:
        Mesh_1.ExportMED(med_path, auto_groups=0, version=40, overwrite=1, meshPart=None, autoDimension=1)
    except:
        raise Exception("ExportMED() failed. Invalid file name?")

    mesh_end = time()
    geom_time = geom_end - geom_start
    mesh_time = mesh_end - geom_end

    if not isDone:
        raise Exception("Modeling failed.")
    else:
        print(" Modeling success".ljust(40), "|", f"Geometry: {geom_time:.2f}s   Mesh: {mesh_time:.2f}s".rjust(40))
