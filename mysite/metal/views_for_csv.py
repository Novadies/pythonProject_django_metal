from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import *

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "polls/upload.html", data)
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
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        # loop over the lines and save them to db via model
        for line in lines:
            fields = line.split(",")
            try:
                question = Question(
                    question_text=fields[0],
                    pub_date=fields[1],
                )
                question.save()
            except Exception as e:
                messages.error(request, "Unable to upload file. "+repr(e))
                pass
    except Exception as e:
        messages.error(request, "Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse("polls:upload_csv"))