uniform sampler2D sampler;
uniform vec2 size;
uniform float time;

varying vec2 tex;

void main()
{
    // Shift texture lookup sideways depending on Y coordinate + time
    vec2 pos = tex + vec2(6.0*sin(pow(tex.y, 2.0)*20.0+time)/size.x, 0.0);
    vec4 color = texture2D(sampler, pos);

    // Vignette effect (brightest at center, darker towards edges)
    float lum = 1.0 - length(tex - vec2(0.5, 0.5));

    // Vignette color is also blue-green'ish
    vec4 vignette = vec4(lum * 0.95, lum * 0.98, lum, 1.0);

    gl_FragColor = vignette * color;
}
