"""
这个模块提供安全方面的功能
"""

import base64
import hashlib
import hmac


def cal_sign(timestamp: str, app_sec: str) -> bytes:
    """cal_sign 计算加密后的 'timestamp\napp_sec'"""
    secret_enc = app_sec.encode('utf-8')
    msg = f"{timestamp}\n{app_sec}".encode('utf-8')
    hmac_code = hmac.new(
        secret_enc, msg, digestmod=hashlib.sha256).digest()

    return base64.b64encode(hmac_code)
