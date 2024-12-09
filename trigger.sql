drop trigger trg_create_weekly_schedule
Drop FUNCTION create_weekly_schedule()

CREATE OR REPLACE FUNCTION create_weekly_schedule()
RETURNS TRIGGER AS $$
DECLARE
    total_hours INT;       -- Tổng số giờ học của lớp (biến PL/pgSQL)
    ngayhoc_next DATE;     -- Ngày học kế tiếp (biến PL/pgSQL)
    sogiohoc INT;          -- Số giờ học mỗi buổi
    so_buoi_hoc INT;       -- Tổng số buổi học cần tạo
    count_buoi INT;        -- Đếm số buổi học đã tạo
BEGIN
    -- Kiểm tra xem đây có phải lịch học đầu tiên hay không
    IF NOT EXISTS (
        SELECT 1
        FROM LichHoc
        WHERE malop = NEW.malop AND ngayhoc < NEW.ngayhoc
    ) THEN
        -- Lấy thông tin lớp học
        SELECT tonggiohoc, ngaybatdau
        INTO total_hours, ngayhoc_next
        FROM LopHoc
        WHERE malop = NEW.malop;

        -- Số giờ học mỗi buổi lấy từ lịch học đầu tiên
        sogiohoc := NEW.sogiohoc;

        -- Tính số buổi học cần thiết
        IF sogiohoc = 0 THEN
            RAISE EXCEPTION 'Số giờ học mỗi buổi không thể bằng 0';
        END IF;

        so_buoi_hoc := CEIL(total_hours / sogiohoc);

        -- Bắt đầu tạo lịch học (kế tiếp hàng tuần)
        count_buoi := 1; -- Bắt đầu từ buổi đầu tiên (đã được thêm)
        WHILE count_buoi < so_buoi_hoc LOOP
            -- Tăng ngày học lên 1 tuần
            ngayhoc_next := ngayhoc_next + INTERVAL '1 week';  -- Dùng biến ngayhoc_next để tính ngày kế tiếp

            -- Thêm bản ghi lịch học mới
            INSERT INTO LichHoc (malop, ngayhoc, giohoc, sogiohoc)
            VALUES (NEW.malop, ngayhoc_next, NEW.giohoc, sogiohoc);

            count_buoi := count_buoi + 1; -- Đếm buổi học
        END LOOP;
    END IF;

    RETURN NEW; -- Kết thúc trigger
END;
$$ LANGUAGE plpgsql;






CREATE TRIGGER trg_create_weekly_schedule
AFTER INSERT ON LichHoc
FOR EACH ROW
EXECUTE FUNCTION create_weekly_schedule();

