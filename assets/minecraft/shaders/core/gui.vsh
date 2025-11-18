// Huge thanks to d (therderdiscohund) for this shader code below.
// Join the Minecraft Commands discord and click the link to see the exact message:
// https://discord.com/channels/154777837382008833/259800273445191690/1440458090787897404

#version 150

// Can't moj_import in things used during startup, when resource packs don't exist.
// This is a copy of dynamicimports.glsl and projection.glsl
layout(std140) uniform DynamicTransforms {
    mat4 ModelViewMat;
    vec4 ColorModulator;
    vec3 ModelOffset;
    mat4 TextureMat;
    float LineWidth;
};
layout(std140) uniform Projection {
    mat4 ProjMat;
};

in vec3 Position;
in vec4 Color;

out vec4 vertexColor;

out vec4 _pos0;
out vec4 _pos2;

void main() {
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);
    vertexColor = Color;
    if (Color == vec4(1)) {
        _pos0 = _pos2 = vec4(0);
        if (gl_VertexID % 4 == 0) _pos0 = vec4(Position, 1);
        else if (gl_VertexID % 4 == 2) _pos2 = vec4(Position, 1);
    }

}