import streamlit as st
import pandas as pd
import os
import io

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & CUSTOM CSS
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

    /* 2. Cố định màu Sidebar */
    [data-testid="stSidebar"] {
        min-width: 260px !important;
        max-width: 280px !important;
        background-color: #1e293b !important;
        border-right: 1px solid #334155 !important;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* 3. Header Card tiêu đề */
    .header-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff !important;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    .header-card h1 {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }
    .version-badge {
        background-color: rgba(255,255,255,0.2);
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }

    /* 4. Định dạng Bảng HTML Responsive */
    .custom-table-container {
        width: 100%;
        overflow-x: auto;
        border: 1px solid #334155;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 13px;
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    .custom-table th {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        font-weight: 700;
        text-align: left;
        padding: 10px 12px;
        border-bottom: 2px solid #334155;
        white-space: nowrap;
    }
    .custom-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #334155;
        color: #f8fafc !important;
        vertical-align: middle;
    }
    .custom-table tr:hover {
        background-color: #1e293b !important;
    }

    /* Column Widths */
    .col-stt { width: 50px !important; text-align: center; font-weight: 600; color: #94a3b8 !important; }
    .col-title { width: 30% !important; font-weight: 600; }
    .col-links { width: 35% !important; }
    .col-note { width: auto !important; }

    /* Nút bấm liên kết nhiều Link */
    .btn-link-action {
        display: inline-block;
        background-color: #0284c7 !important;
        color: #ffffff !important;
        padding: 4px 10px;
        margin: 2px 4px 2px 0;
        border-radius: 4px;
        text-decoration: none !important;
        font-size: 12px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .btn-link-action:hover {
        background-color: #0369a1 !important;
        transform: translateY(-1px);
    }

    .path-box {
        background-color: #0f172a;
        border: 1px dashed #475569;
        padding: 8px;
        border-radius: 5px;
        font-size: 11px;
        word-break: break-all;
        color: #94a3b8 !important;
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
            <div style="background: #1e293b; padding: 25px; border-radius: 10px; border: 1px solid #334155; text-align: center;">
                <h3 style="color: #38bdf8; margin-bottom: 5px;">🛡️ HỆ THỐNG QUẢN LÝ AN TOÀN</h3>
                <span style="background: #0369a1; color: white; padding: 3px 10px; border-radius: 12px; font-weight: 600; font-size: 11px;">Version 2.0 (Multi-Link)</span>
                <hr style="border-color: #334155; margin: 15px 0;">
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
# 3. KHỞI TẠO ĐƯỜNG DẪN & DỮ LIỆU ĐA LINK MẶC ĐỊNH
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

LINK_COLS = ["Link 1", "Link 2", "Link 3", "Link 4", "Link 5"]

DEFAULT_WEBSITES = [
    {'STT': 1, 'Mô tả WEB': 'Hệ thống D-Office', 'Link 1': 'https://doffice.evn.com.vn', 'Link 2': '', 'Link 3': '', 'Link 4': '', 'Link 5': '', 'Ghi chú': 'Quản lý văn bản điều hành'},
    {'STT': 2, 'Mô tả WEB': 'Cổng thông tin Điện lực', 'Link 1': 'https://www.congcuweb.net/', 'Link 2': 'https://evnspc.vn', 'Link 3': '', 'Link 4': '', 'Link 5': '', 'Ghi chú': 'Tra cứu quy định & chỉ đạo'},
    {'STT': 3, 'Mô tả WEB': 'Quản lý an toàn', 'Link 1': 'https://giamsatantoan.evnspc.vn/Home/Index', 'Link 2': '', 'Link 3': '', 'Link 4': '', 'Link 5': '', 'Ghi chú': 'Giám sát an toàn SPC'},
    {'STT': 4, 'Mô tả WEB': 'Lịch tuần', 'Link 1': 'https://lichtuan.evnspc.vn', 'Link 2': '', 'Link 3': '', 'Link 4': '', 'Link 5': '', 'Ghi chú': 'Công ty Điện lực Tây Ninh'},
    {'STT': 5, 'Mô tả WEB': 'Hệ thống HRMS', 'Link 1': 'https://hrms.evn.com.vn', 'Link 2': '', 'Link 3': '', 'Link 4': '', 'Link 5': '', 'Ghi chú': 'Quản lý lao động tiền lương'},
    {'STT': 6, 'Mô tả WEB': 'Hệ thống PMIS', 'Link 1': 'https://pmis.evn.com.vn', 'Link 2': '', 'Link 3': '', 'Link 4': '', 'Link 5': '', 'Ghi chú': 'Quản lý vận hành thiết bị & lưới điện'},
    {'STT': 7, 'Mô tả WEB': 'Hệ thống E-Learning', 'Link 1': 'https://elearning.evn.com.vn', 'Link 2': '', 'Link 3': '', 'Link 4': '', 'Link 5': '', 'Ghi chú': 'Huấn luyện an toàn & thi trực tuyến'}
]

def reindex_df(df):
    if not df.empty:
        df = df.reset_index(drop=True)
        df["STT"] = df.index + 1
        # Đảm bảo đủ các cột Link 1 -> Link 5
        for col in LINK_COLS:
            if col not in df.columns:
                df[col] = ""
            else:
                df[col] = df[col].fillna("")
    return df

def to_excel_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='DATA')
    return output.getvalue()

# Load session state
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
                    st.session_state.data_store[cat] = reindex_df(pd.DataFrame(columns=["STT", "Thư mục / Hồ sơ"] + LINK_COLS + ["Ghi chú"]))
        except Exception:
            pass

    if not st.session_state.data_store:
        for cat in CATEGORIES:
            st.session_state.data_store[cat] = reindex_df(pd.DataFrame([
                {"STT": 1, "Thư mục / Hồ sơ": f"Hồ sơ {cat}", "Link 1": "https://drive.google.com", "Link 2": "", "Link 3": "", "Link 4": "", "Link 5": "", "Ghi chú": "Cập nhật định kỳ"}
            ]))

if "bc_dinhky_df" not in st.session_state:
    if os.path.exists(EXCEL_PATH_BC_DINH_KY):
        try:
            st.session_state.bc_dinhky_df = reindex_df(pd.read_excel(EXCEL_PATH_BC_DINH_KY))
        except Exception:
            pass
    if "bc_dinhky_df" not in st.session_state:
        st.session_state.bc_dinhky_df = reindex_df(pd.DataFrame([
            {"STT": 1, "Tên Báo Cáo / Công Việc": "Báo cáo công tác An toàn định kỳ Quý", "Tần suất": "Hàng Quý", "Đơn vị nhận": "Công ty Điện lực", "Link 1": "https://drive.google.com", "Link 2": "", "Link 3": "", "Link 4": "", "Link 5": "", "Ghi chú": "Nộp trước ngày 20 cuối quý"}
        ]))

if "gsheet_df" not in st.session_state:
    if os.path.exists(EXCEL_PATH_GSHEET):
        try:
            st.session_state.gsheet_df = reindex_df(pd.read_excel(EXCEL_PATH_GSHEET))
        except Exception:
            pass
    if "gsheet_df" not in st.session_state:
        st.session_state.gsheet_df = reindex_df(pd.DataFrame([
            {"STT": 1, "Mô tả Google Sheet": "Bảng Theo Dõi Công Việc Theo Tuần", "Link 1": "https://docs.google.com/spreadsheets", "Link 2": "", "Link 3": "", "Link 4": "", "Link 5": "", "Ghi chú": "Dùng chung phòng An Toàn"}
        ]))

# HEADER HỆ THỐNG
st.markdown("""
    <div class="header-card">
        <h1>🛡️ Hệ Thống Quản Lý An Toàn & Công Tác Chuyên Môn TMT</h1>
        <span class="version-badge">Version 2.0 (Hỗ trợ 5 Links)</span>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. SIDEBAR CHUYÊN NGHIỆP
# ---------------------------------------------------------
st.sidebar.markdown(f"👤 **Xin chào:** `{st.session_state.username}`")

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    if st.button("🚪 Đăng xuất", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

with col_btn2:
    if st.button("🧹 Xóa Cache", use_container_width=True, type="secondary"):
        st.cache_data.clear()
        st.toast("Đã xóa cache thành công!", icon="🎉")

st.sidebar.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("**📁 PHÂN MỤC CHÍNH**")

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

st.sidebar.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("**⚙️ Cấu Hình Thư Mục Lưu File:**")
st.sidebar.markdown(f'<div class="path-box">{EXCEL_DIR}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. HÀM DỰNG BẢNG HTML VỚI NHIỀU LINK TRUY CẬP
# ---------------------------------------------------------
def render_multi_link_table(df, title_col):
    rows_html = ""
    for idx, row in df.iterrows():
        stt = row.get("STT", idx + 1)
        title = row.get(title_col, "")
        note = row.get("Ghi chú", "")
        
        # Tạo chuỗi các nút bấm link
        links_html = ""
        for i, l_col in enumerate(LINK_COLS, 1):
            link_url = str(row.get(l_col, "")).strip()
            if link_url and link_url.lower() != "nan" and link_url != "None":
                links_html += f'<a class="btn-link-action" href="{link_url}" target="_blank">🔗 Link {i}</a>'
        
        if not links_html:
            links_html = '<span style="color: #64748b; font-style: italic;">Chưa có link</span>'

        rows_html += f'''
        <tr>
            <td class="col-stt">{stt}</td>
            <td class="col-title">{title}</td>
            <td class="col-links">{links_html}</td>
            <td class="col-note">{note}</td>
        </tr>
        '''

    full_table_html = f'''
    <div class="custom-table-container">
        <table class="custom-table">
            <thead>
                <tr>
                    <th class="col-stt">STT</th>
                    <th class="col-title">{title_col}</th>
                    <th class="col-links">Các Link truy cập</th>
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
# 6. HIỂN THỊ DỮ LIỆU VÀ FORM CHỈNH SỬA
# ---------------------------------------------------------
def render_excel_import_export(df, current_key, file_prefix):
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
    
    render_multi_link_table(st.session_state.web_tools_df, title_col="Mô tả WEB")

    col_rst1, col_rst2 = st.columns([3, 1])
    with col_rst2:
        if st.button("🔄 Khôi phục mặc định", type="secondary"):
            st.session_state.web_tools_df = reindex_df(pd.DataFrame(DEFAULT_WEBSITES))
            st.toast("Đã khôi phục dữ liệu mặc định!", icon="🎉")
            st.rerun()

    with st.expander("✏️ Chỉnh sửa / Bổ sung thêm Link cho các mục"):
        edited_df = st.data_editor(
            st.session_state.web_tools_df,
            num_rows="dynamic",
            use_container_width=True,
            column_order=["STT", "Mô tả WEB"] + LINK_COLS + ["Ghi chú"],
            key="edit_web_expander"
        )
        if st.button("💾 Lưu thay đổi", type="primary"):
            st.session_state.web_tools_df = reindex_df(edited_df)
            st.success("Đã cập nhật danh sách thành công!")
            st.rerun()

    render_excel_import_export(st.session_state.web_tools_df, "web", "1_DS_WEBsites_CV")

elif main_menu == "2 📋 DM QL Files_CV":
    selected_cat = st.sidebar.selectbox("📂 Chọn mảng công việc:", CATEGORIES)
    if selected_cat:
        st.subheader(f"📂 Quản Lý Hồ Sơ: {selected_cat}")
        current_df = st.session_state.data_store[selected_cat]

        render_multi_link_table(current_df, title_col="Thư mục / Hồ sơ")

        with st.expander(f"✏️ Chỉnh sửa / Bổ sung Link mảng {selected_cat}"):
            edited_df = st.data_editor(
                current_df,
                num_rows="dynamic",
                use_container_width=True,
                column_order=["STT", "Thư mục / Hồ sơ"] + LINK_COLS + ["Ghi chú"],
                key=f"edit_cat_{selected_cat}"
            )
            if st.button("💾 Lưu thay đổi mảng này", type="primary"):
                st.session_state.data_store[selected_cat] = reindex_df(edited_df)
                st.success("Đã cập nhật dữ liệu!")
                st.rerun()

        render_excel_import_export(current_df, selected_cat, f"HoSo_{selected_cat}")

elif main_menu == "3 📊 DS BCdinhky_CV":
    st.subheader("📊 Bảng Danh Sách Báo Cáo Định Kỳ & Công Việc")

    render_multi_link_table(st.session_state.bc_dinhky_df, title_col="Tên Báo Cáo / Công Việc")

    with st.expander("✏️ Chỉnh sửa / Bổ sung Link Báo Cáo"):
        edited_df = st.data_editor(
            st.session_state.bc_dinhky_df,
            num_rows="dynamic",
            use_container_width=True,
            column_order=["STT", "Tên Báo Cáo / Công Việc", "Tần suất", "Đơn vị nhận"] + LINK_COLS + ["Ghi chú"],
            key="edit_bc_expander"
        )
        if st.button("💾 Lưu Báo Cáo Định Kỳ", type="primary"):
            st.session_state.bc_dinhky_df = reindex_df(edited_df)
            st.success("Đã cập nhật Báo cáo định kỳ!")
            st.rerun()

    render_excel_import_export(st.session_state.bc_dinhky_df, "bc", "DanhSach_BaoCao_DinhKy_TMT")

elif main_menu == "4 🟢 DS Gsheet_CV":
    st.subheader("🟢 Bảng Danh Sách Google Sheets_CV")

    render_multi_link_table(st.session_state.gsheet_df, title_col="Mô tả Google Sheet")

    with st.expander("✏️ Chỉnh sửa / Bổ sung Link Google Sheets"):
        edited_df = st.data_editor(
            st.session_state.gsheet_df,
            num_rows="dynamic",
            use_container_width=True,
            column_order=["STT", "Mô tả Google Sheet"] + LINK_COLS + ["Ghi chú"],
            key="edit_gsheet_expander"
        )
        if st.button("💾 Lưu Google Sheets", type="primary"):
            st.session_state.gsheet_df = reindex_df(edited_df)
            st.success("Đã cập nhật danh sách Google Sheets!")
            st.rerun()

    render_excel_import_export(st.session_state.gsheet_df, "gsheet", "DanhSach_Gsheet_TMT")
