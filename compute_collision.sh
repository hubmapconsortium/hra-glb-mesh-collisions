echo "First argument: $1"
echo "Second argument: $2"


first_arg=$1
second_arg=$2

python3 glb_parser.py $first_arg $second_arg; 
./build/compute_collision;




