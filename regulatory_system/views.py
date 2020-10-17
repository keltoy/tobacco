from django.shortcuts import render
from django.db.models import Sum, Count
from regulatory_system.models import Customer, AbnormalFlowDetail, AbnormalFlow, CustomerLatest
from regulatory_system.serializers import CustomerSerializer, AbnormalFlowDetailSerializer, AbnormalFlowSerializer, CustomerLatestSerializer
from django.db import connection, transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
import pandas as pd
import datetime
import os


# Create your views here.

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
    def aaa(self, request):
        flows = AbnormalFlow.objects.all()
        a = self.get_serializer(flows, many=True)

        file_name = "bbb.csv"
        x = pd.DataFrame(a.data)
        x.to_csv("abcd.csv")
        f = open("abcd.csv", 'rb')
        response = FileResponse(f)
        response["content_type"] = 'text/csv'
        response['Content-Disposition'] = "attachment; filename= {}".format(file_name)
        return response

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

        page = self.paginate_queryset(flow_result)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(flow_result)


DOWNLOAD_FILE = "/uploads/download.csv"


def export_csv(data):
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    x = pd.DataFrame(data)
    if os.path.exists(DOWNLOAD_FILE):
        os.remove(DOWNLOAD_FILE)
    x.to_csv(DOWNLOAD_FILE)
    f = open(DOWNLOAD_FILE, 'rb')
    response = FileResponse(f)
    response["content_type"] = 'text/csv'
    response['Content-Disposition'] = "attachment; filename= {}.csv".format(file_name)
    return response
