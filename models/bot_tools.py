import json
import time
from langchain.tools import tool
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from models.utils.wbd import Singleton


@tool(description="頁面停留時間")
def time_sleep(s):
    time.sleep(s)


@tool(description="尋找網頁中符合的特定元素")
def get_simplified_dom() -> str:
    shared_driver = Singleton().get_value()
    page_source = shared_driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    interactive_elements = []
    for element in soup.find_all(
        ['a', 'button', 'input', 'select', 'textarea']
    ):
        elem_info = {
            'tag': element.name,
            'text': element.get_text(strip=True),
            'id': element.get('id'),
            'name': element.get('name'),
            'placeholder': element.get('placeholder'),
        }
        elem_info_clean = {k: v for k, v in elem_info.items() if v}
        if elem_info_clean:
            interactive_elements.append(elem_info_clean)

    return json.dumps(interactive_elements, ensure_ascii=False, indent=2)


@tool(description="當需要搜尋網頁資訊時，使用這個工具。")
def open_website(url: str) -> str:

    shared_driver = Singleton().get_value()
    shared_driver.get(url)
    return f"Open url: {url} successful."


@tool(description="在webdriver中直接執行javascript")
def run_by_js(script: str) -> str:

    shared_driver = Singleton().get_value()
    return shared_driver.execute_script(script)


@tool(description="找到輸入區塊並填上文字")
def find_element_and_send_keys(description: str, text_to_send: str) -> str:
    """
    根據元素的描述性文字 (例如 '搜尋框' 或 '帳號輸入欄位')，
    找到頁面上的元素並輸入指定的文字。
    """
    # 這是一個簡化版的智慧定位，實際應用中可以做得更複雜
    # 這裡我們用 XPath 的 contains() 來做一個模糊匹配

    shared_driver = Singleton().get_value()
    try:
        xpath = f"//*[contains(@placeholder, '{description}') or \
            contains(@aria-label, '{description}') or contains(text(), \
            '{description}') or @id='{description}' or \
            @name='{description}' or @title='{description}']"
        element = shared_driver.find_element(By.XPATH, xpath)
        element.send_keys(text_to_send)
        return f"成功在 '{description}' 輸入文字: '{text_to_send}'。 \
            元素定位器: {xpath}"
    except Exception as e:
        return f"錯誤：找不到描述為 '{description}' 的元素。 {e}"


@tool(description="找到元素並按下")
def find_element_and_click(description: str) -> str:
    """
    根據元素的描述性文字 (例如 '登入按鈕' 或 '下一步')，找到頁面
    上的元素並點擊它。
    """

    shared_driver = Singleton().get_value()
    p1 = f"//*[(self::a or self::button) and \
            (contains(text(), '{description}') or \
            contains(@aria-label, '{description}'))]"
    p2 = f"//input[@type='submit' and @value='{description}' or \
            @name='{description}' or @title='{description}']"
    try:
        xpath = f"{p1} | {p2}"
        # xpath = f"//*[(self::a or self::button) and \
        #     (contains(text(), '{description}') or \
        #     contains(@aria-label, '{description}'))] | \
        #     //input[@type='submit' and @value='{description}' or \
        #     @name='{description}' or @title='{description}']"
        element = shared_driver.find_element(By.XPATH, xpath)
        element.click()
        return f"成功點擊 '{description}'。 元素定位器: {xpath}"
    except Exception as e:
        return f"錯誤：找不到描述為 '{description}' 的可點擊元素。 {e}"
