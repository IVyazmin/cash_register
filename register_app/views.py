import datetime
import io
import uuid

import pdfkit
import qrcode
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404

from cash_register import settings
from register_app.models import Item


@csrf_exempt
def cash_machine(request):
    order = dict(request.POST)
    if "items" not in order:
        return HttpResponseBadRequest()

    order_info = []
    total_sum = 0
    for item_id in set(order["items"]):
        item = get_object_or_404(Item, id=item_id)
        item_num = order["items"].count(item_id)
        item_sum = item_num * item.price
        item_info = {
            "name": item.title,
            "num": item_num,
            "sum": item_sum
        }
        order_info.append(item_info)
        total_sum += item_sum

    cur_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    template = get_template('register_app/order.html')
    html = template.render({
        "items": order_info,
        "cur_time": cur_time,
        "total_sum": total_sum
    })
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }

    pdf_path = f"{datetime.datetime.now().timestamp()}_{uuid.uuid4()}.pdf"
    pdf = pdfkit.from_string(html, False, options)
    file_name = default_storage.save(pdf_path, ContentFile(pdf))
    url_for_get = f"{settings.DOMAIN}media/{file_name}"

    tmp_file = io.BytesIO()
    qrcode.make(url_for_get, box_size=10, border=1).save(tmp_file, "PNG")
    response = HttpResponse(tmp_file.getvalue(), content_type='application/octet-stream')
    return response
