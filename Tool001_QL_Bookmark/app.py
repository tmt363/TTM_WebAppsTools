import streamlit as st
from urllib.parse import urlparse

# Cấu hình trang
st.set_page_config(
    page_title="Work Portal - Quản lý Bookmark Công Việc",
    page_icon="🔖",
    layout="wide"
)

# Khởi tạo dữ liệu Bookmark chuẩn
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = [
        {"id": 1, "title": "Hệ thống ERP", "url": "https://erp.com", "category": "Hệ thống", "color": "#3b82f6", "favorite": True},
        {"id": 2, "title": "Jira Software", "url": "https://jira.com", "category": "Quản lý", "color": "#10b981", "favorite": False},
        {"id": 3, "title": "Power BI Dashboard", "url": "https://powerbi.com", "category": "Báo cáo", "color": "#f59e0b", "favorite": True},
    ]

# Hàm hỗ trợ lấy Favicon
def get_favicon(url):
    domain = urlparse(url).netloc or url
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=64"

# Header & Thanh tìm kiếm
st.title("🔖 Trang Chủ Công Việc Cá Nhân")

col_search, col_fav_filter = st.columns([4, 1])
with col_search:
    search_query = st.text_input("🔍 Tìm kiếm website, ứng dụng...", placeholder="Gõ tên hoặc đường dẫn...")
with col_fav_filter:
    st.write("##")
    show_fav_only = st.checkbox("⭐ Chỉ hiện Yêu thích")

# Sidebar - Thêm Bookmark mới
with st.sidebar:
    st.header("➕ Thêm Website Công Việc")
    title = st.text_input("Tên ứng dụng (ERP, CRM, Jira...)")
    url = st.text_input("Đường dẫn (URL)")
    category = st.text_input("Nhóm ứng dụng", value="Cơ bản")
    color = st.color_picker("Màu đại diện nhóm", "#3b82f6")
    is_fav = st.checkbox("Đánh dấu yêu thích ⭐")

    if st.button("Thêm vào danh sách", type="primary", use_container_width=True):
        if title and url:
            if not url.startswith("http"):
                url = "https://" + url
            new_id = max([b["id"] for b in st.session_state.bookmarks], default=0) + 1
            st.session_state.bookmarks.append({
                "id": new_id, "title": title, "url": url, 
                "category": category, "color": color, "favorite": is_fav
            })
            st.toast("Đã thêm thành công!", icon="✅")
            st.rerun()
        else:
            st.warning("Vui lòng điền đầy đủ Tên và URL!")

# Lọc dữ liệu
filtered_list = st.session_state.bookmarks
if search_query:
    filtered_list = [b for b in filtered_list if search_query.lower() in b["title"].lower() or search_query.lower() in b["url"].lower()]
if show_fav_only:
    filtered_list = [b for b in filtered_list if b["favorite"]]

# Hiển thị Card Dashboard
st.divider()
if not filtered_list:
    st.info("Không tìm thấy website nào phù hợp.")
else:
    cols = st.columns(3)
    for idx, item in enumerate(filtered_list):
        with cols[idx % 3]:
            # Tạo card kiểu dáng đẹp có thanh màu phân loại
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
                    st.markdown(f"[🔗 Truy cập ngay]({item['url']})")
                with c_del:
                    if st.button("🗑️", key=f"del_{item['id']}"):
                        st.session_state.bookmarks = [b for b in st.session_state.bookmarks if b["id"] != item["id"]]
                        st.rerun()
