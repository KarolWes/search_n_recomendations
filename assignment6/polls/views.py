from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader, TemplateDoesNotExist
import pandas as pd
import constants as cs
from get_reviews import review_list, predict_ratings


def get_firstpage(request):
    template = render_firstpage_template('assignment6/firstpage.html', '', request)
    return HttpResponse(template)


def handle_userid_input(request):
    userid = int(request.POST.get('user_id'))
    if userid:
        # add csv file
        reviews = review_list(userid, cs.RATINGS_SMALL_FILE, cs.MOVIE_FILE)
        ans = predict_ratings(userid, reviews, num_similar_users=15, num_movies=20)
        if len(reviews[reviews['userId'] == userid]) == 0:
            template = render_firstpage_template('assignment6/firstpage.html', 'User not found!', request)
            return HttpResponse(template)
        else:
            return redirect('/recommendations')
    else:

        template = render_firstpage_template('assignment6/firstpage.html', 'Invalid input! Enter the valid number',
                                             request)
        return HttpResponse(template.render(template))


def get_recommendations(request):
    # TODO extend task 1.2
    template = loader.get_template('assignment6/secondpage.html')
    return HttpResponse(template.render({}, request))


def render_firstpage_template(template_name, error_message, request):
    try:
        template_context = {
            'error_message': error_message
        }
        template = loader.get_template(template_name)
        return template.render(template_context, request)
    except TemplateDoesNotExist:
        print("Template not found!")
        return None
