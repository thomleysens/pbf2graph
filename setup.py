from setuptools import setup
import versioneer

requirements = [
    # package requirements go here
]

setup(
    name='pbf2graph',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Transform PBF OSM file to routable Graph-Tool graph",
    license="BSD",
    author="Thomas LEYSENS",
    author_email='Email Address',
    url='https://github.com/thomleysens/pbf2graph',
    packages=['pbf2graph'],
    entry_points={
        'console_scripts': [
            'pbf2graph=pbf2graph.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='pbf2graph',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
