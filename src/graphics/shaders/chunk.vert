#version 330 core

// Input vertex data, different for all executions of this shader.
layout(location = 0) in uint packed_data;

// Global variables
int x, y, z;
int block_id;
int face_id;
int ao_id;
int flip_id;

// Uniforms for the projection matrices
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

// Output data; will be interpolated for each fragment.
out vec3 block_color;
out vec2 uv;
out float shading;

// Constants
const float ao_values[4] = float[4](0.1, 0.25, 0.25, 1.0);
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

// Functions
/**
 * @brief
 * Hash function to get a random value between 0 and 1
 * @param p Value to hash
 * @return vec3 Vector of 3 random values
 */
vec3 hash31(float p) {
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));

    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yxx) * p3.zyx) + 0.05;
}

/**
 * @brief
 * Unpacks the data from the packed_data variable
 * @param packed_data Data to unpack
 */
void unpack(uint packed_data) {
    uint b_bit = 6u, c_bit = 6u, d_bit = 8u, e_bit = 3u, f_bit = 2u, g_bit = 1u;
    uint b_mask = 63u, c_mask = 63u, d_mask = 255u, e_mask = 7u;
    uint f_mask = 3u, g_mask = 1u;

    // Bit positions of the values to unpack
    uint fg_bit = f_bit + g_bit;
    uint efg_bit = e_bit + fg_bit;
    uint defg_bit = d_bit + efg_bit;
    uint cdefg_bit = c_bit + defg_bit;
    uint bcdefg_bit = b_bit + cdefg_bit;

    // Values to unpack
    x = int(packed_data >> bcdefg_bit);
    y = int((packed_data >> cdefg_bit) & b_mask);
    z = int((packed_data >> defg_bit) & c_mask);
    block_id = int((packed_data >> efg_bit) & d_mask);
    face_id = int((packed_data >> fg_bit) & e_mask);
    ao_id = int((packed_data >> g_bit) & f_mask);
    flip_id = int(packed_data & g_mask);
}

/**
 * @brief
 * Main function of the vertex shader
 */
void main() {
    unpack(packed_data);
    vec3 in_position = vec3(x, y, z);
    int uv_index = int(gl_VertexID % 6) + ((face_id & 1) + flip_id * 2) * 6;

    uv = uv_coords[uv_indices[uv_index]];
    block_color = hash31(float(block_id));
    shading = face_shading[face_id] * ao_values[ao_id];

    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}
    