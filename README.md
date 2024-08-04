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
1. start the program and generate OUTPUT.csv result file:
    ```bash
    python3 mesh-mesh-collisions.py --input_glb ./examples/VH_F_Kidney_Left.glb

    ```
    For help documentation
    ```bash
    python3 mesh-mesh-collisions.py --help
    
    ```
2. sample result OUTPUT.csv
- distance in meters
- -1 = intersection
- distance measured between two closest points
```bash
source,target,distance
VHF_hilum_of_kidney_L,VHF_kidney_capsule_L,-1
VHF_hilum_of_kidney_L,VHF_major_calyx_L_a,-1
VHF_hilum_of_kidney_L,VHF_major_calyx_L_b,0.0014157565638410548
VHF_hilum_of_kidney_L,VHF_major_calyx_L_c,-1
VHF_hilum_of_kidney_L,VHF_major_calyx_L_d,-1
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_a,0.011878771067593177
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_b,0.014892350577084101
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_c,0.01049842653752553
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_d,0.013852964218697942
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_e,-1
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_f,0.0003293750826728972
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_g,0.0013917394770369632
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_h,0.002076302121193277
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_i,0.0001650410537290576
VHF_hilum_of_kidney_L,VHF_minor_calyx_L_j,0.0026597163618629024
```
