from django.shortcuts import render
from django.db.models import Sum, Count
from regulatory_system.models import Customer, AbnormalFlowDetail, AbnormalFlow, CustomerLatest
from regulatory_system.serializers import CustomerSerializer, AbnormalFlowDetailSerializer, AbnormalFlowSerializer, CustomerLatestSerializer
from django.db import connection, transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from django.forms.models import model_to_dict
import pandas as pd
import datetime
import os
import json


# Create your views here.

CUSTOMER_SHOP_CLASS_DICT = {
    0: "无",
    1: "一档",
    2: "二档",
    3: "三档",
    4: "四档",
    5: "五档",
    6: "六档",
    7: "七档",
    8: "八档",
    9: "九档",
    10: "十档",
    11: "十一档",
    12: "十二档",
    13: "十三档",
    14: "十四档",
    15: "十五档",
    16: "十六档",
    17: "十七档",
    18: "十八档",
    19: "十九档",
    20: "二十档",
}


FLOW_DIRECTION_DICT = {
    0: "",
    1: "本区",
    2: "外区",
    3:"外省",
}


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['post', 'get'])
    def search(self, request):
        data = request.data
        search_users = Customer.objects
        params = {}

        if 'license_id' in data and data['license_id'] != '':
            params['license_id__icontains'] = data['license_id']
        if 'shop' in data and data['shop'] != '':
            params['shop__icontains'] = data['shop']
        if 'name' in data and data['name'] != '':
            params['name'] = data['name']
        if 'phone_number' in data and data['phone_number'] != '':
            params['phone_number'] = data['phone_number']
        if 'address' in data and data['address'] != '':
            params['address__icontains'] = data['address']
        if 'order_phone' in data and data['order_phone'] != '':
            params['order_phone'] = data['order_phone']
        if 'status' in data and data['status'] != '':
            params['status'] = data['status']
        if 'commercial_type__icontains' in data and data['commercial_type'] != '':
            params['commercial_type'] = data['commercial_type']
        if 'shop_class' in data and data['shop_class'] != '':
            params['shop_class'] = data['shop_class']
        if 'key_customer' in data and data['key_customer'] != '':
            params['key_customer'] = data['key_customer']
        if 'market_type' in data and data['market_type'] != '':
            params['market_type'] = data['market_type']
        if 'import_date' in data and data['import_date'] != '':
            params['import_date'] = data['import_date']

        if len(params) == 0:
            return Response()

        result = search_users.filter(**params)

        if 'export' in data and data['export'] == 1:
            if 'key_customer' in data or data['key_customer'] == True:
                queryset = result.values('license_id', 'shop', 'shop_class',
                                         'market_type', 'commercial_type', 'order_number',
                                         'order_quantity', 'money_amount', 'active_date')
                columns = {'license_id': '许可证号', 'shop': '零售户名称', 'shop_class': '档位',
                           'market_type': '市场类型', 'commercial_type': '业态',
                           'order_number': '订货次数', 'order_quantity': '订购数量（万支）',
                           'money_amount': '金额（万元）', 'active_date': '时间'}
                export_data = list(queryset)
                export_df = pd.DataFrame(export_data)
                export_df['active_date'] = export_df['active_date'].map(lambda x: x.strftime('%Y-%m'))
                export_df['shop_class'] = export_df['shop_class'].map(lambda x: CUSTOMER_SHOP_CLASS_DICT[x])
                export_df.rename(columns=columns, inplace=True)

                return export_csv(export_df, "客户信息")
            else:
                queryset = result.values('license_id', 'shop', 'name',
                                         'phone_number', 'address', 'order_phone',
                                         'status', 'commercial_type', 'shop_class', 'active_date')

                columns = {'license_id': '许可证号', 'shop': '零售户名称', 'name': '负责人',
                           'phone_number': '负责人电话', 'address': '经营地址', 'order_phone': '订货电话',
                           'status': '客户状态', 'commercial_type': '业态',
                           'shop_class': '档位', 'active_date': '时间'}
                export_data = list(queryset)
                export_df = pd.DataFrame(export_data)
                export_df['active_date'] = export_df['active_date'].map(lambda x: x.strftime('%Y-%m'))
                export_df['shop_class'] = export_df['shop_class'].map(lambda x: CUSTOMER_SHOP_CLASS_DICT[x])
                export_df.rename(columns=columns, inplace=True)

                return export_csv(export_df, "客户信息")

        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)


class CustomerLatestViewSet(viewsets.ModelViewSet):
    queryset = CustomerLatest.objects.all()
    serializer_class = CustomerLatestSerializer

    @action(detail=False, methods=['post', 'get'])
    @transaction.atomic
    def truncate(self, request):
        with connection.cursor() as cursor:
            cursor.execute("truncate table regulatory_system_customerlatest")

        return Response({"msg": "OK", "code": 0})

    @action(detail=False, methods=['post', 'get'])
    def search(self, request):
        data = request.data
        search_users = CustomerLatest.objects
        params = {}

        if 'license_id' in data and data['license_id'] != '':
            params['license_id__icontains'] = data['license_id']
        if 'shop' in data and data['shop'] != '':
            params['shop__icontains'] = data['shop']
        if 'name' in data and data['name'] != '':
            params['name'] = data['name']
        if 'phone_number' in data and data['phone_number'] != '':
            params['phone_number'] = data['phone_number']
        if 'address' in data and data['address'] != '':
            params['address__icontains'] = data['address']
        if 'order_phone' in data and data['order_phone'] != '':
            params['order_phone'] = data['order_phone']
        if 'status' in data and data['status'] != '':
            params['status'] = data['status']
        if 'commercial_type__icontains' in data and data['commercial_type'] != '':
            params['commercial_type'] = data['commercial_type']
        if 'shop_class' in data and data['shop_class'] != '':
            params['shop_class'] = data['shop_class']
        if 'key_customer' in data and data['key_customer'] != '':
            params['key_customer'] = data['key_customer']
        if 'market_type' in data and data['market_type'] != '':
            params['market_type'] = data['market_type']
        if 'import_date' in data and data['import_date'] != '':
            params['import_date'] = data['import_date']

        if len(params) == 0:
            return Response()

        result = search_users.filter(**params)

        if 'export' in data and data['export'] == 1:
            if 'key_customer' in data or data['key_customer'] == True:
                queryset = result.values('license_id', 'shop', 'shop_class',
                                         'market_type', 'commercial_type', 'order_number',
                                         'order_quantity', 'money_amount', 'active_date')
                columns = {'license_id': '许可证号', 'shop': '零售户名称', 'shop_class': '档位',
                           'market_type': '市场类型', 'commercial_type': '业态',
                           'order_number': '订货次数', 'order_quantity': '订购数量（万支）',
                           'money_amount': '金额（万元）', 'active_date': '时间'}
                export_data = list(queryset)
                export_df = pd.DataFrame(export_data)
                export_df['active_date'] = export_df['active_date'].map(lambda x: x.strftime('%Y-%m'))
                export_df['shop_class'] = export_df['shop_class'].map(lambda x: CUSTOMER_SHOP_CLASS_DICT[x])
                export_df.rename(columns=columns, inplace=True)

                return export_csv(export_df, "客户信息")
            else:
                queryset = result.values('license_id', 'shop', 'name',
                                         'phone_number', 'address', 'order_phone',
                                         'status', 'commercial_type', 'shop_class', 'active_date')

                columns = {'license_id': '许可证号', 'shop': '零售户名称', 'name': '负责人',
                           'phone_number': '负责人电话', 'address': '经营地址', 'order_phone': '订货电话',
                           'status': '客户状态', 'commercial_type': '业态',
                           'shop_class': '档位', 'active_date': '时间'}
                export_data = list(queryset)
                export_df = pd.DataFrame(export_data)
                export_df['active_date'] = export_df['active_date'].map(lambda x: x.strftime('%Y-%m'))
                export_df['shop_class'] = export_df['shop_class'].map(lambda x: CUSTOMER_SHOP_CLASS_DICT[x])
                export_df.rename(columns=columns, inplace=True)

                return export_csv(export_df, "客户信息")

        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)


class AbnormalFlowViewSet(viewsets.ModelViewSet):
    queryset = AbnormalFlow.objects.all()
    serializer_class = AbnormalFlowSerializer

    @action(detail=False, methods=['post', 'get'])
    def search(self, request):
        data = request.data
        flows = AbnormalFlow.objects
        params = {}

        if 'direction' in data and data['direction'] != '':
            params['flow_direction'] = data['direction']
        if 'quantity_start' in data and data['quantity_start'] != '':
            params['flow_quantity__gte'] = data['quantity_start']
        if 'quantity_end' in data and data['quantity_end'] != '':
            params['flow_quantity__lte'] = data['quantity_end']
        if 'date_start' in data and data['date_start'] != '':
            params['flow_date__gte'] = data['date_start']
        if 'date_end' in data and data['date_end'] != '':
            params['flow_date__lte'] = data['date_end']
        if 'license_id' in data and data['license_id'] != '':
            params['license_id__icontains'] = data['license_id']
        if 'shop' in data and data['shop'] != '':
            params['shop__icontains'] = data['shop']

        if len(params) == 0:
            return Response()

        flow_result = flows.filter(**params)

        if 'export' in data and data['export'] == 1:
            queryset =flow_result.values('license_id', 'shop', 'shop_class',
                                         'commercial_type', 'flow_date', 'flow_direction',
                                         'flow_quantity')
            columns = {'license_id': '许可证号', 'shop': '零售户名称', 'shop_class': '档位',
                       'commercial_type': '业态', 'flow_date': '外流月份', 'flow_direction': '流向',
                       'flow_quantity': '真烟数量'}
            export_data = list(queryset)
            export_df = pd.DataFrame(export_data)
            export_df['flow_date'] = export_df['flow_date'].map(lambda x: x.strftime('%Y-%m'))
            export_df['shop_class'] = export_df['shop_class'].map(lambda x: CUSTOMER_SHOP_CLASS_DICT[x])
            export_df['flow_direction'] = export_df['flow_direction'].map(lambda x: FLOW_DIRECTION_DICT[x])
            export_df.rename(columns=columns, inplace=True)

            return export_csv(export_df, "客户信息")

        page = self.paginate_queryset(flow_result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(flow_result, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post', 'get'])
    def count(self, request):
        data = request.data
        flows = AbnormalFlow.objects
        params = {}
        count_params = {}

        if 'direction' in data and data['direction'] != '':
            params['flow_direction'] = data['direction']
        if 'quantity_start' in data and data['quantity_start'] != '':
            params['flow_quantity__gte'] = data['quantity_start']
        if 'quantity_end' in data and data['quantity_end'] != '':
            params['flow_quantity__lte'] = data['quantity_end']
        if 'date_start' in data and data['date_start'] != '':
            params['flow_date__gte'] = data['date_start']
        if 'date_end' in data and data['date_end'] != '':
            params['flow_date__lte'] = data['date_end']
        if 'license_id' in data and data['license_id'] != '':
            params['license_id__icontains'] = data['license_id']
        if 'shop' in data and data['shop'] != '':
            params['shop__icontains'] = data['shop']

        if 'count_start' in data and data['count_start'] != '':
            count_params['num_count__gte'] = data['count_start']
        if 'count_end' in data and data['count_end'] != '':
            count_params['num_count__lte']= data['count_end']

        if len(params) == 0:
            return Response()

        flow_result = flows.filter(**params) \
            .values("license_id", "shop") \
            .annotate(sum_quantity=Sum("flow_quantity"), num_count=Count('license_id')) \
            .filter(**count_params).order_by('num_count')

        if 'export' in data and data['export'] == 1:
            queryset =flow_result.values('license_id', 'shop', 'sum_quantity',
                                         'num_count')
            columns = {'license_id': '许可证号', 'shop': '零售户名称', 'sum_quantity': '数量（万支）',
                       'num_count': '违规次数'}
            export_data = list(queryset)
            export_df = pd.DataFrame(export_data)
            export_df.rename(columns=columns, inplace=True)

            return export_csv(export_df, "客户信息")

        page = self.paginate_queryset(flow_result)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(flow_result)


class AbnormalFlowDetailViewSet(viewsets.ModelViewSet):

    queryset = AbnormalFlowDetail.objects.all()
    serializer_class = AbnormalFlowDetailSerializer

    @action(detail=False, methods=['post', 'get'])
    def search(self, request):
        data = request.data
        flows = AbnormalFlowDetail.objects
        params = {}

        if 'license_id' in data and data['license_id'] != '':
            params['license_id'] = data['license_id']
        if 'date' in data and data['date'] != '':
            params['flow_date'] = data['date']

        if len(params) == 0:
            return Response()

        flow_detail_result = flows.filter(**params)

        if 'export' in data and data['export'] == 1:
            queryset =flow_detail_result.values('license_id', 'brand_name', 'flow_quantity',
                                         'spray_code', 'code_type', 'flow_date',
                                         'shop', 'flow_direction')
            columns = {'license_id': '许可证号', 'brand_name':'品牌名称', 'flow_quantity': '真烟数量',
                       'spray_code':'32位喷码', 'code_type':'类型', 'flow_date': '外流月份',
                       'shop': '零售户名称',  'flow_direction': '流向'}
            export_data = list(queryset)
            export_df = pd.DataFrame(export_data)
            export_df['flow_date'] = export_df['flow_date'].map(lambda x: x.strftime('%Y-%m'))
            export_df['flow_direction'] = export_df['flow_direction'].map(lambda x: FLOW_DIRECTION_DICT[x])
            export_df.rename(columns=columns, inplace=True)

            return export_csv(export_df, "客户信息")

        page = self.paginate_queryset(flow_detail_result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(flow_detail_result, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post', 'get'])
    def stat(self, request):
        data = request.data
        flows = AbnormalFlowDetail.objects
        params = {}

        if 'license_id' in data and data['license_id'] != '':
            params['license_id'] = data['license_id']
        if 'date' in data and data['date'] != '':
            params['flow_date'] = data['date']

        if len(params) == 0:
            return Response()

        flow_detail_result = flows.filter(**params)\
            .values("brand_name")\
            .annotate(sum_quantity=Sum('flow_quantity')).order_by('sum_quantity')

        if 'export' in data and data['export'] == 1:
            queryset =flow_detail_result.values('brand_name', 'sum_quantity')
            columns = {'brand_name': '品牌名称', 'sum_quantity': "数量（万支）"}
            export_data = list(queryset)
            export_df = pd.DataFrame(export_data)
            export_df.rename(columns=columns, inplace=True)

            return export_csv(export_df, "客户信息")

        page = self.paginate_queryset(flow_detail_result)
        if page is not None:
            #serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(page)

        serializer = self.get_serializer(flow_detail_result, many=True)
        return Response(flow_detail_result)

    @action(detail=False, methods=['post', 'get'])
    def sum_by_brand(self, request):
        data = request.data
        flows = AbnormalFlowDetail.objects
        params = {}

        if 'direction' in data and data['direction'] != '':
            params['flow_direction'] = data['direction']
        if 'quantity_start' in data and data['quantity_start'] != '':
            params['flow_quantity__gte'] = data['quantity_start']
        if 'quantity_end' in data and data['quantity_end'] != '':
            params['flow_quantity__lte'] = data['quantity_end']
        if 'date_start' in data and data['date_start'] != '':
            params['flow_date__gte'] = data['date_start']
        if 'date_end' in data and data['date_end'] != '':
            params['flow_date__lte'] = data['date_end']
        if 'license_id' in data and data['license_id'] != '':
            params['license_id__icontains'] = data['license_id']
        if 'shop' in data and data['shop'] != '':
            params['shop__icontains'] = data['shop']

        if len(params) == 0:
            return Response()

        if 'brand' in data and data['brand'] != '':
            params['brand_name__icontains'] = data['brand']

        flow_result = flows.filter(**params) \
            .values("brand_name") \
            .annotate(sum_quantity=Sum("flow_quantity")) \
            .order_by('sum_quantity')


        if 'export' in data and data['export'] == 1:
            queryset =flow_result.values('brand_name', 'sum_quantity')
            columns = {'brand_name': '品牌名称', 'sum_quantity': "数量（万支）"}
            export_data = list(queryset)
            export_df = pd.DataFrame(export_data)
            export_df.rename(columns=columns, inplace=True)

            return export_csv(export_df, "客户信息")
        page = self.paginate_queryset(flow_result)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(flow_result)


DOWNLOAD_PATH = "uploads/"


def export_csv(df, filename):
    #path = DOWNLOAD_PATH + "file" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".csv"
    path = DOWNLOAD_PATH + filename + ".csv"
    if os.path.exists(path):
        os.remove(path)
    df.to_csv(path)
    f = open(path, 'rb')
    response = FileResponse(f)
    response["content_type"] = 'text/csv'
    response['Content-Disposition'] = "attachment; filename={}.csv".format(filename)
    return response
