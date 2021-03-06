from setuptools import setup
from mio0 import version

setup(name="mio0",
      version=version,
      description="Python implementation of the MIO0 Compression algorithm used in Nintendo 64 titles",
      url="",
      author="Andre Meyer",
      author_email="nope",
      license="MIT",
      packages=["mio0"],
      python_requires=">=3",
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Rom Hacking :: N64 :: Compression Algorithm',
            'License :: MIT License',
            'Programming Language :: Python :: 3.8'
      ]
)
