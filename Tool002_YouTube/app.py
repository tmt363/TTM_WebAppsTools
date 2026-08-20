import streamlit as st

st.set_page_config(
    page_title="Tool YouTube - Quản lý & Xem Video",
    page_icon="▶️",
    layout="wide"
)

st.title("▶️ Quản Lý & Xem Video YouTube Công Việc")

if "yt_list" not in st.session_state:
    st.session_state.yt_list = []

# Sidebar thêm Video
with st.sidebar:
    st.header("➕ Thêm Video Mới")
    v_title = st.text_input("Tiêu đề Video")
    v_url = st.text_input("Link YouTube")
    if st.button("Lưu Video", type="primary", use_container_width=True):
        if v_title and v_url:
            st.session_state.yt_list.append({"title": v_title, "url": v_url, "notes": ""})
            st.toast("Đã thêm video!", icon="🎬")
            st.rerun()

# Giao diện chính
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📺 Trình Phát Video")
    yt_input = st.text_input("Hoặc dán trực tiếp link YouTube vào đây để xem ngay:")
    if yt_input:
        st.video(yt_input)
    elif st.session_state.yt_list:
        selected_vid = st.selectbox("Chọn video trong danh sách đã lưu:", [v["title"] for v in st.session_state.yt_list])
        curr = next(v for v in st.session_state.yt_list if v["title"] == selected_vid)
        st.video(curr["url"])
    else:
        st.info("Nhập link YouTube ở trên để xem video.")

with col_right:
    st.subheader("📝 Ghi Chú Trực Tiếp")
    note = st.text_area("Viết ghi chú quan trọng từ video...", height=250)
    if st.button("Lưu Ghi Chú"):
        st.toast("Đã lưu ghi chú thành công!", icon="✅")
