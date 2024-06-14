from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Author, Category, Post, Comment

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Создание пользователей
        user1, created1 = User.objects.get_or_create(username='user1', defaults={'email': 'user1@example.com', 'password': 'password'})
        user2, created2 = User.objects.get_or_create(username='user2', defaults={'email': 'user2@example.com', 'password': 'password'})

        # Создание авторов
        author1, created1 = Author.objects.get_or_create(user=user1)
        author2, created2 = Author.objects.get_or_create(user=user2)

        # Создание категорий
        category1, created1 = Category.objects.get_or_create(name='Sports')
        category2, created2 = Category.objects.get_or_create(name='Politics')
        category3, created3 = Category.objects.get_or_create(name='Education')
        category4, created4 = Category.objects.get_or_create(name='Entertainment')

        # Создание постов
        post1, created1 = Post.objects.get_or_create(author=author1, post_type=Post.ARTICLE, title='Article 1', text='Text of article 1')
        post2, created2 = Post.objects.get_or_create(author=author2, post_type=Post.ARTICLE, title='Article 2', text='Text of article 2')
        post3, created3 = Post.objects.get_or_create(author=author1, post_type=Post.NEWS, title='News 1', text='Text of news 1')

        # Присвоение категорий постам
        post1.categories.add(category1, category2)
        post2.categories.add(category2)
        post3.categories.add(category3, category4)

        # Создание комментариев
        comment1, created1 = Comment.objects.get_or_create(post=post1, user=user1, defaults={'text': 'Comment 1 on article 1'})
        comment2, created2 = Comment.objects.get_or_create(post=post1, user=user2, defaults={'text': 'Comment 2 on article 1'})
        comment3, created3 = Comment.objects.get_or_create(post=post2, user=user1, defaults={'text': 'Comment 1 on article 2'})
        comment4, created4 = Comment.objects.get_or_create(post=post3, user=user2, defaults={'text': 'Comment 1 on news 1'})

        # Применение функций like() и dislike()
        post1.like()
        post1.like()
        post2.like()
        post3.dislike()
        comment1.like()
        comment2.dislike()
        comment3.like()
        comment4.like()

        # Обновление рейтингов авторов
        author1.update_rating()
        author2.update_rating()

        # Вывод username и рейтинга лучшего пользователя
        best_author = Author.objects.order_by('-rating').first()
        self.stdout.write(self.style.SUCCESS(f'Лучший автор: {best_author.user.username}, рейтинг: {best_author.rating}'))

        # Вывод информации о лучшей статье
        best_post = Post.objects.order_by('-rating').first()
        self.stdout.write(self.style.SUCCESS(f'Дата добавления: {best_post.created_at}, Автор: {best_post.author.user.username}, Рейтинг: {best_post.rating}, Заголовок: {best_post.title}, Превью: {best_post.preview()}'))

        # Вывод всех комментариев к лучшей статье
        comments = best_post.comments.all()
        for comment in comments:
            self.stdout.write(self.style.SUCCESS(f'Дата: {comment.created_at}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Текст: {comment.text}'))
