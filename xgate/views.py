from django.shortcuts import render
from .models import viexam


def viexam_view(request):
    exams = viexam.objects.filter(is_public=True)  
    context = {
        'exams': exams,
        'fio': 'Пивницкая Владислава Игоревна',
        'group': '241-672',
    }
    return render(request, 'xgate/exam.html', context)
# Create your views here.
