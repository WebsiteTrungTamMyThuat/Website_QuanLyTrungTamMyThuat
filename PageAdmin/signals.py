from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import NhanVien

@receiver(post_save, sender=User)
def create_nhanvien_for_user(sender, instance, created, **kwargs):
    if created:
        # Tạo bản ghi trong bảng NhanVien khi tạo user mới
        NhanVien.objects.create(
            manv=instance.username, 
            hoten=instance.first_name + ' ' + instance.last_name, 
            gioitinh='',
            ngaysinh=None, 
            diachi='', 
            sdt='', 
            user_id=instance.id  
        )
        
@receiver(post_save, sender=User)
def update_nhanvien_for_user(sender, instance, created, **kwargs):
    try:
        # Kiểm tra xem nhân viên đã tồn tại với user_id không
        nhanvien = NhanVien.objects.get(user_id=instance.id)

        # Cập nhật tất cả các trường thông tin trong NhanVien từ User
        nhanvien.hoten = instance.last_name + ' ' + instance.first_name
        nhanvien.email = instance.email

        # Lưu thay đổi vào cơ sở dữ liệu
        nhanvien.save()
    except NhanVien.DoesNotExist:
        pass 
        
@receiver(post_delete, sender=User)
def delete_nhanvien_for_user(sender, instance, **kwargs):
    # Xóa bản ghi trong bảng NhanVien khi xóa user
    try:
        nhanvien = NhanVien.objects.get(user_id=instance.id)
        nhanvien.delete()
    except NhanVien.DoesNotExist:
        pass