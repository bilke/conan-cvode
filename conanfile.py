import os
from conans import ConanFile, CMake
from conans.tools import download, unzip

class CvodeConan(ConanFile):
    name = "cvode"
    description = """CVODE is a solver for stiff and nonstiff ordinary
                     differential equation systems given in explicit form."""
    version = "2.8.2"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports = ["CMakeLists.txt"]
    url="http://github.com/bilke/conan-cvode"
    license="http://computation.llnl.gov/casc/sundials/download/license.html"

    def source(self):
        zip_name = "%s.tar.gz" % self.version
        download("https://github.com/ufz/cvode/archive/%s" % zip_name , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

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
