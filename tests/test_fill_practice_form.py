import os

from selene import browser, have, command


def test_type_registration_form(browser_managment):
    test_data = {
        'first_name': 'Linus',
        'last_name': 'Torvalds',
        'email': 'torvalds@osdl.org',
        'gender': 'Female',
        'mobile': '9876543210',
        'birth_day': '28',
        'birth_month': 'December',
        'birth_year': '1969',
        'subject1': 'Accounting',
        'subject2': 'Maths',
        'hobby': 'Reading',
        'picture': 'contact.jpg',
        'address': '123,Open Source Development Labs',
        'state': 'NCR',
        'city': 'Delhi'
    }

    picture_path = os.path.abspath(f'../data/{test_data["picture"]}')

    browser.open('/automation-practice-form')

    browser.element('#firstName').type(test_data['first_name'])
    browser.element('#lastName').type(test_data['last_name'])
    browser.element('#userEmail').type(test_data['email'])
    browser.element(f'input[value={test_data["gender"]}]').perform(command.js.click)
    browser.element('#userNumber').type(test_data['mobile'])

    browser.element('#dateOfBirthInput').click()
    browser.element('.react-datepicker__year-select').click()
    browser.all('.react-datepicker__year-select option').element_by(
        have.text(test_data['birth_year'])
    ).click()
    browser.element('.react-datepicker__month-select').click()
    browser.all('.react-datepicker__month-select option').element_by(
        have.text(test_data['birth_month'])
    ).click()
    browser.element(f'.react-datepicker__day--0{test_data["birth_day"]}').click()

    browser.element('#subjectsInput').type(test_data['subject1']).press_enter()
    browser.element('#subjectsInput').type(test_data['subject2']).press_enter()

    browser.all('.custom-checkbox label').element_by(have.text(test_data['hobby'])).click()

    browser.element('#uploadPicture').send_keys(picture_path)

    browser.element('#currentAddress').type(test_data['address'])

    browser.element('#state').click()
    browser.all('[id^="react-select-3-option"]').element_by(have.text(test_data['state'])).click()
    browser.element('#city').click()
    browser.all('[id^="react-select-4-option"]').element_by(have.text(test_data['city'])).click()

    browser.element("#submit").click()

    expected_results = {
        'Student Name': f'{test_data["first_name"]} {test_data["last_name"]}',
        'Student Email': test_data['email'],
        'Gender': test_data['gender'],
        'Mobile': test_data['mobile'],
        'Date of Birth': f'{test_data["birth_day"]} {test_data["birth_month"]},{test_data["birth_year"]}',
        'Subjects': f'{test_data["subject1"]}, {test_data["subject2"]}',
        'Hobbies': test_data['hobby'],
        'Picture': test_data['picture'],
        'Address': test_data['address'],
        'State and City': f'{test_data["state"]} {test_data["city"]}'
    }

    for field, value in expected_results.items():
        browser.all('tr').element_by(have.text(field)).should(have.text(value))
