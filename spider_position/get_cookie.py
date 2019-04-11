import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class GetCookie(object):

    def __init__(self, url):
        self.url = url

    # 定义一个类方法获取cookie
    @property
    def get_cookies(self):
        """
        获取浏览器中的cookie
        :return: cookie tuple
        """
        print('获取新cookie')
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        u'启动selenium获取浏览器cookies'
        driver = webdriver.Chrome(executable_path='/Users/liudianjun/Desktop/chromedriver/chromedriver',
                                  chrome_options=chrome_options
                                  )
        driver.get(self.url)

        time.sleep(0.5)
        cookie = driver.get_cookies()   #获取浏览器cookies
        driver.quit()
        return tuple(cookie)



if __name__ == '__main__':
    url = 'https://www.lagou.com/jobs/list_?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput='
    cookie = GetCookie(url).get_cookies
    print(cookie)