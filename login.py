# 1. 폴더내에 크롬과 동일한 버전의 드라이버가 존재해야 함.(복붙해놓기)
# 2. 참고할 내용
# https://quasarzone.com/bbs/qb_saleinfo/views/915013?_method=post&_token=EsFVwGDEvAVx3R4BZ2kXGcz2voeuzA174YlwpGtY&category=&direction=DESC&keyword=&kind=subject&page=1&popularity=Y&sort=num%2C%20reply&type=
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import slack


# 사용할 변수 선언
url = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"
uid = "ysjjhb10"
upw = "1q2w3e4r!"

# alert 경고창 처리 함수
def alert_process():
    try:
        result = driver.switch_to.alert
        print(result.text)
        result.accept()
    except:
        print("There is no alert message")


# browser = webdriver.Chrome('./chromedriver.exe')
driver = webdriver.Chrome("./chromedriver/chromedriver.exe")

# 네이버 이동
driver.get("http://naver.com")
# 네이버 로그인 페이지로 이동
driver.get(url)
time.sleep(2)

# 아이디 입력폼
tag_id = driver.find_element_by_name("id")
# 패스워드 입력폼
tag_pw = driver.find_element_by_name("pw")

# id 입력
# 입력폼 클릭 -> paperclip에 선언한 uid 내용 복사 -> 붙여넣기
tag_id.click()
pyperclip.copy(uid)
tag_id.send_keys(Keys.CONTROL, "v")
time.sleep(1)

# pw 입력
# 입력폼 클릭 -> paperclip에 선언한 upw 내용 복사 -> 붙여넣기
tag_pw.click()
pyperclip.copy(upw)
tag_pw.send_keys(Keys.CONTROL, "v")
time.sleep(1)

# 로그인 버튼 클릭
login_btn = driver.find_element_by_id("log.login")
login_btn.click()
time.sleep(2)

# 로그인 한 뒤에 포인트 사이트로 이동
driver.get("https://event2.pay.naver.com/event/benefit/list")

# 기존 네이버 포인트 확인
before_my_npoint = driver.find_elements_by_xpath('//dl[@class="my_npoint"]//strong')
before_my_npoint = before_my_npoint[0].text

# 다양한 형태의 적립이 존재한다.
# 1. 클릭만 하면 되는 것
# 2. 특정한 시간에 열리고 버튼을 눌러 특정 사이트로 이동해야 하는 경우
# 3. 모바일 전용
# 4. 인스타 등 구독을 해야 하는 경우

# 일단은 모든 url 한번씩 클릭해보고 나오는 것으로 하자.
# li class="eventList" 목록을 먼저 반환 받는다.
# 그 중에서 class 명이 "item type_system"인 a 태그들에서 url을 가져온다.
# url에 접속한다.
point_elements = driver.find_elements_by_xpath('//*[@id="eventList"]/li/a')
url_list = [element.get_attribute("href") for element in point_elements]

# url 접속해서 포인트 얻기
# 클릭만 하면 포인트 받는 경우만 가능.
for url in url_list:
    driver.get(url)
    time.sleep(0.5)
    alert_process()  # alert 경고창 처리
    time.sleep(1)

time.sleep(1)
driver.get("https://event2.pay.naver.com/event/benefit/list")  # 원래 페이지로 돌아옴

# 갱신된 네이버 포인트 확인
after_my_npoint = driver.find_elements_by_xpath('//dl[@class="my_npoint"]//strong')
after_my_npoint = after_my_npoint[0].text
print("기존 네이버 포인트{0} -> {1}".format(before_my_npoint, after_my_npoint))

# 결과 slack 메시지로 보내기
time.sleep(1)
slack.post_message(
    slack.myToken,
    "auto_bot",
    "기존 네이버 포인트 {0} -> {1}".format(before_my_npoint, after_my_npoint),
)
time.sleep(1)

# driver 종료
driver.quit()
