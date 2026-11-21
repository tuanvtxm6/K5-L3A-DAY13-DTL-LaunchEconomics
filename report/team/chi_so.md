# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

Số "tính thử" lấy từ `src/lab13.py` (hàm `in_E1`) trên 1.200 yêu cầu của đợt chạy thử. Các cột dùng ở đây (`dong_trong_24h`, `mo_lai_trong_7_ngay`, `quyet_dinh_xem_lai`) không phải cột `_simulated`. Số tiền ở phần E2 lấy từ cột phút `_simulated` nên gắn nhãn **[simulated]**.

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | 82,83% (994/1.200) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | 27,12% (48/177) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | 4,25% (51/1.200) |
| Dùng | Nhóm tự đề xuất: tỉ lệ yêu cầu trong phạm vi pilot mà nhân viên nhóm trợ lý có mở gợi ý | Số `trace_id` có event `assistant_opened`, chia số `trace_id` có event `request_closed` thuộc phạm vi `noi_dia` + `hang_nang` của nhóm trợ lý | Không cần tính |
| An toàn | Nhóm tự đề xuất (a): tỉ lệ yêu cầu bị hoàn tiền trùng hoặc sổ cái lệch số tiền đã duyệt | Số `trace_id` có từ hai event `ledger_refund_posted` thành công, hoặc số tiền sổ cái khác số tiền được duyệt, chia số yêu cầu đã hoàn tiền; ngưỡng 0 ca | Không cần tính |
| An toàn | Nhóm tự đề xuất (b): tỉ lệ đơn hoàn sai số tiền qua kiểm tra mẫu (bắt lỗi ngầm như ca 5, 17, nơi số tiền được duyệt đã sai từ đầu nên (a) không thấy) | Số event `audit_sample_checked` có `so_tien_da_hoan` khác `so_tien_dung`, chia số đơn trong mẫu (100 đơn/tuần, chọn ngẫu nhiên); ngưỡng 1% | Không cần tính |

Viết "chỉ số trong đợt chạy thử là …", không viết "trợ lý đã nâng chỉ số": đợt chạy thử không có nhóm đối chứng. Ba con số tính thử trên đây chỉ mô tả đợt chạy thử, không phải tác động của trợ lý.

## Danh sách event

Mọi event đều mang `trace_id` để nối với trace của agent. Với nhóm đối chứng (nhân viên tự làm), `trace_id` được tạo ở event `request_created` của luồng thủ công để vẫn nối được các event đóng, mở lại và sổ cái.

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `assistant_opened` | Giao diện CSKH | `staff_id`, `request_id`, `nhom` (trợ lý hoặc đối chứng), `loai`, `trace_id` | Nhân viên mở gợi ý của trợ lý cho một yêu cầu |
| `assistant_run_finished` | Agent | `request_id`, `attempt`, `status` (`ok` hoặc `loi`), `tokens_in`, `tokens_out`, `tool_calls`, `trace_id` | Khi mỗi lần chạy của agent kết thúc |
| `suggestion_reviewed` | Giao diện CSKH | `staff_id`, `request_id`, `quyet_dinh_xem_lai` (`giu`, `sua`, `bo`), `phut_xem_lai`, `trace_id` | Khi nhân viên quyết định giữ, sửa hoặc bỏ gợi ý |
| `handoff_to_staff` | Agent | `request_id`, `reason` (ví dụ `thieu_du_lieu`, `het_3_lan`), `loai`, `so_lan_chay`, `trace_id` | Khi agent chạy hết số lần tối đa hoặc không xử lý được và chuyển nhân viên |
| `ledger_refund_posted` | Sổ cái hoàn tiền | `request_id`, `so_tien_vnd`, `ket_qua` (`ok` hoặc `loi`), `trace_id` | Khi ghi sổ một khoản hoàn |
| `request_closed` | Hệ thống CSKH | `request_id`, `dong_luc`, `dong_trong_24h`, `loai`, `nhom`, `trace_id` | Khi yêu cầu được đóng |
| `request_reopened` | Hệ thống CSKH | `request_id`, `ly_do_mo_lai` (ví dụ sai số tiền, chưa nhận tiền), `sau_bao_nhieu_ngay`, `trace_id` | Khi khách mở lại yêu cầu trong 7 ngày |
| `rework_logged` | Giao diện CSKH | `staff_id`, `request_id`, `phut_lam_lai` (đo thật), `trace_id` | Khi nhân viên làm lại một yêu cầu mà trợ lý trả lời sai |
| `audit_sample_checked` | Kế toán | `request_id`, `so_tien_da_hoan`, `so_tien_dung` (tính lại theo bảng giá và mã giảm giá hiện hành), `phien_ban_bang_gia`, `trace_id` | Hằng tuần, trên mẫu ngẫu nhiên 100 đơn đã hoàn của nhóm trợ lý |

**Kiểm tra chéo:** với mỗi chỉ số ở bảng E1, event dùng để tính:

- Chỉ số chính (đóng trong 24 giờ, không mở lại trong 7 ngày): `request_closed` (thuộc tính `dong_trong_24h`) và `request_reopened`. Một `trace_id` có `request_closed` với `dong_trong_24h` bằng 1 và không có `request_reopened` trong 7 ngày thì tính là đạt.
- Chỉ số dùng (tỉ lệ bỏ qua gợi ý): `suggestion_reviewed` (đếm `sua` và `bo` trên tổng số event này).
- Chỉ số an toàn (tỉ lệ lỗi lọt đến khách): `request_reopened` chia `request_closed`.
- Chỉ số dùng nhóm đề xuất (tỉ lệ yêu cầu có mở gợi ý): `assistant_opened` chia `request_closed` thuộc phạm vi.
- Chỉ số an toàn nhóm đề xuất (a) (hoàn trùng hoặc sổ cái lệch số đã duyệt): `ledger_refund_posted`, đối chiếu với `so_tien_vnd` đã duyệt.
- Chỉ số an toàn nhóm đề xuất (b) (lỗi ngầm, sai số tiền mà không ai phàn nàn): `audit_sample_checked`. Không dùng được `request_reopened` cho loại lỗi này vì khách không mở lại (ca 17: 212 đơn lệch trong 9 ngày, 0 khách mở lại).
- Chi phí mỗi việc thành công (theo dõi ở E2): `assistant_run_finished` (token, tool, lần chạy), `suggestion_reviewed` (`phut_xem_lai`), `rework_logged` (`phut_lam_lai`), `request_closed` (đếm việc thành công).

Cả sáu chỉ số đều tính được từ danh sách 9 event trên, nên đều đo được. Event `audit_sample_checked` được bổ sung sau câu hỏi duyệt chéo: bản đầu chỉ có 8 event và không bắt được lỗi ngầm.

## E2 · Rủi ro kinh tế

Số lấy từ bảng độ nhạy trong [bang_chi_phi.md](bang_chi_phi.md). Gốc: chi phí mỗi việc thành công 4.472 đ [simulated]; nhân viên tự làm 12.000 đ.

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | Chi phí mỗi việc thành công từ 4.472 đ lên 6.787 đ (+51,8%) [simulated]; đây là yếu tố nhạy nhất | Tỉ lệ ca `rework_logged` trên yêu cầu của nhóm trợ lý theo tuần; hiện 4,9% trong phạm vi `noi_dia` + `hang_nang`; cảnh báo khi vượt 7% | Thu hẹp phạm vi về `noi_dia` và giới hạn 2 lần chạy; chưa mở thêm `hang_nang` cho tới khi dưới 7% | PM trợ lý hoàn phí |
| Phải xem lại 100% yêu cầu | Chi phí mỗi việc thành công 11.743 đ (0,98× so với 12.000 đ) nếu làm lại 9 phút/ca; 12.415 đ (1,03×) nếu dùng 15,3 phút/ca theo dữ liệu; hoà vốn khi mỗi lần xem lại không quá 5,1 phút (hoặc 4,8 phút) [simulated] | Trung bình `phut_xem_lai` theo tuần; tỉ lệ yêu cầu được xem lại; cảnh báo khi trung bình trên 4,8 phút (lấy kịch bản 15,3 phút làm lại, xấu hơn 5,1 phút) | Giảm xem lại theo bậc chỉ khi tỉ lệ `sua` + `bo` không quá 15% hai tuần liên tiếp và mở lại 7 ngày không tăng; thay phút simulated bằng phút đo thật sau tuần đầu | Trưởng nhóm CSKH |
| Khối lượng thấp hơn dự kiến (chi phí cố định 40 triệu đ/tháng) | Chi phí cố định mỗi việc từ 1.185 đ (45.000 yêu cầu/tháng) lên 2.370 đ (một nửa khối lượng); chi phí mỗi việc cộng cố định từ 4.599 đ (0,38×) lên 5.784 đ (0,48×) [simulated]. Ở khối lượng thật của pilot: 15.266 đ = 1,27× (bước 4 người), 8.155 đ = 0,68× (10 người), 5.784 đ = 0,48× (20 người) [simulated] | Số việc thành công mỗi tuần từ event `request_closed` so với kế hoạch; cảnh báo khi dưới 50% | Không mở rộng pilot; xem lại hợp đồng chi phí cố định với nhà cung cấp | Giám đốc vận hành LogiX-VN |
