attribute vec4 position;
attribute vec2 texcoord;

uniform vec2 size;
uniform vec2 offset;
uniform float scale;

varying vec2 tex;

void main()
{
    gl_Position.x = 2.0 * (position.x*scale + offset.x) / size.x - 1.0;
    gl_Position.y = 1.0 - 2.0 * (position.y*scale + offset.y) / size.y;
    gl_Position.z = 0.0;
    gl_Position.w = 1.0;

    tex = texcoord;
}
