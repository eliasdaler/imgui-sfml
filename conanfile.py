#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from conans import ConanFile, CMake
from conans.tools import Git
from conans.errors import ConanInvalidConfiguration

class ImguiSFML(ConanFile):
    """ Imgui-SFML library conan file.

    Options:

    * shared: True or False
      Whether to build this library shared or static

    * fPIC: True or False
      Whether or not to use -fPIC option while building

    * imconfig: None or String
      Use 'None' if you want this library to provide default
      ImGui's imconfig.h file. Otherwise, provide a path to the
      imconfig.h file you want to include in the build.

    * imconfig_install_folder: None or String
      Use 'None' if you want this build to include imconfig.h file,
      otherwise use anything else.
    """

    name = 'ImGui-SFML'
    version = '2.0.1'
    description = 'ImGui binding for use with SFML'
    topics = ('conan', 'sfml', 'gui', 'imgui')
    url = 'https://github.com/eliasdaler/imgui-sfml'
    homepage = 'https://github.com/eliasdaler/imgui-sfml'
    author = 'Elias Daler <eliasdaler@yandex.ru>'
    build_requires = 'sfml/2.5.1@bincrafters/stable'
    license = 'MIT'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
        'imconfig': 'ANY',
        'imconfig_install_folder': 'ANY'
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'imconfig': None,
        'imconfig_install_folder': None
    }
    exports_sources = [
        'imgui-SFML.cpp',
        'imgui-SFML.h',
        'imconfig-SFML.h',
        'imgui-SFML_export.h',
        'CMakeLists.txt',
        'cmake/FindImGui.cmake'
    ]
    exports = 'LICENSE.md'
    _imgui_dir = 'imgui'

    def source(self):
        git = Git(folder=self._imgui_dir)
        git.clone('https://github.com/ocornut/imgui.git', 'v1.69')

    def configure(self):
        imconfig = self.options.imconfig
        if imconfig and not os.path.isfile(str(imconfig)):
            raise ConanInvalidConfiguration("Provided ImGui config is not a file or doesn't exist")
        self.options['sfml'].graphics = True
        self.options['sfml'].window = True
        self.options['sfml'].shared = self.options.shared

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['IMGUI_DIR'] = os.path.join(self.source_folder, self._imgui_dir)
        cmake.definitions['SFML_DIR'] = os.path.join(self.deps_cpp_info['sfml'].lib_paths[0], 'cmake', 'SFML')
        cmake.definitions['IMGUI_SFML_BUILD_EXAMPLES'] = 'OFF'
        cmake.definitions['IMGUI_SFML_FIND_SFML'] = 'ON'
        if self.options.imconfig_install_folder:
            cmake.definitions['IMGUI_SFML_CONFIG_INSTALL_DIR'] = self.options.imconfig_install_folder
        if self.options.imconfig:
            imconfig = str(self.options.imconfig)
            cmake.definitions['IMGUI_SFML_USE_DEFAULT_CONFIG'] = 'OFF'
            cmake.definitions['IMGUI_SFML_CONFIG_NAME'] = os.path.basename(imconfig)
            cmake.definitions['IMGUI_SFML_CONFIG_DIR'] = os.path.dirname(imconfig)
        else:
            cmake.definitions['IMGUI_SFML_USE_DEFAULT_CONFIG'] = 'ON'
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ['ImGui-SFML']
