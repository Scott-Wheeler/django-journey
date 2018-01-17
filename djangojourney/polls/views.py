from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

# Create your views here.
from .models import Question
from mockito.utils import get_obj
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

## response containing links
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list
#     }
#     return HttpResponse(template.render(context, request))

## response containing calculated text
#     response = ", ".join([question.question_text for question in latest_question_list])
#     return HttpResponse(response)

## simple hello world
#     return HttpResponse("Hello world! You're at the polls index")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question":question})


## try to get the question and raise a 404 if it doesn't exist
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question %s does not exist." % question_id)

## simple text
#     return HttpResponse("You're looking at question %s." % question_id)



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        render(request, "polls/detail.html", {
            "question": question,
            "error_message": "Choose your vote!"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being POSTed twice if a
        # user hits the Back button
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))



# initial version
#     return HttpResponse("You're voting on question %s." % question_id)



