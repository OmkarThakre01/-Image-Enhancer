from setuptools import setup, find_packages

setup(
    name="image-enhancer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.0.1",
        "Flask-Cors==3.0.10",
        "numpy==1.19.5",
        "Pillow==8.3.1",
        "opencv-python-headless==4.5.1.48",
        "gunicorn==20.1.0"
    ],
    python_requires=">=3.9,<3.10"
) 