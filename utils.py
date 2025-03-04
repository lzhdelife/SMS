import re
import pyperclip
from win10toast import ToastNotifier

def extract_first_long_number(text):
    # 匹配长度大于等于4,且小于等于6的数字字符串，而且前后都不能是数字
    pattern = r'(?<!\d)\d{4,6}(?!\d)'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    return None


def show_toast_notification(title, message, duration=3):
    # 创建通知对象
    toaster = ToastNotifier()
    # 显示通知，duration表示通知持续的时间（秒）
    toaster.show_toast(title, message, duration=duration, threaded=True)


def copy_verification_code(text):
    number = extract_first_long_number(text)
    if number:
        # 复制到剪贴板
        pyperclip.copy(number)
        print(f"已复制到剪贴板: {number}")
        # 显示通知，收到的文本左右有{}，text[1: -2]可以取到{}中的文本
        show_toast_notification("复制成功", text[1: -2])
        return number
    else:
        print("未找到符合条件的数字字符串")
        # 显示通知
        show_toast_notification("复制失败", f"请检查短信验证码")
        return None
    


if __name__ == "__main__":
    text = "这是一段包含数字1234、56789和100的文本。"
    copy_verification_code(text)