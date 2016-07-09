attribute vec4 position;
attribute vec2 texcoord;

varying vec2 tex;

void main()
{
    gl_Position = position;
    tex = texcoord;
}
