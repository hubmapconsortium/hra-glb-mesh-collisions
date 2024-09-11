# hra_glb_mesh_collisions

[![PyPI - Version](https://img.shields.io/pypi/v/hra-glb-mesh-collisions.svg)](https://pypi.org/project/hra-glb-mesh-collisions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hra-glb-mesh-collisions.svg)](https://pypi.org/project/hra-glb-mesh-collisions)

-----

## Table of Contents

- [hra\_glb\_mesh\_collisions](#hra_glb_mesh_collisions)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [License](#license)
  - [Dependencies](#dependencies)
  - [Usage](#usage)

## Installation

```console
pip install hra-glb-mesh-collisions
```

## License

`hra-glb-mesh-collisions` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Dependencies

System packages:

You may need to install libfcl liboctomap if the program does not work right away using this command (on Ubuntu):

```bash
$ sudo apt install liboctomap-dev libfcl-dev
```

For Python library:

1. pygltflib
2. trimesh

Install python dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Example usage:

```bash
python3 mesh-mesh-collisions.py ./examples/VH_F_Kidney_Left.glb collision_result.csv
```

For help documentation:

```bash
$ python3 mesh-mesh-collisions.py --help

usage: mesh-mesh-collisions.py [-h] [--include-distances] [-v] input_glb output_csv

positional arguments:
  input_glb            path to input glb file
  output_csv           path to output collisions csv file

options:
  -h, --help           show this help message and exit
  --include-distances  include distances even if they dont' colide
  -v, --verbose
```

Sample result ouptut csv:

Notes about the distance colum:
- distance is in meters
- -1 = intersection
- distance measured between two closest points

```csv
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
