attribute vec4 position;
attribute vec2 texcoord;

uniform vec2 size;

varying vec2 tex;

void main()
{
    gl_Position.x = 2.0 * position.x / size.x - 1.0;
    gl_Position.y = 1.0 - 2.0 * position.y / size.y;
    gl_Position.z = 0.0;
    gl_Position.w = 1.0;

    tex = texcoord;
}
