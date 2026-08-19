import streamlit as st
import datetime

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Tool_001_QL Bookmark - Quản lý liên kết",
    page_icon="📌",
    layout="wide"
)

st.title("📌 Tool 001 - Quản lý Bookmark & Ghi chú Website")

# 2. KHỞI TẠO DỮ LIỆU BAN ĐẦU
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = [
        {"title": "Streamlit Cloud", "url": "https://share.streamlit.io", "category": "Công cụ"},
        {"title": "GitHub", "url": "https://github.com", "category": "Lập trình"}
    ]

# 3. THÊM BOOKMARK MỚI
with st.sidebar:
    st.header("➕ Thêm Bookmark Mới")
    new_title = st.text_input("Tên Trang Web")
    new_url = st.text_input("Đường dẫn (URL)")
    new_cat = st.selectbox("Danh mục", ["Công cụ", "Lập trình", "Giải trí", "Khác"])
    
    if st.button("Lưu Bookmark", type="primary"):
        if new_title and new_url:
            st.session_state.bookmarks.append({
                "title": new_title,
                "url": new_url,
                "category": new_cat
            })
            st.success("Đã thêm thành công!")
            st.rerun()
        else:
            st.warning("Vui lòng điền đủ Tên và URL!")

# 4. HIỂN THỊ DANH SÁCH BOOKMARK
st.subheader("📋 Danh sách liên kết đã lưu")
if st.session_state.bookmarks:
    for idx, item in enumerate(st.session_state.bookmarks):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"**[{item['title']}]({item['url']})**")
        with col2:
            st.caption(f"Danh mục: {item['category']}")
        with col3:
            if st.button("❌ Xóa", key=f"del_{idx}"):
                st.session_state.bookmarks.pop(idx)
                st.rerun()
else:
    st.info("Chưa có bookmark nào được lưu.")
