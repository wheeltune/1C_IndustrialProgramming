cmake_minimum_required( VERSION 3.0 )

project( Coloring )

add_custom_command( 
  OUTPUT colors.h
  COMMAND python ${PROJECT_SOURCE_DIR}/colors_generator.py ${PROJECT_SOURCE_DIR}/colors.h
  DEPENDS colors_generator.py
  COMMENT "Generating gray colors"
)

set(SOURCES main.cpp)

add_custom_target( RunGenerator DEPENDS colors.h COMMENT "Checking if re-generation is required" )

add_executable( Coloring ${SOURCES} )
add_dependencies( Coloring RunGenerator )
