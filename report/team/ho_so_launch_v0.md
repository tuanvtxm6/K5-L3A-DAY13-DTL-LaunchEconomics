# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Số tính bằng `src/lab13.py` và đã được người kiểm số tính lại độc lập (xem `bang_chi_phi.md`). Cột trạng thái chỉ dùng: Xong, có bằng chứng · Chưa · Giả lập. Mọi số tính từ cột phút `_simulated` có nhãn [simulated].

Nhóm: DTL · Lớp: L3A

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | 4.472 đ/việc thành công [simulated], gấp 16,3 lần hoá đơn token + tool chia số yêu cầu (274,7 đ); giờ nhân viên chiếm 92,5% [simulated] | Giả lập | Người kiểm số |
| 2 · Ba yếu tố nhạy nhất | 1. Số ca làm lại gấp đôi: +51,8% (6.787 đ) · 2. Tỉ lệ xem lại gấp đôi: +40,7% (6.292 đ) · 3. Lương tăng 25%: +23,1% (5.506 đ) [simulated]; giá token gấp đôi chỉ +5,6% | Giả lập | Người kiểm số |
| 3 · So với nhân viên tự làm | Cả hệ thống (cộng 222 ca nhân viên làm thay): 5.865 đ/yêu cầu = 0,49× của 12.000 đ [simulated]. Phạm vi noi_dia + hang_nang cộng cố định 40 triệu/tháng: 4.599 đ = 0,38× ở 45.000 yêu cầu/tháng, 5.784 đ = 0,48× nếu còn một nửa [simulated]. Ở khối lượng thật của pilot: 0,48× ở bước 20 người, 0,68× ở 10 người, 1,27× ở 4 người (đắt hơn nhân viên trong tuần đầu) [simulated]; 0,38× chỉ đúng khi cả 40 người dùng. quoc_te 1,88× nên bị loại [simulated] | Giả lập | Người kiểm số |
| 4 · Chỉ số chính, dùng, an toàn | Chỉ số trong đợt chạy thử (không có đối chứng, chưa suy ra tác động): chính 82,83% (994/1.200); bỏ qua gợi ý 27,12% (48/177); mở lại 7 ngày 4,25% (51/1.200). Thêm chỉ số dùng (tỉ lệ yêu cầu có mở gợi ý) và hai chỉ số an toàn: hoàn trùng hoặc sổ cái lệch (ngưỡng 0 ca), và sai số tiền qua kiểm tra mẫu 100 đơn/tuần để bắt lỗi ngầm như ca 5, 17 (ngưỡng 1%); 9 event có `trace_id` trong `chi_so.md` | Xong, có bằng chứng | Người gắn nhãn 2 kiêm giữ hồ sơ |
| 5 · Bảng lỗi và cách khắc phục | 20 ca thuộc 5 loại; hai bộ nhãn độc lập trùng 20/20 (100%); bảng khắc phục 5 ca đủ năm loại, mỗi dòng có cách phát hiện đo được và vai trò phụ trách | Xong, có bằng chứng | Người gắn nhãn 2 kiêm giữ hồ sơ |
| 6 · Pilot plan | Chỉ noi_dia + hang_nang, cả 12 depot (40 nhân viên; đợt chạy thử chỉ có 20 người ở 6 depot); chia ngẫu nhiên theo nhân viên 20/20, phân tầng theo depot; MDE 6 điểm, 859 yêu cầu/nhóm, DE 6,96, m ≥ 299; 4 luật dừng có ngưỡng, thời hạn, người dừng; quyết định 2027-01-12 (`pilot_plan.yaml`) | Xong, có bằng chứng | Người viết code |
| 7 · Rủi ro kinh tế | Xem lại 100%: 11.743 đ/việc = 0,98× (9 phút làm lại), 12.415 đ = 1,03× (15,3 phút như dữ liệu) [simulated]; hoà vốn khi mỗi lần xem lại ≤ 4,8 phút nếu làm lại 15,3 phút (≤ 5,1 phút nếu 9 phút); nhóm dùng 4,8 phút [simulated]; khối lượng còn một nửa thì cố định lên 2.370 đ/việc [simulated]; người theo dõi từng rủi ro khi chạy pilot ghi trong `chi_so.md` | Giả lập | Người kiểm số |

**Con số bất lợi nhóm không bỏ qua:** xem lại 100% gần như không tiết kiệm (0,98×, có thể 1,03×) [simulated]; với 40 nhân viên không đủ mẫu cho mức chênh 5 điểm, chọn MDE 6 điểm thì power ở 5 điểm chỉ ≈ 0,64; chi phí đang dựa trên phút simulated.

**Đề xuất: Go có điều kiện** cho pilot giới hạn ở noi_dia + hang_nang (Gate 2a chỉ duyệt kế hoạch pilot). Điều kiện:
(1) Kỹ sư trưởng agent sửa khoá chống hoàn trùng và đối soát sổ cái (ca 7, 20) · kiểm tra 2026-12-04;
(2) Giám đốc vận hành LogiX-VN ký chấp nhận MDE 6 điểm (power 0,64 nếu tác động thật là 5 điểm) · kiểm tra 2026-12-04;
(3a) PM trợ lý hoàn phí bật đủ 9 event có `trace_id` · kiểm tra 2026-12-04, trước ngày bắt đầu; thiếu event nào thì Giám đốc vận hành không cho bắt đầu, vì thiếu event thì không theo dõi được luật dừng an toàn;
(3b) PM trợ lý hoàn phí thay phút simulated bằng phút đo thật sau tuần đầu · kiểm tra 2026-12-14;
(4) Trưởng nhóm CSKH có lộ trình giảm xem lại theo bậc, mỗi lần xem lại ≤ 4,8 phút (hoà vốn với 15,3 phút làm lại), vì xem lại 100% thì không tiết kiệm · kiểm tra 2026-12-21.
Luật dừng chi phí 8.000 đ chỉ tính chi phí chạy, chưa cộng chi phí cố định 40 triệu/tháng, vì ở bước 4 người riêng cố định đã là 11.852 đ/việc [simulated].
Họp quyết định sau pilot: 2027-01-12.
