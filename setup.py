from setuptools import setup

setup(name='vagquery',
        version='0.1',
        description='Queries for VAG public transportation time schedules',
        long_description='This modules enables creating and executing queries for\
                the start.vgn.de site, a page to get the current time schedule\
                for the franconian public transportation company VAG.',
        author='Philipp Weissmann',
        author_email='github@philipp-weissmann.de',
        license='MIT',
        install_requires=['requests'],
        packages=['vagquery'],
        zip_safe=False,
        classifiers=[
                    'Development Status :: 3 - Alpha',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python :: 2.7',
                    'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
                    ],
        keywords='vgn vag public transportation time schedule Nuremberg Erlangen',
        url='http://github.com/derphilipp/vagquery',
        )
