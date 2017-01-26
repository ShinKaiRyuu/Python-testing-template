from behave import *
from nose.tools import assert_equal, assert_in
from features.steps.common_steps import reload_page

from helpers.driver_helpers import update_driver_cookies


@when("I login with username '{username}' and password '{password}'")
def step_impl(context, username, password):
    credentials = {
        'username': username,
        'password': password,
    }
    context.page.login_with(credentials)


@given("I am logged in as '{username}' and password '{password}'")
def step_impl(context, username, password):
    credentials = {
        'username': username,
        'password': password,
    }
    context.execute_steps('''
        Given I am on Main page
    ''')
    update_driver_cookies(context.driver, credentials)
    reload_page(context)


@then("I want to see that I am {login_status}")
def step_impl(context, login_status):
    assert login_status in ['logged in', 'logged out']
    assert_equal(login_status, context.page.get_login_status())


@then('I want to see error message "{error_message}"')
def step_impl(context, error_message):
    assert_in(error_message, context.page.get_error_messages())
