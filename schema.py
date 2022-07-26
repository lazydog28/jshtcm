# -*- coding: utf-8 -*-
# @Time : 7/26/2022 2:30 PM
# @Email : yun981128@gmail.com
# @Author : W
# @Project :jshtcm
# @File : schema.py
# @notice :
from pydantic import BaseModel
from typing import Union


class HospitalArgs(BaseModel):
    sysCode: Union[str, int] = "1001035"


class DeptListArgs(BaseModel):
    clinicalType: str = 1
    hosId: int
    sysCode: Union[str, int] = "1001035"


class DeptSchForDocArgs(BaseModel):
    clinicalType: str = 1
    deptCode: str = None
    deptId: str = deptCode
    specialtyId: str = None
    deptName: str
    visitingArea: str
    hosId: int
    recommendation: str = ""
    type: str = "order"
    source: int = 22
    sysCode: Union[str, int] = "1001035"

    def update(self):
        self.deptId = self.deptCode


class DocSchArgs(BaseModel):
    deptId: str
    deptName: str
    docId: str
    docName: str
    docTitle: str
    docPhoto: str
    hosId: int
    hosName: str
    type: str = "order"
    visitingArea: str = ""
    clinicalType: str = 1
    source: int = 22
    sysCode: Union[str, int] = "1001035"


class NumberSourceArgs(BaseModel):
    sysCode: Union[str, int] = "1001035"
    ampm: str
    categor: str
    docId: str
    deptId: str
    hosId: Union[str, int]
    schDate: str
    schId: str


class AddRegArgs(BaseModel):
    # key不一致参数
    disNo: str = None
    schDate: str = None
    patienId: str = None

    # 必须参数
    clinicalType: str = 1
    visitingArea: str = ""
    ampm: str
    appointmentNumber: str = disNo
    categor: str
    categorName: str
    deptId: str
    deptName: str
    docId: str
    docName: str
    endTime: str = ""
    extend: str = ""
    fee: str
    hosId: Union[str, int]
    hosName: str
    isFlexible: str = ""
    numId: str = ""
    patientId: str = patienId
    resDate: str = schDate
    schId: str
    source: int = 22
    startTime: str = ""
    sysCode: Union[str, int] = "1001035"
    thirdUserId: str = ""
    timeDesc: str
    timePoint: str = ""
    schQukCategor: str

    def update(self):
        self.appointmentNumber = self.disNo
        self.resDate = self.schDate
        self.patientId = self.patienId
