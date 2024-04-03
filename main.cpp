#include "mymesh.h"

#include <time.h>
#include <iostream>
//#include <iomanip>
#include <sys/time.h>

#include <fstream>
#include <sstream>
#include <vector>
#include <filesystem>




// Function to compute minimum distance between vertex-pairs of two Surface_mesh objects
double computeMinimumDistance(const Surface_mesh& mesh1, const Surface_mesh& mesh2) {
    double minDistance = std::numeric_limits<double>::max();

    // Iterate over all vertices of the first mesh
    for (auto v1 : mesh1.vertices()) {
        Point p1 = mesh1.point(v1);

        // Iterate over all vertices of the second mesh
        for (auto v2 : mesh2.vertices()) {
            Point p2 = mesh2.point(v2);

            // Compute the distance between the current pair of vertices
            double dist = std::sqrt(CGAL::squared_distance(p1, p2));

            // Update the minimum distance if necessary
            if (dist < minDistance)
                minDistance = dist;
        }
    }

    return minDistance;
}


int main(int argc, char **argv)
{
    srand( (unsigned)time( NULL ) );


    struct timeval start, end;
    long long microseconds;
    gettimeofday(&start, nullptr);

    

    // Open the CSV file for writing
    std::ofstream outputFile("output.csv");
    if (!outputFile.is_open()) {
        std::cerr << "Error: Unable to open output.csv for writing." << std::endl;
        return 1;
    }

    // Write header to CSV file
    outputFile << "source, target, distance" << std::endl;
  

    std::vector<Mymesh> meshes;
    std::vector<std::string> meshIDs;

    std::string directoryPath = "./temp-model-off";
    std::cout << "\n------------------------------------------------\n" << std::endl;

    std::cout << "Loading mesh: " << std::endl;

    // Iterate over all files in the specified directory
    for (const auto& entry : std::filesystem::directory_iterator(directoryPath)) {
        std::string filename = entry.path().filename().string();
        // Check if the file has a .off extension
        if (filename.size() > 4 && filename.substr(filename.size() - 4) == ".off") {
            // Store the file path
            std::string filePath = entry.path().string();

            // Process the .off file
            //processOffFile(filePath);
            meshes.push_back(Mymesh(filePath));
            meshIDs.push_back(filename);
            std::cout << "  " << filePath.substr(0, filePath.size() - 4)<< std::endl;
        }
    }

    std::cout << "mesh number: " << meshes.size() << std::endl;
    for (Mymesh &mesh: meshes) mesh.create_aabb_tree();

    // Compare each pair of meshes
    for (size_t i = 0; i < meshes.size(); ++i) {
        for (size_t j = i + 1; j < meshes.size(); ++j) {
            //const auto& meshA = meshes[i];
            //const auto& meshB = meshes[j];

            const auto aabbtreeA = meshes[i].get_aabb_tree();
            const auto aabbtreeB = meshes[j].get_aabb_tree();

            // Check if meshes intersect
            if (aabbtreeA->do_intersect(*aabbtreeB)) {
                // If meshes intersect, set minimum distance to -1
                outputFile << meshIDs[i] << "," << meshIDs[j] << ",-1" << std::endl;
            } else {
                // If meshes do not intersect, compute minimum distance between vertex-pairs
                double minDistance = computeMinimumDistance(meshes[i].get_raw_mesh(), meshes[j].get_raw_mesh());

                outputFile << meshIDs[i] << "," << meshIDs[j] << "," << std::setprecision(12) << minDistance << std::endl;
            }
        }
    }

    // Close the CSV file
    outputFile.close();

    // Construct the command to delete the folder and its contents
    std::string command = "rm -r ./temp-model-off";

    // Execute the command using system()
    int result = std::system(command.c_str());

    if (result == 0) {
        std::cout << "\ntemp-model-off folder deleted successfully." << std::endl;
    } else {
        std::cerr << "Error deleting temp-model-off folder." << std::endl;
    }

    std::cout << "CSV file created successfully." << std::endl;


    //
    gettimeofday(&end, nullptr);
    microseconds = (end.tv_sec - start.tv_sec) * 1000000LL + (end.tv_usec - start.tv_usec);
    // Print the elapsed time
    std::cout << "---------------main.cpp---------------Time elapsed: " << microseconds << " microseconds" << std::endl << std::endl << std::endl;


}


