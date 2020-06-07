import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select

message = 'Gruezi, Wir sind eine Paar, die sehr an Ihrer Wohnung interessiert sind und würden uns über einen Besichtigungstermin freuen. \n Grüsse, Ramun and Rizalina'
# '\n\nFür English: 0762751992 \nFür Deutsch: 0765038724 \nGrüsse, Ramun and Rizalina'


def ClickOnOriginalLink(url):
    user_data = {'Firstname': 'Ramun', 'LastName': 'Benedetti', 'Email': 'rizalinko@gmail.com', 'Phone': '0762751992',
                'Message': message}

    opts = Options()
    opts.set_headless()
    browser = Firefox(options=opts)
    browser.get(url)


    for key in user_data.keys():
        form = browser.find_elements_by_name(key)
        try:
            form[0].clear()
            form[0].send_keys(user_data[key])
        except IndexError:
            break

    submit_buttom_name = 'btnSendEmail'
    button = browser.find_elements_by_id(submit_buttom_name)
    button[0].click()

def ClickOnLinkComparis(url):
    user_data = {'ContactFullName': 'Ramun Benedetti', 'ContactEmail': 'rizalinko@gmail.com', 'ContactPhoneNumber': '0762751992',
                 'ContactMessage': message}
    opts = Options()
    opts.set_headless()
    browser = Firefox(options=opts)
    browser.get(url)

    # try to filll the form contact adviser directly
    try:
        for key in user_data.keys():
            form = browser.find_elements_by_id(key)
            form[0].clear()
            form[0].send_keys(user_data[key])

        submit_button_name = 'icon-right.expanded.zero-margin.hf-contact-form-button.button'
        submit_button = browser.find_elements_by_class_name(submit_button_name)
        submit_button[0].click()
        print('Clicked ' + url)

    except IndexError:
        print('Did not find the form to contact advisor directly. Looking for follow link')

        redirect_link = browser.find_elements_by_class_name('follow-link')
        if redirect_link[0].text.count('homegate'):
            print('Originally posted on homegate. This is being taken care of in another programm')
            return
        if redirect_link[0].text.count('anibis'):
            print('Originally posted on anibis. Need to login to apply')
            return

        listnig_id = url.split('/')[-1]
        redirect_link = 'https://www.comparis.ch/immobilien/redirect/tooriginalad?adId={}'.format(listnig_id)

        try:
            ClickOnOriginalLink(redirect_link)
        except IndexError:
            print('Ooops.. Looks like the listing is already gone from original website')


def clickOnlinkHomegate(url):
    user_data = {'firstName': 'Ramun', 'lastName': 'Benedetti', 'email': 'rizalinko@gmail.com', 'phone': '0762751992',
                 'street': 'Am Glattbogen 175', 'city': 'Zurich', 'zip': '8050'}

    opts = Options()
    opts.set_headless()
    browser = Firefox(options=opts)
    browser.get(url)

    for key in user_data.keys():
        form = browser.find_elements_by_name(key)
        try:
            form[0].clear()
            form[0].send_keys(user_data[key])
        except IndexError:
            break

    text_class = 'HgTextArea_textArea_-4ajb'
    message_box = browser.find_elements_by_class_name(text_class)
    message_box[0].clear()
    message_box[0].send_keys(message)

    class_name = "HgButton_hgButton_35t1k.HgButton_primary_1zzAF.HgButton_defaultSize_2pFlx.ContactForm_submitButton_dSxPi"
    submit_button = browser.find_elements_by_class_name(class_name)
    submit_button[0].click()
    print('Clicked '+url)
