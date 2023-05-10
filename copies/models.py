from django.db import models


class Copy(models.Model):
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    loans = models.ManyToManyField("users.User", through="Loan", related_name="loans")


class Loan(models.Model):
    copy = models.ForeignKey("copies.Copy", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    returned = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
