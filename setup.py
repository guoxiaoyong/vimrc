from setuptools import setup

requires = []

setup(name='vimrc',
      version='0.0.1',
      description='vimrc',
      long_description='vimrc',
      author='Guo Xiaoyong',
      author_email='guo.xiaoyong@gmail.com',
      url='https://github.com/guoxiaoyong/vimrc',
      install_requires=requires,
      setup_requires=requires,
      packages=['vimrc'],
      include_package_data=True,
      entry_points={
         'console_scripts': ['vimrc=vimrc:main'],
      },
)
