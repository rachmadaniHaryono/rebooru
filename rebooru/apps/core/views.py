from django.shortcuts import render_to_response

from rebooru.apps.accounts.models import Account
from rebooru.apps.images.models import Image

def index(request):
    """Just displays some accounts and images"""
    context = {
            'accounts': Account.objects.all()[:5],
            'images': Image.objects.all()[:20],
    }

    return render_to_response('core/index.html', context)
