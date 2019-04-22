from django import template

register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content+' '
    hashtags = post.hashtags.order_by('-content')
    
    #hashtags를 순회하면서, content 내에서 해당 문자열(해쉬태그)를 링크를 포함한 문자열로 치환
    for hashtag in hashtags:
        content = content.replace(f'{hashtag.content}'+' ', f'<a href="/posts/hashtag/{hashtag.pk}/">{hashtag.content}</a> ')
    return content
