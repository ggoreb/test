# scripts를 이용한 결과 출력 시 한글 깨짐 처리
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# 인터파크 투어 사이트에서 여행지를 입력 후 검색 -> 결과
# 로그인시 PC 처리가 어려운 경우 -> 모바일 사이트를 이용하여 로그인
# selenium 모듈 가져오기
# pip install selenium

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from Tour import TourInfo

# 사전에 필요한 정보 로드 -> 디비, 쉘, 배치 파일에서 인자로 받아서 세팅
main_url = 'http://tour.interpark.com/'
keyword = '로마'
# 상품 정보를 담는 리스트 (TourInfo 리스트)
tour_list = []

# 드라이버 로드
driver = wd.Chrome('c:/Python/chromedriver.exe')
# 옵션 부여 (프록시, 에이전트 조작, 이미지 생략)

# 사이트 접속 (GET)
driver.get(main_url)

# 검색창을 찾아서 검색어 입력
# id : SearchGNBText
driver.find_element_by_id('SearchGNBText').send_keys(keyword)
# 수정할 경우 -> 뒤에 내용이 붙어버림 -> clear() 후 내용 입력

# 검색 버튼 클릭
driver.find_element_by_css_selector('button.search-btn').click()

# 잠시 대기 -> 페이가 로드된 후 즉각적으로 데이터를 획득하는 행위는 자제
# 명시적 대기 -> 특정 요소가 발견될 때까지 대기
try:
    element = WebDriverWait(driver, 10).until(
        # 지정한 한개의 요소가 발견되면 대기 종료
        EC.presence_of_element_located( (By.CLASS_NAME, 'oTravelBox') )
    )
except Exception as e:
    print('error', e)

# 암시적 대기 -> DOM이 다 로드될 때까지 대기하고 지정 시간보다 일찍 로드되면 바로 진행
driver.implicitly_wait( 10 )

# 절대적 대기 -> 지정 시간만큼 대기 (디도스 방어 솔루션)

# 더보기 버튼을 누른 후 게시판 진입
driver.find_element_by_css_selector('.oTravelBox .moreBtnWrap > .moreBtn').click()

# searchModule.SetCategoryList(16, '') 스크립트 실행
for page in range(1, 2):
    try:
        # 자바스크립트 구동하기
        driver.execute_script("searchModule.SetCategoryList(%s, '')" % page)
        time.sleep(2)

        # 상품명, 코멘트, 기간1, 기간2, 가격, 평점, 썸네일, 링크(상품상세정보)
        boxItems = driver.find_elements_by_css_selector('.oTravelBox > .boxList > li')
        for li in boxItems:
            title = li.find_element_by_css_selector('.proSub').text
            price = li.find_element_by_css_selector('.proPrice').text
            area = li.find_elements_by_css_selector('.info-row .proInfo')[1].text
            link = li.find_element_by_css_selector('a').get_attribute('onclick')
            img = li.find_element_by_css_selector('img').get_attribute('src')
            print('상품명', title)
            print('가격', price)
            print('지역', area)
            print('링크', link)
            print('이미지', img)
            print('=' * 50)
            obj = TourInfo(title, price, area, link, img)
            tour_list.append(obj)
    except Exception as e:
        print('error', e)

# 브라우저 종료
driver.close()
driver.quit()

# 프로세스 종료
import sys
sys.exit()

print(tour_list, len(tour_list))












#
