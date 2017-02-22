# Created by User at 29.01.2017
Feature: Simple hello from tweeter

  Scenario: Hello
    Given I am logged in twitter
    When I request timeline
    Then I want to see my timeline