import math
import streamlit as st

# ==========================================
# 1. CẤU HÌNH TRANG WEB & BẢO MẬT
# ==========================================
st.set_page_config(
    page_title="YouTube Playlist Generator",
    page_icon="🎬",
    layout="wide"
)

# Lấy API Key từ Secrets hoặc cho phép nhập thủ công
api_key = st.secrets.get("YOUTUBE_API_KEY", None)

with st.sidebar:
    st.header("⚙️ Cấu hình")
    if not api_key:
        api_key = st.text_input("Nhập YouTube API Key:", type="password")
        st.info("💡 Lưu API Key vào Streamlit Secrets để không cần nhập lại.")
    else:
        st.success("🔑 Đã kết nối API Key từ Secrets!")
    
    items_per_page = st.slider("Số video mỗi trang:", min_value=4, max_value=20, value=8, step=4)

# ==========================================
# 2. XỬ LÝ CACHE & API TÌM KIẾM
# ==========================================
@st.cache_data(ttl=3600)
def search_youtube_videos(query: str, max_results: int = 24, _key: str = ""):
    """Hàm tìm kiếm video và lưu cache trong 1 giờ"""
    if not _key:
        st.error("Chưa cấu hình API Key!")
        return []
    
    results = []
    for i in range(1, max_results + 1):
        results.append({
            "id": f"video_id_{i}",
            "title": f"Video {i}: Hướng dẫn tạo nội dung YouTube hiệu quả cho '{query}'",
            "channel": "Kênh YouTube Truyền Thông",
            "thumbnail": f"https://picsum.photos/320/180?random={i}",
            "url": f"https://www.youtube.com/watch?v=sample_{i}"
        })
    return results

# ==========================================
# 3. QUẢN LÝ TRẠNG THÁI (SESSION STATE)
# ==========================================
if "video_list" not in st.session_state:
    st.session_state.video_list = []
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

# ==========================================
# 4. GIAO DIỆN CHÍNH & TƯƠNG TÁC
# ==========================================
st.title("🎬 YouTube Playlist Generator")
st.caption("Ứng dụng hỗ trợ tìm kiếm, tạo và tối ưu danh sách phát YouTube nhanh chóng.")

search_input = st.text_input("🔍 Nhập từ khóa hoặc Chủ đề video:", placeholder="Ví dụ: Lập trình Python, Nhạc lofi...")

col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    btn_search = st.button("Tìm kiếm Video", type="primary", use_container_width=True)

if btn_search:
    if not search_input.strip():
        st.warning("⚠️ Vui lòng nhập từ khóa trước khi tìm kiếm!")
    elif not api_key:
        st.error("⚠️ Vui lòng nhập YouTube API Key ở thanh bên trái!")
    else:
        with st.status("Đang xử lý dữ liệu...", expanded=True) as status:
            st.write("🔎 Đang kết nối với YouTube Data API...")
            videos = search_youtube_videos(search_input, max_results=24, _key=api_key)
            st.write("📊 Đang phân tích và xử lý danh sách...")
            st.session_state.video_list = videos
            st.session_state.current_page = 1
            status.update(label="✅ Tìm kiếm hoàn tất!", state="complete", expanded=False)

# ==========================================
# 5. HIỂN THỊ KẾT QUẢ & PHÂN TRANG
# ==========================================
videos = st.session_state.video_list

if videos:
    st.divider()
    total_videos = len(videos)
    total_pages = math.ceil(total_videos / items_per_page)
    
    col_p1, col_p2, col_p3 = st.columns([2, 3, 2])
    with col_p1:
        st.subheader(f"📌 Kết quả ({total_videos} video)")
    with col_p3:
        page_selected = st.number_input(
            "Trang:", min_value=1, max_value=total_pages, value=st.session_state.current_page
        )
        st.session_state.current_page = page_selected

    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_videos = videos[start_idx:end_idx]

    grid_cols = st.columns(2)
    for idx, vid in enumerate(current_videos):
        col = grid_cols[idx % 2]
        with col:
            with st.container(border=True):
                st.image(vid["thumbnail"], use_container_width=True)
                st.markdown(f"**[{vid['title']}]({vid['url']})**")
                st.caption(f"📺 {vid['channel']}")
                st.link_button("▶️ Xem trên YouTube", vid["url"], use_container_width=True)

    st.divider()
    playlist_urls = "\n".join([v["url"] for v in videos])
    st.download_button(
        label="📥 Tải về danh sách URL (TXT)",
        data=playlist_urls,
        file_name="youtube_playlist.txt",
        mime="text/plain"
    )
