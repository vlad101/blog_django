import json

from django.core import serializers
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.syndication.views import Feed
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import truncatewords
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from django.views import generic
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormMixin

from taggit.models import Tag

from .forms import CommentForm, PostForm, PostShareForm, PostSearchForm, NewUserForm

from .models import Comment, Post


class PostListView(LoginRequiredMixin, FormMixin, ListView):
    model = Post
    paginate_by = 3
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        num_visits = self.request.session.get('num_visits', 1)
        self.request.session['num_visits'] = num_visits + 1
        context['num_visits'] = num_visits
        context['form'] = PostForm(initial={
                                            'author': self.request.user,
                                        }
                                    )
        return context

    def get_queryset(self):
        return Post.objects.filter(valid=True)

    def get_success_url(self):
        return reverse('index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form is not None:
            updated_slug = request.POST.copy()
            updated_slug.update({'slug': slugify(form.data['title'])}) 
            form = PostForm(data=updated_slug) 
            form.valid = True
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.slug = slugify(form.data['title'])
        form.save()
        return super(PostListView, self).form_valid(form)

class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(valid=True).filter(post__slug=self.kwargs['slug'])
        context['form_add_comment'] = CommentForm(initial={
                                            'post': self.object,
                                            'author': self.request.user,
                                        }
                                    )
        context['form_edit_post'] = PostForm(initial={
                                            'title': self.object.title,
                                            'slug': self.object.slug,
                                            'body': self.object.body,
                                            'tags': [tag for tag in self.object.tags.all()],
                                            'status': self.object.status,
                                            'updated': now(),
                                        }
                                    )
        context['form_share_post'] = PostShareForm()
        return context

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('post-detail', kwargs={
                                        'year': self.object.created.year,
                                        'month': self.object.created.month,
                                        'day': self.object.created.day,
                                        'slug': self.object.slug,
                                    }
                )

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)

class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(tags__slug=self.kwargs['slug'])
        return context

class LatestPostFeed(Feed):
    title = "My Blog Posts"
    link = ""
    description = "Latest blog posts"

    def items(self):
        return Post.objects.filter(status__exact='p').order_by('-created')[:5]

    def item_title(self, item):
        return item.title    

    def item_description(self, item):
        return truncatewords(item.body, 10) + "... by %s" % item.author 

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Member')
            user.groups.add(group)
            return redirect('/blog')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
                    request, 
                    "registration/register.html", 
                    { 
                        "form" : form 
                    }
            )

@login_required
def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment is not None:
        post = get_object_or_404(Post, id=comment.post.id)
        if post is not None:
            comment.valid = False
            comment.updated = now()
            comment.save()
            return redirect(reverse('post-detail', kwargs={
                                         'year': post.created.year,
                                         'month': post.created.month,
                                         'day': post.created.day,
                                         'slug': post.slug,
                     }
            ))
    return redirect('/blog')

@login_required
def comment_get_edit_form(request, id):
    comment = get_object_or_404(Comment, pk=id)
    if comment is not None:
        context = {
            "modal_form": CommentForm(initial = {
                                    'id': comment.id,
                                    'post': comment.post,
                                    'author': comment.author,
                                    'name': comment.name,
                                    'body': comment.body,
                                    'updated': now(),
                                }
                            ),
            "modal_id": "EditCommentModal",
            "modal_label": "EditCommentModalLabel",
            "modal_form_action_url": "",
            "modal_title": "Edit Comment",
        }
        comment_data = render_to_string('blog/components/modal.html', context)
    return JsonResponse(comment_data, safe=False)

@login_required
def comment_edit(request, id):
    success = False
    comment = get_object_or_404(Comment, id=id)
    if comment is not None and request.method == "POST":
        post = get_object_or_404(Post, pk=comment.post.id)
        if post is not None:
            form = CommentForm(request.POST or None, instance=comment)
            if form is not None:
                if form.is_valid():
                    form.save()
                    success = True
    return JsonResponse({"success":success}, safe=False)

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post is not None:
        post.valid = False
        post.updated = now()
        post.save()
    return redirect('/blog')

@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post is not None and request.method == "POST":
        form = PostForm(request.POST or None, instance=post)
        if form is not None:
            #print(form.errors.as_data())
            if form.is_valid():
                form.save()
                return redirect(reverse('post-detail', kwargs={
                                         'year': post.created.year,
                                         'month': post.created.month,
                                         'day': post.created.day,
                                         'slug': post.slug,
                     }
            ))
    return redirect('/blog')


@login_required
def post_share(request, id):
    post = get_object_or_404(Post, id=id)
    if post is not None and request.method == "POST":
        form = PostShareForm(request.POST)
        if form is not None:
            #print(form.errors.as_data())
            if form.is_valid():
                context = {
                            'comment': form.data['comment'],
                            'post': post,
                            'post_url': "{0}://{1}{2}".format(request.scheme, request.get_host(), post.get_absolute_url()),
                        }
                msg_plain = render_to_string('blog/email/share_post.txt', context)
                msg_html = render_to_string('blog/email/share_post.html', context)

                send_mail(
                    "{0} Shared Post!".format(request.user.get_username()),
                    msg_plain,
                    request.user.email,
                    [form.data['email_to'], ],
                    html_message=msg_html,
                )

                return redirect(reverse('post-detail', kwargs={
                                         'year': post.created.year,
                                         'month': post.created.month,
                                         'day': post.created.day,
                                         'slug': post.slug,
                     }
            ))
    return redirect('/blog')


def search_results(request):
    message = None
    post_list = list()
    if request.method == "GET":
        form = PostSearchForm(request.GET or None)
        if form.is_valid():
            query = form.data['search']
            post_list = Post_Helper().get_post_search_results(query)

            if len(post_list) == 0:
                message = 'No posts match search criteria.'

    return render(
                    request, 
                    "blog/search_results.html", 
                    context = {
                        'post_list' : post_list,
                        'form' : form,
                        'message':  message,
                    }
            )

def post_autocomplete_search(request):
    title_list = list()
    if request.method == "GET":
        query = request.GET.get("term", "")
        post_list = Post_Helper().get_post_search_results(query)
        for post in post_list:
            title_list.append(post.title)
    return HttpResponse(json.dumps(title_list), 'application/json')


class Post_Helper:
    def get_post_search_results(self, query):
        return Post.objects.filter(
                    (Q(valid=True) & Q(status='p')) & (Q(title__icontains=query) | Q(body__icontains=query)) 
                )