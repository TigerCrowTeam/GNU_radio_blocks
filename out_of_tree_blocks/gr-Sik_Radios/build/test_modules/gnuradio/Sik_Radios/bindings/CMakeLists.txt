# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT Sik_Radios_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT Sik_Radios_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND Sik_Radios_python_files python_bindings.cc)

gr_pybind_make_oot(Sik_Radios ../../.. gr::Sik_Radios "${Sik_Radios_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET Sik_Radios_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:Sik_Radios_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/Sik_Radios/)

install(
    TARGETS Sik_Radios_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/Sik_Radios
    COMPONENT pythonapi)
