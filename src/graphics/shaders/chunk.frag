#version 330 core

// Input data ; passed from vertex shader
layout (location = 0) out vec4 fragColor;

// Constants
const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

// Uniforms from application
uniform sampler2D u_texture_0;

// Inputs from vertex shader
in vec3 block_color;
in vec2 uv;
in float shading;

/**
 * @brief
 * Main fragment shader entry point.
 */
void main() {
    vec3 tex_col = texture(u_texture_0, uv).rgb;
    tex_col = pow(tex_col, gamma);

    tex_col.rgb *= block_color;
    tex_col *= shading;

    tex_col = pow(tex_col, inv_gamma);
    fragColor = vec4(tex_col, 1.0);
}