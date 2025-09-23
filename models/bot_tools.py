import json
import time
import yaml
from langchain.tools import tool
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from models.utils.wbd import Singleton
from models.utils.report import ReportSingleton


@tool(description="取得測案步驟檔")
def get_test_case(path: str, filename: str):
    report = ReportSingleton()
    fullpath = f"{path}/{filename}"
    with open(fullpath, "a") as f:
        yaml_string = yaml.dump(
            report.get_value(),
            f,
            allow_unicode=True,
            sort_keys=False
        )
        # f.write(yaml_string)
    print(yaml_string)


# 保留功能
@tool(description="""
      描述webdriver執行的步驟，描述metadata必須包含以下欄位：
      element_name: 網頁元素名稱,
      desc: 簡單說明,
      module: 使用的function name,
      url: 網址連結,
      by: 透過什麼方式指定元素, xpath, css....
      """)
def set_step(
    element_name: str,
    desc: str,
    function_name: str,
    url: str,
    by: str
) -> str:
    report = ReportSingleton()
    desc = {
        "elementName": element_name,
        "desc": desc,
        "module": function_name,
        "url": url,
        "by": by
    }
    report.set_value(desc)
    return desc


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
    test_case = ReportSingleton()
    shared_driver.get(url)
    step = {
        "elementName": "",
        "desc": f"Open {url}",
        "interval": 1,
        "module": "open_website",
        "url": url
    }
    test_case.set_value(step)
    return f"Open url: {url} successful."


@tool(description="在webdriver中直接執行javascript")
def run_by_js(script: str) -> str:

    shared_driver = Singleton().get_value()
    test_case = ReportSingleton()
    step = {
        "elementName": "",
        "desc": "Run script",
        "interval": 1,
        "module": "run_by_js",
        "url": ""
    }
    test_case.set_value(step)
    return shared_driver.execute_script(script)


@tool(description="找到輸入區塊並填上文字")
def find_element_and_send_keys(description: str, text_to_send: str) -> str:
    """
    根據元素的描述性文字 (例如 '搜尋框' 或 '帳號輸入欄位')，
    找到頁面上的元素並輸入指定的文字。
    """

    shared_driver = Singleton().get_value()
    test_case = ReportSingleton()

    try:
        xpath = f"//*[contains(@placeholder, '{description}') or \
            contains(@aria-label, '{description}') or contains(text(), \
            '{description}') or @id='{description}' or \
            @name='{description}' or @title='{description}']"
        element = shared_driver.find_element(By.XPATH, xpath)
        element.send_keys(text_to_send)

        step = {
            "elementName": xpath.replace('\n', ''),
            "desc": description,
            "module": "fine_element_and_send_keys",
            "key": text_to_send
        }
        test_case.set_value(step)
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
    test_case = ReportSingleton()
    p1 = f"//*[(self::a or self::button) and \
            (contains(text(), '{description}') or \
            contains(@aria-label, '{description}'))]"
    p2 = f"//input[@type='submit' and @value='{description}' or \
            @name='{description}' or @title='{description}']"
    try:
        xpath = f"{p1} | {p2}"
        element = shared_driver.find_element(By.XPATH, xpath)
        element.click()

        step = {
            "elementName": xpath.replace('\n', ''),
            "desc": description,
            "module": "fine_element_and_click",
        }
        test_case.set_value(step)
        return f"成功點擊 '{description}'。 元素定位器: {xpath}"
    except Exception as e:
        return f"錯誤：找不到描述為 '{description}' 的可點擊元素。 {e}"
