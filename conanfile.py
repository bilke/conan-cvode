import os
from conans import ConanFile, CMake
from conans.tools import download, unzip

class CVODEConan(ConanFile):
    name = "CVODE"
    description = """CVODE is a solver for stiff and nonstiff ordinary
                     differential equation systems given in explicit form."""
    version = "2.8.2"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt"]
    url="http://github.com/bilke/conan-cvode"
    license="http://computation.llnl.gov/casc/sundials/download/license.html"

    def source(self):
        zip_name = "cvode-%s.tar.gz" % self.version
        download("https://opengeosys.s3.amazonaws.com/ogs6-lib-sources/cvode-2.8.2.tar.gz" , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self)
        if self.options.shared == False:
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
        cmake.definitions["EXAMPLES_INSTALL"] = "OFF"
        cmake.configure(build_dir="build")
        cmake.build(target="install")

    def package_info(self):
        self.cpp_info.libs = ["sundials_cvode", "sundials_nvecserial"]
        self.cpp_info.includedirs = ['include']
