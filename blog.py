from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


def create_webdriver(is_remote: bool = False, service_args: dict = None) -> webdriver:
    """
    创建webdriver实例，本地或远程（例如Docker容器）。

    :param is_remote: 是否使用远程Selenium服务器。
    :param service_args: 传递给webdriver的参数，例如Selenium服务的URL。
    :return: 初始化的webdriver实例。
    """
    if is_remote:
        # 这里需要指定远程Selenium服务器的URL
        command_executor = service_args.get(
            "command_executor", "http://localhost:4444/wd/hub"
        )
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Remote(
            command_executor=command_executor,
            options=chrome_options,
        )
    else:
        # 本地运行的webdriver配置
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 可以根据需要添加或删除配置
        # 确保chromedriver路径正确，或者使用webdriver-manager包来管理驱动程序
        return webdriver.Chrome(options=chrome_options)


def open_urls_and_refresh_tabs(driver: webdriver, refresh_count: int = 1):
    # 自动生成URL列表
    base_url = "https://blog.huacai.one/post/"
    urls = [f"{base_url}{i}" for i in range(40, 46)]

    try:
        # 打开所有URL，并保存每个标签页的句柄
        tab_handles = []
        for url in urls:
            driver.execute_script("window.open('');")  # 打开新标签页
            driver.switch_to.window(driver.window_handles[-1])  # 切换到新标签页
            driver.get(url)  # 打开URL
            print(f"已打开网站，标题为：{driver.title}")
            tab_handles.append(driver.current_window_handle)  # 保存标签页句柄
            driver.execute_script("window.scrollBy(0, 100)")  # 向下滚动100px

        # 根据传入参数决定循环刷新的次数
        for _ in range(refresh_count):
            for handle in tab_handles:
                driver.switch_to.window(handle)  # 切换到对应的标签页
                driver.refresh()  # 刷新当前标签页
                print(f"已刷新网站，标题为：{driver.title}")

    finally:
        # 关闭所有标签页和浏览器
        driver.quit()


if __name__ == "__main__":
    # 示例用法：
    # 本地调试时使用
    # local_driver = create_webdriver()
    # open_urls_and_refresh_tabs(local_driver)
    #
    # 容器中使用时，传递远程服务器的参数
    remote_service_args = {"command_executor": "http://chrome:4444/wd/hub"}
    remote_driver = create_webdriver(is_remote=True, service_args=remote_service_args)
    open_urls_and_refresh_tabs(remote_driver)
