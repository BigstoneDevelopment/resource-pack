// Huge thanks to d (therderdiscohund) for this shader code below.
// Join the Minecraft Commands discord and click the link to see the exact message:
// https://discord.com/channels/154777837382008833/259800273445191690/1440458090787897404

#version 150

// Can't moj_import in things used during startup, when resource packs don't exist.
// This is a copy of dynamicimports.glsl
layout(std140) uniform DynamicTransforms {
    mat4 ModelViewMat;
    vec4 ColorModulator;
    vec3 ModelOffset;
    mat4 TextureMat;
    float LineWidth;
};

in vec4 vertexColor;

in vec4 _pos0;
in vec4 _pos2;

out vec4 fragColor;

void main() {
    if (vertexColor == vec4(1)) {
        vec3 pos0 = _pos0.xyz / _pos0.w;
        vec3 pos2 = _pos2.xyz / _pos2.w;
        if (abs(pos0.x - pos2.x) < 1.5 && abs(pos0.y - pos2.y) > 20.5) discard;
        if (abs(pos0.x - pos2.x) > 260 && abs(pos0.x - pos2.x) < 270 && abs(pos0.y - pos2.y) < 1.5) discard;
    }
    vec4 color = vertexColor;
    if (color.a == 0.0) {
        discard;
    }
    fragColor = color * ColorModulator;
}