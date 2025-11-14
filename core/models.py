from django.db import models
from ckeditor.fields import RichTextField


class Partner(models.Model):
    """Partner organisation whose logo shows on the home page."""

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="partners/")
    website_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Testimonial(models.Model):
    """Testimonials from parents, students or schools."""

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True, help_text="Parent, School Administrator, Student, etc.")
    message = models.TextField()
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        if self.role:
            return f"{self.name} - {self.role}"
        return self.name


class PartnershipApplication(models.Model):
    """Partnership applications from schools."""
    
    CLASS_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('both', 'Both'),
    ]
    
    school_name = models.CharField(max_length=255)
    school_address = models.TextField()
    school_phone = models.CharField(max_length=20)
    school_email = models.EmailField()
    class_type = models.CharField(max_length=10, choices=CLASS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.school_name} - {self.get_class_type_display()}"


class Branch(models.Model):
    """Physical branches for offline programs."""
    name = models.CharField(max_length=255)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Branches"
    
    def __str__(self) -> str:
        return self.name


class Program(models.Model):
    """Educational programs offered."""
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    image = models.ImageField(upload_to="programs/")
    syllabus = models.FileField(upload_to="syllabi/", blank=True, null=True)
    price_online_6weeks = models.DecimalField(max_digits=10, decimal_places=2)
    price_online_12weeks = models.DecimalField(max_digits=10, decimal_places=2)
    price_offline_6weeks = models.DecimalField(max_digits=10, decimal_places=2)
    price_offline_12weeks = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return self.title


class ProgramRegistration(models.Model):
    """Program registrations from users."""
    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    DURATION_CHOICES = [
        ('6weeks', '6 Weeks'),
        ('12weeks', '12 Weeks'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    participants = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.program.title}"


class ContactMessage(models.Model):
    """Contact form submissions."""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.name} - {self.subject}"


class CareerApplication(models.Model):
    """Career applications from professionals."""
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=255)
    cv = models.FileField(upload_to="careers/cv/")
    passport = models.ImageField(upload_to="careers/passport/")
    application_letter = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.full_name} - {self.position}"