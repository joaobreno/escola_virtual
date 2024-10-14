from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import logout
from school.models import *



def profile_user(func):
    def _decorated(request, *args, **kwargs):
        context_dict = {}

        if request.user.is_active:
            context_dict['profile'] = {'username': request.user.username,
                                       'email': request.user.email}
            
            if settings.DEBUG == True:
                return func(request, context_dict, *args, **kwargs)
            else:
                try:
                    return func(request, context_dict, *args, **kwargs)
                except Http404 as e:
                    return render(request, 'error-page.html', {'title': 'Not Found 404',
                                                               'code': '404',
                                                               'message': 'Essa página não existe!'})
                except Exception as e:
                    return render(request, 'error-page.html', {'title': 'Error 500',
                                                               'code': '500',
                                                               'message': 'Houve algum erro na requisição!'})

        else:
            logout(request)
            return HttpResponseRedirect("")

    return _decorated