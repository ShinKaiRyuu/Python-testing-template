# Python testing template

####Testing framework consist of:

* python as runtime
* selenium+webium as a framework for work with browsers
* behave as a module for behave testing technique

####Pre requirements:
- install python 3.5.3x
- install chrome/firefox (don't forget to customize in local_webium_settings)
- install python packages from requirements.txt
- put browser's driver in path

####Run tests:
#####CLI:

  from project directory run "behave features/"
  see test report at ./test-results/report/index.html

#####FROM PYCHARM(PRO ONLY):
- Open Edit configuration dialogue
- Add a new Behave configuration
- Select as working directory 'feature' directory of this project
- To run test select configuration and run it
- Report will be in ide interface


####PLANS:
- v 1.0: All standart scenarios
- v 2.0: Working with API
- v 3.0: Vagrant+Docker
- v 4.0: TODO
