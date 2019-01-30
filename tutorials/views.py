from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Tutorial, TutorialAccess


def create_context():
    tutorials = Tutorial.objects.order_by('id')
    return {'tutorials': tutorials, 'navtype': 'tutorial', 'navitems': tutorials}


@login_required
def tutorials(request):
    context = create_context()
    return render(request, 'tutorials/tutorials.html', context=context)


@login_required
def tutorial(request, t_id):
    user = request.user
    context = create_context()
    try:
        tutorial = Tutorial.objects.get(pk=t_id)
    except Tutorial.DoesNotExist:
        tutorial = None
    context['tutorial'] = tutorial
    if tutorial:
        try:
            tutorial_access = TutorialAccess.objects.get(tutorial=tutorial, user=user)
        except TutorialAccess.DoesNotExist:
            tutorial_access = TutorialAccess(tutorial=tutorial, user=user)
        tutorial_access.access_count += 1
        tutorial_access.save()
    return render(request, 'tutorials/tutorial.html', context=context)
