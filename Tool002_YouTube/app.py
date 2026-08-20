import streamlit as st
import datetime
import json
import pandas as pd
import io
import yt_dlp

# ------------------------------------------
# 1. CẤU HÌNH TRANG WEB TOÀN MÀN HÌNH
# ------------------------------------------
st.set_page_config(
    page_title="Tool002 - YouTube Playlist Extractor",
    page_icon="▶️",
    layout="wide"
)

# ------------------------------------------
# 2. KHỞI TẠO DỮ LIỆU & TRẠNG THÁI
# ------------------------------------------
if "yt_playlists" not in st.session_state:
    st.session_state.yt_playlists = []

if "edit_note_key" not in st.session_state:
    st.session_state.edit_note_key = None

if "add_note_idx" not in st.session_state:
    st.session_state.add_note_idx = None

st.title("▶️ Tool 002 - Trích Xuất Playlist YouTube")
st.caption("Ứng dụng tự động lấy toàn bộ danh sách Video từ Link Playlist YouTube & Quản lý ghi chú.")

# ------------------------------------------
# 3. HÀM CÀO DỮ LIỆU PLAYLIST BẰNG YT-DLP
# ------------------------------------------
def extract_youtube_playlist(playlist_url):
    ydl_opts = {
        'extract_flat': True,  # Lấy thông tin nhanh không cần tải video
        'skip_download': True,
        'quiet': True
    }
    videos = []
    playlist_title = "YouTube Playlist"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if 'title' in info:
            playlist_title = info['title']
            
        if 'entries' in info:
            for idx, entry in enumerate(info['entries']):
                if entry:
                    v_id = entry.get('id', '')
                    v_title = entry.get('title', f'Video #{idx+1}')
                    v_url = entry.get('url') or f"https://www.youtube.com/watch?v={v_id}"
                    duration_sec = entry.get('duration', 0)
                    uploader = entry.get('uploader', 'N/A')
                    
                    # Quy đổi giây sang phút:giây
                    mins, secs = divmod(duration_sec or 0, 60)
                    time_str = f"{int(mins)}p {int(secs)}s" if duration_sec else "N/A"
                    
                    videos.append({
                        "stt": idx + 1,
                        "title": v_title,
                        "url": v_url,
                        "duration": time_str,
                        "uploader": uploader
                    })
    return playlist_title, videos

# ------------------------------------------
# 4. KHUNG TRÍCH XUẤT PLAYLIST
# ------------------------------------------
with st.expander("🚀 **Trích Xuất Playlist Mới (Bấm để mở)**", expanded=True):
    with st.form("extract_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            cat_input = st.selectbox("Danh mục phân loại:", ["Học tập", "Công việc", "Giải trí", "Âm nhạc", "Khác"])
            custom_title = st.text_input("Tên tùy chỉnh (Để trống sẽ lấy tên gốc):")
        with col2:
            url_input = st.text_input("Dán Link Playlist YouTube vào đây:", placeholder="https://www.youtube.com/playlist?list=PL...")
            
        btn_submit = st.form_submit_button("⚡ Trích Xuất Ngay", type="primary", use_container_width=True)
        
        if btn_submit:
            if not url_input.strip():
                st.error("⚠️ Vui lòng dán đường dẫn Playlist YouTube!")
            else:
                with st.spinner("⏳ Đang cào dữ liệu từ YouTube, vui lòng đợi vài giây..."):
                    try:
                        pl_title, v_list = extract_youtube_playlist(url_input.strip())
                        final_title = custom_title.strip() if custom_title.strip() else pl_title
                        
                        if v_list:
                            new_pl = {
                                "category": cat_input,
                                "title": final_title,
                                "url": url_input.strip(),
                                "videos": v_list,
                                "notes": [],
                                "date": str(datetime.date.today())
                            }
                            st.session_state.yt_playlists.append(new_pl)
                            st.success(f"🎉 Đã lấy thành công {len(v_list)} video từ '{final_title}'!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Không tìm thấy video nào trong Playlist này. Hãy kiểm tra lại link (cần là link công khai)!")
                    except Exception as e:
                        st.error(f"❌ Lỗi trích xuất: {e}")

st.divider()

# ------------------------------------------
# 5. HIỂN THỊ DANH SÁCH PLAYLIST VÀ VIDEO
# ------------------------------------------
if not st.session_state.yt_playlists:
    st.info("💡 Chưa có Playlist nào được trích xuất. Hãy dán link ở trên để bắt đầu!")
else:
    for idx, item in enumerate(st.session_state.yt_playlists):
        with st.container(border=True):
            # TẦNG 1: THÔNG TIN PLAYLIST
            c1, c2, c3, c4, c5 = st.columns([0.5, 1.2, 3.5, 1.5, 1])
            with c1:
                st.subheader(f"#{idx+1}")
            with c2:
                st.caption(f"🏷️ **{item['category']}**")
                st.caption(f"📅 {item['date']}")
            with c3:
                st.subheader(f"🎬 {item['title']}")
                st.caption(f"Tổng số: **{len(item['videos'])} video**")
            with c4:
                st.link_button("🚀 Mở trên YouTube", item['url'], use_container_width=True)
            with c5:
                if st.button("🗑️ Xóa", key=f"del_pl_{idx}", use_container_width=True):
                    st.session_state.yt_playlists.pop(idx)
                    st.rerun()

            # DANH SÁCH VIDEO TRONG PLAYLIST
            with st.expander(f"📋 **Xem danh sách {len(item['videos'])} Video chi tiết**"):
                # Chuyển dữ liệu video thành Bảng DataFrame đẹp mắt
                df_v = pd.DataFrame(item['videos'])
                df_v.columns = ["STT", "Tên Video", "Đường Dẫn URL", "Thời Lượng", "Kênh YouTube"]
                st.dataframe(df_v, use_container_width=True, hide_index=True)

            # TẦNG 2: GHI CHÚ
            st.markdown("**📝 Ghi chú Playlist:**")
            notes_data = item.get("notes", [])
            for n_idx, n_item in enumerate(notes_data):
                nc1, nc2 = st.columns([10, 1])
                with nc1:
                    st.info(f"📌 **{n_item['text']}** *(⏱️ {n_item['date']})*")
                with nc2:
                    if st.button("🗑️", key=f"del_n_{idx}_{n_idx}"):
                        item["notes"].pop(n_idx)
                        st.rerun()

            if st.session_state.add_note_idx == idx:
                new_n_text = st.text_area("Nhập ghi chú mới:", key=f"area_add_{idx}")
                if st.button("💾 Lưu Ghi Chú", type="primary", key=f"save_add_{idx}"):
                    if new_n_text.strip():
                        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        item["notes"].append({"text": new_n_text.strip(), "date": now_str})
                        st.session_state.add_note_idx = None
                        st.rerun()
            else:
                if st.button("➕ Thêm ghi chú", key=f"btn_add_n_{idx}"):
                    st.session_state.add_note_idx = idx
                    st.rerun()

# ------------------------------------------
# 6. XUẤT FILE EXCEL CHUẨN ĐẸP (.XLSX)
# ------------------------------------------
st.divider()
st.subheader("⚙️ Xuất Dữ Liệu Ra File Excel (.xlsx)")

if st.session_state.yt_playlists:
    export_rows = []
    for pl in st.session_state.yt_playlists:
        notes_str = " | ".join([f"[{n['date']}] {n['text']}" for n in pl.get("notes", [])])
        for v in pl.get("videos", []):
            export_rows.append({
                "Danh mục": pl["category"],
                "Tên Playlist": pl["title"],
                "STT": v["stt"],
                "Tên Video": v["title"],
                "Thời Lượng": v["duration"],
                "Kênh YouTube": v["uploader"],
                "Link Video": v["url"],
                "Ghi chú Playlist": notes_str,
                "Ngày trích xuất": pl["date"]
            })
            
    df_export = pd.DataFrame(export_rows)
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_export.to_excel(writer, index=False, sheet_name='YouTube_Playlist')
        
    st.download_button(
        label="📊 Tải Về File Excel (.xlsx Chuẩn Không Lỗi Phông)",
        data=buffer.getvalue(),
        file_name="danh_sach_playlist_youtube.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )
