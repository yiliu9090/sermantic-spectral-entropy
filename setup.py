import setuptools 

with open("README.md", "r") as fh: 
    description = fh.read() 

setuptools.setup( 
    name="spectral-sermantic-entropy", 
    version="0.0.1", 
    author="Yi Liu", 
    author_email="", 
    packages=["semantic_spectral_entropy"], 
    description="Implementation of Semantic Spectral Entropy", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="", 
    license='MIT', 
    python_requires='>=3.8', 
    install_requires=["numpy","pandas","scikit-learn", "collections" ] 
) 