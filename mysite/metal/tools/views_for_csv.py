from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from metal.tools.csv_to_bd import zapis

from metal.models import *

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "metal/upload_form.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not a CSV')
            return HttpResponseRedirect(reverse("polls:upload_csv"))
        # if file is too large - error
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB). " % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("polls:upload_csv"))
        # loop over the lines and save them to db via model
        try:
            zapis(csv_file)
        except Exception as e:
            messages.error(request, "Unable to upload file. "+repr(e))
    except Exception as e:
        messages.error(request, "Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse('start-url'))