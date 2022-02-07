from django.db import models

#
# class Maintenance(models.Model):
#     issued_date = models.DateTimeField()
#     issue_reason = models.TextField()
#     cost = models.FloatField()
#     next_available_date = models.DateTimeField()
#     # created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     # created_at = models.DateTimeField(auto_now_add=True)
#     # changed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     # changed_at = models.DateTimeField(auto_now=True)
#
#
# class Expenses(models.Model):
#
#
#
# class Assets(models.Model):
#
#     # category types
#     PHOTOGRAPHY = 'ph'
#     VIDEOGRAPHY = 'vd'
#     ACCESSORIES = 'ac'
#     IT_EQUIPMENTS = 'it'
#     OTHER_MACHINES = 'om'
#     OTHER = 'ot'
#     NOT_DEFINED = 'nd'
#
#     # statuses
#     AVAILABLE = 'av'
#     NOT_AVAILABLE = 'na'
#     MAINTENANCE = 'ma'
#     REPAIR = 'rp'
#     RENTED = 'rt'
#
#     # category choices
#     CATEGORIES = [
#         (PHOTOGRAPHY, 'photography'),
#         (VIDEOGRAPHY, 'videography'),
#         (ACCESSORIES, 'accessories'),
#         (IT_EQUIPMENTS, 'IT equipments'),
#         (OTHER_MACHINES, 'other machines'),
#         (OTHER, 'other'),
#         (NOT_DEFINED, 'not defined')
#     ]
#
#     # statuses
#     STATUSES = [
#         (AVAILABLE, 'available'),
#         (NOT_AVAILABLE, 'not available'),
#         (MAINTENANCE, 'under maintenance'),
#         (REPAIR, 'under repair'),
#         (RENTED, 'rt')
#     ]
#
#     product_name = models.CharField(max_length=200)
#     brand = models.CharField(max_length=200, null=True, blank=True)
#     category = models.CharField(max_length=2, default='nd', choices=CATEGORIES)
#     owner = models.ForeighKey(get_user_model(), on_delete=models.CASCADE)
#     status = models.CharField(max_length=2, default='av', choices=STATUSES)
#
#     maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
#     description = models.TextField(blank=True, null=True)
#     created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     changed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     changed_at = models.DateTimeField(auto_now=True)
