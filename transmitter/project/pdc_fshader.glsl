#version 330

in vec3 vpoint;
in vec3 uv;

uniform int c0;
uniform int c1;
uniform int c2;
uniform int c3;
uniform int c4;
uniform int c5;
uniform int c6;
uniform int c7;
uniform int c8;

uniform int starting;

out vec3 color;

uniform int time;
uniform isampler1D color_tab;


vec3 c(int i);

void main() {

    if (starting == 1) {
        
        if (uv.r <= 0.0 && uv.g >= 0.0) {
            color = vec3(1.0, 0.0, 0.0);
        } else if (uv.r >= 0.0 && uv.g >= 0.0) {
            color = vec3(0.0, 1.0, 0.0);
        } else if (uv.r <= 0.0 && uv.g <= 0.0) {
            color = vec3(0.0, 1.0, 0.0);
        } else {
            color = vec3(1.0, 0.0, 0.0);
        }
        //color = vec3(1.0, 0.0, 0.0);

    } else {
        // Top left
        if (uv.r <= -(2.0/3.0) && uv.g >= 2.0/3.0 ||
            uv.r <= (1.0/3.0) && uv.r > 0.0 && uv.g >= 2.0/3.0 || 
            uv.r <=-(2.0/3.0) && uv.g < 0.0 && uv.g > -(1.0/3.0) ||
            uv.r <=(1.0/3.0) && uv.r > 0.0 && uv.g >= -(1.0/3.0) && uv.g < 0.0) {
                //color = vec3(0.0, 0.0, 0.0);
                color = c(c0);

        } else if ( // Top center
            uv.r <= -(1.0/3.0) && uv.r >= -(2.0/3.0) && uv.g >= 2.0/3.0 ||
            uv.r <= (2.0/3.0) && uv.r > 1.0/3.0 && uv.g >= 2.0/3.0 || 
            uv.r <= -(1.0/3.0) && uv.r >= -(2.0/3.0) && uv.g < 0.0 && uv.g > -(1.0/3.0) ||
            uv.r <=(2.0/3.0) && uv.r > 1.0/3.0 && uv.g >= -(1.0/3.0) && uv.g < 0.0) {
                //color = vec3(0.0, 1.0, 0.0);
                color = c(c1);
        } else  if ( // Top right
            uv.r <= 0.0 && uv.r >= -(1.0/3.0) && uv.g >= 2.0/3.0 ||
            uv.r > 2.0/3.0 && uv.g >= 2.0/3.0 || 
            uv.r <= 0.0 && uv.r >= -(1.0/3.0) && uv.g < 0.0 && uv.g > -(1.0/3.0) ||
            uv.r > 2.0/3.0 && uv.g >= -(1.0/3.0) && uv.g < 0.0) {
                //color = vec3(0.0, 0.0, 1.0);
                color = c(c2);
        } else if ( // Middle left
            uv.r <= -(2.0/3.0) && uv.g <= 2.0/3.0 && uv.g > 1.0/3.0 ||
            uv.r <= (1.0/3.0) && uv.r > 0.0 && uv.g < 2.0/3.0 && uv.g > 1.0/3.0 || 
            uv.r <=-(2.0/3.0) && uv.g < 0.0 && uv.g > -(2.0/3.0) && uv.g < -(1.0/3.0) ||
            uv.r <=(1.0/3.0) && uv.r > 0.0 && uv.g < -(1.0/3.0) && uv.g > -(2.0/3.0)) {
                //color = vec3(1.0, 1.0, 0.0);
                color = c(c3);
        } else if( // Middle center
            uv.r <= -(1.0/3.0) && uv.r >= -(2.0/3.0) && uv.g >= 1.0/3.0 && uv.g < 2.0/3.0 ||
            uv.r <= (2.0/3.0) && uv.r > 1.0/3.0 && uv.g >= 1.0/3.0 && uv.g < 2.0/3.0 || 
            uv.r <= -(1.0/3.0) && uv.r >= -(2.0/3.0) && uv.g < -(1.0/3.0) && uv.g > -(2.0/3.0) ||
            uv.r <=(2.0/3.0) && uv.r > 1.0/3.0 && uv.g >= -(2.0/3.0) && uv.g < -(1.0/3.0)) {
                //color = vec3(0.0, 1.0, 1.0);
                color = c(c4);
        } else  if ( // Middle right
            uv.r <= 0.0 && uv.r >= -(1.0/3.0) && uv.g >= 1.0/3.0 && uv.g < 2.0/3.0 ||
            uv.r > 2.0/3.0 && uv.g >= 1.0/3.0 && uv.g < 2.0/3.0 || 
            uv.r <= 0.0 && uv.r >= -(1.0/3.0) && uv.g < -(1.0/3.0) && uv.g > -(2.0/3.0) ||
            uv.r > 2.0/3.0 && uv.g >= -(2.0/3.0) && uv.g < -(1.0/3.0)) {
                //color = vec3(1.0, 0.0, 1.0);
                color = c(c5);
        } else if (// Bottom left
            uv.r <= -(2.0/3.0) && uv.g >= 0 && uv.g < 1.0/3.0 ||
            uv.r <= (1.0/3.0) && uv.r > 0.0 && uv.g >= 0 && uv.g < 1.0/3.0 || 
            uv.r <=-(2.0/3.0) && uv.g < -(2.0/3.0) ||
            uv.r <=(1.0/3.0) && uv.r > 0.0 && uv.g < -(2.0/3.0)) {
                //color = vec3(0.5, 0.5, 1.0);
                color = c(c6);
        } else if ( // Bottom center
            uv.r <= -(1.0/3.0) && uv.r >= -(2.0/3.0) && uv.g >= 0.0 && uv.g < 1.0/3.0 ||
            uv.r <= (2.0/3.0) && uv.r > 1.0/3.0 && uv.g >= 0.0 && uv.g < 1.0/3.0 || 
            uv.r <= -(1.0/3.0) && uv.r >= -(2.0/3.0) && uv.g < -(2.0/3.0) ||
            uv.r <=(2.0/3.0) && uv.r > 1.0/3.0 && uv.g < -(2.0/3.0)) {
                //color = vec3(0.5, 0.5, 0.5);
                color = c(c7);
        } else if ( // Bottom right
            uv.r <= 0.0 && uv.r >= -(1.0/3.0) && uv.g >= 0.0 && uv.g < 1.0/3.0 ||
            uv.r > 2.0/3.0 && uv.g >= 0.0 && uv.g < 1.0/3.0 || 
            uv.r <= 0.0 && uv.r >= -(1.0/3.0) && uv.g < -(2.0/3.0) ||
            uv.r > 2.0/3.0 && uv.g < -(2.0/3.0)) {
                //color = vec3(1.0, 1.0, 1.0);
                color = c(c8);
        } else {
            color = vec3(0.0, 0.0, 0.0);

        }

    }

}

vec3 c(int i) {
    if (i == 0) {
        return vec3(1.0, 0.0, 0.0);
    } else if (i == 1) {
        return vec3(0.0, 1.0, 0.0);
    } else if (i == 2) {
        return vec3(0.0, 0.0, 1.0);
    } else {
        return vec3(0.0, 0.0, 0.0);
    }
}
