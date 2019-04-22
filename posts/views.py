# posts/views.py
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from .forms import PostForm, ImageForm, CommentForm
from .models import Post, Image, Comment, Hashtag

def list(request):
    
    if request.user.is_authenticated:
    # 1] 모든 유저의 전체 포스트 조회
    # posts = get_list_or_404(Post.objects.order_by('-pk'))
    
    # 2] 내가 팔로우하고있는 유저의 포스트만 조회
    # posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-pk')
    
    # 3] 2 + 나의 포스트 쿼리 합치기 (장고스럽게 체인하기)
        followings = request.user.followings.all()
        posts = Post.objects.filter(
                Q(user__in=followings) | Q(user=request.user.id)
            ).order_by('-pk')
        
    # 4] python chain (파이썬스럽게 체인하기)
    # followings = request.user.followings.all()
    # chain_followings = chain(followings, [request.user])
    # posts = Post.objects.filter(user_in=chain_followings).order_by('-pk')
    else:
        posts = Post.objects.order_by('-pk')
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/list.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            
            # hashtag - post.save() 가 된 이후에 hashtag 코드가 와야함.
            # 1. 게시글을 순회하면서 띄어쓰기를 잘라야함
            for word in post.content.split():
            # 2. 자른 단어가 # 으로 시작하나?
                if word.startswith('#'):
            # 3. 이 해시태그가 기존 해시태그에 있는 건지?
            #       없다면 해시태그 생성, 이미 있다면 굳이 더 안만들어도 되겠죠?
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    # 모델 객체의 인스턴스, boolean 을 튜플로 리턴한다
                    # 없으면 새로 생성 : (hashtag, True), 있으면 : (hashtag, False)
                    post.hashtags.add(hashtag[0])
                    
                    
                    # 내가 짜려고 시도했지만 망한 코드
                    # if word not in Hashtag.objects.all():
                    #     hash_word = Hashtag.objects.create(content=word)
                    #     # hash_word = Hashtag(content=word)
                    # else:
                    #     hash_word = Hashtag.objects.get(content=word)
                    # post.hashtags.add(hash_word)
                    # # hash_word.post_set.add(post)
                    # # hash_word.save()
            
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {
        'post_form': post_form,
        'image_form': image_form,
        }
    return render(request, 'posts/form.html', context)

@login_required    
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user == post.user:
        if request.method == 'POST':
            post_form = PostForm(request.POST, instance=post)
            if post_form.is_valid():
                post_form.save()
                
                # 해쉬태그 다 날린다음에 다시 등록하기
                # hashtag update
                post.hashtags.clear()
                for word in post.content.split():
                    if word[0] == '#':   # if word.startwith('#'):
                        hashtag, new = Hashtag.objects.get_or_create(content=word)
                        post.hashtags.add(hashtag)
            
                return redirect('posts:list')
        else:
            post_form = PostForm(instance=post)
        context = {'post_form': post_form,}
        return render(request, 'posts/form.html', context)
    return redirect('posts:list')
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user == post.user:
        if request.method == 'POST':
            post.delete()
    return redirect('posts:list')

@login_required 
def create_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post_id = post_pk
            comment.save()
    return redirect('posts:list')
    
def delete_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            comment.delete()
    return redirect('posts:list')
    
    
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 이미 해당 유저가 like_users 에 존재하면 해당 유저를 삭제(좋아요 취소)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    # 없으면 추가(좋아요)
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')
        
@login_required
def explore(request):
    # posts = Post.objects.order_by('-pk')
    # 내 포스트는 제외하고 조회
    posts = Post.objects.exclude(user=request.user).order_by('-pk')
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/explore.html', context)
    
def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    posts = hashtag.post_set.order_by('-pk')
    context = {
        'hashtag': hashtag,
        'posts': posts,
    }
    return render(request, 'posts/hashtag.html', context)