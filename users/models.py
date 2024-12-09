from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL


class Agent(models.Model):
    agent_id = models.CharField(primary_key=True, max_length=50)
    agent_first_name = models.CharField(max_length=100, blank=True, null=True)
    agent_last_name = models.CharField(max_length=100, blank=True, null=True)
    agent_phone_nb = models.CharField(max_length=20, blank=True, null=True)
    agent_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agent'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Books(models.Model):
    # Changed 'user' field to reference settings.AUTH_USER_MODEL for compatibility with the built-in custom user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    agent = models.ForeignKey('Agent', models.DO_NOTHING)
    package = models.ForeignKey('Package', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books'
        unique_together = (('user', 'agent', 'package'),)


class Branch(models.Model):
    agent = models.OneToOneField(Agent, models.DO_NOTHING, primary_key=True)
    branch_nb = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    branch_phone = models.CharField(max_length=20, blank=True, null=True)
    branch_country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    # Changed 'user' field to reference settings.AUTH_USER_MODEL for compatibility with the built-in custom user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class Flight(models.Model):
    flight_id = models.CharField(primary_key=True, max_length=50)
    flight_number = models.CharField(max_length=50, blank=True, null=True)
    start_city = models.CharField(max_length=100, blank=True, null=True)
    end_city = models.CharField(max_length=100, blank=True, null=True)
    takeoff_time = models.TimeField(blank=True, null=True)
    landing_time = models.TimeField(blank=True, null=True)
    flight_date = models.DateField(blank=True, null=True)
    flight_class = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flight'


class FlightBooking(models.Model):
    # Changed 'user' field to reference settings.AUTH_USER_MODEL for compatibility with the built-in custom user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'flight_booking'
        unique_together = (('user', 'flight'),)


class Hotel(models.Model):
    hotel_id = models.CharField(primary_key=True, max_length=50)
    start_stay = models.DateField(blank=True, null=True)
    end_stay = models.DateField(blank=True, null=True)
    hotel_city = models.CharField(max_length=100, blank=True, null=True)
    room_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel'


class HotelBooking(models.Model):
    # Changed 'user' field to reference settings.AUTH_USER_MODEL for compatibility with the built-in custom user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel_booking'
        unique_together = (('user', 'hotel'),)


class Package(models.Model):
    package_id = models.CharField(primary_key=True, max_length=50)
    pkg_start_date = models.DateField(blank=True, null=True)
    pkg_end_date = models.DateField(blank=True, null=True)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pkg_destination = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package'


class PackageFlight(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'package_flight'
        unique_together = (('flight', 'package'),)


class PackageHotel(models.Model):
    hotel = models.OneToOneField(Hotel, models.DO_NOTHING, primary_key=True)
    package = models.ForeignKey(Package, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'package_hotel'
        unique_together = (('hotel', 'package'),)
