Feature: Log in

  Scenario: Unsuccessful login
    Given I am on Login page
    When I login with username 'abcd@ed.ba' and password '111111'
    Then I want to see error message "Incorrect username or password."
