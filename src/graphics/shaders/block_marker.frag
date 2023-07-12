#version 330 core

// Output data ; will be interpolated for each fragment.
layout(location = 0) out vec4 fragColor;

// Input data ; will be interpolated for each fragment.
in vec3 marker_color;
in vec2 uv;

// Uniforms
uniform sampler2D u_texture_0;

/**
 * @brief
 * Main function of the program
 */
void main() {
    fragColor = texture(u_texture_0, uv);
    fragColor.rgb *= marker_color;
    fragColor.a = (fragColor.r + fragColor.b > 1.0) ? 0.0 : 1.0;
}