# login xpaths
loginemailxpath="//*[@id='TikTok_Ads_SSO_Login_Email_Input']"
loginpswdxpath="//*[@id='TikTok_Ads_SSO_Login_Pwd_Input']"
loginSubmitxpath="(//button[@name='loginBtn'])[1]"
loginCaptcha="//div[@role='dialog']"
otpcodebox="//input[@id='TikTok_Ads_SSO_Login_Code_Input']"

# Home page pop-up xpaths
dashBoardGotIt="//button[span[text()='Got it']]"
closeBtnXpath="//span[@class='arco-modal-close-icon']"
dashBoardSkip="//button[.//span[text()='Skip']]"
chatOK="//button[.//span[text()='OK']]"
chatcrossicon="//div[@style='cursor: pointer; display: flex; flex-shrink: 0;']/img"

# Invitation xpaths
findcreator_xpath="//div[contains(text(), 'Find creators')]"
searchBox='//input[@placeholder="Search creators by username or user ID"]'
firstusername = "(//*[@class='text-body-m-medium text-neutral-text1 text-overflow-single'])[1]"
saveicon_xpath = '(//button[@data-tid="m4b_button" and @data-e2e="3ae7a02c-0a1b-60bb"])[1]'
invitation_xpath="//div[contains(text(), 'Target collaboration')]"
colabbtn_xpath='//button[text()="Invite to collaborate"]'
create_invitation_btn_xpath = '(//button[@data-tid="m4b_button" and span[text()="Create invitation"]])[2]'
# chosecreator_xpath='//input[@data-tid="m4b_input" and @data-e2e="e3bfd954-fc29-96dc" and @placeholder="Search creators by username or user ID"]'
addsavecreator_xpath='//button[@data-tid="m4b_button" and text()="Add saved creators"]'
checkbtn_xpath='//label[@class="arco-checkbox"]/input'
addbtn_xpath='//button[text()="Add"]'

choseproduct_xpath = '//div[text()="Choose products"]'
addproduct_xpath = '//button[text()="Add products"]'
addproduct2_xpath='//button[@data-e2e="a4c45b99-f2b8-b8fd"]'
dropdown_XPath = '//span[@class="arco-select-view-value" and text()="Product name"]'
IDoption_xpath = '//li[@role="option" and @class="arco-select-option m4b-select-option" and text()="Product ID"]' 
cardInput_Xpath='//input[@data-tid="m4b_input_search" and @placeholder="Search products"]'
cardcheck_xpath = '(//label[@class="arco-checkbox"]/input)[1]'
ADDBTN_xpath = '//button[span/text()="Add"]'
commsioninput_xpath='(//input[@role="spinbutton" and @data-tid="m4b_input_number" and @data-e2e="3a1bf7cf-465b-f541" and @placeholder="1.00-80.00"])[1]'
checkbox_xpath = '//div[@class="arco-checkbox-mask"]'

setupfresample_xpath = '//div[text()="Set up free samples"]'
radiobtn_xpath = "//button[@class='arco-switch arco-switch-type-circle m4b-switch' and @type='button']"
autobtn_xpath = "(//span[@class='arco-icon-hover arco-radio-icon-hover arco-radio-mask-wrapper'])[2]"
okbtn_xpath  ="//button[@class='arco-btn arco-btn-primary arco-btn-size-large arco-btn-shape-square' and @type='button']"

createinvitation_xpath = "//div[contains(text(), 'Create invitation')]"
invitationname_xpath = "//input[@placeholder='Invitation name']"
date_xpath = "//div[@class='arco-picker-input']//input[@placeholder='End date']"
email_xpath = '//input[@id="target_complete_details_contacts_7_input"]'
phone_xpath = '//input[@placeholder="Please enter a phone number"]'
messagearea_xpath = '//textarea[@id="target_complete_details_message_input"]'
sendbtn_xpath = '//button[span="Send"]'
messagebtn_xpath='//button[@data-e2e="1885d36e-bb16-5d32"]'
sharebtn_xpath="//button[normalize-space(text())='Share']"
#----------------------------------------Btach messages XPATHS-----------------------------------------#