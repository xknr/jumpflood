#version 330 core

in vec2 vUv;
out vec4 FragColor;

uniform sampler2D uTexture;    

uniform float chooseMain;

uniform bool bDisplayDistance;

uniform vec2 screenSize;
uniform int step;



vec2 calcCenterCoord() {
    // return gl_FragCoord.xy - vec2(0.5);
    return floor(gl_FragCoord.xy);    
}





#define MAX_DISTANCE 1e10

const vec4 INVALID_COLOR = vec4(1.0, 1.0, 1.0, 1.0);

bool isInvalid(vec4 col) 
{
    // Higher order 8 bits of x coordinate cannot be 255.
    // .5 to leave space for any possible floating point precision loss.
    const float INVALID_LIMIT = (254.0 + 0.5) / 255.0;

    return col.b > INVALID_LIMIT;
}

// Encodes 2d integer coordinates as 8-bit rgba values.
// Accepted range is [0, 65279] 
// (65279 = 254 * 256 + 255)
vec4 encode(ivec2 src) 
{
    // For better visibility, we place the lower 
    // bits into r,g and higher bits into b,a.
    return vec4(ivec4(src % 256, src / 256)) / 255.0;
}

// Inverse of the encode operation.
ivec2 decode(vec4 src) {
    src *= 255.0;
    return ivec2(src.ba) * 256 + ivec2(src.rg);
}





void main_encode() 
{    
    vec4 col = texture2D(uTexture, vUv);
 
    if (col.r > 0.5) {
        FragColor = encode(ivec2(calcCenterCoord()));
    } else {
        FragColor = INVALID_COLOR;
    }
}

void main_flood() 
{
    vec2 centerCoord = calcCenterCoord();
    
    vec4 best = INVALID_COLOR;
    float bestDist = MAX_DISTANCE;
        
    // For all 8 neighbors and itself:
    for(int j = -step; j <= step; j += step)
    {
        for(int i = -step; i <= step; i += step)
        {
            ivec2 currCoord = ivec2(centerCoord) + ivec2(i, j);

            vec2 currUv = (vec2(currCoord) + vec2(0.5)) / screenSize;            

            vec4 curr = texture(uTexture, currUv);

            // RGBA8 needs no test bc 1,1,1,1 yields a big distance value.
            // if (isInvalid(curr)) continue;
                
            float dist = distance(decode(curr), centerCoord);

            if (dist < bestDist) {
                best = curr;
                bestDist = dist;
            }            
        }        
    }

    if (!bDisplayDistance) 
    {
        FragColor = best;
    } 
    else 
    {
        // No need to check bc invalid color yields a distance big enough to overflow.
        //float dst;
        //if (isInvalid(best)) {
        //    dst = MAX_DISTANCE;
        //} else {
        //    dst = distance(decode(best), centerCoord);
        //}

        float dst = distance(decode(best), centerCoord);

        // This looks good enough:
        #define DIST_COLOR_SCALE 128.0

        float gray = dst / DIST_COLOR_SCALE;

        // Reverse gamma to make it *look* correct.
        // gray = pow(gray, 1.0 / 2.1);

        FragColor = vec4(vec3(gray), 1.0);
    }
}

void main(void) {
    if (chooseMain > 0.5) {
        main_flood();
    } else {
        main_encode();
    }
}