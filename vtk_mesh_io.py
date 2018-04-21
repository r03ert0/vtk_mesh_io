"""Read and Write ASCII-encoded triangular VTK mesh files. Nothing less nothing more.
"""

import re

def read_points(rows, index):
    """Read 3-d points in a VTK mesh file

    Parameters
    ----------
    rows : array
        rows of the VTK file
    index: int
        index of the row where the POINT data starts

    Returns
    -------
    points : array
        An array of 3-d coordinates

    """
    cols = rows[index].split(' ')
    npoints = int(cols[1])
    irow = index + 1
    npsum = 0
    points = []
    while npsum < npoints:
        cols = re.findall(r'[-\.\de]+', rows[irow])
        for j in range(0, len(cols), 3):
            points.append([float(cols[j]), float(cols[j+1]), float(cols[j+2])])
            npsum = npsum + 1
        irow = irow + 1

    return points

def read_polygons(rows, index):
    """Read triangles in a VTK mesh file

    Parameters
    ----------
    rows : array
        rows of the VTK file
    index: int
        index of the row where the POLYGONS data starts

    Returns
    -------
    polygons : array
        An array of triplets of indices to POINTS

    """
    cols = rows[index].split(' ')
    npolygons = int(cols[1])
    irow = index + 1
    npsum = 0
    polygons = []
    while npsum < npolygons:
        cols = re.findall(r'\d+', rows[irow])
        for j in range(0, len(cols), 4):
            if int(cols[j]) == 3:
                polygons.append([int(cols[j+1]), int(cols[j+2]), int(cols[j+3])])
            else:
                print("ERROR: Mesh contains non-triangular faces")
            npsum = npsum + 1
        irow = irow + 1

    return polygons

def read_vtk_mesh(path):
    """Read a triangular VTK mesh file

    Parameters
    ----------
    path : string
        path to an ASCII encoded, triangular VTK mesh file

    Returns
    -------
    mesh : dictionary
        A dictionary containing the points and vertices of the VTK
        mesh file. The elements of the dictionary are:
        version: the version of the VTK file
        encoding: the encoding of the file, should be ASCII
        points: an array of 3-d coordinates
        polygons: an array of triplets of vertex indices
    """
    file = open(path, "r")
    txt = file.read()
    file.close()
    rows = txt.split('\n')

    mesh = {}
    mesh["version"] = rows[0]
    mesh["encoding"] = rows[2]
    if mesh["encoding"] != "ASCII":
        print("ERROR: File encoding is not ASCII")

    nrows = len(rows)
    for i in range(nrows):
        cols = rows[i].split(' ')
        if cols[0] == "POINTS":
            mesh["points"] = read_points(rows, i)
        if cols[0] == "POLYGONS":
            mesh["polygons"] = read_polygons(rows, i)

    return mesh

def write_vtk_mesh(points, triangles, path):
    """Writes a triangular mesh in ASCII VTK format

    Parameters
    ----------
    points: array
        array of 3-d coordinates
    triangles: array
        array of triplets of vertex indices, 0 based
    path : string
        path where the VTK mesh file should be saved
    """
    file = open(path, "w")
    file.write("# vtk DataFile Version 3.0\n")
    file.write("vtk output\n")
    file.write("ASCII\n")
    file.write("DATASET POLYDATA\n")

    # write points
    file.write("POINTS {npoints} float\n".format(npoints=len(points)))
    for i in range(0, len(points)):
        file.write("{x} {y} {z}\n".format(x=points[i][0], y=points[i][1], z=points[i][2]))

    # write polygons
    file.write("POLYGONS {npolygons} {nindices}\n".format(
        npolygons=len(triangles),
        nindices=len(triangles)*4)
              )
    for i in range(0, len(triangles)):
        file.write("3 {x} {y} {z}\n".format(
            x=triangles[i][0],
            y=triangles[i][1],
            z=triangles[i][2])
                  )

    file.close()
