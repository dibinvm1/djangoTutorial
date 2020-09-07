from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F

from .models import Choice, Question

def index(request):
    
    question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'question_list' : question_list} 
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question,pk=question_id)

    context = {'question': question}
    return render(request, 'polls/detail.html', context)


def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        context = {'question' : question, 'error_message':"You didn't select a choice"}
        return render(request, 'polls/detail.html',context)
    else:
        selected_choice.votes = F('votes') +1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})
