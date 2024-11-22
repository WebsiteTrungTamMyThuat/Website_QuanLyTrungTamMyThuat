from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import NhanVien, TaiKhoanNhanVien

@receiver(post_save, sender=User)
def create_nhanvien_for_user(sender, instance, created, **kwargs):
    if created:
        # Tạo bản ghi trong bảng NhanVien khi tạo user mới
        NhanVien.objects.create(
            manv=instance.username,  # Giả sử manv là username trong auth_user
            hoten=instance.first_name + ' ' + instance.last_name,  # Tạo họ tên từ first_name và last_name
            gioitinh='',  # Thêm giá trị mặc định nếu cần
            ngaysinh=None,  # Thêm giá trị mặc định nếu cần
            diachi='',  # Thêm giá trị mặc định nếu cần
            sdt='',  # Thêm giá trị mặc định nếu cần
            user_id=instance.id  # Liên kết với user_id trong bảng NhanVien
        )
        
@receiver(post_save, sender=User)
def update_nhanvien_for_user(sender, instance, created, **kwargs):
    try:
        # Kiểm tra xem nhân viên đã tồn tại với user_id không
        nhanvien = NhanVien.objects.get(user_id=instance.id)

        # Cập nhật tất cả các trường thông tin trong NhanVien từ User
        nhanvien.hoten = instance.first_name + ' ' + instance.last_name
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