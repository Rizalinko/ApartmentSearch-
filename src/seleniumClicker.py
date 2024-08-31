import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import json


def read_udata(jname):
    '''
    Reads user data from the json
    :return: json of the user data to be submitted to website
    '''
    with open(jname) as jsfile:
        return json.load(jsfile)

def ClickOnOriginalLink(url):
    '''

    :param url: url of the page with the contact form to fill up for the aprt application
    :return:
    '''

    # Read user data from json
    # Returned json has the following structure: {'Firstname': '', 'LastName': '', 'Email': '', 'Phone': '',
    #      'Message': message}
    user_data = read_udata('FormData')


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

    # Reads user data
    # the user_data json is in the following format: user_data = {'ContactFullName': 'Ramun Benedetti', 'ContactEmail': 'rizalinko@gmail.com', 'ContactPhoneNumber': '0762751992',
    #                  'ContactMessage': message}
    user_data = read_udata('FormDataComparis.json')

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
    # The user data json is in the following format: {'firstName': '', 'lastName': '', 'email': '', 'phone': '',
    #                  'street': '', 'city': '', 'zip': ''}
    user_data = read_udata('FormDataHomegate.json')


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

    # message is not in the read in json. get the message value from the base form
    message = read_udata('FormData.json')['message']
    message_box[0].send_keys(message)

    class_name = "HgButton_hgButton_35t1k.HgButton_primary_1zzAF.HgButton_defaultSize_2pFlx.ContactForm_submitButton_dSxPi"
    submit_button = browser.find_elements_by_class_name(class_name)
    submit_button[0].click()
    print('Clicked '+url)
