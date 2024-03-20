import argparse
import numpy as np
import os
from pygltflib import GLTF2


def glb_plain_parser(input_glb, output_dir):

    # file = "C:/Users/catherine/Desktop/Research/ccf-releases/v1.1/models/" + organ + '.glb'
    #file = os.path.join(input_dir, organ + '.glb')
    #file = os.path.join(input_glb, organ + '.glb')
    data_type_dict = {5121: 'uint8', 5123: 'uint16', 5125: 'uint32', 5126: 'float32'}
    number_of_components = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT2': 4, 'MAT3': 9, 'MAT4': 16}

    glb = GLTF2.load(input_glb)
    binary_blob = glb.binary_blob()
    #output_organ_dir = os.path.join(output_dir, organ)

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

        save_single_mesh(points, triangles, mesh_name, output_dir)#output_organ_dir)


def save_single_mesh(points, triangles, mesh_name, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, mesh_name + '.off')

    with open(output_path, 'w') as f:
        f.write("OFF\n")
        f.write("{} {} 0\n".format(len(points), len(triangles)))

        for point in points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))

        for triangle in triangles:
            f.write("3 {} {} {}\n".format(triangle[0], triangle[1], triangle[2]))

        print("  {} has {} points, {} triangle faces".format(mesh_name, len(points), len(triangles)))


if __name__ == "__main__":
    # input_dir = "../../ccf-releases/v1.3/models/"
    # output_dir = "../../models/plain"
    # folder_name = "temp-model-off"

    # # Check if the folder already exists, and if not, create it
    # if not os.path.exists(folder_name):
    #     os.mkdir(folder_name)
    #     print(f"Temporal folder '{folder_name}' created successfully.\n")
    # else:
    #     print(f"Temporal folder '{folder_name}' already exists.\n")  

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_glb', type=str, help="input file path of the glb file", default="./model-glb")   #../../ccf-releases/v1.3/models/")
    #parser.add_argument('--output_dir', type=str, help="output directory of off files", default="./temp-model-off")
    args = parser.parse_args()

    #print(f'{folder_name}'"\n")

    input_glb = args.input_glb
    #output_dir = args.output_dir
    output_dir = "./temp-model-off"
    #files = os.listdir(input_glb)

    #for f in files:
        #if f.endswith('.glb'):
            #print(f)

            #organ = f[:-4]
            #print(organ)
            #print("start parsing {}\n".format(organ))

    glb_plain_parser(input_glb, output_dir)

            #print("end parsing {}\n".format(organ))

    # if os.path.exists(folder_name):
    #     os.rmdir(folder_name)
    #     print(f"Temporal folder '{folder_name}' removed successfully.\n")       







