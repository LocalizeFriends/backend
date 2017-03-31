from django.http import JsonResponse

def validate_with_form(form_class):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if request.method == 'GET':
                data = request.GET
            elif request.method == 'POST':
                data = request.POST
            else:
                raise NotImplementedError()
            form = form_class(data)
            if form.is_valid():
                return view(request, form.cleaned_data, *args, **kwargs)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'There were validation errors.',
                    'errors': form.errors
                }, status=400)
        return wrapper
    return decorator
