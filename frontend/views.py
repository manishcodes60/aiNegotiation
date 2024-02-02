from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
import pandas as pd
import io
import json

from frontend.gpt import text_process
from .forms import *
from nltk import tokenize

# Create your views here.

def index(request):
    return render(request, "index.html")

def requirements(request):
    return render(request, "requirements.html")

def dataTeam(request):

    file_path = 'frontend/data/data_science_team.json'

    try:
        with open(file_path, 'r') as file:
            team_data = json.load(file)
    except FileNotFoundError:
        return HttpResponse('JSON file not found.', status=404)
    except json.JSONDecodeError:
        return HttpResponse('Invalid JSON format.', status=500)

    return render(request, "data_science_teams.html", {'team_data': team_data})

def negotiationTeam(request):

    file_path = 'frontend/data/negotiation_team_data.json'

    try:
        with open(file_path, 'r') as file:
            team_data = json.load(file)
    except FileNotFoundError:
        return HttpResponse('JSON file not found.', status=404)
    except json.JSONDecodeError:
        return HttpResponse('Invalid JSON format.', status=500)

    return render(request, "negotiation_team.html", {'team_data': team_data})

def aiTranscript(request):
    return render(request, "ai_supported_transcript.html")

def aiQuasi(request):
    return render(request, "ai_supported_quasi.html")

def contact(request):
    return render(request, "contact.html")

def process_transcript(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        transcript_text = data.get('input_value', None)
        # transcript_text = request.POST.get('transcriptText')
        # sentences = tokenize.sent_tokenize(transcript_text)
        result = text_process(transcript_text)

        # Convert the DataFrame to an Excel file
        excel_file = io.BytesIO()
        result.to_excel(excel_file, sheet_name='Sheet1', index=False)
        excel_file.seek(0)

        # Prepare the response with the Excel file
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=data.xlsx'

        return response

        # df_html = result.to_html()
        # return render(request, "ai_supported_transcript.html", {'df_html': df_html})

    else:
        return render(request, "ai_supported_transcript.html")
