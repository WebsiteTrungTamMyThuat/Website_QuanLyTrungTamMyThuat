

document.addEventListener("DOMContentLoaded", () => {
    // Lấy mã tài khoản từ session được truyền từ Django
    const mahv = idtaikhoan.trim(); 
    fetchTimetable(mahv);
});

let currentWeekIndex = 0;



function generateTimetable(weekIndex) {

    // Tính ngày đầu tuần và cuối tuần
    const startOfWeek = getStartOfWeek(new Date(), weekIndex);
    const endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(startOfWeek.getDate() + 7);

    const contentContainer = document.querySelector(".timetable .content");
    const weekNamesContainer = document.querySelector(".timetable .week-names");

    // Xóa nội dung cũ
    contentContainer.innerHTML = "";
    weekNamesContainer.innerHTML = "";

    // Tạo tiêu đề các ngày trong tuần
    for (let i = 0; i < 7; i++) {
        const date = new Date(startOfWeek);
        date.setDate(startOfWeek.getDate() + i);
        const dayDiv = document.createElement("div");
        dayDiv.textContent = formatDate(date);
        weekNamesContainer.appendChild(dayDiv);

        const dayContent = document.createElement("div");
        dayContent.classList.add("day-cell");
        dayContent.dataset.date = formatDate(date);
        contentContainer.appendChild(dayContent);
    }

    // Lọc các lớp học trong tuần hiện tại
    const currentWeekClasses = weeksData.filter(event => {
        const classDate = new Date(event.date);
        return classDate >= startOfWeek && classDate < endOfWeek;
    });

    // Hiển thị lịch học cho tuần hiện tại
    currentWeekClasses.forEach(event => {
        const classDate = formatDate(new Date(event.date));

        // Tìm ô tương ứng với ngày
        const targetCell = contentContainer.querySelector(`.day-cell[data-date="${classDate}"]`);

        if (targetCell) {
            // Tạo nội dung lịch học
            const eventDiv = document.createElement("div");
            eventDiv.innerHTML = `
                <div class="accent-${event.color}-gradient">
                    <div class="course">
                        <div class="className">${event.className}</div>
                        <div class="location">Phòng: ${event.room}</div>
                        <div class="startTime">Bắt đầu: ${event.startTime}</div>
                        <div class="totalTime">Thời lượng: ${event.totalTime}</div>
                    </div>
                </div>
            `;

            // Thêm lịch học vào ô tương ứng
            targetCell.appendChild(eventDiv);
        }
    });
}

// Hàm định dạng ngày
function formatDate(date) {
    const day = date.getDate().toString().padStart(2, "0");
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const year = date.getFullYear();
    return `${year}-${month}-${day}`;
}

function generateTimeIntervals() {
    const timeIntervalContainer = document.getElementById("time-interval-container");
    timeIntervalContainer.innerHTML = ""; // Xóa nội dung cũ

    const intervals = [
        "7:00 - 9:00", "9:30 - 11:30", "1:00 - 3:00", 
        "3:30 - 5:30", "6:00 - 8:00"
    ];

    // Tạo các khung giờ
    intervals.forEach(interval => {
        const div = document.createElement("div");
        div.textContent = interval;
        timeIntervalContainer.appendChild(div);
    });
}

// Hàm thay đổi tuần
function changeWeek(direction) {
    currentWeekIndex += direction;
    console.log("Chuyển đến tuần:", currentWeekIndex);
    generateTimetable(currentWeekIndex);
}

// Hàm lấy ngày đầu tuần
function getStartOfWeek(currentDate, weekOffset) {
    const date = new Date(currentDate);
    const day = date.getDay();
    const diffToMonday = day === 0 ? -6 : 1 - day; // Đưa về thứ Hai (1)
    date.setDate(date.getDate() + diffToMonday + weekOffset * 7);
    return new Date(date.getFullYear(), date.getMonth(), date.getDate()); // Reset giờ phút
}
// Khởi tạo thời khóa biểu
document.addEventListener("DOMContentLoaded", () => {
    generateTimetable(currentWeekIndex);
});