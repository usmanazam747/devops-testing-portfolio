*** Settings ***
Documentation     E-Commerce Platform - User Management Test Suite
Library           SeleniumLibrary
Library           String
Test Setup        Open Browser To Application
Test Teardown     Close Browser
Suite Setup       Set Suite Variables
Suite Teardown    Log    Test Suite Completed

*** Variables ***
${BASE_URL}       http://localhost:3000
${BROWSER}        chrome
${DELAY}          0.5s
${USERNAME}       robotuser
${EMAIL}          robot@example.com
${PASSWORD}       RobotPass123!

*** Keywords ***
Set Suite Variables
    Set Global Variable    ${SCREENSHOTS_DIR}    ${CURDIR}/screenshots
    Create Directory    ${SCREENSHOTS_DIR}

Open Browser To Application
    ${chrome_options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${chrome_options}    add_argument    --headless
    Call Method    ${chrome_options}    add_argument    --no-sandbox
    Call Method    ${chrome_options}    add_argument    --disable-dev-shm-usage
    Open Browser    ${BASE_URL}    ${BROWSER}    options=${chrome_options}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Capture Page Screenshot On Failure
    ${timestamp}=    Get Time    epoch
    Capture Page Screenshot    ${SCREENSHOTS_DIR}/failure_${timestamp}.png

*** Test Cases ***
User Can Register Successfully
    [Documentation]    Test that a new user can register successfully
    [Tags]    registration    smoke
    
    Go To    ${BASE_URL}/register
    Wait Until Page Contains Element    id:username    timeout=10s
    
    Input Text    id:username    ${USERNAME}
    Input Text    id:email    ${EMAIL}
    Input Text    id:password    ${PASSWORD}
    Input Text    id:first_name    Robot
    Input Text    id:last_name    Test
    
    Click Button    id:register-button
    
    Wait Until Page Contains    successfully registered    timeout=10s
    Page Should Contain    successfully registered

User Cannot Register With Duplicate Username
    [Documentation]    Test that registration fails with duplicate username
    [Tags]    registration    negative
    
    Go To    ${BASE_URL}/register
    Wait Until Page Contains Element    id:username    timeout=10s
    
    Input Text    id:username    existinguser
    Input Text    id:email    new@example.com
    Input Text    id:password    ${PASSWORD}
    
    Click Button    id:register-button
    
    Wait Until Page Contains    already exists    timeout=10s
    Page Should Contain    already exists

User Can Login Successfully
    [Documentation]    Test that registered user can login
    [Tags]    login    smoke    critical
    
    Go To    ${BASE_URL}/login
    Wait Until Page Contains Element    id:username    timeout=10s
    
    Input Text    id:username    ${USERNAME}
    Input Text    id:password    ${PASSWORD}
    
    Click Button    id:login-button
    
    Wait Until Location Contains    dashboard    timeout=10s
    Location Should Contain    dashboard
    
    Page Should Contain Element    id:user-dashboard

User Cannot Login With Invalid Credentials
    [Documentation]    Test that login fails with wrong credentials
    [Tags]    login    negative
    
    Go To    ${BASE_URL}/login
    Wait Until Page Contains Element    id:username    timeout=10s
    
    Input Text    id:username    wronguser
    Input Text    id:password    wrongpassword
    
    Click Button    id:login-button
    
    Wait Until Page Contains    Invalid credentials    timeout=10s
    Page Should Contain    Invalid credentials

User Can View Product Catalog
    [Documentation]    Test browsing product catalog
    [Tags]    products    smoke
    
    Go To    ${BASE_URL}/products
    Wait Until Page Contains Element    class:product-card    timeout=10s
    
    ${product_count}=    Get Element Count    class:product-card
    Should Be True    ${product_count} > 0
    
    Page Should Contain Element    class:product-card

User Can View Product Details
    [Documentation]    Test viewing individual product details
    [Tags]    products
    
    Go To    ${BASE_URL}/products
    Wait Until Page Contains Element    class:product-card    timeout=10s
    
    Click Element    xpath://div[@class='product-card'][1]
    
    Wait Until Location Contains    /product/    timeout=10s
    Wait Until Page Contains Element    class:product-detail    timeout=10s
    
    Page Should Contain Element    class:product-detail
    Page Should Contain Element    id:product-name
    Page Should Contain Element    id:product-price

User Can Add Product To Cart
    [Documentation]    Test adding product to shopping cart
    [Tags]    cart    critical
    
    # First login
    Go To    ${BASE_URL}/login
    Input Text    id:username    ${USERNAME}
    Input Text    id:password    ${PASSWORD}
    Click Button    id:login-button
    Wait Until Location Contains    dashboard    timeout=10s
    
    # Browse and add to cart
    Go To    ${BASE_URL}/products
    Wait Until Page Contains Element    class:product-card    timeout=10s
    Click Element    xpath://div[@class='product-card'][1]
    
    Wait Until Page Contains Element    id:add-to-cart    timeout=10s
    Click Button    id:add-to-cart
    
    Wait Until Page Contains    added to cart    timeout=10s
    Page Should Contain    added to cart

User Can Complete Checkout Process
    [Documentation]    Test complete purchase flow from cart to order
    [Tags]    checkout    critical    e2e
    
    # Login
    Go To    ${BASE_URL}/login
    Input Text    id:username    ${USERNAME}
    Input Text    id:password    ${PASSWORD}
    Click Button    id:login-button
    Wait Until Location Contains    dashboard    timeout=10s
    
    # Add product to cart
    Go To    ${BASE_URL}/products
    Wait Until Page Contains Element    class:product-card    timeout=10s
    Click Element    xpath://div[@class='product-card'][1]
    Wait Until Page Contains Element    id:add-to-cart    timeout=10s
    Click Button    id:add-to-cart
    Sleep    2s
    
    # Go to cart
    Click Element    id:cart-icon
    Wait Until Page Contains Element    id:cart-items    timeout=10s
    
    # Proceed to checkout
    Click Button    id:checkout-button
    Wait Until Page Contains Element    class:checkout-form    timeout=10s
    
    # Fill checkout form
    Input Text    id:address    123 Test Street
    Input Text    id:city    Test City
    Input Text    id:postal_code    12345
    
    # Complete order
    Click Button    id:place-order-button
    
    Wait Until Page Contains    order placed    timeout=10s
    Page Should Contain Element    class:order-confirmation
    Page Should Contain    thank you

Search Functionality Works
    [Documentation]    Test product search feature
    [Tags]    search
    
    Go To    ${BASE_URL}/products
    Wait Until Page Contains Element    id:search-box    timeout=10s
    
    Input Text    id:search-box    test product
    Press Keys    id:search-box    RETURN
    
    Wait Until Page Contains Element    class:product-card    timeout=10s
    Page Should Contain Element    class:product-card

User Can Update Profile
    [Documentation]    Test updating user profile information
    [Tags]    profile
    
    # Login
    Go To    ${BASE_URL}/login
    Input Text    id:username    ${USERNAME}
    Input Text    id:password    ${PASSWORD}
    Click Button    id:login-button
    Wait Until Location Contains    dashboard    timeout=10s
    
    # Go to profile
    Click Element    id:profile-link
    Wait Until Page Contains Element    id:edit-profile-button    timeout=10s
    
    # Edit profile
    Click Button    id:edit-profile-button
    Input Text    id:first_name    UpdatedName
    Click Button    id:save-profile-button
    
    Wait Until Page Contains    updated successfully    timeout=10s
    Page Should Contain    updated successfully

*** Keywords ***
Login As User
    [Arguments]    ${username}    ${password}
    Go To    ${BASE_URL}/login
    Input Text    id:username    ${username}
    Input Text    id:password    ${password}
    Click Button    id:login-button
    Wait Until Location Contains    dashboard    timeout=10s
