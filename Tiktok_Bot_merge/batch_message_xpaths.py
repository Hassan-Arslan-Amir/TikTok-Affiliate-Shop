loginemailxpath = "//*[@id='TikTok_Ads_SSO_Login_Email_Input']"
loginpswdxpath = "//*[@id='TikTok_Ads_SSO_Login_Pwd_Input']"
loginSubmitxpath = "(//button[@name='loginBtn'])[1]"
loginCaptcha = "//div[@role='dialog']"
otpcodebox = "//input[@id='TikTok_Ads_SSO_Login_Code_Input']"
hatcreator_xpath = "//*[@class='index-module_uname__VNMFM']"

Performancebtn_xpath = "//span[text()='Performance']"
GMVbtn_xpath = (
    "//div[@fieldtag='GMV']//button[contains(@class, 'index-module__button--ytUv6')]"
)
GMVbtn_xpath1 = "//span[text()='$100-$1K']"
GMVbtn_xpath2 = "//span[text()='$1K-$10K']"
GMVbtn_xpath3 = "(//span[text()='$10K+'])[1]"
Averageview_xpath = (
    '//div[@class="arco-typography" and text()="Average views per video"]'
)
Morethanhundrad_xpath = (
    '(//li[@role="option" and contains(text(), "More than 100")])[1]'
)

Follwerbtn_xpath = "//button[normalize-space(.)='Followers']"
Follwergender_xpath = "//button[normalize-space(.)='Follower gender']"
Femalebtn_xpath = (
    "//li[@class='arco-select-option m4b-select-option' and text()='Female']"
)
Malebtn_xpath = "//li[@class='arco-select-option m4b-select-option' and text()='Male']"
Follwerage_xpath = "//div[@class='w-full flex justify-between items-center']//div[@class='arco-typography' and contains(text(),'Follower age')]"
Follwerage_xpath0 = (
    '//span[text()="18 - 24" and contains(@class, "arco-select-option")]'
)
Follwerage_xpath1 = (
    '//span[text()="25 - 34" and contains(@class, "arco-select-option")]'
)
Follwerage_xpath2 = (
    '//span[text()="35 - 44" and contains(@class, "arco-select-option")]'
)
Follwerage_xpath3 = (
    '//span[text()="45 - 54" and contains(@class, "arco-select-option")]'
)
Follwerage_xpath4 = '//span[text()="55+" and contains(@class, "arco-select-option")]'

CreatorsBtn_xpath = "//button[normalize-space(.)='Creators']"
Productcategory_xpath = "//button[contains(., 'Product category')]"
CreatorsBtn_xpath2 = '(//label[@data-e2e="d7d35802-fd28-d757"]/input[@type="radio"]/following-sibling::button[@data-tid="m4b_button"])[1]'

messageArea1 = "//textarea[@placeholder='Send a message']"
messageArea2 = "//textarea[@placeholder='im_sdk_agent_operate_input_pro']"
messageSendXpath = "//button[@type='button'][.//span[text()='Send']]"

sidebarelements = '(//div[@class="arco-tabs-header"]/div[@role="tab" and span/span/div/div[contains(text(), "Products")]])[1]'
cardInputXpath = "//input[@placeholder='Search ID']"
cardInputID_Xpath = "//input[@placeholder='Search ID']"
searchIcon = "(//span[@class='arco-input-group-suffix'])[2]"
productcard = "(//div[contains(@class, 'py-16') and contains(@class, 'hover:bg-neutral-bg2') and contains(@class, 'cursor-pointer') and contains(@class, 'bg-white') and contains(@class, 'flex') and contains(@class, 'items-start') and contains(@class, 'relative')])[1]"
sendproduct = "(//button[@data-tid='m4b_button' and @data-e2e='a7fd9ff4-af7c-a295' and @class='arco-btn arco-btn-text arco-btn-size-small arco-btn-shape-square m4b-button absolute top-0 bottom-0 m-auto right-16 index-module__sendButton--Qq1NZ arco-btn-primary-text' and @type='button'])[1]"
sendproduct2 = "(//button[@data-tid='m4b_button' and @data-e2e='a7fd9ff4-af7c-a295' and @class='arco-btn arco-btn-text arco-btn-size-small arco-btn-shape-square m4b-button absolute top-0 bottom-0 m-auto right-16 index-module__sendButton--Qq1NZ arco-btn-primary-text' and @type='button'])[2]"
productcardname = (
    '(//div[@data-e2e="bffe5aab-5663-c763"]/span[@class="text-overflow-muli-2"])[1]'
)
text_xpath = (
    ".//span[@class='text-body-m-medium text-neutral-text1 text-overflow-single']"
)
alreadMessage = "//div[@class='chatd-bubble-main chatd-bubble-main--self chatd-bubble-main--left chatd-bubble-main--platform-pc index-module_bubble__f4ksL']"
searchBox = '//input[@placeholder="Search names, products, hashtags, or keywords"]'
firstusername = (
    "(//*[@class='text-body-m-medium text-neutral-text1 text-overflow-single'])[1]"
)


# pop xpath
dashBoardGotIt = "//button[span[text()='Got it']]"
closeBtnXpath = "//span[@class='arco-modal-close-icon']"
dashBoardSkip = "//button[.//span[text()='Skip']]"
chatOK = "//button[.//span[text()='OK']]"
chatcrossicon = "//div[@style='cursor: pointer; display: flex; flex-shrink: 0;']/img"

# reply xpath
reply_xpath = '//div[@class="chatd-bubble-main chatd-bubble-main--other chatd-bubble-main--left chatd-bubble-main--platform-pc index-module_bubble__f4ksL"]/pre[@class="index-module_content__9a00-"]'
