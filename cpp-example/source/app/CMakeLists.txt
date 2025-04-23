# ##############################################################################
# GENERAL SETTINGS
# ##############################################################################
set(TARGET "cpp-example-app")
project(${TARGET})

# ##############################################################################
# DEPENDENCIES
# ##############################################################################

# ##############################################################################
# TARGETS
# ##############################################################################
add_executable(${TARGET} "")

set_target_properties(${TARGET} PROPERTIES POSITION_INDEPENDENT_CODE ON)
set_target_properties(${TARGET} PROPERTIES LINKER_LANGUAGE CXX)
target_compile_features(${TARGET} PRIVATE cxx_std_20)

target_compile_options(${TARGET} PUBLIC $<IF:$<NOT:$<CXX_COMPILER_ID:MSVC>>,
                                        -fPIC,>)

target_sources(
  ${TARGET}
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src/example_app.cpp)

# ##############################################################################
# LINKED LIBRARIES
# ##############################################################################

target_link_libraries(
  ${TARGET}
  PRIVATE cpp::example
)