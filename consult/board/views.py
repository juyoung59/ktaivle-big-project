from django.shortcuts import render
from .models import Post, Reply
from .forms import BoardWriteForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# Create your views here.
def board(request):
    posts_faq = Post.objects.filter(category="FAQ")
    posts_inquiry = Post.objects.filter(category="Inquiry")
        
    return render(request, 'board.html', {'posts_faq':posts_faq, 'posts_inquiry':posts_inquiry})

@login_required
@require_http_methods(['GET', 'POST'])
def posting(request):
    if request.method == 'POST':
        write_form = BoardWriteForm(request.POST, instance=request.user)
        if form.is_valid():
            writer = request.user.username
            form = Post(
                title = write_form.title,
                contents = write_form.contents,
                writer = writer,
                category = write_form.category                
            )
            form.save()
            return redirect('board:board')
    else:
        form = BoardWriteForm(instance=request.user)
        return render(request, 'board_posting.html',{'form':form})