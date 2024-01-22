import utils
import os
import trimesh
import sys



def read_all_off_files(directory_path):
    # Ensure the directory path ends with a slash
    directory_path = directory_path.rstrip('/') + '/'
    
    print(directory_path)

    # List all files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    for f in files:
    	print(f)

    # Filter only .off files
    off_files = [f for f in files if f.lower().endswith('.off')]
    
    name_list = []
    mesh_list = []

    # # Read each .off file
    for off_file in off_files:
    	file_path = os.path.join(directory_path, off_file)
    	mesh = trimesh.load_mesh(file_path)
    	print('mesh read successfully')
    	name_list.append(off_file.replace(".off", ""))
    	mesh_list.append(mesh)
    print(len(mesh_list))

    return name_list, mesh_list


if __name__ == "__main__":


	if (len(sys.argv) < 2) :
		# Example usage:
		print(f"Example usage: python computer_collision.py /path/to/your/directory")

	if (len(sys.argv) == 2) :
		directory_path = sys.argv[1] #'D:/project/lcrcorridor/lcr-github/hra-glb-mesh-collisions/examples'

		print(len(sys.argv))
		name_list, mesh_list = read_all_off_files(directory_path)

		print(f"| node_id | target_id | minimum_distance ( -1 : collision )")

		for i in range(len(mesh_list)):
			for j in range(i + 1, len(mesh_list)):
				if (utils.collision_test(mesh_list[i], mesh_list[j])):
					print(f"{name_list[i]} | {name_list[j]} | -1 ")
				else:
					print(f"{name_list[i]} | {name_list[j]} | {utils.compute_minimum_distance(mesh_list[i], mesh_list[j])} ")