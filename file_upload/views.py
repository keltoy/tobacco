from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from file_upload.models import RelevantDocument, Presentation
from file_upload.serializers import RelevantDocumentSerializer, PresentationSerializer
from regulatory_system.models import AbnormalFlow, AbnormalFlowDetail, CustomerLatest, Customer
import datetime
import xlrd

# Create your views here.

FLOW_DICT = {"本区": 1, "外区": 2, "外省": 3}

CUSTOMER_SHOP_CLASS_DICT = {
 "一档": 1,
 "二档": 2,
 "三档": 3,
 "四档": 4,
 "五档": 5,
 "六档": 6,
 "七档": 7,
 "八档": 8,
 "九档": 9,
 "十档": 10,
 "十一档": 11,
 "十二档": 12,
 "十三档": 13,
 "十四档": 14,
 "十五档": 15,
 "十六档": 16,
 "十七档": 17,
 "十八档": 18,
 "十九档": 19,
 "二十档": 20,
}


class RelevantDocumentViewSet(viewsets.ModelViewSet):
    queryset = RelevantDocument.objects.all()
    serializer_class = RelevantDocumentSerializer
    permission_classes = (IsAdminUser, )


class PresentationViewSet(viewsets.ModelViewSet):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    permission_classes = (IsAdminUser, )


class UploadFlowView(APIView):
    parser_classes = (MultiPartParser,)
    #permission_classes = (IsAdminUser, )

    def post(self, request):
        res = {"code": 0, "msg": "ok"}
        files = request.FILES.getlist('file', None)
        for file in files:
            f = self.import_flow_file(file)
            if f['code'] != 0:
                return Response(f)
        return Response(res)

    def import_flow_file(self, file):
        res = {"code": 0, "msg": "ok"}
        try:
            workbook = xlrd.open_workbook(filename=None, file_contents=file.read(), encoding_override='utf-8')
            default_sheet = workbook.sheets()[0]
            flow_list = []
            for i in range(1, default_sheet.nrows):
                row = default_sheet.row_values(i)
                types = default_sheet.row_types(i)
                date_time = datetime.datetime.strptime(row[1], '%Y-%m')
                flow_date = date_time.strftime('%Y-%m-%d')
                flow_direction = 0
                if row[2] in FLOW_DICT:
                    flow_direction = FLOW_DICT[row[2]]
                license_id = row[3]
                shop = row[4]
                if types[3] == 2:
                    license_id = str(int(row[3]))
                elif types[3] == 1 and "*" in license_id:
                    shop = "未追溯到户"
                quantity = row[5]
                flow_list.append(AbnormalFlow(
                    license_id=license_id,
                    flow_direction=flow_direction,
                    flow_date=flow_date,
                    shop=shop,
                    flow_quantity=quantity
                ))

                AbnormalFlow.objects.bulk_create(flow_list, ignore_conflicts=True)
        except BaseException as e:
            res['code'] = 1
            res['msg'] = "e"

        return res


class UploadFlowDetailView(APIView):
    parser_classes = (MultiPartParser,)
    #permission_classes = (IsAdminUser, )

    def post(self, request):
        res = {"code": 0, "msg": "ok"}
        files = request.FILES.getlist('file', None)
        flow_date = datetime.datetime.now().replace(day=1).strftime("%Y-%m-%d")
        if 'flow_date' in request.POST:
            flow_date = request.POST['flow_date']
        for file in files:
            f = self.import_flow_detail_file(file, flow_date)
            if f['code'] != 0:
                return Response(f)
        return Response(res)

    def import_flow_detail_file(self, file, flow_date):
        res = {"code": 0, "msg": "ok"}
        try:
            workbook = xlrd.open_workbook(filename=None, file_contents=file.read(), encoding_override='utf-8')
            default_sheet = workbook.sheets()[0]
            flow_detail_list = []
            for i in range(1, default_sheet.nrows):
                row = default_sheet.row_values(i)
                types = default_sheet.row_types(i)
                license_id = row[1]
                if types[1] == 2:
                    license_id = str(int(row[1]))
                brand = row[2]
                quantity = row[3]
                spray_code = row[4]
                if types[4] == 2:
                    spray_code = str(int(row[4]))

                flow_date = flow_date


                flow_detail_list.append(AbnormalFlowDetail(
                    license_id=license_id,
                    brand_name=brand,
                    flow_quantity=quantity,
                    spray_code= spray_code,
                    code_type="有效",
                    flow_date=flow_date,
                ))

            AbnormalFlowDetail.objects.bulk_create(flow_detail_list, ignore_conflicts=True)
        except BaseException as e:
            res['code'] = 1
            res['msg'] = e

        return res


class UploadCustomerView(APIView):
    parser_classes = (MultiPartParser,)
    #permission_classes = (IsAdminUser, )

    def post(self, request):
        res = {"code": 0, "msg": "ok"}
        files = request.FILES.getlist('file', None)
        is_key = 0
        active_date = datetime.datetime.now().strftime('%Y-%m-%d')
        import_date = active_date
        only_history = False
        if 'is_key' in request.POST:
            is_key = request.POST['is_key']
        if 'active_date' in request.POST:
            active_date = request.POST['active_date']
        if 'import_date' in request.POST:
            import_date = request.POST['import_date']
        if 'only_history' in request.POST:
            only_history = request.POST['only_history']

        for file in files:
            f = self.import_customer_file(file, int(is_key), active_date, import_date, only_history)
            if f['code'] != 0:
                return Response(f)
        return Response(res)

    def import_customer_file(self, file, is_key, active_date, import_date, only_history):
        if is_key:
            return self.import_key_customer_file(file, active_date, import_date, only_history)
        else:
            return self.import_common_customer_file(file, active_date, import_date, only_history)

    def import_common_customer_file(self, file, active_date, import_date, only_history):
        res = {"code": 0, "msg": "ok"}
        try:
            workbook = xlrd.open_workbook(filename=None, file_contents=file.read(), encoding_override='utf-8')
            default_sheet = workbook.sheets()[0]
            customer_list = []
            for i in range(1, default_sheet.nrows):
                row = default_sheet.row_values(i)
                types = default_sheet.row_types(i)
                license_id = row[1]
                shop = row[2]
                if types[1] == 2:
                    license_id = str(int(row[1]))
                elif types[1] == 1 and "*" in license_id:
                    shop = "未追溯到户"
                name = row[3]
                phone_number = row[4]
                if types[4] == 2:
                    phone_number = str(int(row[4]))
                address = row[5]
                order_phone = row[6]
                if types[6] == 2:
                    order_phone = str(int(row[6]))
                status = row[7]
                commercial_type = row[8]
                shop_class = CUSTOMER_SHOP_CLASS_DICT[row[9]]

                if only_history:
                    customer_list.append(Customer(
                        license_id=license_id,
                        name=name,
                        phone_number=phone_number,
                        address=address,
                        order_phone=order_phone,
                        status=status,
                        shop=shop,
                        commercial_type=commercial_type,
                        shop_class=shop_class,
                        key_customer=False,
                        active_date=active_date,
                        import_date=import_date))
                else:
                    customer_list.append(CustomerLatest(
                        license_id=license_id,
                        name=name,
                        phone_number=phone_number,
                        address=address,
                        order_phone=order_phone,
                        status=status,
                        shop=shop,
                        commercial_type=commercial_type,
                        shop_class=shop_class,
                        key_customer=False,
                        active_date=active_date,
                        import_date=import_date))

            if only_history:
                Customer.objects.bulk_create(customer_list, ignore_conflicts=True)
            else:
                query_set = CustomerLatest.objects.filter(key_customer=False).delete()
                if not query_set:
                    query_set.delete()
                CustomerLatest.objects.bulk_create(customer_list, ignore_conflicts=True)
                Customer.objects.bulk_create(customer_list, ignore_conflicts=True)
        except BaseException as e:
            res['code'] = 1
            res['msg'] = e

        return res

    def import_key_customer_file(self, file, active_date, import_date, only_history):
        res = {"code": 0, "msg": "ok"}
        try:
            workbook = xlrd.open_workbook(filename=None, file_contents=file.read(), encoding_override='utf-8')
            default_sheet = workbook.sheets()[0]
            customer_list = []
            for i in range(2, default_sheet.nrows - 1):
                row = default_sheet.row_values(i)
                types = default_sheet.row_types(i)
                date_time = datetime.datetime.strptime(row[1], '%Y-%m')
                valid_date = date_time.strftime('%Y-%m-%d')
                license_id = row[2]
                shop = row[3]
                if types[2] == 2:
                    license_id = str(int(row[2]))
                elif types[2] == 1 and "*" in license_id:
                    shop = "未追溯到户"
                shop_class = CUSTOMER_SHOP_CLASS_DICT[row[4]]
                market_type = row[5]
                commercial_type = row[6]
                order_number = int(row[7])
                order_quantity = row[8]
                money_amount = row[9]

                if only_history:
                    customer_list.append(Customer(
                        license_id=license_id,
                        shop=shop,
                        commercial_type=commercial_type,
                        shop_class=shop_class,
                        key_customer=False,
                        valid_date=valid_date,
                        import_date=import_date,
                        market_type=market_type,
                        order_number=order_number,
                        order_quantity=order_quantity,
                        money_amount=money_amount
                    ))
                else:
                    customer_list.append(CustomerLatest(
                        license_id=license_id,
                        shop=shop,
                        commercial_type=commercial_type,
                        shop_class=shop_class,
                        key_customer=True,
                        active_date=valid_date,
                        import_date=import_date,
                        market_type=market_type,
                        order_number=order_number,
                        order_quantity=order_quantity,
                        money_amount=money_amount
                    ))

            if only_history:
                Customer.objects.bulk_create(customer_list, ignore_conflicts=True)
            else:
                CustomerLatest.objects.filter(key_customer=True).delete()
                CustomerLatest.objects.bulk_create(customer_list, ignore_conflicts=True)
                Customer.objects.bulk_create(customer_list, ignore_conflicts=True)
        except BaseException as e:
            res['code'] = 1
            res['msg'] = e

        return res


