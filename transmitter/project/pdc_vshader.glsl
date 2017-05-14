#version 330

in vec3 vpoint;

out vec3 uv;

void main() {
	uv = vpoint;
    gl_Position = vec4(vpoint, 1.0);
}
