# hra-glb-mesh-collisions
A CLI to extract mesh-mesh collision information from GLB files

## Dependencies

For Python library:
1. pygltflib
    ```bash
    pip install pygltflib
    ```

2. trimesh
    ```bash
    pip install trimesh
    ```

## Usage
1. convert glb files of 3D models to off (Object File Format) files:
    ```bash
    cd $glbparser
    python glb_parser.py --input_dir input_dir_3D_model_glb --output_dir output_dir_3D_model_off
    ```

2. generate mesh_collision_matrix
    ```bash
    cd $compute_collision
    python compute_collision.py /path/to/your/offfile/directory
    ```
3. sample result
```bash
| node_id | target_id | minimum_distance ( -1 : collision )
VH_F_renal_pyramid_L_b | VH_F_renal_pyramid_L_c | 0.00581706732973548
VH_F_renal_pyramid_L_b | VH_F_renal_pyramid_L_h | 0.033958358068466095
VH_F_renal_pyramid_L_b | VH_F_renal_pyramid_L_i | 0.036266068238102786
VH_F_renal_pyramid_L_b | VH_F_renal_pyramid_L_k | 0.056490684201869
VH_F_renal_pyramid_L_c | VH_F_renal_pyramid_L_h | 0.04081904008643359
VH_F_renal_pyramid_L_c | VH_F_renal_pyramid_L_i | 0.050566784682148945
VH_F_renal_pyramid_L_c | VH_F_renal_pyramid_L_k | 0.0653510531862599
VH_F_renal_pyramid_L_h | VH_F_renal_pyramid_L_i | 0.0034600071016649284
VH_F_renal_pyramid_L_h | VH_F_renal_pyramid_L_k | 0.017098977841348874
VH_F_renal_pyramid_L_i | VH_F_renal_pyramid_L_k | 0.002434104111354548
```