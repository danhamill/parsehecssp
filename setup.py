import setuptools

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setuptools.setup(
 name='parsehecssp',
 version = '0.0.1',
 author = 'Daniel Hamill',
 author_email = 'daniel.hamill@hey.com',
 description = 'Parse HEC-SSP report Files',
 long_description=readme,
 packages = ['parsehecssp', 'parsehecssp.features'],
 license='MIT',
#  package_dir={'':'parsehecssp'},
 classifiers=[
    "Development Status :: 1 - Beta",
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    "License :: OSI Approved :: MIT License",
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    "Topic :: Utilities",
    'Topic :: Scientific/Engineering :: GIS',
]
 
)
