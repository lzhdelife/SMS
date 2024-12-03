import re

class SmsCodeUtils:
    LEVEL_DIGITAL_6 = 4
    LEVEL_DIGITAL_4 = 3
    LEVEL_DIGITAL_OTHERS = 2
    LEVEL_TEXT = 1
    LEVEL_CHARACTER = 0
    LEVEL_NONE = -1

    @staticmethod
    def contains_chinese(text: str) -> bool:
        """是否包含中文"""
        return bool(re.search(r"[\u4e00-\u9fa5]|。", text))

    @staticmethod
    def contains_code_keywords(keywords_regex: str, content: str) -> bool:
        """是否包含验证码关键字"""
        return bool(SmsCodeUtils.parse_keyword(keywords_regex, content))

    @staticmethod
    def parse_keyword(keywords_regex: str, content: str) -> str:
        """解析文本内容中的验证码关键字"""
        match = re.search(keywords_regex, content)
        return match.group() if match else ""

    @staticmethod
    def parse_sms_code_if_exists(keywords_regex: str, content: str) -> str:
        """解析文本中的验证码并返回"""
        return SmsCodeUtils.parse_by_default_rule(keywords_regex, content)

    @staticmethod
    def parse_by_default_rule(keywords_regex: str, content: str) -> str:
        """按默认规则解析验证码，如果不存在返回空字符"""
        keyword = SmsCodeUtils.parse_keyword(keywords_regex, content)
        if not keyword:
            return ""
        if SmsCodeUtils.contains_chinese(content):
            return SmsCodeUtils.get_sms_code_cn(keyword, content)
        else:
            return SmsCodeUtils.get_sms_code_en(keyword, content)

    @staticmethod
    def remove_all_white_spaces(content: str) -> str:
        """去掉所有空白字符"""
        return re.sub(r"\s*", "", content)

    @staticmethod
    def get_sms_code_cn(keyword: str, content: str) -> str:
        """获取中文短信中包含的验证码"""
        code_regex = r"(?<![a-zA-Z0-9])[a-zA-Z0-9]{4,8}(?![a-zA-Z0-9])"
        handled_content = SmsCodeUtils.remove_all_white_spaces(content)
        sms_code = SmsCodeUtils.get_sms_code(code_regex, keyword, handled_content)
        if not sms_code:
            sms_code = SmsCodeUtils.get_sms_code(code_regex, keyword, content)
        return sms_code

    @staticmethod
    def get_sms_code_en(keyword: str, content: str) -> str:
        """获取英文短信中包含的验证码"""
        code_regex = r"(?<![0-9])[0-9]{4,8}(?![0-9])"
        sms_code = SmsCodeUtils.get_sms_code(code_regex, keyword, content)
        if not sms_code:
            content = SmsCodeUtils.remove_all_white_spaces(content)
            sms_code = SmsCodeUtils.get_sms_code(code_regex, keyword, content)
        return sms_code

    @staticmethod
    def get_sms_code(code_regex: str, keyword: str, content: str) -> str:
        """解析验证码"""
        possible_codes = re.findall(code_regex, content)
        if not possible_codes:
            return ""

        filtered_codes = [
            code for code in possible_codes if SmsCodeUtils.is_near_to_keyword(keyword, code, content)
        ]

        if not filtered_codes:
            filtered_codes = possible_codes

        max_match_level = SmsCodeUtils.LEVEL_NONE
        min_distance = len(content)
        sms_code = ""

        for filtered_code in filtered_codes:
            cur_level = SmsCodeUtils.get_match_level(filtered_code)
            if cur_level > max_match_level:
                max_match_level = cur_level
                min_distance = SmsCodeUtils.distance_to_keyword(keyword, filtered_code, content)
                sms_code = filtered_code
            elif cur_level == max_match_level:
                cur_distance = SmsCodeUtils.distance_to_keyword(keyword, filtered_code, content)
                if cur_distance < min_distance:
                    min_distance = cur_distance
                    sms_code = filtered_code

        return sms_code

    @staticmethod
    def get_match_level(matched_str: str) -> int:
        """获取验证码匹配度"""
        if re.fullmatch(r"[0-9]{6}", matched_str):
            return SmsCodeUtils.LEVEL_DIGITAL_6
        if re.fullmatch(r"[0-9]{4}", matched_str):
            return SmsCodeUtils.LEVEL_DIGITAL_4
        if re.fullmatch(r"[0-9]+", matched_str):
            return SmsCodeUtils.LEVEL_DIGITAL_OTHERS
        if re.fullmatch(r"[a-zA-Z]+", matched_str):
            return SmsCodeUtils.LEVEL_CHARACTER
        return SmsCodeUtils.LEVEL_TEXT

    @staticmethod
    def is_near_to_keyword(keyword: str, possible_code: str, content: str, magic_number: int = 30) -> bool:
        """判断可能的验证码是否靠近关键字"""
        cur_index = content.find(possible_code)
        if cur_index == -1:
            return False

        begin_index = max(0, cur_index - magic_number)
        end_index = min(len(content), cur_index + len(possible_code) + magic_number)
        return keyword in content[begin_index:end_index]

    @staticmethod
    def distance_to_keyword(keyword: str, possible_code: str, content: str) -> int:
        """计算关键字与可能验证码的距离"""
        keyword_idx = content.find(keyword)
        possible_code_idx = content.find(possible_code)
        return abs(keyword_idx - possible_code_idx) if keyword_idx != -1 and possible_code_idx != -1 else float('inf')


if __name__ == "__main__":
    content = "【微信支付】754207(微信验证码，请勿泄露)，您于2024-09-02 11:57:21发起交易7700.00元"
    keywords_regex = r"验证码"

    result = SmsCodeUtils.parse_sms_code_if_exists(keywords_regex, content)
    print(f"解析出的验证码: {result}")
