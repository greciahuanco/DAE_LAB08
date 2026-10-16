from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AuthorProfile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name="profile")
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to="authors/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Author Profile"
        verbose_name_plural = "Author Profiles"

    def __str__(self):
        return f"Profile of {self.author}"


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Publication(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    publication_date = models.DateField()
    edition = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ["-publication_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["book", "publisher", "edition"],
                name="unique_book_publisher_edition"
            )
        ]

    def __str__(self):
        return f"{self.book.title} - {self.publisher.name} (Ed. {self.edition})"


class Book(models.Model):
    title = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13, unique=True)
    summary = models.TextField(blank=True)
    publication_date = models.DateField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    cover = models.ImageField(upload_to="covers/", null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    categories = models.ManyToManyField(Category, related_name="books", blank=True)
    publishers = models.ManyToManyField(Publisher, through="Publication", related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]

    def __str__(self):
        return self.title