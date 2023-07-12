#version 330 core

// Input vertex data, different for all executions of this shader.
layout (location = 0) in vec3 in_position;
layout (location = 1) in int voxel_id;
layout (location = 2) in int face_id;
layout (location = 3) in int ao_id;
layout (location = 4) in int flip_id;

// Uniforms for the shader
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

// Output data ; will be interpolated for each fragment.
out vec3 voxel_color;
out vec2 uv;
out float shading;

// Values that stay constant for the whole mesh.
const float ao_values[4] = float[4](0.1, 0.25, 0.5, 1.0);
const float face_shading[6] = float[6](
    1.0, 0.5, 
    0.5, 0.8,
    0.5, 0.8
);

const vec2 uv_coords[4] = vec2[4](
    vec2(0, 0), vec2(0, 1),
    vec2(1, 0), vec2(1, 1)
);

const int uv_indices[24] = int[24](
    1, 0, 2, 1, 2, 3,
    3, 0, 2, 3, 1, 0,
    3, 1, 0, 3, 0, 2,
    1, 2, 3, 1, 0, 2
);


/**
 * @brief 
 * Hash function to generate random numbers from a seed. Produces a vec3 of
 * values between 0 and 1. 
 * @param p Value to hash.
 * @return vec3 Three random values between 0 and 1.
 */ 
vec3 hash31(float p) {
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));

    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}

/**
 * @brief
 * Main function of the shader.
 */
void main() {
    int uv_index = gl_VertexID % 6 + ((face_id & 1) + flip_id * 2) * 6;
    
    uv = uv_coords[uv_indices[uv_index]];
    voxel_color = hash31(voxel_id);
    shading = face_shading[face_id] * ao_values[ao_id];

    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}