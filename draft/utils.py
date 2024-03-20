import numpy as np
import trimesh



def is_point_inside_plane(point_to_test, face_vertice1, plane_normal, tolerance=1e-10):
    # Vector from a point on the plane to the point to test
    vector_to_test = point_to_test - face_vertice1

    # Dot product of the normal vector and the vector to the test point
    dot_product = np.dot(plane_normal, vector_to_test)

    return np.abs(dot_product) < tolerance  # Tolerance for numerical imprecision


def is_line_parallel_to_plane(line_direction, plane_normal, tolerance=1e-10):
    # Check if the dot product is close to 0 (indicating parallelism)
    dot_product = np.dot(line_direction, plane_normal)
    return np.abs(dot_product) < tolerance


#test if a line segment intersect a face
def compute_line_segment_plane_intersection_point(line_vertice_A, line_vertice_B, face_vertice1, plane_normal, tolerance=1e-10):
    line_direction = line_vertice_B - line_vertice_A
    dot_product = np.dot(line_direction, plane_normal)             

    if np.abs(dot_product) > tolerance: #the line segment is not parallel to the plane
        # The factor of the point between A -> B (0 - 1)
        # if 'fac' is between (0 - 1) the point intersects with the segment.
        # Otherwise:
        #  < 0.0: behind A.
        #  > 1.0: infront of B.
        temp_vector = line_vertice_A - face_vertice1
        factor = - (np.dot(plane_normal, temp_vector)) / dot_product
        #print(f"The factor is  {factor}.")

        if (factor > 0.0 and factor < 1.0): 
            # the intersection point is on the line segment
            return line_vertice_A + (line_direction * factor)

    # The intersection point is not on the line segment or The line segment is parallel to plane.
    return None


def is_point_inside_triangle(point_to_test, triangle_vertice1, triangle_vertice2, triangle_vertice3):
    v0 = triangle_vertice3 - triangle_vertice1
    v1 = triangle_vertice2 - triangle_vertice1
    v2 = point_to_test - triangle_vertice1

    #compute doc product
    dot00 = np.dot(v0, v0)
    dot01 = np.dot(v0, v1)
    dot02 = np.dot(v0, v2)
    dot11 = np.dot(v1, v1)
    dot12 = np.dot(v1, v2)

    # Compute barycentric coordinates
    invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * invDenom
    v = (dot00 * dot12 - dot01 * dot02) * invDenom

    return (u >= 0) and (v >= 0) and (u + v <= 1)
    

def line_segment_triangle_collision_test(line_vertice_A, line_vertice_B, triangle_vertice1, triangle_vertice2, triangle_vertice3,):

    line_vertice_a = line_vertice_A
    line_vertice_b = line_vertice_B

    point1 = triangle_vertice1
    point2 = triangle_vertice2
    point3 = triangle_vertice3

    plane_normal = np.cross(point2 - point1, point3 - point1)
    #line_direction = line_vertice_b - line_vertice_a

    # is A inside the plane
    if is_point_inside_plane(line_vertice_a, point1, plane_normal):
        # is B inside the plane
        if is_point_inside_plane(line_vertice_b, point1, plane_normal):#line segment AB is inside the plane
            #test if A or B is inside or intersects triangle
            if is_point_inside_triangle(line_vertice_a, point1, point2, point3) or is_point_inside_triangle(line_vertice_b, point1, point2, point3):

                # A or B is inside the triangle, 2 faces intersect!!!
                return True
            # A and B are not inside triangle but on the plane, not intersect
            return False

        else:#only A is inside the plane

            if (is_point_inside_triangle(line_vertice_a, point1, point2, point3)):# A is inside the triangle
                # A is inside the triangle. 2 faces intersect!!!
                return True
            else:# A is not inside the triangle. 
                # line segment does not intersect triangle!
                return False

    # A is not inside the plane, test if B is inside the plane
    elif is_point_inside_plane(line_vertice_b, point1, plane_normal):
        #is point B inside the triangle? If yes, RETURN, 2 faces intersect! If no, return, line segment does not intersect triangle!
        
        #only B is inside the plane
        # test if B is inside the triangle.
        if (is_point_inside_triangle(line_vertice_b, point1, point2, point3)):
            # B is inside the triangle. 2 faces intersect!!!
            return True
        else:# B is not inside the triangle but in the plane.
            #line segment does not intersect triangle!
            return False

    # A and B are not in the plane, return the intersection point if that point is on the line segment
    result = compute_line_segment_plane_intersection_point(line_vertice_a, line_vertice_b, point1, plane_normal)

    if result is not None :
        #intersection point is on the line segment

        #test if the intersection point is inside the triangle
        if (is_point_inside_triangle(result, point1, point2, point3)):
            return True

    else:#intersection point is not on the line segment or the line segment is parallel to the plane,
        #so the line segment and the triangle do not intersect
        return False



def collision_test(first_mesh, second_mesh):

    #intersections = 0
    mesh1 = first_mesh
    mesh2 = second_mesh

    #print(mesh1.is_watertight)

    # Iterate through faces and check if the point is contained in each face
    for face1 in mesh1.faces:
        face1_vertices = mesh1.vertices[face1]  # Get the vertices of the face

        for face2 in mesh2.faces:
            face2_vertices = mesh2.vertices[face2]

            line_vertice_a = np.array(face1_vertices[0])
            line_vertice_b = np.array(face1_vertices[1])
            line_vertice_c = np.array(face1_vertices[2])


            point1 = np.array(face2_vertices[0])
            point2 = np.array(face2_vertices[1])
            point3 = np.array(face2_vertices[2])

            # test 5 lines
            if (line_segment_triangle_collision_test(line_vertice_a, line_vertice_b, point1, point2, point3) or 
                line_segment_triangle_collision_test(line_vertice_a, line_vertice_c, point1, point2, point3) or 
                line_segment_triangle_collision_test(line_vertice_b, line_vertice_c, point1, point2, point3) or 
                line_segment_triangle_collision_test(point1, point2, line_vertice_a, line_vertice_b, line_vertice_c) or 
                line_segment_triangle_collision_test(point1, point3, line_vertice_a, line_vertice_b, line_vertice_c)):
                return True

    return False

def compute_minimum_distance(first_mesh, second_mesh):
    min_distance = 1000000.0

    mesh1 = first_mesh
    mesh2 = second_mesh

    for vertice1 in mesh1.vertices:
        for vertice2 in mesh2.vertices:

            distance = np.linalg.norm(vertice1 - vertice2)
            min_distance = np.minimum(min_distance, distance)

    return min_distance


# pointX = np.array([12.3845, -6.78, 7.5355])
# pointY = np.array([2.3925, 20.28, 9.1823])
# print(np.linalg.norm(pointY - pointX))


# squared_dist = np.sum((pointX-pointY)**2, axis=0)
# dist = np.sqrt(squared_dist)
# print(f"using 2nd method {dist}")



#mesh1 = trimesh.load_mesh('D:/project/lcrcorridor/VH_F_Kidney_L/VH_F_renal_pyramid_L_c.off')
#mesh2 = trimesh.load_mesh('D:/project/lcrcorridor/VH_F_Kidney_L/VH_F_renal_pyramid_L_d.off')

#print(compute_minimum_distance(mesh1, mesh2))













