import streamlit as st
from yt_dlp import YoutubeDL
import pandas as pd
import io

st.set_page_config(page_title="Tạo Danh Sách Phát YouTube", page_icon="🎬", layout="wide")

st.title("🎬 Công Cụ Tạo & Tải Danh Sách Phát YouTube")
st.write("Dán link video hoặc danh sách phát YouTube vào bên dưới để tự động lấy dữ liệu.")

playlist_url = st.text_input("🔗 Nhập Link YouTube (Video hoặc Playlist):")

if st.button("🚀 Bắt đầu lấy dữ liệu"):
    if not playlist_url:
        st.warning("Vui lòng nhập đường link!")
    else:
        with st.spinner("Đang trích xuất dữ liệu từ YouTube..."):
            ydl_opts = {
                'extract_flat': True,
                'skip_download': True,
                'quiet': True,
            }
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(playlist_url, download=False)
                    
                videos = []
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            videos.append({
                                "Tên Video": entry.get('title'),
                                "Link Video": entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}",
                                "Thời lượng (giây)": entry.get('duration')
                            })
                else:
                    videos.append({
                        "Tên Video": info.get('title'),
                        "Link Video": info.get('webpage_url'),
                        "Thời lượng (giây)": info.get('duration')
                    })

                df = pd.DataFrame(videos)
                st.success(f"Đã tìm thấy {len(df)} video!")
                st.dataframe(df, use_container_width=True)

                # Xuất file Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='YouTube_Playlist')
                excel_data = output.getvalue()

                st.download_button(
                    label="📥 Tải về file Excel",
                    data=excel_data,
                    file_name="YouTube_Playlist_Data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Lỗi khi trích xuất: {e}")
