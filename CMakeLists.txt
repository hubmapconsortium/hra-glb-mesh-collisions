cmake_minimum_required(VERSION 3.9)
project(HTTP_SERVICE)

set(CMAKE_BUILD_TYPE "Release")
set(CGAL_DIR "$ENV{HOME}/CGAL-5.5.3")


find_package(CGAL REQUIRED)
find_package (Eigen3 REQUIRED NO_MODULE)
find_package(Boost 1.45.0 COMPONENTS filesystem)

set(Boost_USE_STATIC_LIBS OFF) 
set(Boost_USE_MULTITHREADED ON)  
set(Boost_USE_STATIC_RUNTIME OFF) 


add_executable(compute_collision main.cpp)

file(GLOB GEOMETRY_SRC_FILES geometry/*.cpp)
add_library(geometry ${GEOMETRY_SRC_FILES})
target_include_directories(geometry PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/geometry)
target_link_libraries(geometry PUBLIC Eigen3::Eigen)

target_link_libraries(geometry PUBLIC CGAL::CGAL)
# target_link_libraries(geometry PUBLIC ${CGAL_LIBRARIES} ${CGAL_3RD_PARTY_LIBRARIES})

target_link_libraries(compute_collision Eigen3::Eigen)
target_link_libraries(compute_collision CGAL::CGAL)
target_link_libraries(compute_collision geometry)





if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS}) 
    target_link_libraries(compute_collision ${Boost_LIBRARIES})
endif()



