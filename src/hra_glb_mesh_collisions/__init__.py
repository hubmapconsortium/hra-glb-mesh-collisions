#!/usr/bin/env python
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


def glb_plain_parser(input_glb, output_off_dir, verbose=False):
    """
    Parses a GLB file and extracts mesh data, saving it as OFF files.

    Args:
        input_glb (str): Path to the input GLB file.
        output_off_dir (str): Directory to save the extracted OFF files.
        verbose (bool): If True, print detailed information during processing.
    """
    data_type_dict = {5121: "uint8", 5123: "uint16", 5125: "uint32", 5126: "float32"}

    glb = GLTF2.load(input_glb)
    binary_blob = glb.binary_blob()

    for mesh in glb.meshes:
        mesh_name = mesh.name

        triangles_accessor = glb.accessors[mesh.primitives[0].indices]
        triangles_buffer_view = glb.bufferViews[triangles_accessor.bufferView]
        dtype = data_type_dict[triangles_accessor.componentType]

        triangles = np.frombuffer(
            binary_blob[
                triangles_buffer_view.byteOffset
                + triangles_accessor.byteOffset : triangles_buffer_view.byteOffset
                + triangles_buffer_view.byteLength
            ],
            dtype=dtype,
            count=triangles_accessor.count,
        ).reshape((-1, 3))

        points_accessor = glb.accessors[mesh.primitives[0].attributes.POSITION]
        points_buffer_view = glb.bufferViews[points_accessor.bufferView]
        dtype = data_type_dict[points_accessor.componentType]

        points = np.frombuffer(
            binary_blob[
                points_buffer_view.byteOffset
                + points_accessor.byteOffset : points_buffer_view.byteOffset
                + points_buffer_view.byteLength
            ],
            dtype=dtype,
            count=points_accessor.count * 3,
        ).reshape((-1, 3))

        save_single_mesh(points, triangles, mesh_name, output_off_dir, verbose)


def save_single_mesh(points, triangles, mesh_name, output_off_dir, verbose=False):
    """
    Saves a single mesh as an OFF file.

    Args:
        points (np.ndarray): Array of mesh points.
        triangles (np.ndarray): Array of mesh triangles.
        mesh_name (str): Name of the mesh.
        output_off_dir (str): Directory to save the OFF file.
        verbose (bool): If True, print detailed information during processing.
    """
    if not os.path.exists(output_off_dir):
        os.makedirs(output_off_dir)

    output_path = os.path.join(output_off_dir, mesh_name + ".off")

    with open(output_path, "w") as f:
        f.write("OFF\n")
        f.write("{} {} 0\n".format(len(points), len(triangles)))

        for point in points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))

        for triangle in triangles:
            f.write("3 {} {} {}\n".format(triangle[0], triangle[1], triangle[2]))

        if verbose:
            print(
                "  {} has {} points, {} triangle faces".format(
                    mesh_name, len(points), len(triangles)
                )
            )


def clean_folder(temp_off_dir, create_dir=False):
    """
    Cleans a folder by removing all files and optionally recreates the directory.

    Args:
        temp_off_dir (str): Path to the directory to clean.
        create_dir (bool): If True, recreate the directory after cleaning.
    """
    if os.path.exists(temp_off_dir):
        for filename in os.listdir(temp_off_dir):
            file_path = os.path.join(temp_off_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.removedirs(temp_off_dir)

    if create_dir:
        os.mkdir(temp_off_dir)


def compute_collision(
    input_off_dir, output_csv, include_distances=False, verbose=False
):
    """
    Computes collisions between meshes and saves the results to a CSV file.

    Args:
        input_off_dir (str): Directory containing the input OFF files.
        output_csv (str): Path to the output CSV file.
        include_distances (bool): If True, include distances between non-colliding meshes.
        verbose (bool): If True, print detailed information during processing.
    """
    # Create a pattern to match all .off files
    pattern = input_off_dir + "/*.off"
    # Use glob to find all files in the folder that match the pattern
    off_files = list(sorted(glob.glob(pattern)))
    meshes = []
    file_names = []
    manager = CollisionManager()

    for off_file in off_files:
        # Extract the filename without the path and extension
        file_name = os.path.basename(off_file).replace(".off", "")
        mesh = trimesh.load(off_file, file_type="off")
        meshes.append(mesh)
        file_names.append(file_name)
        manager.add_object(file_name, mesh)

    with open(output_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["source", "target", "distance"])

        collisions, collided = manager.in_collision_internal(return_names=True)
        if collisions:
            for mesh_a, mesh_b in collided:
                writer.writerow([mesh_a, mesh_b, "-1"])

        if include_distances:
            collided = list(map(lambda x: tuple(sorted(x)), collided))
            for i in range(len(meshes)):
                if verbose:
                    print(file_names[i])

                for j in range(i + 1, len(meshes)):
                    if (file_names[i], file_names[j]) not in collided:
                        # closest_points, distances, _ = closest_point(meshes[j], meshes[i].vertices)
                        v1, v2 = meshes[i].vertices, meshes[j].vertices
                        tree2 = cKDTree(v2)
                        dists12, _ = tree2.query(v1, k=1)
                        writer.writerow([file_names[i], file_names[j], min(dists12)])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-distances",
        action="store_true",
        help="include distances even if they dont' colide",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("input_glb", help="path to input glb file")
    parser.add_argument("output_csv", help="path to output collisions csv file")

    args = parser.parse_args()
    input_glb = args.input_glb
    output_csv = args.output_csv
    temp_off_dir = args.output_csv + "__temp"

    clean_folder(temp_off_dir, True)

    glb_plain_parser(input_glb, temp_off_dir, verbose=args.verbose)
    compute_collision(
        temp_off_dir,
        output_csv,
        include_distances=args.include_distances,
        verbose=args.verbose,
    )

    clean_folder(temp_off_dir)

if __name__ == "__main__":
    main()
