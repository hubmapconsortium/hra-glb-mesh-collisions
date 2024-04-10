# hra-glb-mesh-collisions
A CLI to extract mesh-mesh collision information from GLB files

## Dependencies

For Python library:
1. pygltflib
    ```bash
    pip install pygltflib
    ```

For C++ libraries:

1. [Download CGAL 5.5.3](https://github.com/CGAL/cgal/releases/download/v5.5.3/CGAL-5.5.3.zip)
    Extract the compressed file to the '$ENV{HOME}' folder.

2. CMake
    ```bash
    sudo apt-get install build-essential libssl-dev
    cd /tmp
    wget https://github.com/Kitware/CMake/releases/download/v3.20.0/cmake-3.20.0.tar.gz
    tar -zxvf cmake-3.20.0.tar.gz
    cd cmake-3.20.0
    ./bootstrap
    make
    sudo make install
    ```
3. Boost
    ```bash
    sudo apt-get update
    sudo apt-get install libboost-all-dev
    ```
4. GMP
    ```bash
    sudo apt-get install libgmp-dev
    ```
5. MPFR
    ```bash
    sudo apt-get install libmpfr-dev
    ```
6. Eigen3
    ```bash
    sudo apt install libeigen3-dev
    ```

## Compilation

We use CMake to configure the program with third-party dependencies and generate the native build system by creating a CMakeLists.txt file. 

1. :
    ```bash
    mkdir build
    cd build
    cmake ..
    make
    ```

## Usage
1. convert glb files of 3D models to off (Object File Format) files:
    ```bash
    bash mesh-mesh-collisions.sh --input_glb ./examples/VH_F_Kidney_Left.glb

    ```
    For help documentation
    ```bash
    bash mesh-mesh-collisions.sh --help
    
    ```
2. sample result
```bash
| source | target | distance ( -1 : collision )
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