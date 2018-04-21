# vtk_mesh_io

A simple VTK mesh reader and writer

This is how to use it

```
import vtk_mesh_io as vtkio

# mesh will be a dictionary, where mesh["points"] is an array with vertices and
# mesh["polygons"] is an array of triplets of vertex indices
mesh = vtkio.read_vtk_mesh("data/brain.vtk")

# to write a VTK mesh, just provide arrays of vertices, triangles, and a path
vtkio.write_vtk_mesh(mesh["points"], mesh["polygons"], "test/brain_output.vtk")
```

The code passes `pylint` and uses `pytest` for running test.
