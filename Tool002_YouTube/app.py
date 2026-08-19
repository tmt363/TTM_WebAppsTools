import streamlit as st

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Tool_002_YouTube - Công cụ YouTube",
    page_icon="▶️",
    layout="wide"
)

st.title("▶️ Tool 002 - Quản lý & Xem YouTube")

# 2. BỘ XEM VÀ PHÂN TÍCH VIDEO YOUTUBE
yt_url = st.text_input("Nhập link Video YouTube (ví dụ: https://www.youtube.com/watch?v=...):")

if yt_url:
    try:
        st.video(yt_url)
        st.success("Tải video thành công!")
    except Exception as e:
        st.error("Link video không hợp lệ, vui lòng kiểm tra lại!")

st.divider()

# 3. GHI CHÚ NHANH KHI XEM VIDEO
st.subheader("📝 Ghi chú nội dung Video")
note = st.text_area("Nhập nội dung ghi chú:", height=150)
if st.button("Lưu Ghi Chú"):
    if note:
        st.toast("Đã lưu ghi chú thành công!", icon="✅")
    else:
        st.warning("Vui lòng nhập nội dung ghi chú!")
