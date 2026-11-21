# Team

## Thông tin nhóm

- Tên nhóm: DTL
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY13-DTL-LaunchEconomics` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/tuanvtxm6/K5-L3A-DAY13-DTL-LaunchEconomics, nhánh `main`, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |    Lục Anh Tuấn    |   2A202603634   |    26ai.tuanla2@vinuni.edu.vn   |    tuanvtxm6    |    Người viết code     |
|   2 |    Nguyễn Thùy Lam    |   2A202603632   |    26ai.lamnt5@vinuni.edu.vn  |  ThuyLam4719      |     Người gán nhãn 1   |
|   3 |    Mai Lâm Tấn Đạt    |   2A202603645   |   26ai.datmlt@vinuni.edu.vn    |    tandat411    |     Người kiểm số, người gán nhãn 2, kiêm giữ hồ sơ    |
|   4 |        |      |       |        |         |

Bốn vai của lab:

- **Người viết code:** viết và chạy `src/lab13.py`.
- **Người kiểm số:** tính tay một con số để đối chiếu, điền bảng.
- **Người gắn nhãn 1:** đọc đề, theo dõi điều kiện "Xong khi"; gắn nhãn 20 ca độc lập ở CP3.
- **Người gắn nhãn 2, kiêm giữ hồ sơ:** điền `report/team/ho_so_launch_v0.md` từ đầu buổi; gắn nhãn 20 ca độc lập ở CP3.

Đổi người viết code sau giờ giải lao, để ít nhất hai người trong nhóm tự tay tính được chi phí.

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## LucAnhTuan-2A202603634

### Phần việc phụ trách

- Người viết code: `src/lab13.py` cho nhiệm vụ A, B và D1; số trong `report/team/bang_chi_phi.md`.
- Nhiệm vụ D: `report/team/pilot_plan.yaml`; chốt mục 6 và đề xuất của `report/team/ho_so_launch_v0.md`; viết `report/team/group_report.md`.

### Đóng góp cụ thể

- Ba hàm A1 (ba phép thử ĐẠT), hàm `mo_hinh` (A2), tách theo loại (A3), chi phí cố định (A4), bảng độ nhạy B1–B4, cỡ mẫu D1.
- `pilot_plan.yaml`: chia theo nhân viên 20/20, MDE 6 điểm (859/nhóm, DE 6,96), năm câu D2, 4 luật dừng NẾU – TRONG – THÌ – KHÔNG THÌ, ngày quyết định 2027-01-12.

### Bằng chứng

- `src/lab13.py`, `report/team/bang_chi_phi.md`, `report/team/pilot_plan.yaml`, `report/team/group_report.md`, `report/team/2A202603634_LucAnhTuan.md`; chi phí mỗi việc thành công 4.472 đ [simulated].

## NguyenThuyLam-2A202603632

### Phần việc phụ trách

- Người gắn nhãn 1: gắn nhãn 20 ca lỗi theo năm loại Google PAIR, theo dõi điều kiện "Xong khi" của CP3, soạn bảng khắc phục 5 ca trong `report/team/bang_loi.md`.
- Soạn bản nháp đầu tiên của `report/team/ho_so_launch_v0.md`, sau đó bàn giao cho người giữ hồ sơ (Đạt).

### Đóng góp cụ thể

- Bộ nhãn người 1 cho 20 ca và bảng khắc phục đủ năm loại (ca 9, 7, 18, 4, 17) trong `report/team/bang_loi.md`; Lam đã xác nhận bộ nhãn. Tỉ lệ đồng thuận với người 2: 20/20.
- Đề xuất bộ nhãn người 1 được tạo bằng AI theo ý kiến mới của giảng viên mà nhóm báo lại; Lam rà soát/xác nhận trước khi chốt.
- Bản nháp hồ sơ launch v0 với số đối chiếu và nhãn simulated.

### Bằng chứng

- `report/team/bang_loi.md`, `report/team/ho_so_launch_v0.md`, `report/team/2A202603632_NguyenThuyLam.md`.

## MaiLamTanDat-2A202603645

### Phần việc phụ trách

- Người kiểm số: tính lại độc lập số của CP1, CP2, D1 và E1; ghi cách tính tay vào `report/team/bang_chi_phi.md`.
- Người gắn nhãn 2: gắn nhãn 20 ca ở CP3; đồng thuận với Lam 20/20.
- Người giữ hồ sơ: điền `report/team/chi_so.md` và cập nhật `report/team/ho_so_launch_v0.md`.

### Đóng góp cụ thể

- Kiểm số độc lập bằng script không dùng `lab13.py`: A2, A3, A4, B1–B4 khớp bản của Tuấn (chi phí mỗi việc thành công 4.472 đ [simulated]); D1 khớp (1.251; m ≥ 299; power ≈ 0,64); E1 khớp (82,83% · 27,12% · 4,25%).
- Điền `chi_so.md`: ba chỉ số tính thử, hai chỉ số nhóm đề xuất, 8 event có `trace_id`, ba dòng rủi ro kinh tế lấy từ bảng độ nhạy.
- Cập nhật `ho_so_launch_v0.md`: tên nhóm và lớp, mục 4, số 12.415 đ ở mục 7.

### Bằng chứng

- `report/team/bang_chi_phi.md` (mục "Kiểm số độc lập"), `report/team/chi_so.md`, `report/team/ho_so_launch_v0.md`, `report/team/2A202603645_MaiLamTanDat.md`.
