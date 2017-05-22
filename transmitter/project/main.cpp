// glew must be before glfw
#include <GL/glew.h>
#include <GLFW/glfw3.h>

// contains helper functions such as shader compiler
#include "icg_helper.h"

#include <glm/gtc/type_ptr.hpp>

#include <iostream>
#include <bitset>

#include <map>


//#include <vector>;
#include <string>
using namespace std;

//vector<char>;

// vertex position of the triangle
const GLfloat triangle_vertex_positions[] = {-1.0f, -1.0f, 0.0f, 
                                            1.0f, -1.0f, 0.0f, 
                                            -1.0f,  1.0f, 0.0f, 
                                            1.0f, 1.0f, 0.0f};

map<string, string> tab_bin_to_ter;



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

int starting_time = 10000;

int starting;

// Annonce fonction
void rempl_c(int[]);
string conv_string_to_bin_string(string s);
string bin_to_ter(string s);



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

    tab_bin_to_ter["000"] = "00";
    tab_bin_to_ter["001"] = "01";
    tab_bin_to_ter["010"] = "02";
    tab_bin_to_ter["011"] = "10";
    tab_bin_to_ter["100"] = "11";
    tab_bin_to_ter["101"] = "12";
    tab_bin_to_ter["110"] = "20";
    tab_bin_to_ter["111"] = "21";

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

// 
string conv_ascii_to_RGB(string s) {

    // convert to ascii
    string str_bin = "";
    for (int i = 0; i < s.size(); i++) {
        string sub = s.substr(i, 1);
        string sub_bin = conv_string_to_bin_string(sub);

        str_bin = str_bin + sub_bin;
    }

    cout << "Binary: " << str_bin << endl;


    // Add offset to be a multiple of 3
    int str_bin_size;
    if (str_bin.size()%3 == 0) {
        str_bin_size = str_bin.size()/3;
    } else if (str_bin.size()%3 == 1) {
        str_bin_size = (str_bin.size()/3)+1;
        str_bin = str_bin + "00";
    } else if (str_bin.size()%3 == 2) {
        str_bin_size = (str_bin.size()/3)+1;
        str_bin = str_bin + "0";
    }

    cout << "Size_bin: " << str_bin << endl;


    // convert to ternary
    string str_ter = "";
    for( int i = 0; i < str_bin_size; i++) {
        str_ter = str_ter + bin_to_ter(str_bin.substr(i*3, 3));
    }

    cout << "Ternary: " << str_ter << endl;


    return str_ter;








}

// http://stackoverflow.com/questions/10184178/fastest-way-to-convert-string-to-binary
string conv_string_to_bin_string(string s) {
    string sret = "";
    for (std::size_t i = 0; i < s.size(); ++i) {
        sret = sret + bitset<8>(s.c_str()[i]).to_string();
        //cout << bitset<8>(s.c_str()[i]) << endl;
    }


    return sret;
}

string bin_to_ter(string s) {
    if (s.size() != 3) {
        cout << "Not the right size" <<endl;
        return "";
    }
 
    return tab_bin_to_ter[s]; 
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

    conv_ascii_to_RGB("BONJOUR!!");

    
    // render loop
    while(!glfwWindowShouldClose(window)) {
        Display();
        glfwSwapBuffers(window);
        glfwPollEvents();
        break;
    }

    // close OpenGL window and terminate GLFW
    glfwDestroyWindow(window);
    glfwTerminate();
    return EXIT_SUCCESS;
}
