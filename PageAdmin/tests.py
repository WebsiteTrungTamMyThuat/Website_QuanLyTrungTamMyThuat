from django.test import TestCase
from .models import GiaoVien
# Create your tests here.

class GiaoVienTestCase(TestCase):
    def test_danh_sach_giao_vien(self):
        
        # Lấy tất cả giáo viên
        dsgv = GiaoVien.objects.all()
        print(dsgv.query)

        # Kiểm tra số lượng giáo viên
        self.assertEqual(dsgv.count(), 1)