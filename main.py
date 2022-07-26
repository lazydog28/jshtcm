# -*- coding: utf-8 -*-
# @Time : 7/26/2022 6:12 PM
# @Email : yun981128@gmail.com
# @Author : W
# @Project :jshtcm
# @File : main.py
# @notice :
import time
from schema import AddRegArgs, DeptSchForDocArgs, DocSchArgs, NumberSourceArgs
from api import Api


def appointment():
    """
    预约程序入口 用来测试是否能够正常预约
    :return:
    """
    api = Api()
    hospitals = api.get_hospital()
    print("请选择院区，输入院区前方序号")
    for index, hospital in enumerate(hospitals):
        print("{}):{}".format(index, hospital["aliasName"]))
    hospital_index = int(input("请输入院区序号："))
    hospital = hospitals[hospital_index]
    deptlist = api.get_deptlist(hospital["hosId"])
    print("请选择科室类别，输入科室类别前方序号")
    for index, deptclass in enumerate(deptlist):
        print("{}):{}".format(index, deptclass["deptName"]))
    deptclass_index = int(input("请输入科室类别序号："))
    deptclass = deptlist[deptclass_index]
    print("请选择科室，输入科室前方序号")
    for index, dept in enumerate(deptclass["deptList"]):
        print("{}):{}".format(index, dept["deptName"]))
    dept_index = int(input("请输入科室序号："))
    dept = deptclass["deptList"][dept_index]
    all_args = {**dept, **hospital}
    args = DeptSchForDocArgs(**all_args)
    doc_list = api.get_dept_sch_for_doc(args)
    print("请选择医生，输入医生前方序号")
    for index, doc in enumerate(doc_list):
        print("{}):{}".format(index, doc["docName"]))
    doc_index = int(input("请输入医生序号："))
    doc = doc_list[doc_index]
    all_args = {**doc, **dept, **hospital}
    args = DocSchArgs(**all_args)
    doc_schDate = api.get_doc_sch(args)
    # 筛选出可预约的时间
    doc_schDate = [
        x
        for x in doc_schDate
        if sum(
            [int(y["numRemain"]) > 0 and y["schState"] == "0" for y in x["schDateList"]]
        )
        > 0
    ]
    if len(doc_schDate) == 0:
        print("没有可预约的时间")
        return
    print("请选择日期，输入日期前方序号")
    for index, schDate in enumerate(doc_schDate):
        print("{}):{}".format(index, schDate["schDate"]))
    schDate_index = int(input("请输入日期序号："))
    schDate = doc_schDate[schDate_index]
    print("请选择时段,输入时段前方序号")
    for index, sch in enumerate(schDate["schDateList"]):
        print("{}):{}".format(index, sch["ampmName"]))
    sch_index = int(input("请输入时段序号:"))
    sch = schDate["schDateList"][sch_index]
    all_args = {**sch, **doc, **dept, **hospital}
    args = NumberSourceArgs(**all_args)
    appointment_time_list = api.get_number_source(args)
    print("请选择预约时间，输入预约时间前方序号")
    for index, timeDesc in enumerate(appointment_time_list):
        print("{}):{}".format(index, timeDesc["timeDesc"]))
    time_index = int(input("请输入预约时间序号："))
    appointment_time = appointment_time_list[time_index]
    pat_card_list = api.get_pat_card_list()
    print("请选择就诊卡，输入就诊卡前方序号")
    for index, pat_card in enumerate(pat_card_list):
        print("{}):{}".format(index, pat_card["name"]))
    pat_card_index = int(input("请输入就诊卡序号："))
    pat_card = pat_card_list[pat_card_index]
    all_args = {**sch, **doc, **dept, **hospital, **appointment_time, **pat_card}
    args = AddRegArgs(**all_args)
    response = api.add_reg(args)
    print(response)


def monitor():
    """
    监控程序入口 用来实际的抢挂号，每10S检测一次指定日期的指定医生的挂号情况
    :return:
    """
    api = Api()
    hospitals = api.get_hospital()
    print("请选择院区，输入院区前方序号")
    for index, hospital in enumerate(hospitals):
        print("{}):{}".format(index, hospital["aliasName"]))
    hospital_index = int(input("请输入院区序号："))
    hospital = hospitals[hospital_index]
    deptlist = api.get_deptlist(hospital["hosId"])
    print("请选择科室类别，输入科室类别前方序号")
    for index, deptclass in enumerate(deptlist):
        print("{}):{}".format(index, deptclass["deptName"]))
    deptclass_index = int(input("请输入科室类别序号："))
    deptclass = deptlist[deptclass_index]
    print("请选择科室，输入科室前方序号")
    for index, dept in enumerate(deptclass["deptList"]):
        print("{}):{}".format(index, dept["deptName"]))
    dept_index = int(input("请输入科室序号："))
    dept = deptclass["deptList"][dept_index]
    all_args = {**dept, **hospital}
    args = DeptSchForDocArgs(**all_args)
    doc_list = api.get_dept_sch_for_doc(args)
    print("请选择医生，输入医生前方序号")
    for index, doc in enumerate(doc_list):
        print("{}):{}".format(index, doc["docName"]))
    doc_index = int(input("请输入医生序号："))
    doc = doc_list[doc_index]
    all_args = {**doc, **dept, **hospital}
    args = DocSchArgs(**all_args)
    doc_schDate = api.get_doc_sch(args)
    print("请选择日期，输入日期前方序号")
    for index, schDate in enumerate(doc_schDate):
        print("{}):{}".format(index, schDate["schDate"]))
    schDate_index = int(input("请输入日期序号："))
    schDate = doc_schDate[schDate_index]
    while True:
        try:
            doc_schDate = api.get_doc_sch(args)
            # 筛选出可预约的时间
            doc_schDate = [
                x
                for x in doc_schDate
                if sum(
                    [
                        int(y["numRemain"]) > 0
                        and y["schState"] == "0"
                        and y["schDate"] == schDate
                        for y in x["schDateList"]
                    ]
                )
                > 0
            ]
            if len(doc_schDate) == 0:
                print("没有可预约的时间,等待10S后再次检测")
                time.sleep(10)
                continue

            for sch_index, sch in enumerate(schDate["schDateList"]):
                all_args = {**sch, **doc, **dept, **hospital}
                args = NumberSourceArgs(**all_args)
                appointment_time_list = api.get_number_source(args)
                for appointment_time_index, appointment_time in enumerate(
                    appointment_time_list
                ):
                    print("目标医师当前存在可预约时间，程序将尝试自动预约。如未收到预约成功消息，请前往预约界面手动预约。")
                    pat_card_list = api.get_pat_card_list()
                    pat_card = pat_card_list[0]
                    all_args = {
                        **sch,
                        **doc,
                        **dept,
                        **hospital,
                        **appointment_time,
                        **pat_card,
                    }
                    args = AddRegArgs(**all_args)
                    response = api.add_reg(args)
                    if response["code"] == "0":
                        print("预约成功！请在10分钟内前往订单页面付款并停止程序运行！若未及时停止程序运行，程序将在10分钟后自动重新预约！")
                        time.sleep(600)
                    else:
                        print("预约失败！请前往预约界面手动预约！")
                        time.sleep(600)
            print("等待10S后重新预约")
            time.sleep(10)
        except KeyboardInterrupt:
            print("程序已停止")
            break
        except Exception as e:
            print("程序异常，程序将在10S后重新预约")
            time.sleep(10)
            continue


if __name__ == "__main__":
    monitor()
