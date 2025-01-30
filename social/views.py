from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Comment, UserProfile, Like, Dislike
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.models import User

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()

        
        for post in posts:
            post.like_count = Like.objects.filter(post=post).count()
            post.dislike_count = Dislike.objects.filter(post=post).count()
            post.user_likes = Like.objects.filter(post=post, user=request.user).exists()
            post.user_dislikes = Dislike.objects.filter(post=post, user=request.user).exists()

        return render(request, 'social/post_list.html', {'post_list': posts, 'form': form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('post-list')

        posts = Post.objects.all().order_by('-created_on')
        return render(request, 'social/post_list.html', {'post_list': posts, 'form': form})


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('created_on')

        # Count likes and dislikes
        like_count = Like.objects.filter(post=post).count()
        dislike_count = Dislike.objects.filter(post=post).count()

        # Check if the user has liked or disliked the post
        user_likes = Like.objects.filter(post=post, user=request.user).exists()
        user_dislikes = Dislike.objects.filter(post=post, user=request.user).exists()

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'like_count': like_count,
            'dislike_count': dislike_count,
            'user_likes': user_likes,
            'user_dislikes': user_dislikes,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('created_on')

        # Count likes and dislikes
        like_count = Like.objects.filter(post=post).count()
        dislike_count = Dislike.objects.filter(post=post).count()

        # Check if the user has liked or disliked the post
        user_likes = Like.objects.filter(post=post, user=request.user).exists()
        user_dislikes = Dislike.objects.filter(post=post, user=request.user).exists()

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'like_count': like_count,
            'dislike_count': dislike_count,
            'user_likes': user_likes,
            'user_dislikes': user_dislikes,
        }

        return render(request, 'social/post_detail.html', context)


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)

        # Check if user has already liked the post, if not, add like
        if not Like.objects.filter(user=request.user, post=post).exists():
            Like.objects.create(user=request.user, post=post)

        # If the user had previously disliked the post, remove the dislike
        Dislike.objects.filter(user=request.user, post=post).delete()

        return redirect('post-detail', pk=pk)


class PostDislikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)

        # Check if user has already disliked the post, if not, add dislike
        if not Dislike.objects.filter(user=request.user, post=post).exists():
            Dislike.objects.create(user=request.user, post=post)

        # If the user had previously liked the post, remove the like
        Like.objects.filter(user=request.user, post=post).delete()

        return redirect('post-detail', pk=pk)



class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body', 'image']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        return self.request.user == self.get_object().author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        return self.request.user == self.get_object().author


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        profile, created = UserProfile.objects.get_or_create(user=user)
        posts = Post.objects.filter(author=user).order_by('-created_on')

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
        }

        return render(request, 'social/profiles.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user.pk})

    def test_func(self):
        return self.request.user == self.get_object().user
