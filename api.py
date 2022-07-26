# -*- coding: utf-8 -*-
# @Time : 7/26/2022 2:30 PM
# @Email : yun981128@gmail.com
# @Author : W
# @Project :jshtcm
# @File : api.py
# @notice :

from hashlib import md5
import requests
import json
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import time
import base64
from typing import Union
from ddddocr import DdddOcr
from configparser import ConfigParser
from schema import AddRegArgs, DeptSchForDocArgs, DocSchArgs, NumberSourceArgs

ocr = DdddOcr()

config = ConfigParser()
config.read("conf.ini", encoding="utf-8")


# 异常处理装饰器
def exception_handler(func):
    def wrapper(*args, **kwargs):
        for _ in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"函数{func.__name__}出现异常,异常关键词为：", e, "程序将在5S后重试")
                time.sleep(5)
        raise Exception("程序异常，重试运行后仍无法成功")

    return wrapper


class Api:
    def __init__(self):
        """
        初始化
        """
        print("初始化")
        # 读取配置
        self.sys_code = config.get("江苏省中医院", "sysCode")
        self.desKey = config.get("江苏省中医院", "desKey")
        self.phsId = config.get("江苏省中医院", "phsId")
        self.host = config.get("江苏省中医院", "host")
        self.token = config.get("江苏省中医院", "token", fallback=None)
        username = config.get("江苏省中医院", "username", fallback=None)
        password = config.get("江苏省中医院", "password", fallback=None)
        assert (self.token is not None) or (
            username is not None and password is not None
        ), "初始化，用户名/账号密码必传入其一"

        if not self.token:
            access_token = self.login(username, password)
            self.token = self.get_he_ren_token(access_token)
            config.set("江苏省中医院", "token", self.token)
            with open("conf.ini", "w", encoding="utf-8") as f:
                config.write(f)
        print("获取token成功")

    def encrypt(
        self,
        key: str = None,
        plaintext: str = None,
    ) -> str:
        """
        Encrypts a plaintext string using DES
        :param key:
        :param plaintext:
        :return:
        """
        if key is None:
            key = self.desKey
        if plaintext is None:
            plaintext = "1001035_" + str(int(time.time() * 1000))
        key = key.encode()
        plaintext = plaintext.encode()
        plaintext = pad(plaintext, DES.block_size)
        cipher = DES.new(key, DES.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext)
        return base64.encodebytes(ciphertext).decode("utf-8").strip()

    @exception_handler
    def get_hospital(self) -> dict:
        """
          获取医区信息
        :return:院区信息
        """
        url = f"{self.host}/phs-base/getHospital"
        payload = json.dumps({"args": {"sysCode": self.sys_code}, "token": self.token})
        headers = {
            "phsSign": self.encrypt(),
            "phsId": self.phsId,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if (
            str(response.json().get("code")) != "200"
            and str(response.json().get("code")) != "0"
        ):
            print(response.json().get("message") or response.json().get("msg"))
        return response.json()["result"]

    @exception_handler
    def get_deptlist(self, hos_id: Union[str, int]) -> dict:
        """
        获取科室列表
        :param hos_id:医院id
        :return: 科室列表
        """
        url = f"{self.host}/phs-reg/reg/getDeptList"
        payload = json.dumps(
            {
                "args": {
                    "clinicalType": "1",
                    "hosId": hos_id,
                    "sysCode": self.sys_code,
                },
                "token": self.token,
            }
        )
        headers = {
            "phsSign": self.encrypt(),
            "phsId": self.phsId,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if (
            str(response.json().get("code")) != "200"
            and str(response.json().get("code")) != "0"
        ):
            print(response.json().get("message") or response.json().get("msg"))
        return response.json()["result"]["dataList"]

    @exception_handler
    def get_dept_sch_for_doc(self, args: DeptSchForDocArgs) -> dict:
        """
        获取医生信息
        :param args: 请求参数
        :return:
        """
        args.update()
        payload = {
            "args": {
                **args.dict(),
            },
            "token": self.token,
        }
        payload = json.dumps(payload)
        url = f"{self.host}/phs-reg/reg/getDeptSchForDoc"
        headers = {
            "phsSign": self.encrypt(),
            "phsId": self.phsId,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if (
            str(response.json().get("code")) != "200"
            and str(response.json().get("code")) != "0"
        ):
            print(response.json().get("message") or response.json().get("msg"))
        return response.json()["result"]["schDocResultList"]

    @exception_handler
    def get_doc_sch(self, arg: DocSchArgs):
        """
        获取医生排班信息
        :param arg: 请求参数
        :return:
        """
        url = f"{self.host}/phs-reg/reg/getDocSch"

        payload = {"args": {**arg.dict()}, "token": self.token}
        payload = json.dumps(payload)
        headers = {
            "phsSign": self.encrypt(),
            "phsId": self.phsId,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if (
            str(response.json().get("code")) != "200"
            and str(response.json().get("code")) != "0"
        ):
            print(response.json().get("message") or response.json().get("msg"))
        return response.json()["result"]["dataList"]

    @exception_handler
    def get_pat_card_list(self) -> list:
        """
        获取就诊卡，即挂号人信息
        :param args:请求参数
        :return:
        """
        payload = {
            "args": {
                "sysCode": self.sys_code,
            },
            "token": self.token,
        }
        payload = json.dumps(payload)
        headers = {
            "phsSign": self.encrypt(),
            "phsId": self.phsId,
            "Content-Type": "application/json",
        }
        url = f"{self.host}/phs-base/relevantPatient/getPatCardList"
        response = requests.request("POST", url, headers=headers, data=payload)
        if (
            str(response.json().get("code")) != "200"
            and str(response.json().get("code")) != "0"
        ):
            print(response.json().get("message") or response.json().get("msg"))
        return response.json()["result"]

    @exception_handler
    def add_reg(self, args: AddRegArgs) -> dict:
        """
        提交订单
        :param args: 请求参数
        :return:
        """
        args.update()
        payload = json.dumps(
            {
                "args": {
                    **args.dict(),
                },
                "token": self.token,
            }
        )
        headers = {
            "phsSign": self.encrypt(),
            "phsId": self.phsId,
            "Content-Type": "application/json",
        }
        url = f"{self.host}/phs-reg/reg/addReg"
        response = requests.request("POST", url, headers=headers, data=payload)
        if (
            str(response.json().get("code")) != "200"
            and str(response.json().get("code")) != "0"
        ):
            print(response.json().get("message") or response.json().get("msg"))
        print(response.text)
        return response.json()

    @exception_handler
    def get_verification_code(self) -> [str, str]:
        """
        获取验证码
        :return: srt:verifyCode,uniqueId
        """
        url = "http://wechat.jshtcm.com/cas-wechat/*.jsonRequest"
        payload = [{}]
        payload = json.dumps(payload)
        headers = {
            "Content-Type": "application/json",
            "X-Service-Id": "cas-wechat.smsService",
            "X-Service-Method": "getVerifyCodeInfo",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception("获取验证码失败")
        body = json.loads(response.json()["body"])
        verifyCode = body["verifyCode"]
        uniqueId = body["uniqueId"]
        verifyCode = base64.b64decode(verifyCode)
        verifyCode = ocr.classification(verifyCode)
        return verifyCode, uniqueId

    @exception_handler
    def login(self, username: Union[str, int], password: str) -> str:
        """
        登录
        :param username: 用户名/手机号
        :param password: 密码
        :return:accessToken
        """
        if type(username) == int:
            username = str(username)
        url = "http://wechat.jshtcm.com/cas-wechat/logon/login"
        verifyCode, uniqueId = self.get_verification_code()

        payload = json.dumps(
            {
                "tenantId": "hcn.jsszyy",
                "pwd": md5(password.encode()).hexdigest(),
                "forAccessToken": True,
                "rid": "patient",
                "verifyCode": verifyCode,
                "uniqueId": uniqueId,
                "loginName": username,
            }
        )
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json().get("code") != 200:
            raise Exception(
                response.json().get("msg") or "登录失败"
            )
        return response.json()["properties"]["accessToken"]

    @exception_handler
    def get_he_ren_token(self, x_access_token: str) -> str:
        """
        获取患者端token
        :param x_access_token:登陆后的token
        :return:token
        """
        url = "http://wechat.jshtcm.com/cas-wechat/*.jsonRequest"
        payload = json.dumps([{"openId": ""}])
        headers = {
            "X-Service-Method": "getHeRenToken",
            "X-Access-Token": x_access_token,
            "X-Service-Id": "cas-wechat.heRenService",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if (
            str(response.json().get("code")) != "200"
            and str(response.json().get("code")) != "0"
        ):
            print(response.json().get("message") or response.json().get("msg"))
        return response.json()["body"]

    @exception_handler
    def get_number_source(self, args: NumberSourceArgs) -> dict:
        """
        获取预约时间
        :param args:
        :return:
        """
        payload = {
            "args": {
                **args.dict(),
            },
            "token": self.token,
        }
        payload = json.dumps(payload)
        headers = {
            "phsSign": self.encrypt(),
            "phsId": self.phsId,
            "Content-Type": "application/json",
        }
        url = f"{self.host}/phs-reg/reg/getNumberSource"
        response = requests.request("POST", url, headers=headers, data=payload)
        if (
            str(response.json().get("code")) != "200"
            and str(response.json().get("code")) != "0"
        ):
            print(response.json().get("message") or response.json().get("msg"))
        return response.json()["result"]


if __name__ == "__main__":
    api = Api()
    print(api.get_hospital())
