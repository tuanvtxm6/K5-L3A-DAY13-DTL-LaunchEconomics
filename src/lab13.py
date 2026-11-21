"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
from statistics import NormalDist

import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)

CHI_PHI_CO_DINH = 40_000_000   # đồng / tháng
YEU_CAU_MOI_THANG = 45_000
PHAM_VI_PILOT = ['noi_dia', 'hang_nang']
SIM = '[simulated]'


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    if k is None:
        return 1 / p
    return (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    if k is None:
        return 1.0
    return 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')
    print(f'  so_lan_chay_ky_vong(0.8, 2)               = {so_lan_chay_ky_vong(0.8, 2):.2f}')
    print(f'  so_lan_chay_ky_vong(0.8)                  = {so_lan_chay_ky_vong(0.8):.2f}')
    print(f'  he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) = {he_so_chi_phi_moi_viec_thanh_cong(0.8, 3):.2f}')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    reqs = reqs.copy()
    # Chỉ giữ các lần chạy thuộc các yêu cầu đang xét (để A3 lọc theo loại được)
    runs = runs[runs['request_id'].isin(reqs['request_id'])]

    if max_lan_chay is not None:
        # Bỏ các lần chạy vượt giới hạn; yêu cầu cần nhiều lần hơn thì chuyển nhân viên,
        # nên không còn phút xem lại / làm lại của trợ lý cho yêu cầu đó.
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0

    # Tử số: MỌI lần chạy, kể cả lần lỗi. Giá token tính cho 1.000 token.
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai   # simulated
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai   # simulated
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai

    # Mẫu số: chỉ yêu cầu thành công
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())

    return dict(
        token=tien_token.sum(),
        tool=tien_tool.sum(),
        chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),
        xem_lai=xem_lai,
        lam_lai=lam_lai,
        tong=tong,
        thanh_cong=thanh_cong,
        cps=tong / thanh_cong if thanh_cong else float('inf'),
        hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs),
    )


# ---------- Nhiệm vụ D1 · Cỡ mẫu ----------
def co_mau(p1, p2, alpha=0.05, power=0.8):
    """Cỡ mẫu mỗi nhóm để so hai tỉ lệ (công thức trong docs/du_lieu_va_cong_thuc.md)."""
    za = NormalDist().inv_cdf(1 - alpha / 2)
    zb = NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    tu = (za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(tu / (p2 - p1) ** 2)


def he_so_thiet_ke(m, icc):
    return 1 + (m - 1) * icc


def co_mau_hieu_dung(c, m, icc):
    """c cụm × m yêu cầu mỗi cụm, chia cho hệ số thiết kế. Luôn nhỏ hơn c / ICC."""
    return c * m / he_so_thiet_ke(m, icc)


def m_toi_thieu(n_can, c, icc):
    """m nhỏ nhất để c·m / (1 + (m − 1)·ICC) ≥ n_can. None nếu không đạt được (n_can ≥ c / ICC)."""
    mau = c - n_can * icc
    if mau <= 0:
        return None
    return math.ceil(n_can * (1 - icc) / mau)


# ---------- In kết quả ----------
def tieu_de(s):
    print(f'\n===== {s} =====')


def dong(nhan, gia_tri, nhan_phu=''):
    print(f'  {nhan:42s} {gia_tri:>16,.0f} {nhan_phu}')


def in_A2(kq, so_yc):
    tieu_de('A2 · Mô hình chi phí từ trace (1.200 yêu cầu)')
    dong('Token (mọi lần chạy)', kq['token'], 'đo từ trace')
    dong('Tool (mọi lần chạy)', kq['tool'], 'đo từ trace')
    dong('  Trong đó, lần chạy thứ 2 và 3', kq['chay_lai'], 'đo từ trace')
    dong('Xem lại', kq['xem_lai'], SIM)
    dong('Làm lại', kq['lam_lai'], SIM)
    dong('Tổng chi phí', kq['tong'], 'có phần ' + SIM)
    dong('Số việc thành công', kq['thanh_cong'])
    dong('Chi phí mỗi việc thành công', kq['cps'], SIM)
    print(f'  {"Hoá đơn token + tool chia số yêu cầu":42s} {kq["hoa_don_moi_yc"]:>16,.1f} đo từ trace')
    print(f'  → Chi phí mỗi việc thành công gấp {kq["cps"] / kq["hoa_don_moi_yc"]:.1f} lần hoá đơn chia số yêu cầu {SIM}')
    for k in ['token', 'tool', 'xem_lai', 'lam_lai']:
        print(f'  → Tỉ trọng {k:8s}: {kq[k] / kq["tong"] * 100:5.1f}%')
    gio_nv = (kq['xem_lai'] + kq['lam_lai']) / kq['tong'] * 100
    print(f'  → Giờ nhân viên (xem lại + làm lại) chiếm {gio_nv:.1f}% tổng chi phí {SIM}')
    khong_tc = so_yc - kq['thanh_cong']
    he_thong = (kq['tong'] + khong_tc * BASELINE) / so_yc
    print(f'  → Chi phí cả hệ thống mỗi yêu cầu (cộng {khong_tc} ca không thành công × 12.000 đ): '
          f'{he_thong:,.0f} đ = {he_thong / BASELINE:.2f}× {SIM}')


def in_A3(runs, reqs):
    tieu_de('A3 · Tách theo loại yêu cầu')
    print(f'  {"loai":10s} {"so_yc":>6s} {"ti_le_tc":>9s} {"lan_chay/yc":>12s} {"cps (đ)":>10s} {"so_12k":>7s}')
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        r = reqs[reqs['loai'] == loai]
        kq = mo_hinh(runs, r)
        so_lan = runs['request_id'].isin(r['request_id']).sum() / len(r)
        print(f'  {loai:10s} {len(r):6d} {kq["thanh_cong"] / len(r) * 100:8.1f}% {so_lan:12.2f} '
              f'{kq["cps"]:10,.0f} {kq["cps"] / BASELINE:6.2f}×  {SIM}')

    print('\n  Tỉ lệ lần chạy status = ok theo lần thử (attempt):')
    bang = runs.merge(reqs[['request_id', 'loai']], on='request_id')
    bang['ok'] = (bang['status'] == 'ok').astype(float)
    pv = bang.pivot_table(index='loai', columns='attempt', values='ok', aggfunc='mean')
    so_run = bang.pivot_table(index='loai', columns='attempt', values='ok', aggfunc='count')
    for loai in pv.index:
        o = '  '.join(f'lần {a}: {pv.loc[loai, a] * 100:5.1f}% (n={int(so_run.loc[loai, a])})'
                      for a in pv.columns if not math.isnan(pv.loc[loai, a]))
        print(f'  {loai:10s} {o}')


def in_A4(runs, reqs):
    tieu_de('A4 · Chi phí cố định 40 triệu đ/tháng (phạm vi noi_dia + hang_nang)')
    pv = reqs[reqs['loai'].isin(PHAM_VI_PILOT)]
    kq = mo_hinh(runs, pv)
    print(f'  Phạm vi: {len(pv)} yêu cầu, {kq["thanh_cong"]} thành công; tổng {kq["tong"]:,.0f} đ; '
          f'cps {kq["cps"]:,.0f} đ {SIM}')
    # Hai dòng đầu cho bảng A4; ba dòng sau là khối lượng thật ở từng bước rollout của pilot
    # (4 / 10 / 20 trong 40 nhân viên dùng trợ lý), vẫn trả đủ 40 triệu đ/tháng.
    for ten, he_so in [('45.000 yêu cầu/tháng', 1.0), ('Một nửa khối lượng', 0.5),
                       ('Pilot 4 người (10%)', 0.10), ('Pilot 10 người (25%)', 0.25),
                       ('Pilot 20 người (50%)', 0.50)]:
        tc_thang = YEU_CAU_MOI_THANG * he_so * kq['thanh_cong'] / len(reqs)
        co_dinh = CHI_PHI_CO_DINH / tc_thang
        tong_viec = kq['cps'] + co_dinh
        print(f'  {ten:22s} việc TC/tháng {tc_thang:9,.0f}  cố định/việc {co_dinh:7,.0f} đ  '
              f'cps + cố định {tong_viec:7,.0f} đ = {tong_viec / BASELINE:.2f}× {SIM}')


def in_B(runs, reqs):
    goc = mo_hinh(runs, reqs)
    tieu_de('B1 · Đổi từng yếu tố')
    kich_ban = {
        'Giá token gấp đôi':          dict(gia_vao=52, gia_ra=260),
        'Giá token giảm một nửa':     dict(gia_vao=13, gia_ra=65),
        'Tỉ lệ xem lại gấp đôi':      dict(he_so_xem_lai=2),
        'Tỉ lệ xem lại giảm một nửa': dict(he_so_xem_lai=0.5),
        'Số ca làm lại gấp đôi':      dict(he_so_lam_lai=2),
        'Số ca làm lại giảm một nửa': dict(he_so_lam_lai=0.5),
        'Lương nhân viên tăng 25%':   dict(luong_phut=2500),
        'Chỉ cho chạy tối đa 2 lần':  dict(max_lan_chay=2),
        'Chỉ cho chạy 1 lần':         dict(max_lan_chay=1),
    }
    print(f'  {"Gốc (A2)":30s} {goc["cps"]:8,.0f} đ {SIM}')
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        print(f'  {ten:30s} {cps:8,.0f} đ {(cps / goc["cps"] - 1) * 100:+6.1f}%  {SIM}')

    tieu_de('B2 · Đổi một cặp: giá token gấp đôi + xem lại gấp đôi')
    cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)['cps']
    rieng = (mo_hinh(runs, reqs, gia_vao=52, gia_ra=260)['cps'] - goc['cps']) \
        + (mo_hinh(runs, reqs, he_so_xem_lai=2)['cps'] - goc['cps'])
    print(f'  Cặp: {cap:,.0f} đ ({(cap / goc["cps"] - 1) * 100:+.1f}%) {SIM}; '
          f'tổng hai tác động riêng: {rieng / goc["cps"] * 100:+.1f}% (mô hình cộng tuyến tính)')

    tieu_de('B3 · Giới hạn chạy lại: chi phí cả hệ thống')
    print(f'  {"Giới hạn":9s} {"Tổng trợ lý":>14s} {"Không TC":>9s} {"Cả hệ thống":>14s} {"cps":>8s}')
    for k in [1, 2, 3]:
        kq = mo_hinh(runs, reqs, max_lan_chay=k)
        khong_tc = len(reqs) - kq['thanh_cong']
        he_thong = kq['tong'] + khong_tc * BASELINE
        print(f'  {k} lần     {kq["tong"]:14,.0f} {khong_tc:9d} {he_thong:14,.0f} {kq["cps"]:8,.0f}  {SIM}')

    tieu_de('B4 · Xem lại 100% (phạm vi noi_dia + hang_nang)')
    pv = reqs[reqs['loai'].isin(PHAM_VI_PILOT)]
    runs_pv = runs[runs['request_id'].isin(pv['request_id'])]
    co_ok = runs_pv.loc[runs_pv['status'] == 'ok', 'request_id'].nunique()
    so_lam_lai = int((pv['ket_qua'] == 'lam_lai').sum())
    tc = int((pv['ket_qua'] == 'thanh_cong').sum())
    token_tool = (runs_pv['tokens_in'] / 1000 * GIA_VAO + runs_pv['tokens_out'] / 1000 * GIA_RA
                  + runs_pv['tool_calls'] * GIA_TOOL).sum()
    xem_lai = co_ok * 5 * LUONG_PHUT
    phut_lam_lai_tb = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated'].mean()
    phut_lam_lai_tv = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated'].median()
    print(f'  {len(pv)} yêu cầu; {co_ok} có ≥ 1 lần chạy ok (xem lại 5 phút); {so_lam_lai} ca lam_lai; '
          f'{tc} thành công; token + tool {token_tool:,.0f} đ')
    print(f'  Phút làm lại trong dữ liệu: trung bình {phut_lam_lai_tb:.1f}, trung vị {phut_lam_lai_tv:.1f} {SIM}')
    for phut in [9, round(phut_lam_lai_tb, 1)]:
        lam_lai = so_lam_lai * phut * LUONG_PHUT
        tong = token_tool + xem_lai + lam_lai
        cps = tong / tc
        hoa_von = (BASELINE * tc - lam_lai - token_tool) / (co_ok * LUONG_PHUT)
        print(f'  Làm lại {phut:4} phút/ca: tổng {tong:12,.0f} đ → cps {cps:7,.0f} đ = {cps / BASELINE:.2f}×; '
              f'hoà vốn khi mỗi lần xem lại ≤ {hoa_von:.1f} phút {SIM}')


def in_D1(reqs):
    from statsmodels.stats.power import NormalIndPower
    from statsmodels.stats.proportion import proportion_effectsize

    p1, icc = 0.70, 0.02
    tieu_de('D1 · Cỡ mẫu (baseline 0,70; +5 điểm; alpha 0,05; power 0,8; ICC 0,02)')
    n5 = co_mau(p1, 0.75)
    print(f'  a) Chia theo yêu cầu: {n5:,} yêu cầu mỗi nhóm')

    m = 75
    de = he_so_thiet_ke(m, icc)
    n_nv = math.ceil(n5 * de)
    nguoi = math.ceil(n_nv / m)
    print(f'  b) Theo nhân viên, m = {m}: DE = {de:.2f}; n = {n_nv:,} mỗi nhóm → {nguoi} người mỗi nhóm, '
          f'tổng {2 * nguoi} > 40: không đủ người')

    c_nv = 20
    print(f'  c) {c_nv} nhân viên mỗi nhóm: cỡ mẫu hiệu dụng tối đa c / ICC = {c_nv / icc:,.0f} < {n5:,}: không đạt '
          f'(với m = 75: {co_mau_hieu_dung(c_nv, 75, icc):,.0f})')

    c_dp = 6
    print(f'  d) {c_dp} depot mỗi nhóm: tối đa {c_dp / icc:,.0f} (chỉ {c_dp} cụm < 20)')

    n6 = co_mau(p1, 0.76)
    m6 = m_toi_thieu(n6, c_nv, icc)
    print(f'  e) Mức chênh 6 điểm: {n6:,} mỗi nhóm; {c_nv} người mỗi nhóm cần m ≥ {m6} yêu cầu mỗi người '
          f'(DE = {he_so_thiet_ke(m6, icc):.2f})')

    power5 = NormalIndPower().power(effect_size=proportion_effectsize(0.75, p1), nobs1=n6, alpha=0.05)
    print(f'  Nếu thiết kế cho 6 điểm (n = {n6}) mà tác động thật chỉ 5 điểm: power ≈ {power5:.2f}')

    tieu_de('D3 · Tỉ lệ mo_lai_trong_7_ngay hiện tại (trước khi đặt luật an toàn)')
    pv = reqs[reqs['loai'].isin(PHAM_VI_PILOT)]
    print(f'  Toàn bộ: {reqs["mo_lai_trong_7_ngay"].mean() * 100:.2f}% '
          f'({int(reqs["mo_lai_trong_7_ngay"].sum())}/{len(reqs)})')
    print(f'  Phạm vi noi_dia + hang_nang: {pv["mo_lai_trong_7_ngay"].mean() * 100:.2f}% '
          f'({int(pv["mo_lai_trong_7_ngay"].sum())}/{len(pv)})')
    ti_le_lam_lai = (pv['ket_qua'] == 'lam_lai').mean() * 100
    print(f'  Tỉ lệ lam_lai trong phạm vi: {ti_le_lam_lai:.1f}%')


def in_E1(reqs):
    tieu_de('E1 · Tính thử ba chỉ số trên 1.200 yêu cầu (đợt chạy thử, không có đối chứng)')
    chinh = (reqs['dong_trong_24h'] == 1) & (reqs['mo_lai_trong_7_ngay'] == 0)
    xem = reqs[reqs['duoc_xem_lai'] == 1]
    bo_qua = xem['quyet_dinh_xem_lai'].isin(['sua', 'bo'])
    an_toan = reqs['mo_lai_trong_7_ngay'] == 1
    print(f'  Chính  · đóng trong 24h và không mở lại 7 ngày: {chinh.mean() * 100:.2f}% ({chinh.sum()}/{len(reqs)})')
    print(f'  Dùng   · bỏ qua gợi ý (sua + bo) / được xem lại: {bo_qua.mean() * 100:.2f}% ({bo_qua.sum()}/{len(xem)})')
    print(f'  An toàn· mở lại trong 7 ngày:                    {an_toan.mean() * 100:.2f}% ({an_toan.sum()}/{len(reqs)})')


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)

    tieu_de('A1 · Ba phép thử đáp án biết trước')
    kiem_tra_dap_an_biet_truoc()

    ket_qua = mo_hinh(runs, reqs)
    in_A2(ket_qua, len(reqs))
    in_A3(runs, reqs)        # CP1 · A3
    in_A4(runs, reqs)        # CP1 · A4
    in_B(runs, reqs)         # CP2 · B1–B4
    in_D1(reqs)              # CP4 · D1 (+ tỉ lệ mở lại cho D3)
    in_E1(reqs)              # CP5 · E1 (số cho chi_so.md)
