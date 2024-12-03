import re
import pyperclip
from win10toast import ToastNotifier
from SmsCodeUtils import SmsCodeUtils

def show_toast_notification(title, message, duration=3):
    # 创建通知对象
    toaster = ToastNotifier()
    # 显示通知，duration表示通知持续的时间（秒）
    toaster.show_toast(title, message, duration=duration, threaded=True)


def copy_verification_code(text):
    keywords_regex = r"验证码"
    number = SmsCodeUtils.parse_sms_code_if_exists(keywords_regex,text)
    if number is not None:
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
    text = "【微信支付】754207(微信验证码，请勿泄露)，您于2024-09-02 11:57:21发起交易7700.00元"
    copy_verification_code(text)