import streamlit as st
import pandas as pd
import os
import io

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & CUSTOM CSS TỐI ƯU DARK/LIGHT MODE
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hệ Thống Quản Lý An Toàn TMT",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* 1. Ép giao diện tràn viền tối đa */
    .main .block-container {
        max-width: 99% !important;
        padding: 0.5rem 0.8rem !important;
    }

    /* 2. Ép Cố Định Màu Cho Sidebar (Chống Lỗi Dark Mode) */
    [data-testid="stSidebar"] {
        min-width: 250px !important;
        max-width: 270px !important;
        background-color: #f1f5f9 !important;
        border-right: 1px solid #cbd5e1 !important;
    }

    [data-testid="stSidebar"] * {
        color: #0f172a !important; /* Ép chữ Sidebar luôn màu tối rõ nét */
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 0.8rem 0.6rem !important;
    }

    /* Đảm bảo tất cả nút bấm trong Sidebar căn lề trái thẳng hàng */
    [data-testid="stSidebar"] .stButton > button {
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 12px !important;
    }

    /* 3. Header Card tiêu đề */
    .header-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff !important;
        padding: 10px 18px;
        border-radius: 6px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    .header-card h1 {
        color: #ffffff !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }
    .version-badge {
        background-color: rgba(255,255,255,0.25);
        color: #ffffff !important;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }

    /* 4. Định dạng Bảng HTML Responsive */
    .custom-table-container {
        width: 100%;
        overflow-x: auto;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 13px;
        background-color: #ffffff !important;
    }
    .custom-table th {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
        font-weight: 700;
        text-align: left;
        padding: 10px 12px;
        border-bottom: 2px solid #cbd5e1;
        white-space: nowrap;
    }
    .custom-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #e2e8f0;
        color: #0f172a !important;
        vertical-align: middle;
    }
    .custom-table tr:hover {
        background-color: #f1f5f9 !important;
    }

    /* Tỷ lệ cột */
    .col-stt { width: 50px !important; text-align: center; font-weight: 600; color: #475569 !important; }
    .col-title { width: 28% !important; font-weight: 600; }
    .col-link { width: 130px !important; text-align: center; }
    .col-note { width: auto !important; }

    /* Nút bấm liên kết */
    .btn-link-action {
        display: inline-block;
        background-color: #0d6efd !important;
        color: #ffffff !important;
        padding: 5px 12px;
        border-radius: 4px;
        text-decoration: none !important;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
        white-space: nowrap;
    }
    .btn-link-action:hover {
        background-color: #0b5ed7 !important;
    }

    .path-box {
        background-color: #e2e8f0;
        border: 1px dashed #94a3b8;
        padding: 6px;
        border-radius: 5px;
        font-size: 10px;
        word-break: break-all;
        color: #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. BẢO MẬT ĐĂNG NHẬP
# ---------------------------------------------------------
USER_CREDENTIALS = {"tmt": "123456", "admin": "123456"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
                <h3 style="color: #1e3c72; margin-bottom: 5px;">🛡️ HỆ THỐNG QUẢN LÝ AN TOÀN</h3>
                <span style="background: #e7f1ff; color: #0d6efd; padding: 3px 10px; border-radius: 12px; font-weight: 600; font-size: 11px;">Version 1.0</span>
                <hr style="margin: 12px 0;">
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("##### 🔐 Đăng Nhập Tài Khoản")
            user_input = st.text_input("Tên đăng nhập:", value="tmt")
            pass_input = st.text_input("Mật khẩu:", type="password")
            submit_login = st.form_submit_button("🔑 ĐĂNG NHẬP", type="primary", use_container_width=True)
            
            if submit_login:
                if user_input in USER_CREDENTIALS and USER_CREDENTIALS[user_input] == pass_input:
                    st.session_state.logged_in = True
                    st.session_state.username = user_input
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("❌ Mật khẩu hoặc Tên đăng nhập không chính xác!")
    st.stop()

# ---------------------------------------------------------
# 3. KHỞI TẠO ĐƯỜNG DẪN & DỮ LIỆU MẶC ĐỊNH CHUẨN TỪ FILE ANH TRÍ
# ---------------------------------------------------------
EXCEL_DIR = r"D:\0 2025 0 LUU OFFICE drive\0000 chua luu\0 0 0 app\000TmT_VBA_source\Dashboard_AnToan"
if not os.path.exists(EXCEL_DIR):
    EXCEL_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_PATH_WEB = os.path.join(EXCEL_DIR, "DanhMuc_CongCu_WEB_TMT.xlsx")
EXCEL_PATH_QUAN_LY = os.path.join(EXCEL_DIR, "QuanLy_AnToan_TMT.xlsx")
EXCEL_PATH_BC_DINH_KY = os.path.join(EXCEL_DIR, "DanhSach_BaoCao_DinhKy_TMT.xlsx")
EXCEL_PATH_GSHEET = os.path.join(EXCEL_DIR, "DanhSach_Gsheet_TMT.xlsx")

CATEGORIES = [
    "DTTU_01 AT", "DTTU_01 AT 01 Bao cao", "DTTU_01 AT 01 Bao cao 2026",
    "DTTU_02 PCTT", "DTTU_03 PCCC", "DTTU_04 HL", "DTTU_05 ATDTXD",
    "DTTU_ATGT", "DTTU_CNTT", "DTTU_DCAT", "DTTU_DCNN va Cac loai xe",
    "DTTU_DGRR", "DTTU_HNTH cac loai", "DTTU_KIEM TRA",
    "DTTU_KIEM TRA-Thuc hien Kien Nghi", "DTTU_UCKC",
    "DTTU_UCKC dien tap cac loai", "DTTU_khac 01 PHOI HOP CAC TO",
    "DTTU_khac 02 XEM DE BIET CTY", "DTTU_khac 03 ATD dia phuong",
    "DTTU_khac 03 XEM DE BIET dia phuong", "Quy dinh 0000 Discussion",
    "Quy dinh GOV", "Quy dinh PCTN", "Quy dinh PCTN file tham khao cac Doi",
    "Quy dinh SPC va EVN", "Quy dinh trao doi EVN-SPC-PCTN"
]

DEFAULT_WEBSITES = [
    {'STT': 1, 'Mô tả WEB': 'D-Office', 'Link truy cập': 'https://doffice.evn.com.vn', 'Ghi chú': 'Công văn / văn bản EVN'},
    {'STT': 2, 'Mô tả WEB': 'Công cụ web trực tuyến', 'Link truy cập': 'https://www.congcuweb.net/', 'Ghi chú': 'Hiệu chỉnh tên công văn / văn bản'},
    {'STT': 3, 'Mô tả WEB': 'QLAT SPC', 'Link truy cập': 'https://giamsatantoan.evnspc.vn/Home/Index', 'Ghi chú': 'Quản lý giám sát an toàn SPC'},
    {'STT': 4, 'Mô tả WEB': 'Lịch tuần', 'Link truy cập': 'https://lichtuan.evnspc.vn', 'Ghi chú': 'Công ty Điện lực Tây Ninh'},
    {'STT': 5, 'Mô tả WEB': 'Hệ thống PMIS', 'Link truy cập': 'https://pmis.evn.com.vn', 'Ghi chú': 'Quản lý vận hành thiết bị & lưới điện'},
    {'STT': 6, 'Mô tả WEB': 'Tritm.la Dashboard 2026 DTTU ', 'Link truy cập': 'https://docs.google.com/spreadsheets/d/1gVAroFIytWwrBMCScYuXWbzlS1ZNXrPY4Pcgb__Dv-c/edit?gid=964445540#gid=964445540', 'Ghi chú': 'Google sheet CV'},
    {'STT': 7, 'Mô tả WEB': 'Hệ thống Giám sát Thiên tai Việt Nam', 'Link truy cập': 'https://vndms.gov.vn/', 'Ghi chú': 'Cảnh báo và phòng chống thiên tai'},
    {'STT': 8, 'Mô tả WEB': 'Hệ thống HRMS', 'Link truy cập': 'https://hrms.evn.com.vn', 'Ghi chú': 'Quản lý lao động tiền lương'},
    {'STT': 9, 'Mô tả WEB': 'Hệ thống E-Learning', 'Link truy cập': 'https://elearning.evn.com.vn', 'Ghi chú': 'Huấn luyện an toàn & thi trực tuyến'},
    {'STT': 10, 'Mô tả WEB': 'Cổng Dịch vụ công Quốc gia', 'Link truy cập': 'https://dichvucong.gov.vn', 'Ghi chú': 'Thực hiện thủ tục hành chính PCCC/ĐTXD'},
    {'STT': 11, 'Mô tả WEB': 'Cổng Thông tin Bộ Công Thương', 'Link truy cập': 'https://moit.gov.vn', 'Ghi chú': 'Theo dõi văn bản quy phạm kỹ thuật'},
    {'STT': 12, 'Mô tả WEB': 'Cổng Báo cáo Phòng chống thiên tai', 'Link truy cập': 'https://pctt.evn.com.vn', 'Ghi chú': 'Cập nhật tình hình PCTT & TKCN'},
    {'STT': 13, 'Mô tả WEB': 'Hệ thống Quản lý Đầu tư Xây dựng (IMIS)', 'Link truy cập': 'https://imis.evn.com.vn', 'Ghi chú': 'Theo dõi an toàn dự án ĐTXD'},
    {'STT': 14, 'Mô tả WEB': 'Hệ thống Thông tin Báo cáo EVN', 'Link truy cập': 'https://baocao.evn.com.vn', 'Ghi chú': 'Tổng hợp chỉ tiêu an toàn - kỹ thuật'},
    {'STT': 15, 'Mô tả WEB': 'Lưu trữ Hồ sơ / Biểu mẫu TMT', 'Link truy cập': 'https://drive.google.com', 'Ghi chú': 'Kho lưu trữ dữ liệu dùng chung TMT'},
    {'STT': 16, 'Mô tả WEB': 'Thư viện Quy chuẩn - Quy định An toàn', 'Link truy cập': 'https://drive.google.com', 'Ghi chú': 'Tra cứu tài liệu an toàn PCCC & ĐT'}
]

def reindex_df(df):
    if not df.empty:
        df = df.reset_index(drop=True)
        df["STT"] = df.index + 1
    return df

def to_excel_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='WEBSITES')
    return output.getvalue()

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "1 🌐 DS WEBsites_CV"

if "web_tools_df" not in st.session_state:
    if os.path.exists(EXCEL_PATH_WEB):
        try:
            st.session_state.web_tools_df = reindex_df(pd.read_excel(EXCEL_PATH_WEB))
        except Exception:
            st.session_state.web_tools_df = reindex_df(pd.DataFrame(DEFAULT_WEBSITES))
    else:
        st.session_state.web_tools_df = reindex_df(pd.DataFrame(DEFAULT_WEBSITES))

if "data_store" not in st.session_state:
    st.session_state.data_store = {}
    if os.path.exists(EXCEL_PATH_QUAN_LY):
        try:
            excel_file = pd.ExcelFile(EXCEL_PATH_QUAN_LY)
            for idx, cat in enumerate(CATEGORIES):
                sheet_name = f"MKT_{idx+1}"
                if sheet_name in excel_file.sheet_names:
                    df_read = pd.read_excel(excel_file, sheet_name=sheet_name)
                    st.session_state.data_store[cat] = reindex_df(df_read)
                else:
                    st.session_state.data_store[cat] = pd.DataFrame(columns=["STT", "Thư mục / Hồ sơ", "Link xem", "Ghi chú"])
        except Exception:
            pass

    if not st.session_state.data_store:
        for cat in CATEGORIES:
            st.session_state.data_store[cat] = pd.DataFrame([
                {"STT": 1, "Thư mục / Hồ sơ": f"Hồ sơ {cat}", "Link xem": "https://drive.google.com", "Ghi chú": "Cập nhật định kỳ"}
            ])

if "bc_dinhky_df" not in st.session_state:
    if os.path.exists(EXCEL_PATH_BC_DINH_KY):
        try:
            st.session_state.bc_dinhky_df = reindex_df(pd.read_excel(EXCEL_PATH_BC_DINH_KY))
        except Exception:
            pass
    if "bc_dinhky_df" not in st.session_state:
        st.session_state.bc_dinhky_df = pd.DataFrame([
            {"STT": 1, "Tên Báo Cáo / Công Việc": "Báo cáo công tác An toàn định kỳ Quý", "Tần suất": "Hàng Quý", "Đơn vị nhận": "Công ty Điện lực", "Link biểu mẫu": "https://drive.google.com", "Ghi chú": "Nộp trước ngày 20 cuối quý"},
            {"STT": 2, "Tên Báo Cáo / Công Việc": "Báo cáo công tác PCCC & CNCH", "Tần suất": "Hàng Tháng", "Đơn vị nhận": "Phòng An toàn", "Link biểu mẫu": "https://drive.google.com", "Ghi chú": "Nộp trước ngày 25 hàng tháng"}
        ])

if "gsheet_df" not in st.session_state:
    if os.path.exists(EXCEL_PATH_GSHEET):
        try:
            st.session_state.gsheet_df = reindex_df(pd.read_excel(EXCEL_PATH_GSHEET))
        except Exception:
            pass
    if "gsheet_df" not in st.session_state:
        st.session_state.gsheet_df = pd.DataFrame([
            {"STT": 1, "Mô tả Google Sheet": "Bảng Theo Dõi Công Việc Theo Tuần", "Link Google Sheet": "https://docs.google.com/spreadsheets", "Ghi chú": "Dùng chung phòng An Toàn"},
            {"STT": 2, "Mô tả Google Sheet": "Theo Dõi Kiến Nghị Kiểm Tra", "Link Google Sheet": "https://docs.google.com/spreadsheets", "Ghi chú": "Cập nhật trực tuyến"}
        ])

# HEADER HỆ THỐNG
st.markdown("""
    <div class="header-card">
        <h1>🛡️ Hệ Thống Quản Lý An Toàn & Công Tác Chuyên Môn TMT</h1>
        <span class="version-badge">Version 1.0</span>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. SIDEBAR CHUYÊN NGHIỆP
# ---------------------------------------------------------
st.sidebar.markdown(f"👤 **User:** `{st.session_state.username}`")

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    if st.button("🚪 Thoát", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

with col_btn2:
    if st.button("🧹 Cache", use_container_width=True, type="secondary"):
        st.cache_data.clear()
        st.toast("Đã xóa cache!", icon="🎉")

st.sidebar.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("**📁 MỤC LÀM VIỆC**")

menu_options = [
    ("1 🌐 DS WEBsites_CV", "1 🌐 DS WEBsites_CV"),
    ("2 📋 DM QL Files_CV", "2 📋 DM QL Files_CV"),
    ("3 📊 DS BCdinhky_CV", "3 📊 DS BCdinhky_CV"),
    ("4 🟢 DS Gsheet_CV", "4 🟢 DS Gsheet_CV")
]

for label, key_val in menu_options:
    is_active = (st.session_state.active_tab == key_val)
    btn_type = "primary" if is_active else "secondary"
    if st.sidebar.button(label, key=f"menu_{key_val}", type=btn_type, use_container_width=True):
        st.session_state.active_tab = key_val
        st.rerun()

main_menu = st.session_state.active_tab

st.sidebar.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("**📌 Thư mục Excel:**")
st.sidebar.markdown(f'<div class="path-box">{EXCEL_DIR}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. HÀM DỰNG BẢNG HTML CHUẨN CÚ PHÁP
# ---------------------------------------------------------
def render_perfect_table(df, title_col, link_col, btn_label="🔗 Mở Web"):
    rows_html = ""
    for _, row in df.iterrows():
        stt = row.get("STT", "")
        title = row.get(title_col, "")
        link = row.get(link_col, "#")
        note = row.get("Ghi chú", "")
        
        btn_html = f'<a class="btn-link-action" href="{link}" target="_blank">{btn_label}</a>' if link and str(link) != 'nan' else '-'
        rows_html += f'<tr><td class="col-stt">{stt}</td><td class="col-title">{title}</td><td class="col-link">{btn_html}</td><td class="col-note">{note}</td></tr>'

    full_table_html = f'''
    <div class="custom-table-container">
        <table class="custom-table">
            <thead>
                <tr>
                    <th class="col-stt">STT</th>
                    <th class="col-title">{title_col}</th>
                    <th class="col-link">Liên kết</th>
                    <th class="col-note">Ghi chú</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    '''
    st.markdown(full_table_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. HIỂN THỊ DỮ LIỆU & BỘ CÔNG CỤ NHẬP / XUẤT EXCEL
# ---------------------------------------------------------
def render_io_excel_tools(df, current_key, file_prefix):
    st.markdown("---")
    col_up, col_down = st.columns([1.2, 1])
    
    with col_up:
        st.markdown("##### 📥 Tải lên / Thay thế dữ liệu từ file Excel (.xlsx)")
        uploaded_file = st.file_uploader(f"Chọn file Excel để cập nhật [{file_prefix}]", type=["xlsx", "xls"], key=f"uploader_{current_key}")
        if uploaded_file is not None:
            try:
                new_df = pd.read_excel(uploaded_file)
                new_df = reindex_df(new_df)
                if st.button("🔥 Xác nhận đè dữ liệu mới", type="primary", key=f"btn_confirm_{current_key}"):
                    if current_key == "web":
                        st.session_state.web_tools_df = new_df
                    elif current_key == "bc":
                        st.session_state.bc_dinhky_df = new_df
                    elif current_key == "gsheet":
                        st.session_state.gsheet_df = new_df
                    else:
                        st.session_state.data_store[current_key] = new_df
                    st.balloons()
                    st.success("Tải dữ liệu từ Excel thành công!")
                    st.rerun()
            except Exception as e:
                st.error(f"Lỗi đọc file Excel: {e}")

    with col_down:
        st.markdown("##### 📤 Xuất dữ liệu ra file Excel")
        excel_bytes = to_excel_bytes(df)
        st.download_button(
            label="💾 Tải file Excel về máy",
            data=excel_bytes,
            file_name=f"{file_prefix}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# Main Logic
if main_menu == "1 🌐 DS WEBsites_CV":
    st.subheader("🌐 Bảng Danh Sách WEBsites_CV")
    
    render_perfect_table(
        st.session_state.web_tools_df, 
        title_col="Mô tả WEB", 
        link_col="Link truy cập", 
        btn_label="🔗 Truy cập Web"
    )

    col_rst1, col_rst2 = st.columns([3, 1])
    with col_rst2:
        if st.button("🔄 Khôi phục 16 Web mặc định", type="secondary"):
            st.session_state.web_tools_df = reindex_df(pd.DataFrame(DEFAULT_WEBSITES))
            st.toast("Đã khôi phục 16 Web mặc định!", icon="🎉")
            st.rerun()

    with st.expander("✏️ Chỉnh sửa / Thêm bớt dữ liệu trực tiếp"):
        edited_df = st.data_editor(
            st.session_state.web_tools_df,
            num_rows="dynamic",
            use_container_width=True,
            column_order=["STT", "Mô tả WEB", "Link truy cập", "Ghi chú"],
            key="edit_web_expander"
        )
        if st.button("💾 Lưu chỉnh sửa", type="primary"):
            st.session_state.web_tools_df = reindex_df(edited_df)
            st.success("Đã cập nhật dữ liệu thành công!")
            st.rerun()

    render_io_excel_tools(st.session_state.web_tools_df, "web", "1 DS WEBsites_CV out_20260926 macdinh")

elif main_menu == "2 📋 DM QL Files_CV":
    selected_cat = st.sidebar.selectbox("📂 Chọn mảng công việc:", CATEGORIES)
    if selected_cat:
        st.subheader(f"📂 Quản Lý Hồ Sơ: {selected_cat}")
        current_df = st.session_state.data_store[selected_cat]

        render_perfect_table(
            current_df, 
            title_col="Thư mục / Hồ sơ", 
            link_col="Link xem", 
            btn_label="🔗 Mở hồ sơ"
        )

        with st.expander(f"✏️ Chỉnh sửa dữ liệu mảng {selected_cat}"):
            edited_df = st.data_editor(
                current_df,
                num_rows="dynamic",
                use_container_width=True,
                column_order=["STT", "Thư mục / Hồ sơ", "Link xem", "Ghi chú"],
                key=f"edit_cat_{selected_cat}"
            )
            if st.button("💾 Lưu chỉnh sửa mảng này", type="primary"):
                st.session_state.data_store[selected_cat] = reindex_df(edited_df)
                st.success("Đã cập nhật dữ liệu!")
                st.rerun()

        render_io_excel_tools(current_df, selected_cat, f"HoSo_{selected_cat}")

elif main_menu == "3 📊 DS BCdinhky_CV":
    st.subheader("📊 Bảng Danh Sách Báo Cáo Định Kỳ & Công Việc")

    render_perfect_table(
        st.session_state.bc_dinhky_df, 
        title_col="Tên Báo Cáo / Công Việc", 
        link_col="Link biểu mẫu", 
        btn_label="🔗 Tải biểu mẫu"
    )

    with st.expander("✏️ Chỉnh sửa Báo Cáo Định Kỳ"):
        edited_df = st.data_editor(
            st.session_state.bc_dinhky_df,
            num_rows="dynamic",
            use_container_width=True,
            column_order=["STT", "Tên Báo Cáo / Công Việc", "Tần suất", "Đơn vị nhận", "Link biểu mẫu", "Ghi chú"],
            key="edit_bc_expander"
        )
        if st.button("💾 Lưu Báo Cáo Định Kỳ", type="primary"):
            st.session_state.bc_dinhky_df = reindex_df(edited_df)
            st.success("Đã cập nhật Báo cáo định kỳ!")
            st.rerun()

    render_io_excel_tools(st.session_state.bc_dinhky_df, "bc", "DanhSach_BaoCao_DinhKy_TMT")

elif main_menu == "4 🟢 DS Gsheet_CV":
    st.subheader("🟢 Bảng Danh Sách Google Sheets_CV")

    render_perfect_table(
        st.session_state.gsheet_df, 
        title_col="Mô tả Google Sheet", 
        link_col="Link Google Sheet", 
        btn_label="🔗 Mở GSheet"
    )

    with st.expander("✏️ Chỉnh sửa danh sách Google Sheets"):
        edited_df = st.data_editor(
            st.session_state.gsheet_df,
            num_rows="dynamic",
            use_container_width=True,
            column_order=["STT", "Mô tả Google Sheet", "Link Google Sheet", "Ghi chú"],
            key="edit_gsheet_expander"
        )
        if st.button("💾 Lưu Google Sheets", type="primary"):
            st.session_state.gsheet_df = reindex_df(edited_df)
            st.success("Đã cập nhật danh sách Google Sheets!")
            st.rerun()

    render_io_excel_tools(st.session_state.gsheet_df, "gsheet", "DanhSach_Gsheet_TMT")
