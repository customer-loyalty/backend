import concurrent.futures as pool
import xlwt
from django.db.models import Count
from django.http import HttpResponse
from functools import wraps
from django.utils.formats import date_format
from accountapp.models import Client
_DEFAULT_POOL = pool.ThreadPoolExecutor()


def threadpool(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        return (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)

    return wrap


@threadpool
def static_count_message(account):
    from accountapp.models import Client

    a = Client.objects.filter(client__username=account).values_list(
        'name', 'surname', 'card__cardType',
        'card__cardId', 'card__bonusBalance',
        'purchase_amount__total_amount', 'reg')
    d = []
    for i in a:
        date_string = date_format(i[-1])
        print(date_string, 124)
        i = list(i[0:-1])+[date_string]
        print(list(i[0:-1]))
        d.append(tuple(i))
    return d


def export_xls(request, account):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    wb = xlwt.Workbook(encoding='utf-8')

    def xls(columns, rows, name):
        ws = wb.add_sheet(name)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
    t = static_count_message(account)
    result = t.result()
    columns1 = ['Имя клиента', 'Фамилия', 'Тип карты',
                'Номер карты', 'Бонусный баланс',
                'Общая сумма покупки', 'Дата регистрации']
    xls(columns1,  result, 'client')
    wb.save(response)
    return response
