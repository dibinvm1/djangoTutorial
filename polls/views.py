from django.db.models import F, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse
from django.views import generic


from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'

    def get_queryset(self):
        return Question.objects.annotate(choice_count=Count('choices')).\
            filter(pub_date__lte=timezone.now(),choice_count__gt=0).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model =Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.annotate(choice_count=Count('choices')).\
            filter(pub_date__lte=timezone.now(),choice_count__gt=0)


class ResultsView(generic.DetailView):
    model =Question
    template_name = 'polls/results.html'
    
    def get_queryset(self):
        return Question.objects.annotate(choice_count=Count('choices')).\
            filter(pub_date__lte=timezone.now(),choice_count__gt=0)


def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        context = {'question' : question, 'error_message':"You didn't select a choice"}
        return render(request, 'polls/detail.html',context)
    else:
        selected_choice.votes = F('votes') +1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

