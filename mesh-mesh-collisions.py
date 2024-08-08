import argparse
import csv
import glob
import os

import numpy as np
import trimesh
from pygltflib import GLTF2
from scipy.spatial import cKDTree
from trimesh.collision import CollisionManager
from trimesh.proximity import closest_point


def glb_plain_parser(input_glb, output_off_dir):
    """
    Parses a GLB file and extracts the mesh data.

    Args:
        input_glb (str): The path to the GLB file.
        output_off_dir (str): The directory to save the extracted mesh data.

    Returns:
        None
    """

    data_type_dict = {5121: 'uint8', 5123: 'uint16',
                      5125: 'uint32', 5126: 'float32'}

    glb = GLTF2.load(input_glb)
    binary_blob = glb.binary_blob()

    for mesh in glb.meshes:

        mesh_name = mesh.name

        triangles_accessor = glb.accessors[mesh.primitives[0].indices]
        triangles_buffer_view = glb.bufferViews[triangles_accessor.bufferView]
        dtype = data_type_dict[triangles_accessor.componentType]

        triangles = np.frombuffer(
            binary_blob[triangles_buffer_view.byteOffset + triangles_accessor.byteOffset:
                        triangles_buffer_view.byteOffset + triangles_buffer_view.byteLength],
            dtype=dtype,
            count=triangles_accessor.count,
        ).reshape((-1, 3))

        points_accessor = glb.accessors[mesh.primitives[0].attributes.POSITION]
        points_buffer_view = glb.bufferViews[points_accessor.bufferView]
        dtype = data_type_dict[points_accessor.componentType]

        points = np.frombuffer(
            binary_blob[points_buffer_view.byteOffset + points_accessor.byteOffset:
                        points_buffer_view.byteOffset + points_buffer_view.byteLength],
            dtype=dtype,
            count=points_accessor.count * 3,
        ).reshape((-1, 3))

        save_single_mesh(points, triangles, mesh_name,
                         output_off_dir)


def save_single_mesh(points, triangles, mesh_name, output_off_dir):
    """
    Save a single mesh in the OFF format.

    Args:
        points (list): List of points in the mesh.
        triangles (list): List of triangles in the mesh.
        mesh_name (str): Name of the mesh.
        output_off_dir (str): Directory to save the mesh file.

    Returns:
        None

    Raises:
        None
    """

    if not os.path.exists(output_off_dir):
        os.makedirs(output_off_dir)

    output_path = os.path.join(output_off_dir, mesh_name + '.off')

    with open(output_path, 'w') as f:
        f.write("OFF\n")
        f.write("{} {} 0\n".format(len(points), len(triangles)))

        for point in points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))

        for triangle in triangles:
            f.write("3 {} {} {}\n".format(
                triangle[0], triangle[1], triangle[2]))

        print("  {} has {} points, {} triangle faces".format(
            mesh_name, len(points), len(triangles)))


def clean_folder(temp_off_dir):
    """
    Remove all files and directories within the specified directory.

    Parameters:
    - temp_off_dir (str): The path to the directory to be cleaned.

    Returns:
    None
    """

    if os.path.exists(temp_off_dir):
        for filename in os.listdir(temp_off_dir):
            file_path = os.path.join(temp_off_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.removedirs(temp_off_dir)


def compute_collision(input_off_dir, output_csv):
    """
    Compute collisions between meshes in the given input directory and write the results to a CSV file.

    Parameters:
    - input_off_dir (str): The directory path containing the input .off files.
    - output_csv (str): The path of the output CSV file.

    Returns:
    None
    """

    # Create a pattern to match all .off files
    pattern = input_off_dir + '/*.off'
    # Use glob to find all files in the folder that match the pattern
    off_files = glob.glob(pattern)
    meshes = []
    file_names = []
    manager = CollisionManager()

    for off_file in off_files:
        # Extract the filename without the path and extension
        file_name = os.path.basename(off_file).replace('.off', '')
        mesh = trimesh.load(off_file, file_type='off')
        meshes.append(mesh)
        file_names.append(file_name)

    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['source', 'target', 'distance'])

        for i in range(len(meshes)):
            print(file_names[i])
            for j in range(i + 1, len(meshes)):
                manager.add_object(file_names[i], meshes[i])
                manager.add_object(file_names[j], meshes[j])
                collision = manager.in_collision_internal(return_names=False)
                manager.remove_object(file_names[i])
                manager.remove_object(file_names[j])
                if collision:
                    writer.writerow([file_names[i], file_names[j], '-1'])
                else:
                    # closest_points, distances, _ = closest_point(meshes[j], meshes[i].vertices)
                    v1, v2 = meshes[i].vertices, meshes[j].vertices
                    tree2 = cKDTree(v2)
                    dists12, _ = tree2.query(v1, k=1)
                    writer.writerow(
                        [file_names[i], file_names[j], min(dists12)])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('input_glb', help="path to input glb file")
    parser.add_argument(
        'output_csv', help="path to output collisions csv file")

    args = parser.parse_args()
    input_glb = args.input_glb
    output_csv = args.output_csv
    temp_off_dir = args.output_csv + '__temp'

    clean_folder(temp_off_dir)

    if not os.path.exists(temp_off_dir):
        os.mkdir(temp_off_dir)

    glb_plain_parser(input_glb, temp_off_dir)

    compute_collision(temp_off_dir, output_csv)

    clean_folder(temp_off_dir)
