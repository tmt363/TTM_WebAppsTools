import streamlit as st
from urllib.parse import urlparse
import math

# Cấu hình trang
st.set_page_config(
    page_title="Work Portal & Ghi Chú 100 Trang",
    page_icon="🔖",
    layout="wide"
)

# Chỉnh lề tránh che tiêu đề
st.markdown("""
    <style>
        .block-container { padding-top: 2rem !important; }
    </style>
""", unsafe_allow_html=True)

# 1. KHỞI TẠO DỮ LIỆU
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = [
        {"id": 1, "title": "Hệ thống ERP", "url": "https://erp.com", "category": "Hệ thống", "color": "#3b82f6", "favorite": True},
        {"id": 2, "title": "Jira Software", "url": "https://jira.com", "category": "Quản lý", "color": "#10b981", "favorite": False},
        {"id": 3, "title": "Power BI Dashboard", "url": "https://powerbi.com", "category": "Báo cáo", "color": "#f59e0b", "favorite": True},
    ]

# Dữ liệu danh sách Ghi chú 100 Trang
if "notes_db" not in st.session_state:
    st.session_state.notes_db = [
        {"id": i, "title": f"Ghi chú tài liệu mục {i}", "content": f"Nội dung chi tiết quy trình hướng dẫn số {i}...", "page": (i % 100) + 1}
        for i in range(1, 15)  # Mẫu 14 mục ghi chú
    ]

if "edit_note_id" not in st.session_state:
    st.session_state.edit_note_id = None

def get_favicon(url):
    domain = urlparse(url).netloc or url
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=64"

# 2. TẠO TABS GIAO DIỆN
tab1, tab2 = st.tabs(["🔖 Work Portal", "📝 Ghi Chú Tài Liệu (Dàn 100 Trang)"])

# ================= TAB 1: BOOKMARK WORK PORTAL =================
with tab1:
    st.title("🔖 Trang Chủ Công Việc Cá Nhân")
    col_search, col_fav_filter = st.columns([4, 1])
    with col_search:
        search_query = st.text_input("🔍 Tìm kiếm website...", key="search_bm")
    with col_fav_filter:
        st.write("##")
        show_fav_only = st.checkbox("⭐ Chỉ hiện Yêu thích", key="fav_bm")

    filtered_list = st.session_state.bookmarks
    if search_query:
        filtered_list = [b for b in filtered_list if search_query.lower() in b["title"].lower() or search_query.lower() in b["url"].lower()]
    if show_fav_only:
        filtered_list = [b for b in filtered_list if b["favorite"]]

    st.divider()
    if not filtered_list:
        st.info("Không tìm thấy website nào.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(filtered_list):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"<div style='background-color: {item['color']}; height: 4px; border-radius: 2px; margin-bottom: 10px;'></div>", unsafe_allow_html=True)
                    c_icon, c_title, c_fav = st.columns([1, 4, 1])
                    with c_icon:
                        st.image(get_favicon(item["url"]), width=32)
                    with c_title:
                        st.markdown(f"**[{item['title']}]({item['url']})**")
                        st.caption(f"🏷️ {item['category']}")
                    with c_fav:
                        fav_icon = "⭐" if item["favorite"] else "☆"
                        if st.button(fav_icon, key=f"fav_{item['id']}"):
                            item["favorite"] = not item["favorite"]
                            st.rerun()

                    c_link, c_del = st.columns([3, 1])
                    with c_link:
                        st.markdown(f"[🔗 Truy cập]({item['url']})")
                    with c_del:
                        if st.button("🗑️", key=f"del_{item['id']}"):
                            st.session_state.bookmarks = [b for b in st.session_state.bookmarks if b["id"] != item["id"]]
                            st.rerun()

# ================= TAB 2: GHI CHÚ 100 TRANG & HIỆU CHỈNH =================
with tab2:
    st.title("📝 Quản Lý Ghi Chú Tài Liệu Dài")

    # BỘ PHÂN TRANG (Tối đa 100 trang)
    col_p1, col_p2 = st.columns([1, 3])
    with col_p1:
        current_page = st.number_input("📖 Chọn Trang (1 - 100)", min_value=1, max_value=100, value=1, step=1)
    
    st.markdown(f"### 📄 Danh Sách Ghi Chú - Trang {current_page}")

    # Lọc ghi chú theo Trang được chọn
    notes_on_page = [n for n in st.session_state.notes_db if n["page"] == current_page]

    if not notes_on_page:
        st.info(f"Trang {current_page} chưa có ghi chú nào. Hãy tạo mới bên sidebar!")
    else:
        for note in notes_on_page:
            with st.container(border=True):
                # NẾU ĐANG BẤM SỬA/HIỆU CHỈNH MỤC NÀY
                if st.session_state.edit_note_id == note["id"]:
                    st.subheader(f"🛠️ Hiệu Chỉnh Ghi Chú #{note['id']}")
                    edit_title = st.text_input("Tiêu đề", value=note["title"], key=f"edit_t_{note['id']}")
                    edit_content = st.text_area("Nội dung", value=note["content"], key=f"edit_c_{note['id']}")
                    
                    c_save, c_cancel = st.columns([1, 1])
                    with c_save:
                        if st.button("💾 Lưu Cập Nhật", key=f"save_btn_{note['id']}", type="primary"):
                            note["title"] = edit_title
                            note["content"] = edit_content
                            st.session_state.edit_note_id = None
                            st.toast("Đã hiệu chỉnh thành công!", icon="✅")
                            st.rerun()
                    with c_cancel:
                        if st.button("❌ Hủy", key=f"cancel_btn_{note['id']}"):
                            st.session_state.edit_note_id = None
                            st.rerun()
                else:
                    # HIỂN THỊ NỘI DUNG VÀ NÚT HIỆU CHỈNH
                    c_info, c_act = st.columns([4, 1])
                    with c_info:
                        st.markdown(f"**{note['title']}**")
                        st.write(note["content"])
                    with c_act:
                        if st.button("✏️ Hiệu Chỉnh", key=f"btn_edit_{note['id']}"):
                            st.session_state.edit_note_id = note["id"]
                            st.rerun()
                        if st.button("🗑️ Xóa", key=f"btn_del_note_{note['id']}"):
                            st.session_state.notes_db = [n for n in st.session_state.notes_db if n["id"] != note["id"]]
                            st.toast("Đã xóa mục ghi chú!", icon="🗑️")
                            st.rerun()

# ================= SIDEBAR CHUNG =================
with st.sidebar:
    st.header("➕ Thêm Mới Dữ Liệu")
    add_type = st.radio("Chọn loại thêm:", ["Website Bookmark", "Ghi Chú Tài Liệu"])

    if add_type == "Website Bookmark":
        b_title = st.text_input("Tên ứng dụng")
        b_url = st.text_input("URL")
        b_cat = st.text_input("Nhóm", value="Cơ bản")
        b_color = st.color_picker("Màu", "#3b82f6")
        b_fav = st.checkbox("Yêu thích ⭐")
        if st.button("Thêm Bookmark", type="primary", use_container_width=True):
            if b_title and b_url:
                new_id = max([b["id"] for b in st.session_state.bookmarks], default=0) + 1
                st.session_state.bookmarks.append({"id": new_id, "title": b_title, "url": b_url, "category": b_cat, "color": b_color, "favorite": b_fav})
                st.toast("Đã thêm Bookmark!", icon="✅")
                st.rerun()
    else:
        n_title = st.text_input("Tiêu đề Ghi Chú")
        n_content = st.text_area("Nội dung Ghi Chú")
        n_page = st.number_input("Gắn vào Trang (1-100)", min_value=1, max_value=100, value=1)
        if st.button("Lưu Ghi Chú", type="primary", use_container_width=True):
            if n_title and n_content:
                new_id = max([n["id"] for n in st.session_state.notes_db], default=0) + 1
                st.session_state.notes_db.append({"id": new_id, "title": n_title, "content": n_content, "page": int(n_page)})
                st.toast(f"Đã lưu vào Trang {n_page}!", icon="📝")
                st.rerun()
