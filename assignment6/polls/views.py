from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader, TemplateDoesNotExist
from . import constants as cs, get_reviews as rev




def get_firstpage(request):
    template = render_firstpage_template('assignment6/firstpage.html', '', request)
    return HttpResponse(template)


def handle_userid_input(request):
    userid = int(request.POST.get('user_id'))
    if userid:
        # add csv file
        reviews = rev.review_list(userid, cs.RATINGS_SMALL_FILE, cs.MOVIE_FILE)
        if len(reviews[reviews['userId'] == userid]) == 0:
            template = render_firstpage_template('assignment6/firstpage.html', 'User not found!', request)
            return HttpResponse(template)
        else:
            return redirect('get_recommendations', userid=userid)
    else:

        template = render_firstpage_template('assignment6/firstpage.html', 'Invalid input! Enter the valid number',
                                             request)
        return HttpResponse(template.render(template))


def get_recommendations(request, userid):
    print("hello, you are inside reco func")
    userid = int(userid)
    reviews = rev.review_list(userid, cs.RATINGS_SMALL_FILE, cs.MOVIE_FILE)
    data = rev.prepare_for_output(userid, reviews)
    return render(request, cs.RECOMENDATION_SITE_TEMPLATE, {"userid":userid, "movies":data})


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
