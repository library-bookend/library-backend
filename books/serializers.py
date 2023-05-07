from rest_framework import serializers
from .models import Book
from copies.models import Copy


class BookSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        isbn = validated_data.get("isbn")
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            validated_data["copies_amount"] = 1
            book = Book.objects.create(**validated_data)
            Copy.objects.create(book=book)
            book.copies_amount = 1
            book.save()
        else:
            Copy.objects.create(book=book)
            book.copies_amount += 1
            book.save()
        return book

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "author",
            "pages",
            "isbn",
            "copies_amount",
            "book_cover",
            "followers"
        ]
        depth = 2
        read_only_fields = ["copies_amount", "followers"]
