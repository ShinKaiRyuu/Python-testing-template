from behave import *
import tweepy


@given("I am logged in twitter")
def step_impl(context):
    auth = tweepy.OAuthHandler('dXZrNVzMlbJTrNnKwmLg963lF', 'hmLPqWb40MGlfimF4V975mB0x7GpI6Dg8fAxd36sdiwsr6XOY8')
    auth.set_access_token('350953442-Rpkl1bQGZyovHHqvc6e26V36FOkhoF0nptxAzBXN',
                          '3YlFl1OWAGLJ3hB1tuy6dgBGRBiqTeFLuMFZPwuca7WUg')
    context.api = tweepy.API(auth)


@when("I request timeline")
def step_impl(context):
    context.public_tweets = context.api.home_timeline()


@then("I want to see my timeline")
def step_impl(context):
    assert (len(context.public_tweets) != 0)
