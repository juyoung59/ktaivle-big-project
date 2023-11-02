from django.shortcuts import render, redirect
from .forms import SurveyForm

def submit(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('submitted')
    else:
        form = SurveyForm()
    
    return render(request, 'survey.html', {'form': form})

def submitted(request):
    return render(request, 'submitted.html')