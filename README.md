# Python testing template
Template for test framework

Framework consist of:
    python as runtime
    selenium+webium as a framework for work with browsers
    behave as a module for behave testing technique

Pre requirements:
    install python 3.5.3x
    install chrome/firefox (don't forget to customize in local_webium_settings)
    install python packages from requirements.txt
    put browser's driver in path

Run tests:
CLI:
    from project directory run "behave features/"
    see test report at ./test-results/report/index.html
FROM PYCHARM:
    Open Edit configuration dialogue
    Add a new Behave configuration
    Select as working directory 'feature' directory of this project
    To run test select configuration and run it
    Report will be in ide interface