find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_SIK_RADIOS gnuradio-Sik_Radios)

FIND_PATH(
    GR_SIK_RADIOS_INCLUDE_DIRS
    NAMES gnuradio/Sik_Radios/api.h
    HINTS $ENV{SIK_RADIOS_DIR}/include
        ${PC_SIK_RADIOS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_SIK_RADIOS_LIBRARIES
    NAMES gnuradio-Sik_Radios
    HINTS $ENV{SIK_RADIOS_DIR}/lib
        ${PC_SIK_RADIOS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-Sik_RadiosTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_SIK_RADIOS DEFAULT_MSG GR_SIK_RADIOS_LIBRARIES GR_SIK_RADIOS_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_SIK_RADIOS_LIBRARIES GR_SIK_RADIOS_INCLUDE_DIRS)
