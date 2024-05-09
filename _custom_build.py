from setuptools import Extension
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    def run(self):
        self.run_command("build_ext")
        return super().run()

    def initialize_options(self):
        super().initialize_options()
        if self.distribution.ext_modules == None:
            self.distribution.ext_modules = []

        import numpy as np
        self.distribution.ext_modules.append(
            Extension(
                "pystruct.models.utils",
                sources=["src/utils.pyx"],
                include_dirs = [np.get_include()],
            )
        )
        self.distribution.ext_modules.append(
            Extension(
                "pystruct.inference._viterbi",
                sources=["pystruct/inference/_viterbi.pyx"],
                include_dirs = [np.get_include()],
            )
        )