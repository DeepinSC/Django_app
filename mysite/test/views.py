from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('test/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context,request))

def detail(request,question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'test/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'test/results.html',{'question':question})
# no generic views used above --- #


class IndexView(generic.ListView):
    template_name = 'test/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    template_name = 'test/detail.html'
    model = Question
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    template_name = 'test/results.html'
    model = Question

def vote(request, question_id):
    question = get_object_or_404(Question,pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request,'test/detail.html',{"question":question,"error_message":"Youd didn't select any choice.",})
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('test:results',args=(question_id)))
# Create your views here.
