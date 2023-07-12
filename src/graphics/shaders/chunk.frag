#version 330 core

// Input data ; passed from vertex shader
layout (location = 0) out vec4 fragColor;

// Constants
const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

// Uniforms from application
uniform sampler2DArray u_texture_array_0;

// Inputs from vertex shader
in vec2 uv;
in float shading;

// Flat inputs from vertex shader
flat in int face_id;
flat in int block_id;

/**
 * @brief
 * Main fragment shader entry point.
 */
void main() {
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, block_id)).rgb;
    tex_col = pow(tex_col, gamma);
    tex_col *= shading;
    tex_col = pow(tex_col, inv_gamma);

    fragColor = vec4(tex_col, 1.0);
}