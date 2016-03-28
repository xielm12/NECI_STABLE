macro( neci_print_summary )


message(STATUS "")
message(STATUS "---------------------------------------------------------")
message(STATUS "")
message(STATUS " BUILD SUMMARY")
message(STATUS "")

message(STATUS "---------------------------------------------------------")
message(STATUS "Target libraries: ${${PROJECT_NAME}_ALL_LIBS}")
message(STATUS "Target executables: ${${PROJECT_NAME}_ALL_EXES}")
message(STATUS "")
message(STATUS "Fortran compiler: ${CMAKE_Fortran_COMPILER} (${CMAKE_Fortran_COMPILER_ID})")
message(STATUS "C++ compiler: ${CMAKE_CXX_COMPILER} (${CMAKE_CXX_COMPILER_ID})")
message(STATUS "Implicit C++ linker flags: ${CMAKE_CXX_IMPLICIT_LINK_LIBRARIES}")
message(STATUS "Implicit Fortran linker flags: ${CMAKE_Fortran_IMPLICIT_LINK_LIBRARIES}")
message(STATUS "Global C++ compile flags: ${CMAKE_CXX_FLAGS_RELEASE}")
message(STATUS "Global Fortran compile flags: ${CMAKE_Fortran_FLAGS}")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")


message(STATUS "")
message(STATUS "  +---------------------------------------------------+")
message(STATUS "  | ${PROJECT_NAME} configuration now complete                   |")
message(STATUS "  |                                                   |")
message(STATUS "  | VERSION ${${PROJECT_NAME}_VERSION_STR}                                     |")
message(STATUS "  | SHAID   ${${PROJECT_NAME}_GIT_SHA1}  |")
message(STATUS "  +---------------------------------------------------+")
message(STATUS "")
message(STATUS "  You can now do 'make' to compile the software.")
message(STATUS "")

endmacro()
