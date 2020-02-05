from django.db import models


class Item(models.Model):
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class BookShelf(Item):
    GENDER_CHOICES = (("M", "남성"), ("F", "여성"), ("N", "공개하지 않음"))
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default="내 책장")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="N")
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{} # {}".format(self.name, self.owner.email)


class MyBook(Item):
    bookshelf = models.ForeignKey(BookShelf, on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    current_page = models.IntegerField(default=0)
    total_page = models.IntegerField(blank=True)
    star = models.IntegerField()

    def __str__(self):
        return self.book.name


class Memo(Item):
    book = models.ForeignKey(MyBook, on_delete=models.CASCADE)
    page = models.IntegerField(default=0)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, default="")

    def __str__(self):
        return self.subject
