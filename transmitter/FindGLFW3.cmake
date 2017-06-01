FIND_PATH( GLFW3_INCLUDE_DIRS GLFW/glfw3.h
    $ENV{GLFWDIR}/include
    /usr/local/include
    /usr/include)

FIND_LIBRARY( GLFW3_LIBRARIES NAMES glfw3 glfw PATHS
    $ENV{GLFWDIR}/lib
    $ENV{GLFWDIR}/support/msvc80/Debug
    $ENV{GLFWDIR}/support/msvc80/Release
    /usr/local/lib
    /usr/lib)

SET(GLFW3_FOUND "NO")
IF(GLFW3_LIBRARIES AND GLFW3_INCLUDE_DIRS)
    SET(GLFW3_FOUND "YES")
    message(STATUS "Found GLFW3: ${GLFW3_LIBRARIES}")
ENDIF(GLFW3_LIBRARIES AND GLFW3_INCLUDE_DIRS)
