get_filename_component(DIREC ${CMAKE_CURRENT_LIST_DIR} NAME)
file(GLOB_RECURSE SOURCES "*.cpp")
file(GLOB_RECURSE HEADERS "*.h")

macro(deploy)
    set(SHADERS "${ARGN}")
    get_filename_component(DIREC ${CMAKE_CURRENT_LIST_DIR} NAME)
    set(TN copy_shaders_${DIREC})
    add_custom_target(${TN} ALL)
    foreach(SHADER ${SHADERS})
        add_custom_command(
            TARGET ${TN}
            COMMAND ${CMAKE_COMMAND} -E copy ${SHADER} ${CMAKE_CURRENT_BINARY_DIR}
            COMMENT "Copying ${SHADER} to build folder")
    endforeach()
endmacro()

file(GLOB SHADERS
  pdc_vshader.glsl
  pdc_fshader.glsl)
deploy(${SHADERS})

add_executable(${DIREC} ${SOURCES} ${HEADERS} ${SHADERS})
target_link_libraries(${DIREC} ${COMMON_LIBS})
