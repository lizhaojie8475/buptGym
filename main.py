from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
import time
import sys

item = 3  # 0：羽毛球 1：乒乓球 2：游泳馆 3：健身房 4: 沙河健身房（测试）
area_list = ['5982', '5983', '5984', '5985', '6002']
room_list = ['', '', '', '15415', '15478']
area_id = area_list[item]
now = datetime.datetime.now() + datetime.timedelta(days=1)
query_date = now.strftime("%Y%m%d")

def get_cookies():
    cookies = []
    cookie_1 = {"name": "PHPSESSID", "value": "hiij0rduk4184c8t48spb4inf0"}
    cookie_2 = {"name": "think_language", "value": "zh-cn"}
    cookies.append(cookie_1)
    cookies.append(cookie_2)

    return cookies


if __name__ == "__main__":
    if datetime.datetime.now().hour != 11:
        sys.exit()

    timeIndexes = ["02", "03", "04", "05", "06", "07", "08"]
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d37) NetType/WIFI Language/zh_CN')
    browser = webdriver.Chrome(options=chrome_options)

    i = 0
    while 1:
        if i >= len(timeIndexes):
            break
        reserve_td_ids = room_list[item] + '_' + query_date + timeIndexes[i]
        req_url = 'https://reservation.bupt.edu.cn//index.php/Wechat/Booking/confirm_booking?area_id=' + area_id + '&td_id=' + reserve_td_ids + '&query_date=' + query_date

        # 开始请求
        browser.get(req_url)

        # add cookie
        browser.add_cookie(get_cookies()[0])
        browser.add_cookie(get_cookies()[1])

        # 再次请求
        browser.get(req_url)
        if browser.title == "跳转中":  # 表示所选时间段还未开放
            time.sleep(0.5)
            continue
        else:
            i += 1
        # 选择余额支付
        browser.find_element(By.CSS_SELECTOR, "input[value='确认预约']").click()
        time.sleep(0.45)
        browser.find_element(By.CSS_SELECTOR, "input[type='radio'][id='package_pay_54168']").click()
        time.sleep(0.3)
        browser.find_element(By.CSS_SELECTOR, "button[class='btn btn-primary g-submit']").click()

    #关闭浏览器
    browser.close()
    #关闭chreomedriver进程
    browser.quit()