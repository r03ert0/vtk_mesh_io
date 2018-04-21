"""Test vtk_mesh_io.py
"""

import os
import vtk_mesh_io as vtkio

def test_read_points():
    """Test that the number of points read from the test mesh is correct"""
    mesh = vtkio.read_vtk_mesh("data/brain.vtk")
    assert len(mesh["points"]) == 744

def test_read_triangles():
    """Test that the number of polygons read from the test mesh is correct"""
    mesh = vtkio.read_vtk_mesh("data/brain.vtk")
    assert len(mesh["polygons"]) == 1484

def test_write():
    """Test that mesh writing does produce a file"""
    mesh = vtkio.read_vtk_mesh("data/brain.vtk")
    vtkio.write_vtk_mesh(mesh["points"], mesh["polygons"], "test/brain_output.vtk")
    assert os.path.isfile("test/brain_output.vtk")
