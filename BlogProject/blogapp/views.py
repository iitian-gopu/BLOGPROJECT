from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.views.generic import CreateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.core.mail import send_mail
from .forms import  *
from taggit.models import Tag
import datetime

# Create your views here.




def post_listview(request,tag_slug=None):
    post_list=Post.objects.all().filter(status='published')
    tag=None
    
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)    

    return render(request,'blogapp/blog_list.html',{'post_list':post_list,'page': page_number,'tag':tag})

def post_detailview(request,slug):
    post=get_object_or_404(Post,slug=slug )
    comments = post.comments.filter(active=True)
    new_comment = None
    csubmit=False
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            csubmit=True
            return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()

    return render(request,'blogapp/post_detail.html',{'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'csubmit':csubmit})

def emailsendview(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    
    if request.method=='POST':
        form=EmailForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) recommends you to read"{}"'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='Read Post At:\n {}\n\n{}\'s comment:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject, message, 'gopaldjango2020@gmail.com', [cd['to']])
            sent=True
    else:
        form=EmailForm()        
            
    return render(request,'blogapp/mail.html',{'form':form,'post':post,'sent':sent})  



def reply_page(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input
            reply = form.save(commit=False)
    
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url+'#'+str(reply.id))

    return redirect("/")




    
    