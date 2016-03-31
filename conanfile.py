import os
from conans import ConanFile, CMake
from conans.tools import download, unzip

class CVODEConan(ConanFile):
    name = "CVODE"
    version = "2.8.2"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt"]
    url="http://github.com/bilke/conan-cvode"
    license="http://computation.llnl.gov/casc/sundials/download/license.html"

    ZIP_FOLDER_NAME = "cvode-%s" % version
    INSTALL_DIR = "_install"
    CMAKE_OPTIONS = "-DBUILD_TESTING=OFF -DEXAMPLES_INSTALL=OFF"

    def source(self):
        zip_name = self.ZIP_FOLDER_NAME + ".tar.gz"
        download("https://opengeosys.s3.amazonaws.com/ogs6-lib-sources/cvode-2.8.2.tar.gz" , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        CMAKE_OPTIONALS = ""
        BUILD_OPTIONALS = ""
        if self.options.shared == False:
            CMAKE_OPTIONALS += "-DBUILD_SHARED_LIBS=OFF"
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
            BUILD_OPTIONALS = "-- /maxcpucount"
        else:
            self.run("mkdir _build")
            if self.settings.os == "Macos":
                BUILD_OPTIONALS = "-- -j $(sysctl -n hw.ncpu)"
            else:
                BUILD_OPTIONALS = " -- -j $(nproc)"
        cd_build = "cd _build"
        self.run("%s && cmake .. -DCMAKE_INSTALL_PREFIX=../%s %s %s %s" % (cd_build, self.INSTALL_DIR, self.CMAKE_OPTIONS, CMAKE_OPTIONALS, cmake.command_line))
        self.run("%s && cmake --build . %s %s" % (cd_build, cmake.build_config, BUILD_OPTIONALS))
        self.run("%s && cmake --build . --target install %s" % (cd_build, cmake.build_config))

    def package(self):
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
        libs = [
            "sundials_cvode",
            "sundials_nvecserial"
        ]
        self.cpp_info.libs = libs
        self.cpp_info.includedirs = ['include']
