# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Elsi(CMakePackage):
    """ELSI provides a unified interface for electronic structure
    codes to a variety of eigenvalue solvers."""

    homepage = "https://wordpress.elsi-interchange.org/"
    url      = "http://wordpress.elsi-interchange.org/wp-content/uploads/2019/06/elsi-2.3.0.tar.gz"

    version('2.3.0', sha256='f2fad2a16c8e8c7f54f87753b34e2eecea074416251620268a7633272646ce92')

    # Variants (translation of cmake options)
    variant(
        'add_underscore', default=True,
        description="Suffix C functions with an underscore"
    )
    variant(
        'elpa2_kernel', default="none", description="ELPA2 Kernel",
        values=('BGQ', 'AVX', 'AVX2', 'AVX512'), multi=False
    )
    variant(
        'enable_pexsi', default=True, description='Enable PEXSI support'
    )
    variant(
        'enable_sips', default=False, description='Enable SLEPc-SIPs support'
    )
    variant(
        'use_external_elpa', default=True,
        description="Build ELPA using SPACK"
    )
    variant(
        'use_external_ntpoly', default=True,
        description="Build NTPoly using SPACK"
    )
    variant(
        'use_external_omm', default=False,
        description="Use external libOMM and MatrixSwitch"
    )
    variant(
        'use_external_pexsi', default=True,
        description="Use external PEXSI"
    )
    variant(
        'use_mpi_iallgather', default=True,
        description="Use non-blocking collective MPI functions"
    )

    # Basic dependencies
    depends_on('blas', type="link")
    depends_on('lapack', type="link")
    depends_on('cmake', type="build")
    depends_on('mpi')
    depends_on('scalapack', type="link")

    # Library dependencies
    depends_on('elpa', when='+use_external_elpa')
    depends_on('ntpoly', when='+use_external_ntpoly')
    depends_on('slepc', when='+enable_sips')
    depends_on('petsc', when='+enable_sips')
    depends_on('pexsi', when='+use_external_pexsi')

    def cmake_args(self):
        from os.path import dirname

        args = []

        # Compiler Information
        # (ELSI wants these explicitly set)
        args += ["-DCMAKE_Fortran_COMPILER=" + self.spec["mpi"].mpifc]
        args += ["-DCMAKE_C_COMPILER=" + self.spec["mpi"].mpicc]
        args += ["-DCMAKE_CXX_COMPILER=" + self.spec["mpi"].mpicxx]

        # Handle the various variants
        if "-add_underscore" in self.spec:
            args += ["-DADD_UNDERSCORE=OFF"]
        if "elpa2_kernel" in self.spec.variants and \
                self.spec.variants["elpa2_kernel"].value != "none":
            kernel = self.spec.variants["elpa2_kernel"].value
            args += ["-DELPA2_KERNEL=" + kernel]
        if '+enable_pexsi' in self.spec:
            args += ["-DENABLE_PEXSI=ON"]
        if '+enable_sips' in self.spec:
            args += ["-DENABLE_SIPS=ON"]
        if '+use_external_elpa' in self.spec:
            args += ["-DUSE_EXTERNAL_ELPA=ON"]
            # Setup the searchpath for elpa
            elpa = self.spec['elpa']
            elpa_module = find(elpa.prefix, 'elpa.mod')
            args += ["-DINC_PATHS=" + dirname(elpa_module[0])]
        if '+use_external_ntpoly' in self.spec:
            args += ["-DUSE_EXTERNAL_NTPOLY=ON"]
        if '+use_external_omm' in self.spec:
            args += ["-DUSE_EXTERNAL_OMM=ON"]
        if '+use_external_pexsi' in self.spec:
            args += ["-DUSE_EXTERNAL_PEXSI=ON"]
        if '-use_mpi_iallgather' in self.spec:
            args += ["-DUSE_MPI_IALLGATHER=OFF"]

        return args
