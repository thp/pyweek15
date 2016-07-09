uniform sampler2D sampler;
uniform vec2 dimensions;

varying vec2 tex;

void main()
{
    float radius = 10.0 * abs(0.3 - tex.y);
    vec2 offset = vec2(radius / dimensions.x, radius / dimensions.y);
    gl_FragColor = 0.3 * texture2D(sampler, tex)
                 + 0.1 * texture2D(sampler, tex + vec2(0, -offset.y))
                 + 0.1 * texture2D(sampler, tex + vec2(0, offset.y))
                 + 0.1 * texture2D(sampler, tex + vec2(-offset.x, 0))
                 + 0.1 * texture2D(sampler, tex + vec2(offset.x, 0))
                 + 0.075 * texture2D(sampler, tex + vec2(-offset.x, -offset.y))
                 + 0.075 * texture2D(sampler, tex + vec2(offset.x, offset.y))
                 + 0.075 * texture2D(sampler, tex + vec2(-offset.x, offset.y))
                 + 0.075 * texture2D(sampler, tex + vec2(offset.x, -offset.y));
}
