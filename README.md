# LangChainTools

基於 LangChain 打造的 AI 對話系統，能理解自然語言指令，並透過 Selenium 和系統命令列工具來自動化控制網頁瀏覽與系統操作。

## 專案介紹

本專案旨在建立一個智慧代理人 (Agent)，模擬一位資深的自動化測試工程師。使用者可以透過簡單的中文指令，讓 AI 操作網頁瀏覽器執行開啟網頁、填寫表單、點擊按鈕等任務，甚至執行終端機命令。

其核心是利用 LangChain 框架，結合 Google Gemini 大型語言模型 (LLM) 的強大理解能力，以及一系列自定義的工具 (Tools) 來完成具體操作。

## 主要功能

  * **自然語言理解**：能聽懂如「打開 Google 然後搜尋 LangChain」之類的指令。
  * **網頁自動化**：
      * 開啟指定 URL 的網頁。
      * 智慧分析頁面，找出可互動的元素 (輸入框、按鈕、連結等)。
      * 在指定的輸入框中填寫文字。
      * 點擊頁面上的按鈕或連結。
      * 可直接執行 JavaScript 來操作網頁。
  * **系統命令執行**：能夠在終端機 (Linux/macOS) 環境下執行系統命令。
  * **逐步執行與回報**：AI 會遵循「觀察 -\> 行動」的模式，並向使用者回報每一步的執行結果。

## 技術架構

  * **語言模型 (LLM)**: `langchain-google-genai` (Google Gemini)
  * **代理人框架 (Agent Framework)**: `LangChain`
  * **網頁自動化**: `Selenium`
  * **網頁解析**: `BeautifulSoup4`
  * **工具集 (Tools)**:
      * **網頁工具 (`models/bot_tools.py`)**: 包含開啟網頁、分析 DOM、輸入文字、點擊元素等 Selenium 相關操作。
      * **命令列工具 (`models/cmd_tools.py`)**: 執行終端機命令。
  * **WebDriver 管理**: 使用單例模式 (Singleton) 管理 Selenium WebDriver (`models/utils/wbd.py`)，確保整個應用程式共用同一個瀏覽器實例。
  * **提示工程 (Prompt Engineering)**: 透過精心設計的系統提示 (`system/prompt/robot_prompt.py`) 來引導 AI 的行為，使其表現得像一位專業的自動化工程師。

## 安裝與設定

1.  **複製專案**

    ```bash
    git clone <your-repository-url>
    cd langchaintools
    ```

2.  **安裝依賴套件**

    ```bash
    pip install -r requirements.txt
    ```

    *若無 `requirements.txt`，請手動安裝:*

    ```bash
    pip install langchain langchain-google-genai selenium beautifulsoup4 python-dotenv
    ```

3.  **下載 WebDriver**
    本專案預設使用 Microsoft Edge 瀏覽器。請下載與您的 Edge 瀏覽器版本相符的 `msedgedriver`，並將其執行檔放置在專案的根目錄下。

      * [Microsoft Edge WebDriver 下載頁面](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

4.  **設定環境變數**
    在專案根目錄下建立一個 `.env` 檔案，並填入以下內容：

    ```env
    # .env
    AIModel="gemini-pro"
    API_KEY="YOUR_GOOGLE_API_KEY"
    ```

    請將 `YOUR_GOOGLE_API_KEY` 替換成您自己的 Google AI Studio API 金鑰。

## 如何執行

一切設定完成後，直接執行主程式：

```bash
python robotAgent.py
```

程式啟動後，您會看到提示訊息，即可開始輸入指令。

```
你好！我是您的測試案例生成助理。請告訴我您想做什麼？(輸入 exit 退出)
指令 >
```

## 使用範例

  * **範例 1: 搜尋資訊**

    ```
    指令 > 開啟 https://www.google.com/
    指令 > 在搜尋框輸入'LangChain'
    指令 > 按下Google 搜尋按鈕
    ```

  * **範例 2: 執行系統命令**

    ```
    指令 > 執行 ls -l
    ```

## 專案結構

```
.
├── .gitignore               # Git 忽略設定檔
├── README.md                # 專案說明文件
├── models
│   ├── bot_tools.py         # Selenium 網頁操作工具
│   ├── cmd_tools.py         # 終端機命令工具
│   └── utils
│       └── wbd.py           # WebDriver 管理器
├── robotAgent.py            # 程式主入口
├── system
│   └── prompt
│       └── robot_prompt.py  # AI 代理人的系統提示
└── .env                     # (需自行建立) 環境變數設定檔
```
