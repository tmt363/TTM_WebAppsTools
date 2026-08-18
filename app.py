import io
import re
import subprocess
import pandas as pd
import streamlit as st

# Tự động cài đặt thư viện xlsxwriter nếu chưa có
try:
    import xlsxwriter
except ImportError:
    subprocess.run(["pip", "install", "xlsxwriter", "-q"])
    import xlsxwriter

from yt_dlp import YoutubeDL

# 1. Cấu hình giao diện
st.set_page_config(
    page_title="TTM_make_Youtube_playlists", page_icon="🎬", layout="centered"
)

st.title("🎬 TTM_make_Youtube_playlists")
st.write("Cào dữ liệu YouTube và xuất file Excel chuẩn 100%.")

url = st.text_input(
    "1. Dán đường link YouTube vào đây:",
    placeholder="https://www.youtube.com/playlist?list=...",
)
filename_input = st.text_input(
    "2. Đặt tên file Excel muốn lưu:", value="TTM_Youtube_Data"
)


# 2. Hàm cào dữ liệu
def get_youtube_data(link):
    ydl_opts = {
        "extract_flat": True,
        "skip_download": True,
        "quiet": True,
        "ignoreerrors": True,
    }
    results = []
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(link, download=False)
            if not info:
                return None, "❌ Link không hợp lệ hoặc Playlist không tồn tại!"
            if "entries" in info:
                for idx, entry in enumerate(info["entries"], 1):
                    if entry:
                        v_id = entry.get("id")
                        v_title = entry.get("title", "Không có tiêu đề")
                        v_duration = entry.get("duration", 0)
                        mins, secs = divmod(int(v_duration or 0), 60)
                        duration_str = f"{mins:02d}:{secs:02d}"
                        v_url = entry.get("url", "")
                        if not v_url.startswith("http"):
                            v_url = (
                                f"https://www.youtube.com/watch?v={v_id}"
                                if v_id
                                else "N/A"
                            )
                        results.append(
                            {
                                "STT": idx,
                                "Tên Video/Playlist": v_title,
                                "Thời lượng": duration_str,
                                "ID": v_id or "N/A",
                                "Link": v_url,
                            }
                        )
                return pd.DataFrame(results), None
            else:
                return (
                    None,
                    "⚠️ Đường link không thuộc cấu trúc Playlist/Kênh chuẩn!",
                )
        except Exception as e:
            return None, f"❌ Lỗi: {e}"


# 3. Hàm tạo file Excel binary (index=False loại bỏ cột Unnamed: 0)
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Loại bỏ chỉ số dòng để không sinh cột Unnamed: 0
        df.to_excel(writer, index=False, sheet_name="Data")

        workbook = writer.book
        worksheet = writer.sheets["Data"]

        # Định dạng dòng tiêu đề
        header_format = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "bg_color": "#D9E1F2",
                "font_name": "Arial",
                "font_size": 11,
            }
        )

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Căn chỉnh độ rộng cột tự động
        for idx, col in enumerate(df.columns):
            lens = [len(str(val)) if pd.notna(val) else 0 for val in df[col]]
            max_len = max(max(lens, default=0), len(str(col))) + 3
            worksheet.set_column(idx, idx, min(max_len, 65))

    return output.getvalue()


# 4. Thực thi nút bấm
if st.button("🚀 BẤM ĐỂ LẤY DỮ LIỆU & TẢI EXCEL", type="primary"):
    if not url:
        st.warning("⚠️ Bạn chưa nhập link YouTube!")
    else:
        with st.spinner("⏳ Đang quét dữ liệu YouTube, vui lòng đợi vài giây..."):
            df, err = get_youtube_data(url)
            if err:
                st.error(err)
            elif df is not None and not df.empty:
                st.success(f"🎉 Thành công! Đã lấy được {len(df)} mục.")
                st.dataframe(df.head(10))

                clean_name = (
                    re.sub(r'[\\/*?:"<>|]', "", filename_input)
                    .strip()
                    .replace(" ", "_")
                )
                if not clean_name.endswith(".xlsx"):
                    clean_name += ".xlsx"

                # Xuất file Excel chuẩn
                excel_data = convert_df_to_excel(df)

                st.download_button(
                    label="💾 TẢI FILE EXCEL VỀ MÁY TÍNH",
                    data=excel_data,
                    file_name=clean_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )