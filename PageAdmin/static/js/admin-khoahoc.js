const weeksData = [
    [
        { date: "2024-11-20", time: "8:00 - 10:00", className: "Hội họa cơ bản", room: "Phòng Mỹ thuật 1", startTime: "8:00", totalTime: "2h", color: "orange" },
        { date: "2024-11-21", time: "10:00 - 12:00", className: "Lịch sử nghệ thuật", room: "Phòng Mỹ thuật 2", startTime: "10:00", totalTime: "2h", color: "purple" },
        { date: "2024-11-22", time: "14:00 - 16:00", className: "Điêu khắc", room: "Phòng Mỹ thuật 3", startTime: "14:00", totalTime: "2h", color: "green" },
        { date: "2024-11-24", time: "16:00 - 18:00", className: "Thiết kế đồ họa", room: "Phòng Máy tính", startTime: "16:00", totalTime: "2h", color: "cyan" },
    ],
    [
        { date: "2024-11-27", time: "10:00 - 12:00", className: "Hội họa nâng cao", room: "Phòng Mỹ thuật 1", startTime: "10:00", totalTime: "2h", color: "pink" },
        { date: "2024-11-28", time: "12:00 - 14:00", className: "Kỹ thuật tô màu nước", room: "Phòng Mỹ thuật 2", startTime: "12:00", totalTime: "2h", color: "blue" },
        { date: "2024-11-29", time: "8:00 - 10:00", className: "Thiết kế poster", room: "Phòng Thiết kế", startTime: "8:00", totalTime: "2h", color: "purple" },
        { date: "2024-11-30", time: "14:00 - 16:00", className: "Nghệ thuật hiện đại", room: "Phòng Hội thảo", startTime: "14:00", totalTime: "2h", color: "orange" },
    ],
    [
        { date: "2024-12-04", time: "8:00 - 10:00", className: "Phác thảo chân dung", room: "Phòng Mỹ thuật 3", startTime: "8:00", totalTime: "2h", color: "green" },
        { date: "2024-12-05", time: "10:00 - 12:00", className: "Lịch sử mỹ thuật Việt Nam", room: "Phòng Mỹ thuật 2", startTime: "10:00", totalTime: "2h", color: "blue" },
        { date: "2024-12-06", time: "16:00 - 18:00", className: "Thiết kế logo", room: "Phòng Máy tính", startTime: "16:00", totalTime: "2h", color: "cyan" },
        { date: "2024-12-07", time: "18:00 - 20:00", className: "Nghệ thuật tranh tường", room: "Phòng Mỹ thuật 1", startTime: "18:00", totalTime: "2h", color: "pink" },
    ],
];

let currentWeekIndex = 0;

function generateTimetable(weekIndex) {
    const startOfWeek = getStartOfWeek(new Date(), weekIndex);
    const contentContainer = document.querySelector(".timetable .content");
    const weekNamesContainer = document.querySelector(".timetable .week-names");

    // Cập nhật tiêu đề tuần
    const endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(startOfWeek.getDate() + 6);
    document.getElementById("current-week-label").innerText = `Tuần ${weekIndex + 1} (${formatDate(startOfWeek)} - ${formatDate(endOfWeek)})`;

    // Xóa nội dung cũ
    contentContainer.innerHTML = "";
    weekNamesContainer.innerHTML = "";

    // Tạo tiêu đề ngày trong tuần
    for (let i = 0; i < 7; i++) {
        const date = new Date(startOfWeek);
        date.setDate(startOfWeek.getDate() + i);

        const dayDiv = document.createElement("div");
        dayDiv.textContent = formatDate(date);
        if (i === 5 || i === 6) dayDiv.classList.add("weekend");
        weekNamesContainer.appendChild(dayDiv);
    }

    // Tạo nội dung thời khóa biểu
    const weekData = weeksData[weekIndex] || [];
    for (let i = 0; i < 42; i++) { // 7 ngày x 6 khoảng thời gian
        const cell = document.createElement("div");

        const day = new Date(startOfWeek);
        day.setDate(startOfWeek.getDate() + (i % 7));
        const dateString = formatDate(day);
        const timeInterval = getTimeInterval(Math.floor(i / 7));

        const item = weekData.find((event) => event.date === dateString && event.time === timeInterval);
        if (item) {
            cell.innerHTML = `
                <div class="accent-${item.color}-gradient">
                    <div class="course">
                        <div class="className">${item.className}</div>
                        <div class="location"><label>Phòng học: </label>${item.room}</div>
                        <div class="startTime"><label>Thời gian: </label>${item.startTime}</div>
                        <div class="totalTime"><label>Tổng thời gian: </label>${item.totalTime}</div>
                    </div>
                </div>
            `;
        }
        contentContainer.appendChild(cell);
    }
}

// Hàm định dạng ngày
function formatDate(date) {
    const day = date.getDate().toString().padStart(2, "0");
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const year = date.getFullYear();
    return `${year}-${month}-${day}`;
}

// Hàm lấy khoảng thời gian
function getTimeInterval(index) {
    const intervals = [
        "8:00 - 10:00",
        "10:00 - 12:00",
        "12:00 - 14:00",
        "14:00 - 16:00",
        "16:00 - 18:00",
        "18:00 - 20:00",
    ];
    return intervals[index] || "";
}

// Hàm thay đổi tuần
function changeWeek(direction) {
    currentWeekIndex = Math.max(0, Math.min(currentWeekIndex + direction, weeksData.length - 1));
    generateTimetable(currentWeekIndex);
}

// Hàm lấy ngày đầu tuần
function getStartOfWeek(currentDate, weekOffset) {
    const date = new Date(currentDate);
    date.setDate(date.getDate() - date.getDay() + 1 + weekOffset * 7); // Bắt đầu từ thứ Hai
    return new Date(date.getFullYear(), date.getMonth(), date.getDate()); // Reset giờ phút
}

// Khởi tạo thời khóa biểu
document.addEventListener("DOMContentLoaded", () => {
    generateTimetable(currentWeekIndex);
});
