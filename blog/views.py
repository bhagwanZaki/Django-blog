from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView , DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, request
from django.urls import reverse
# Create your views here.
def home(request):
    context ={
        'posts' : Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by = 10
    # def get_context_data(self, **kwargs):
    #     posts = get_object_or_404(Post,id=self.kwargs['pk'])
    #     total_like = posts.num_likes()
    #     context = super().get_context_data(**kwargs)
    #     context['total_like'] = total_like
        
    #     return context


class UserPostListView(ListView):
    model = Post
    template_name='blog/user_posts.html'
    context_object_name='posts'
    
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        liked = True
        posts = get_object_or_404(Post,id=self.kwargs['pk'])
        total_like = posts.num_likes()

        if posts.like.filter(id=self.request.user.id).exists():
            liked = False
        
        context = super().get_context_data(**kwargs)
        context['total_like'] = total_like
        context['liked'] = liked
        return context

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html',{'title' : 'About'})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False

# unlike 
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        liked =  False
    else:
        post.like.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)])) 

@login_required
def like_main_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

# unlike and like condition
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    
    return HttpResponseRedirect(reverse('blog-home')) 