from selenium.common import NoSuchElementException

from chrome_manager import *
from utils import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class CrawlerService(ChromeDriverService):
    def start_crawler(self, url, headless: bool, maximize: bool = True, wait: int = 3):
        img_links = []

        try:
            self.start(url, headless, maximize, wait)
            time.sleep(3)

            if not self.browser:
                raise SystemExit("Chrome browser failed to start.")

            WebDriverWait(self.browser, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "entryIframe"))
            )
            print("iframe으로 전환 성공")

            # 2. 이제 iframe 내부에서 원하는 요소를 찾습니다.
            #    이전과 동일한 코드를 사용하면 됩니다.
            first_element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'BXtr_') and contains(@class, 'tAvTy')]"))
            )
            print("첫 번째 요소 찾기 성공")

            subtab = first_element.find_element(By.CSS_SELECTOR, "div.place_fixed_subtab")
            container = subtab.find_element(By.CSS_SELECTOR, "div.ngGKH.Xz1i7")
            review_button = container.find_element(By.CSS_SELECTOR, "li.Zt2Kl.NIebS")

            review_button.click()
            time.sleep(3)
            print("리뷰 버튼 클릭 성공!")

            place_section = self.browser.find_element(By.CSS_SELECTOR, "div.place_section_content")
            wzrbNs = place_section.find_elements(By.CSS_SELECTOR, "div.wzrbN")

            for wzrbN in wzrbNs:
                try:
                    # 항목 내부에 img 태그가 없는 경우를 대비
                    img = wzrbN.find_element(By.TAG_NAME, "img")
                    img_link = img.get_attribute("src")
                    img_links.append(img_link)
                except NoSuchElementException:
                    # 이미지가 없는 항목은 건너뜁니다.
                    print("이미지를 찾을 수 없는 항목이 있어 건너뜁니다.")
                    continue

            # 최종 결과 출력
            print(f"총 {len(img_links)}개의 이미지 링크를 수집했습니다.")
            print(img_links)

        except Exception as e:
            print(f"ERROR: {e}")

        finally:
            print(img_links)
            self.stop()


if __name__ == "__main__":
    service = CrawlerService()
    service.start_crawler("https://map.naver.com/p/entry/place/1094965330?c=15.00,0,0,0,dh&placePath=/photo?additionalHeight=76&fromPanelNum=1&locale=ko&svcName=map_pcv5&timestamp=202509051056&from=map&fromPanelNum=1&locale=ko&svcName=map_pcv5&timestamp=202509051015&additionalHeight=76&filterType=AI%20View&subFilter=INTERIOR", False)