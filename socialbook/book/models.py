import uuid

from django.db import models

# Create your models here.
#book
#auther
#publisher
#publication date
# so every book will have one auther or more and one publisher but auther and publisher can have many books
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    publisher = models.CharField(max_length=255)
    authors = models.   #list of authors as comma separated string
    def __str__(self):
        return self.title
class Author(models.Model):
    id = models.uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class Publisher(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('book', 'author')
class BookPublisher(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('book', 'publisher')
