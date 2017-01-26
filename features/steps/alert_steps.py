from behave import *
from selenium.webdriver.common.alert import Alert


@step("I accept alert")
def accept_alert(context):
    Alert(context.driver).accept()


@step("I dismiss alert")
def dismiss_alert(context):
    Alert(context.driver).dismiss()
