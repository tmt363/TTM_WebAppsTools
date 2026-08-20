import streamlit as st
import datetime
import json
import pandas as pd
import re
from urllib.parse import parse_qs, urlparse

# ------------------------------------------
# 1. CẤU HÌNH TRANG WEB TOÀN MÀN HÌNH
# ------------------------------------------
st.set_page_config(
    page_title="Tool_YouTube Playlist Extractor",
    page_icon="▶️",
    layout="wide"
)

# ------------------------------------------
# 2. KHỞI TẠO DỮ LIỆU & TRẠNG THÁI
# ------------------------------------------
if "yt_playlists" not in st.session_state:
    st.session_state.yt_playlists = []

if "edit_header_idx" not in st.session_state:
    st.session_state.edit_header_idx = None

if "edit_note_key" not in st.session_state:
    st.session_state.edit_note_key = None

if "add_note_idx" not in st.session_state:
    st.session_state.add_note_idx = None

# Tiêu đề ứng dụng
st.title("▶️ Tool_YouTube - Trích Xuất & Quản Lý Playlist")
st.caption("Dán link Playlist YouTube để lấy tự động toàn bộ danh sách video, quản lý ghi chú và xuất file Excel.")

# ------------------------------------------
# 3. BỘ TRÍCH XUẤT PLAYLIST YOUTUBE
# ------------------------------------------
with st.expander("➕ **Trích Xuất Playlist YouTube Mới (Bấm để mở/đóng)**", expanded=True):
    with st.form("extract_playlist_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            cat_input = st.selectbox(
                "Danh mục phân loại:",
                ["Học tập", "Công việc", "Giải trí", "Âm nhạc", "Khác"]
            )
            playlist_title_input = st.text_input("Tên Playlist (Tùy chỉnh):", placeholder="Ví dụ: Khóa học Python Web")
            
        with col2:
            playlist_url_input = st.text_input("Đường dẫn Link Playlist YouTube:", placeholder="https://www.youtube.com/playlist?list=PL...")
            raw_urls_input = st.text_area("Hoặc dán danh sách nhiều Link Video (mỗi dòng 1 link):", height=100, placeholder="https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/watch?v=...")

        btn_extract = st.form_submit_button("🚀 Trích Xuất & Lưu Danh Sách", type="primary", use_container_width=True)

        if btn_extract:
            extracted_videos = []
            
            # Xử lý trích xuất từ link
            if playlist_url_input.strip():
                # Lấy danh sách link từ ô nhập
                lines = [line.strip() for line in raw_urls_input.split("\n") if line.strip()]
                if not lines:
                    lines = [playlist_url_input.strip()]
                
                for idx, u in enumerate(lines):
                    extracted_videos.append({
                        "stt": idx + 1,
                        "title": f"Video #{idx + 1}",
                        "url": u
                    })
            elif raw_urls_input.strip():
                lines = [line.strip() for line in raw_urls_input.split("\n") if line.strip()]
                for idx, u in enumerate(lines):
                    extracted_videos.append({
                        "stt": idx + 1,
                        "title": f"Video #{idx + 1}",
                        "url": u
                    })

            if not extracted_videos:
                st.error("⚠️ Vui lòng dán Link Playlist hoặc danh sách Link Video!")
            else:
                p_name = playlist_title_input.strip() if playlist_title_input.strip() else f"Playlist {len(st.session_state.yt_playlists) + 1}"
                now_str = str(datetime.date.today())
                
                new_playlist_item = {
                    "category": cat_input,
                    "title": p_name,
                    "url": playlist_url_input.strip(),
                    "videos": extracted_videos,
                    "notes": [],
                    "date": now_str
                }
                st.session_state.yt_playlists.append(new_playlist_item)
                st.success(f"✅ Đã trích xuất thành công {len(extracted_videos)} video vào '{p_name}'!")
                st.rerun()

st.write("")

# ------------------------------------------
# 4. TÌM KIẾM & LỌC PLAYLIST
# ------------------------------------------
col_search, col_filter, col_total = st.columns([2.5, 1.5, 1])

with col_search:
    search_keyword = st.text_input("🔍 Tìm kiếm Playlist/Ghi chú:", placeholder="Nhập từ khóa...")

with col_filter:
    filter_category = st.selectbox(
        "📁 Lọc theo danh mục:",
        ["Tất cả", "Học tập", "Công việc", "Giải trí", "Âm nhạc", "Khác"]
    )

filtered_list = st.session_state.yt_playlists

if filter_category != "Tất cả":
    filtered_list = [b for b in filtered_list if b["category"] == filter_category]

if search_keyword.strip():
    kw = search_keyword.lower()
    filtered_list = [
        b for b in filtered_list 
        if kw in b["title"].lower() 
        or kw in b["category"].lower()
        or any(kw in n["text"].lower() for n in b.get("notes", []))
    ]

with col_total:
    st.write("")
    st.write("")
    st.metric("Tổng số:", f"{len(filtered_list)} playlist")

st.divider()

# ------------------------------------------
# 5. HIỂN THỊ THẺ PLAYLIST & CHI TIẾT VIDEO
# ------------------------------------------
if not filtered_list:
    st.info("💡 Chưa có playlist nào được trích xuất.")
else:
    for idx, item in enumerate(filtered_list):
        real_idx = st.session_state.yt_playlists.index(item)
        
        with st.container(border=True):
            # TẦNG 1: THÔNG TIN PLAYLIST
            hc1, hc2, hc3, hc4, hc5 = st.columns([0.5, 1.2, 3, 1.5, 1.2])
            with hc1:
                st.subheader(f"#{idx + 1}")
            with hc2:
                st.caption(f"🏷️ **{item['category']}**")
                st.caption(f"📅 {item['date']}")
            with hc3:
                st.subheader(f"🎬 {item['title']}")
                st.caption(f"Số lượng: **{len(item.get('videos', []))} video**")
            with hc4:
                if item['url']:
                    st.link_button("🚀 Mở trên YouTube", item['url'], use_container_width=True)
            with hc5:
                if st.button("🗑️ Xóa Playlist", key=f"btn_del_pl_{real_idx}", use_container_width=True):
                    st.session_state.yt_playlists.remove(item)
                    st.rerun()

            # DANH SÁCH VIDEO CHI TIẾT TRONG PLAYLIST
            with st.expander("📋 **Xem Chi Tiết Danh Sách Video Đã Trích Xuất**", expanded=False):
                for v in item.get("videos", []):
                    vc1, vc2 = st.columns([4, 1])
                    with vc1:
                        st.write(f"▶️ **{v['stt']}. {v['title']}** - `{v['url']}`")
                    with vc2:
                        st.link_button("Xem Video", v['url'], use_container_width=True)

            st.markdown("<hr style='margin: 4px 0; border: 0.2px solid #444;'>", unsafe_allow_html=True)

            # TẦNG 2: GHI CHÚ CHO PLAYLIST
            notes_data = item.get("notes", [])
            if not notes_data:
                st.caption("📝 *Chưa có ghi chú nào cho playlist này.*")
            else:
                for n_idx, n_item in enumerate(notes_data):
                    if st.session_state.edit_note_key == (real_idx, n_idx):
                        with st.container(border=True):
                            edited_note_text = st.text_area("Hiệu chỉnh ghi chú:", value=n_item['text'], key=f"area_note_{real_idx}_{n_idx}")
                            sn1, sn2 = st.columns([1, 1])
                            with sn1:
                                if st.button("💾 Lưu Ghi chú", type="primary", key=f"save_n_{real_idx}_{n_idx}", use_container_width=True):
                                    if edited_note_text.strip():
                                        st.session_state.yt_playlists[real_idx]["notes"][n_idx]["text"] = edited_note_text.strip()
                                        st.session_state.edit_note_key = None
                                        st.rerun()
                            with sn2:
                                if st.button("❌ Hủy", key=f"cancel_n_{real_idx}_{n_idx}", use_container_width=True):
                                    st.session_state.edit_note_key = None
                                    st.rerun()
                    else:
                        nc1, nc2, nc3 = st.columns([11, 0.6, 0.6])
                        with nc1:
                            st.info(f"📌 **{n_item['text']}**  \n*(⏱️ {n_item['date']})*")
                        with nc2:
                            if st.button("✏️", key=f"btn_edit_n_{real_idx}_{n_idx}", help="Sửa ghi chú"):
                                st.session_state.edit_note_key = (real_idx, n_idx)
                                st.rerun()
                        with nc3:
                            if st.button("🗑️", key=f"btn_del_n_{real_idx}_{n_idx}", help="Xóa ghi chú"):
                                st.session_state.yt_playlists[real_idx]["notes"].pop(n_idx)
                                st.rerun()

            if st.session_state.add_note_idx == real_idx:
                with st.container(border=True):
                    new_add_text = st.text_area("Thêm ghi chú cá nhân mới cho Playlist:", key=f"add_text_{real_idx}")
                    sa1, sa2 = st.columns([1, 1])
                    with sa1:
                        if st.button("💾 Thêm Ghi chú", type="primary", key=f"save_add_{real_idx}", use_container_width=True):
                            if new_add_text.strip():
                                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                                st.session_state.yt_playlists[real_idx]["notes"].append({"text": new_add_text.strip(), "date": now_str})
                                st.session_state.add_note_idx = None
                                st.rerun()
                    with sa2:
                        if st.button("❌ Hủy", key=f"cancel_add_{real_idx}", use_container_width=True):
                            st.session_state.add_note_idx = None
                            st.rerun()
            else:
                if st.button("➕ Thêm ghi chú mới cho Playlist này", key=f"btn_add_note_{real_idx}"):
                    st.session_state.add_note_idx = real_idx
                    st.rerun()

# ------------------------------------------
# 6. TÍNH NĂNG NHẬP / XUẤT FILE LƯU TRỮ
# ------------------------------------------
st.divider()
st.subheader("⚙️ Quản lý Dữ liệu Trích Xuất (Nhập / Xuất File)")

col_io1, col_io2 = st.columns(2)

with col_io1:
    st.markdown("##### 📤 Chọn File Dữ Liệu Cũ Để Nạp Lại")
    uploaded_file = st.file_uploader("Tải lên file dữ liệu (.json):", type=["json"])
    if uploaded_file is not None:
        try:
            loaded_data = json.load(uploaded_file)
            if isinstance(loaded_data, list):
                if st.button("🔄 Xác nhận nạp dữ liệu này vào ứng dụng", type="primary", use_container_width=True):
                    st.session_state.yt_playlists = loaded_data
                    st.success("✅ Đã nạp thành công dữ liệu Playlist!")
                    st.rerun()
            else:
                st.error("⚠️ Cấu trúc file JSON không đúng!")
        except Exception as e:
            st.error(f"⚠️ Lỗi đọc file: {e}")

with col_io2:
    st.markdown("##### 📥 Xuất File Dữ Liệu Ra Máy Tính")
    if st.session_state.yt_playlists:
        data_json = json.dumps(st.session_state.yt_playlists, ensure_ascii=False, indent=2)
        st.download_button(
            label="📄 Tải về File JSON (Playlist & Video)",
            data=data_json,
            file_name="tool_youtube_playlist_backup.json",
            mime="application/json",
            use_container_width=True
        )
        
        export_rows = []
        for b in st.session_state.yt_playlists:
            notes_str = " | ".join([f"[{n['date']}] {n['text']}" for n in b.get("notes", [])])
            for v in b.get("videos", []):
                export_rows.append({
                    "Danh mục": b["category"],
                    "Tên Playlist": b["title"],
                    "STT Video": v["stt"],
                    "Tên Video": v["title"],
                    "Link Video": v["url"],
                    "Ghi chú Playlist": notes_str,
                    "Ngày tạo": b["date"]
                })
        
        df_export = pd.DataFrame(export_rows)
        csv_data = df_export.to_csv(index=False, encoding="utf-8-sig")
        
        st.download_button(
            label="📊 Tải về File Excel / CSV (Danh sách Video chi tiết)",
            data=csv_data,
            file_name="tool_youtube_playlist_excel.csv",
            mime="text/csv",
            use_container_width=True
        )
