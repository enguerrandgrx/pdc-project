#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <algorithm>



#include <iostream>
#include <bitset>

#include <map>

#include <thread>



#include <string>
using namespace std;




// pos triangle
const GLfloat tri_v_pos[] = {-1.0f, -1.0f, 0.0f, 
                                            1.0f, -1.0f, 0.0f, 
                                            -1.0f,  1.0f, 0.0f, 
                                            1.0f, 1.0f, 0.0f};

map<string, string> tab_bin_to_ter;

GLFWwindow* window;

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

string input = "";
string st;
int counter;

int starting_time = 10;

int starting;

int last;

// Annonce fonction
void rempl_c(int[], int par);
string conv_string_to_bin_string(string s);
string bin_to_ter(string s);
string conv_ascii_to_RGB(string s);
void Display(int tab[9], int par);
string conv_ascii_to_RGB2(string s);



void Init() {

    int status;

    string vs_code, fs_code;
    {
        ifstream vs_stream("pdc_vshader.glsl", ios::in);
        if(vs_stream.is_open()) {
            vs_code = string(istreambuf_iterator<char>(vs_stream),
                                        istreambuf_iterator<char>());
            vs_stream.close();
        } else {
            printf("Could not open pdc_vshader.glsl");
            status = 0;
        }

        ifstream fs_stream("pdc_fshader.glsl", ios::in);
        if(fs_stream.is_open()) {
            fs_code = string(istreambuf_iterator<char>(fs_stream),
                                          istreambuf_iterator<char>());
            fs_stream.close();
        } else {
            printf("Could not open pdc_fshader.glsl");
            status = 0;
        }

    }

    char const *vshader = vs_code.c_str();
    char const *fshader = fs_code.c_str();

    GLint ter = GL_FALSE;
    int len;

    //  Vertex Shader
    GLuint vs_id = glCreateShader(GL_VERTEX_SHADER);

    fprintf(stdout, "Compiling Vertex shader: ");
    char const * v_source_pointer = vshader;
    glShaderSource(vs_id, 1, &v_source_pointer , NULL);
    glCompileShader(vs_id);

    // check
    glGetShaderiv(vs_id, GL_COMPILE_STATUS, &ter);
    glGetShaderiv(vs_id, GL_INFO_LOG_LENGTH, &len);
    if(!ter) {
        vector<char> vertex_shader_error_message(len);
        glGetShaderInfoLog(vs_id, len, NULL,
                           &vertex_shader_error_message[0]);
        fprintf(stdout, "Failed:\n%s\n", &vertex_shader_error_message[0]);
        status = 0;
    }
    else{
        fprintf(stdout, "Success\n");
    }



    // Fragment Shader
    GLuint fs_id = glCreateShader(GL_FRAGMENT_SHADER);

    fprintf(stdout, "Compiling Fragment shader: ");
    char const * f_source_pointer = fshader;
    glShaderSource(fs_id, 1, &f_source_pointer , NULL);
    glCompileShader(fs_id);

    // check
    glGetShaderiv(fs_id, GL_COMPILE_STATUS, &ter);
    glGetShaderiv(fs_id, GL_INFO_LOG_LENGTH, &len);
    if(!ter) {
        vector<char> fs_err_mess(len);
        glGetShaderInfoLog(fs_id, len, NULL,
                           &fs_err_mess[0]);
        fprintf(stdout, "Failed:\n%s\n", &fs_err_mess[0]);
        status = 0;
    }
    else
        fprintf(stdout, "Success\n");


    fprintf(stdout, "Linking shader program: ");
    GLuint program_id = glCreateProgram();
    glAttachShader(program_id, vs_id);
    glAttachShader(program_id, fs_id);
    glLinkProgram(program_id);


    glGetProgramiv(program_id, GL_LINK_STATUS, &ter);
    glGetProgramiv(program_id, GL_INFO_LOG_LENGTH, &len);
    vector<char> err_mess(max(len, int(1)));
    glGetProgramInfoLog(program_id, len, NULL, &err_mess[0]);
    if(!ter) {
        fprintf(stdout, "Failed:\n%s\n", &err_mess[0]);
        status = 0;
    }
    else {
        fprintf(stdout, "Success\n");
    }

    glDeleteShader(vs_id);
    glDeleteShader(fs_id);

    fflush(stdout);

    status = program_id;

    if(status == 0)
        printf("Failed linking:\n  vshader: %s\n  fshader: %s\n  gshader: %s\n",
               "pdc_vshader.glsl", "pdc_fshader.glsl", NULL);



    if(!program_id) {
        exit(EXIT_FAILURE);
    }

    glUseProgram(program_id);

    loc_time = glGetUniformLocation(program_id, "time");
    loc_starting = glGetUniformLocation(program_id, "starting");

    glUniform1i(loc_starting, 1);


    
    
    // Setup vertex arrays
    GLuint v_array_id;
    glGenVertexArrays(1, &v_array_id);
    glBindVertexArray(v_array_id);
    
    GLuint v_buffer;
    glGenBuffers(1, &v_buffer);
    glBindBuffer(GL_ARRAY_BUFFER, v_buffer);
    glBufferData(GL_ARRAY_BUFFER, sizeof(tri_v_pos),
                 tri_v_pos, GL_STATIC_DRAW);

    GLuint v_point_id = glGetAttribLocation(program_id, "vpoint");
    glEnableVertexAttribArray(v_point_id);
    glVertexAttribPointer(v_point_id, 3, GL_FLOAT, false,
                          0, 0);

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


    st = conv_ascii_to_RGB2(input);


/*    int rem_st_9 = st.size()%9;


    switch(rem_st_9) {
        case 0: break;
        case 1: st = st + "22222222" ; break;
        case 2: st = st + "2222222"; break;
        case 3: st = st + "222222"; break;
        case 4: st = st + "22222"; break;
        case 5: st = st + "2222"; break;
        case 6: st = st + "222"; break;
        case 7: st = st + "22"; break;
        case 8: st = st + "2"; break;
    }
*/
    st = st + "22222222";

    counter = 0;

    last = st.size()/8;



}

void preDisplay() {

    cout << "Mot à transmettre: " << input << endl;

    int par = 1;


    while(!glfwWindowShouldClose(window)) {
        
        
        float time = glfwGetTime() ;

        int timef = time;

        int timeim = timef%3;

        int tab[8] = {0, 0, 0, 0, 0, 0, 0, 0};

        if (time > starting_time) {
            string s = st.substr(counter*8, 8);

            cout << s << endl;



            for (int i = 0; i < 8; i++) {
                tab[i] = stoi(s.substr(i, 1));
            }

            glUniform1i(loc_starting, 0);
            counter++;
            
            if(counter == last) {
                par = 2;
            }
            
            //cout << par << endl;

            Display(tab, par);

            glfwSwapBuffers(window);
            glfwPollEvents();

            this_thread::sleep_for(chrono::milliseconds(400));
            
            par = (par + 1)%2;


        } else {


                Display(tab, par);
                glfwSwapBuffers(window);
                glfwPollEvents();


        }


    }


}

void Display(int tab[8], int par) {
    glClear(GL_COLOR_BUFFER_BIT);
/*
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


    float time = glfwGetTime() ;

    int timef = time;

    int timeim = timef%3;
    glUniform1i(loc_time, timeim);
*/
    rempl_c(tab, par);


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

void rempl_c(int tab[], int par) {
    glUniform1i(loc_c0, tab[0]);
    glUniform1i(loc_c1, tab[1]);
    glUniform1i(loc_c2, tab[2]);
    glUniform1i(loc_c3, tab[3]);
    glUniform1i(loc_c4, tab[4]);
    glUniform1i(loc_c5, tab[5]);
    glUniform1i(loc_c6, tab[6]);
    glUniform1i(loc_c7, tab[7]);
    glUniform1i(loc_c8, par);
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

    //cout << "Size_bin: " << str_bin << endl;


    // convert to ternary
    string str_ter = "";
    for( int i = 0; i < str_bin_size; i++) {
        str_ter = str_ter + bin_to_ter(str_bin.substr(i*3, 3));
    }

    cout << "Ternary: " << str_ter << endl;


    return str_ter;

}


string conv_ascii_to_RGB2(string s) {
    string str_bin = "";
    for(int i = 0; i < s.size(); i++) {
        string car = s.substr(i, 1);
        string car_bin = conv_string_to_bin_string(car);
        car_bin = car_bin + '0';
        
        for(int j = 0; j < 3; j++) {
            string sub3 = car_bin.substr(j*3, 3);
            int k = sub3[0] - '0';
            int l = sub3[1] - '0';
            int m = sub3[2] - '0';
            
            
            int sum = (k+l+m)%2;
            car_bin = car_bin + to_string(sum);
        }
        
        str_bin = str_bin + car_bin;
    }
    
    cout << str_bin << endl;
    
    string str_ter = "";
    for( int i = 0; i < s.size()*4; i++) {
        str_ter = str_ter + bin_to_ter(str_bin.substr(i*3, 3));
    }
    
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
    unsigned char i = 'ï';
    
    cout << i << endl;
    
    if(!glfwInit()) {
        fprintf(stderr, "Failed to initialize GLFW\n");
        return EXIT_FAILURE;
    }

    
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    
    window = glfwCreateWindow(512, 512, "Project PDC", NULL, NULL);

    if(!window) {
        glfwTerminate();
        return EXIT_FAILURE;
    }

    glfwMakeContextCurrent(window);
    
    glfwSetKeyCallback(window, KeyCallback);




    glewExperimental = GL_TRUE;
    if(glewInit() != GLEW_NO_ERROR) {
        fprintf(stderr, "Failed to initialize GLEW\n");
        return EXIT_FAILURE;
    }

    cout << "OpenGL" << glGetString(GL_VERSION) << endl;
    
    Init();
    
    preDisplay();



    glfwDestroyWindow(window);
    glfwTerminate();
    return EXIT_SUCCESS;
}
