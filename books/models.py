from django.db import models

class Genre(models.TextChoices):
    FANTASY = 'Fantasy'
    ROMANCE = 'Romance'
    SCIENCE_FICTION = 'Science Fiction'
    HORROR = 'Horror'
    MYSTERY = 'Mystery'
    ADVENTURE = 'Adventure'
    BIOGRAPHY = 'Biography'
    CLASSICS = 'Classics'
    DRAMA = 'Drama'
    FAMILY = 'Family'
    HISTORY = 'History'
    HISTORY_FICTION = 'History Fiction'
    LITERARY_FICTION = 'Literary Fiction'
    MUSICAL = 'Musical'
    RELIGION = 'Religion'
    SATIRE = 'Satire'
    SOCIETY = 'Society'
    THRILLER = 'Thriller'
    WESTERN = 'Western'
    UNDEFINED = 'Undefined'

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    genre = models.CharField(choices=Genre.choices, default=Genre.UNDEFINED, max_length=50)
    pages = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    amount = models.IntegerField()
    book_cover = models.TextField()
    loans = models.ManyToManyField("users.User", through="Loan", related_name='loans')
    followers = models.ManyToManyField("users.User", through="Follow", related_name='following')
    
class Loan(models.Model):
    book =  models.ForeignKey('books.Book', on_delete=models.CASCADE)
    user =  models.ForeignKey('users.User', on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    returned = models.BooleanField(default=False)

class Follow(models.Model):
    book =  models.ForeignKey('books.Book', on_delete=models.CASCADE)
    user =  models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
