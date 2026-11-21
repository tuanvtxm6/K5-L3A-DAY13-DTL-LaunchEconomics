# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: DTL
- Lớp: L3A
- Thành viên: xem `TEAM.md` (3 người: Lục Anh Tuấn, Nguyễn Thùy Lam, Mai Lâm Tấn Đạt)

## 2. Mục tiêu và cách tiếp cận

Dựng hồ sơ launch v0 cho trợ lý hoàn phí LogiX-VN để hội đồng Gate 2a quyết định có cho chạy pilot hay không. Nhóm đi theo thứ tự A → E, mỗi nhiệm vụ dùng lại số của nhiệm vụ trước: tính chi phí thật từ trace, tìm yếu tố nhạy nhất, phân loại lỗi, rồi mới thiết kế pilot và chỉ số. Mọi số do `src/lab13.py` tính và được người kiểm số tính lại bằng script độc lập.

## 3. Giải pháp

- **A · Chi phí** ([bang_chi_phi.md](bang_chi_phi.md)): hàm `mo_hinh` cộng token + tool trên mọi lần chạy (kể cả lỗi) cùng tiền xem lại và làm lại, chia cho số việc thành công; tách theo `loai`; cộng chi phí cố định 40 triệu đ/tháng.
- **B · Độ nhạy** ([bang_chi_phi.md](bang_chi_phi.md)): gọi lại `mo_hinh` với 9 kịch bản, một cặp, giới hạn 1/2/3 lần chạy và kịch bản xem lại 100%.
- **C · Bảng lỗi** ([bang_loi.md](bang_loi.md)): hai người gắn nhãn 20 ca theo năm loại Google PAIR, so nhãn, chọn 5 ca đủ năm loại để gán cách khắc phục.
- **D · Pilot** ([pilot_plan.yaml](pilot_plan.yaml)): tính đủ năm câu D1 trước, rồi so ba cách chia (yêu cầu, nhân viên, depot) trước khi chọn.
- **E · Chỉ số và hồ sơ** ([chi_so.md](chi_so.md), [ho_so_launch_v0.md](ho_so_launch_v0.md)): tính thử ba chỉ số, liệt kê 8 event có `trace_id`, lấy rủi ro kinh tế từ bảng độ nhạy, ghép thành hồ sơ bảy mục.

## 4. Kết quả

- Chi phí mỗi việc thành công **4.472 đ** [simulated], gấp 16,3 lần hoá đơn token chia số yêu cầu; giờ nhân viên chiếm 92,5% [simulated]. Cả hệ thống 5.865 đ/yêu cầu = 0,49× của 12.000 đ [simulated].
- quoc_te 1,88× và chạy lại không giúp (lần 3 chỉ đúng 2,2%) → phạm vi pilot chỉ noi_dia (0,22×) + hang_nang (0,69×) [simulated].
- Yếu tố nhạy nhất: số ca làm lại (+51,8%), tỉ lệ xem lại (+40,7%), lương (+23,1%) [simulated]. Giới hạn 2 lần chạy rẻ nhất cho cả hệ thống (6.901.220 đ) [simulated].
- Xem lại 100%: 11.743 đ = 0,98× (12.415 đ = 1,03× nếu làm lại 15,3 phút) [simulated].
- Bảng lỗi: đồng thuận 20/20. Chỉ số trong đợt chạy thử: chính 82,83%, bỏ qua gợi ý 27,12%, mở lại 7 ngày 4,25%.
- Pilot: chia theo nhân viên 20/20, MDE 6 điểm (859/nhóm, m ≥ 299, power 0,64 ở mức 5 điểm), 4 luật dừng, quyết định 2027-01-12.
- **Đề xuất cuối: Go có điều kiện** cho pilot noi_dia + hang_nang, kèm các điều kiện có người phụ trách và ngày kiểm tra.

**Duyệt chéo · hội đồng là nhóm WhatEver.** Điểm và quyết định của hội đồng: điền khi nhận phiếu. Năm câu hỏi nhận được và cách nhóm xử lý:

| Câu hỏi của hội đồng | Nhóm trả lời / đã sửa |
| --- | --- |
| Bằng chứng hai người gắn nhãn độc lập (20/20), và ca 8 thuộc loại nào | Ca 8 là Hệ thống: trợ lý viện dẫn điều khoản không tồn tại là vi phạm chính sách; trích dẫn đã lộ ra nên không phải Ngầm. Git không chứng minh được độc lập (nhãn 1 push 15:27, nhãn 2 push 16:02); bằng chứng nhóm có là lý do phân loại riêng của người 2 cho từng ca |
| Ngưỡng ≤ 5 phút có còn hoà vốn khi làm lại 15,3 phút | Không: hoà vốn là 4,8 phút; ở 5 phút chi phí 12.415 đ = 1,03× [simulated]. Đã hạ ngưỡng điều kiện (4) và luật dừng 4 xuống 4,8 phút |
| Event nào bắt lỗi ngầm như ca 5, 17 | Bản đầu không có: đối soát sổ cái chỉ so với số đã duyệt, mà ở ca 5, 17 số duyệt đã sai. Đã thêm event thứ 9 `audit_sample_checked` (kiểm tra mẫu 100 đơn/tuần, ngưỡng 1%) và tách chỉ số an toàn thành hai |
| Event kiểm tra 14/12 mà bắt đầu 07/12 | Tuần đầu không dùng cho chỉ số chính nhưng thiếu event thì không theo dõi được luật dừng an toàn. Đã tách điều kiện: event kiểm tra 04/12, trước ngày bắt đầu; Giám đốc vận hành có quyền không cho bắt đầu |
| Chi phí cố định ở khối lượng thật của pilot | 0,38× chỉ đúng khi cả 40 người dùng. Đã thêm vào `lab13.py`: 1,27× (4 người), 0,68× (10 người), 0,48× (20 người) [simulated]; luật dừng chi phí 8.000 đ ghi rõ chưa cộng cố định |

## 5. Khó khăn và cách xử lý

- **Cài đặt trên máy Windows của Tuấn (người viết code):** lệnh `py -3 -m venv .venv` trong README báo lỗi vì máy không có Python launcher `py`. Đã dùng `python -m venv .venv` (Python 3.13.5 của Miniconda) rồi cài `requirements.txt`; kiểm tra in `san sang`.
- **Nhóm chỉ có 3 người cho 4 vai:** ban đầu một người nhận cả hai vai gắn nhãn, không đáp ứng yêu cầu gắn nhãn độc lập của CP3. Đã chia lại: Lam gắn nhãn 1, Đạt kiêm kiểm số, gắn nhãn 2 và giữ hồ sơ.
- **Đợt chạy thử chỉ có 20 nhân viên ở 6 depot**, không đủ để chia 20 + 20; bản đầu của `pilot_plan.yaml` ghi nhầm phạm vi "6 depot đã chạy thử". Người kiểm số phát hiện khi soát chéo; đã sửa thành cả 12 depot (40 nhân viên), bốc thăm phân tầng theo depot.
- **Không đủ mẫu cho mức chênh 5 điểm:** với 40 nhân viên, cách chia theo cụm tốt nhất chỉ đạt tối đa 1.000 < 1.251. Nhóm chấp nhận MDE 6 điểm và ghi rõ power 0,64 trong hồ sơ.
- **File mẫu báo cáo cá nhân bị xoá nhầm** khi tạo báo cáo riêng; đã khôi phục `MSSV_HoTen.md` từ lịch sử git.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md`.

| Thành viên | Vai | Phần chính |
| --- | --- | --- |
| Lục Anh Tuấn | Người viết code | `src/lab13.py` (A, B, D1), `bang_chi_phi.md`, `pilot_plan.yaml`, `group_report.md` |
| Nguyễn Thùy Lam | Người gắn nhãn 1 | Nhãn người 1 và bảng khắc phục trong `bang_loi.md`, bản nháp `ho_so_launch_v0.md` |
| Mai Lâm Tấn Đạt | Người kiểm số, gắn nhãn 2, giữ hồ sơ | Kiểm số độc lập, nhãn người 2, `chi_so.md`, cập nhật `ho_so_launch_v0.md` |

## 7. Hạn chế và hướng cải thiện

- Chi phí phụ thuộc hai cột phút simulated (92,5% tổng chi phí); kết luận có thể đổi khi có phút đo thật, nên pilot phải đo `phut_xem_lai` và `phut_lam_lai` thật từ tuần 1.
- Đợt chạy thử không có đối chứng, nên ba chỉ số E1 chỉ mô tả đợt chạy thử, chưa nói được tác động của trợ lý.
- MDE 6 điểm làm pilot có khoảng 1/3 khả năng bỏ sót tác động thật 5 điểm. Pilot đã dùng cả 40 nhân viên của 12 depot nên không thể thêm cụm; chỉ có thể kéo dài thời gian đo hoặc chạy lại một đợt pilot thứ hai rồi gộp kết quả.
- Nhóm thiếu một người nên không đổi người viết code sau giờ giải lao như hướng dẫn; bù lại bằng kiểm số độc lập cho mọi bảng A, B, D1, E1.
- Không có bằng chứng kỹ thuật cho việc hai người gắn nhãn độc lập (hội đồng hỏi). Lần sau mỗi người nộp nhãn riêng (commit hoặc file khoá) trước khi xem nhãn của người kia.
- Bốn chỗ yếu do hội đồng chỉ ra (ngưỡng hoà vốn, event lỗi ngầm, ngày kiểm tra event, chi phí cố định ở khối lượng pilot) đã sửa sau duyệt chéo; xem bảng ở mục 4.

## 8. Tài liệu tham khảo

- Erol và cộng sự, *Cost-of-Pass: An Economic Framework for Evaluating Language Models*, arxiv.org/abs/2504.13359
- Google PAIR, *People + AI Guidebook*, chương "Errors + Graceful Failure", pair.withgoogle.com
- Tài liệu statsmodels, `NormalIndPower` và `proportion_effectsize` (mục `stats.power`)
- Tài liệu lab: `docs/du_lieu_va_cong_thuc.md`, `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`
- Công cụ AI: Claude Code (hỗ trợ viết code và soạn hồ sơ); khai chi tiết trong báo cáo cá nhân
