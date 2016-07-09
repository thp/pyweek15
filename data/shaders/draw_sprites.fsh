uniform sampler2D sampler;
uniform vec4 color;

varying vec2 tex;

void main()
{
    gl_FragColor = color * texture2D(sampler, tex);
}
