#version 330 core

in vec2 vUv;
out vec4 FragColor;

uniform sampler2D uTexture;    

uniform bool bUseTexture;

void main() {
    if (bUseTexture) {
        FragColor = texture(uTexture, vUv);
    } else {
        FragColor = vec4(1.0, 1.0, 1.0, 1.0);
    }
}