// glew must be before glfw
#include <GL/glew.h>
#include <GLFW/glfw3.h>

// contains helper functions such as shader compiler
#include "icg_helper.h"

#include <glm/gtc/type_ptr.hpp>


// vertex position of the triangle
const GLfloat triangle_vertex_positions[] = {-1.0f, -1.0f, 0.0f, 
                                            1.0f, -1.0f, 0.0f, 
                                            -1.0f,  1.0f, 0.0f, 
                                            1.0f, 1.0f, 0.0f};


GLuint loc_time;
GLuint loc_starting;
GLuint program_id;

GLuint loc_c0;
GLuint loc_c1;
GLuint loc_c2;
GLuint loc_c3;
GLuint loc_c4;
GLuint loc_c5;
GLuint loc_c6;
GLuint loc_c7;
GLuint loc_c8;

int starting_time = 10;

int starting;

void rempl_c(int[]);

void Init() {
    // sets background color
    glClearColor(0.937, 0.937, 0.937 /*gray*/, 1.0 /*solid*/);
    
    // compile the shaders
    program_id = icg_helper::LoadShaders("pdc_vshader.glsl",
                                                "pdc_fshader.glsl");
    if(!program_id) {
        exit(EXIT_FAILURE);
    }

    glUseProgram(program_id);

    loc_time = glGetUniformLocation(program_id, "time");
    loc_starting = glGetUniformLocation(program_id, "starting");

    glUniform1i(loc_starting, 1);

    
    // setup vertex array;
    // vertex arrays wrap buffers & attributes together
    // creating it is mandatory in newer OpenGL versions (>= 3.0)
    GLuint vertex_array_id;
    glGenVertexArrays(ONE, &vertex_array_id);
    glBindVertexArray(vertex_array_id);
    
    // generate memory for vertex buffer
    GLuint vertex_buffer;
    glGenBuffers(ONE, &vertex_buffer);
    // the subsequent commands will affect the specified buffer
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer);
    // pass the vertex positions to OpenGL
    glBufferData(GL_ARRAY_BUFFER, sizeof(triangle_vertex_positions),
                 triangle_vertex_positions, GL_STATIC_DRAW);

    // creates Vertex Attribute to store Vertex Positions
    GLuint vertex_point_id = glGetAttribLocation(program_id, "vpoint");
    glEnableVertexAttribArray(vertex_point_id);
    //glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer);
    glVertexAttribPointer(vertex_point_id, 3, GL_FLOAT, DONT_NORMALIZE,
                          ZERO_STRIDE, ZERO_BUFFER_OFFSET);

    loc_c0 = glGetUniformLocation(program_id, "c0");
    loc_c1 = glGetUniformLocation(program_id, "c1");
    loc_c2 = glGetUniformLocation(program_id, "c2");
    loc_c3 = glGetUniformLocation(program_id, "c3");
    loc_c4 = glGetUniformLocation(program_id, "c4");
    loc_c5 = glGetUniformLocation(program_id, "c5");
    loc_c6 = glGetUniformLocation(program_id, "c6");
    loc_c7 = glGetUniformLocation(program_id, "c7");
    loc_c8 = glGetUniformLocation(program_id, "c8");

}

void Display() {
    glClear(GL_COLOR_BUFFER_BIT);

    int smap0[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
    int smap1[9] = {0, 1, 2, 1, 2, 0, 2, 0, 1};
    int smap2[9] = {1, 2, 0, 2, 0, 1, 0, 1, 2};
    int smap3[9] = {2, 0, 1, 0, 1, 2, 1, 2, 0};



    float time = glfwGetTime() ;

    int timef = time;

    int timeim = timef%3;

    if (time > starting_time) {
        glUniform1i(loc_starting, 0);
    }

    if(timeim == 0 && timef >= starting_time) {
        rempl_c(smap1);
    } else if (timeim == 1 && timef >= starting_time) {
        rempl_c(smap2);
    } else if (timeim == 2 && timef >= starting_time) {
        rempl_c(smap3);
    }

    glUniform1i(loc_time, timeim);

    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
}

void ErrorCallback(int error, const char* description) {
    fputs(description, stderr);
}

void KeyCallback(GLFWwindow* window, int key, int scancode,
                 int action, int mods) {
    if(key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
        glfwSetWindowShouldClose(window, GL_TRUE);
    }
}

void rempl_c(int tab[]) {
    glUniform1i(loc_c0, tab[0]);
    glUniform1i(loc_c1, tab[1]);
    glUniform1i(loc_c2, tab[2]);
    glUniform1i(loc_c3, tab[3]);
    glUniform1i(loc_c4, tab[4]);
    glUniform1i(loc_c5, tab[5]);
    glUniform1i(loc_c6, tab[6]);
    glUniform1i(loc_c7, tab[7]);
    glUniform1i(loc_c8, tab[8]);
    return;
}

int main(int argc, char *argv[]) {
    // GLFW Initialization
    if(!glfwInit()) {
        fprintf(stderr, "Failed to initialize GLFW\n");
        return EXIT_FAILURE;
    }

    glfwSetErrorCallback(ErrorCallback);
    
    // hint GLFW that we would like an OpenGL 3 context (at least)
    // http://www.glfw.org/faq.html#how-do-i-create-an-opengl-30-context
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    
    // attempt to open the window: fails if required version unavailable
    // note some Intel GPUs do not support OpenGL 3.2
    // note update the driver of your graphic card
    GLFWwindow* window = glfwCreateWindow(512, 512, "Project PDC", NULL, NULL);
    if(!window) {
        glfwTerminate();
        return EXIT_FAILURE;
    }

    // makes the OpenGL context of window current on the calling thread
    glfwMakeContextCurrent(window);

    // set the callback for keyboard keys
    glfwSetKeyCallback(window, KeyCallback);

    // GLEW Initialization (must have a context)
    // https://www.opengl.org/wiki/OpenGL_Loading_Library
    glewExperimental = GL_TRUE; // fixes glew error (see above link)
    if(glewInit() != GLEW_NO_ERROR) {
        fprintf(stderr, "Failed to initialize GLEW\n");
        return EXIT_FAILURE;
    }

    cout << "OpenGL" << glGetString(GL_VERSION) << endl;
    
    // initialize our OpenGL program
    Init();
    
    // render loop
    while(!glfwWindowShouldClose(window)) {
        Display();
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // close OpenGL window and terminate GLFW
    glfwDestroyWindow(window);
    glfwTerminate();
    return EXIT_SUCCESS;
}
