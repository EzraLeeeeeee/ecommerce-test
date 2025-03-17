import os
import shutil
import stat
import pytest

def remove_readonly(func, path, _):
    """ 解除唯讀權限，以便刪除檔案 """
    os.chmod(path, stat.S_IWRITE)
    func(path)

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """ 在 Pytest 測試開始前清空 allure-results 資料夾 """
    results_dir = "./allure-results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir, onerror=remove_readonly)  # 解除鎖定並刪除
    os.makedirs(results_dir)
