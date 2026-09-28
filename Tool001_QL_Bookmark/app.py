import streamlit as st
import datetime
import json
import pandas as pd

# ------------------------------------------
# 1. CẤU HÌNH TRANG WEB TOÀN MÀN HÌNH
# ------------------------------------------
st.set_page_config(
    page_title="Tool_QL Bookmark",
    page_icon="🔖",
    layout="wide"
)

# ------------------------------------------
# 2. KHỞI TẠO DỮ LIỆU & TRẠNG THÁI
# ------------------------------------------
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = [
        {
            "category": "Công việc",
            "title": "Google Colab",
            "url": "https://colab.research.google.com",
            "notes": [
                {"text": "Nơi chạy và cập nhật code cho Streamlit webapp.", "date": "2026-08-19 14:00"},
                {"text": "Lưu ý đường dẫn lưu file Drive: /content/drive/MyDrive/Colab Notebooks/", "date": "2026-08-19 15:30"}
            ],
            "date": "2026-08-19"
        },
        {
            "category": "Giải trí",
            "title": "YouTube",
            "url": "https://youtube.com",
            "notes": [
                {"text": "Nghe nhạc Lofi học tập và làm việc.", "date": "2026-08-19 10:00"}
            ],
            "date": "2026-08-19"
        }
    ]

if "edit_header_idx" not in st.session_state:
    st.session_state.edit_header_idx = None

if "edit_note_key" not in st.session_state:
    st.session_state.edit_note_key = None

if "add_note_idx" not in st.session_state:
    st.session_state.add_note_idx = None

# Tiêu đề ứng dụng
st.title("🔖 Tool_QL Bookmark")
st.caption("Giao diện tối ưu: Thông tin trang web ở trên, Ghi chú trải rộng toàn màn hình bên dưới.")

# ------------------------------------------
# 3. PHẦN THÊM BOOKMARK MỚI (THU GỌN)
# ------------------------------------------
with st.expander("➕ **Thêm Bookmark Mới (Bấm để mở/đóng)**", expanded=False):
    with st.form("add_bookmark_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([1, 1.5, 2])
        
        with col1:
            cat_input = st.selectbox(
                "Danh mục:",
                ["Công việc", "Học tập", "Giải trí", "Tin tức", "Tài chính", "Khác"]
            )
        with col2:
            title_input = st.text_input("Tên Trang Web:", placeholder="Ví dụ: VnExpress")
        with col3:
            url_input = st.text_input("Đường dẫn (URL):", placeholder="https://vnexpress.net")
            
        first_note = st.text_area("Ghi chú ban đầu (Không bắt buộc):", placeholder="Nhập ghi chú đầu tiên...")
        
        btn_add = st.form_submit_button("📌 Lưu Bookmark Mới", type="primary", use_container_width=True)
        
        if btn_add:
            if not title_input.strip() or not url_input.strip():
                st.error("⚠️ Vui lòng nhập đầy đủ Tên Trang Web và Đường dẫn URL!")
            else:
                formatted_url = url_input if url_input.startswith("http") else f"https://{url_input}"
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                
                notes_list = []
                if first_note.strip():
                    notes_list.append({"text": first_note.strip(), "date": now_str})
                    
                new_item = {
                    "category": cat_input,
                    "title": title_input,
                    "url": formatted_url,
                    "notes": notes_list,
                    "date": str(datetime.date.today())
                }
                st.session_state.bookmarks.append(new_item)
                st.success(f"✅ Đã thêm '{title_input}' thành công!")
                st.rerun()

st.write("")

# ------------------------------------------
# 4. TÌM KIẾM & LỌC
# ------------------------------------------
col_search, col_filter, col_total = st.columns([2.5, 1.5, 1])

with col_search:
    search_keyword = st.text_input("🔍 Tìm kiếm nhanh:", placeholder="Nhập từ khóa...")

with col_filter:
    filter_category = st.selectbox(
        "📁 Lọc theo danh mục:",
        ["Tất cả", "Công việc", "Học tập", "Giải trí", "Tin tức", "Tài chính", "Khác"]
    )

filtered_list = st.session_state.bookmarks

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
    st.metric("Tổng số:", f"{len(filtered_list)} web")

st.divider()

# ------------------------------------------
# 5. HIỂN THỊ DẠNG THẺ TẦNG
# ------------------------------------------
if not filtered_list:
    st.info("💡 Chưa có bookmark nào hoặc không tìm thấy kết quả phù hợp.")
else:
    for idx, item in enumerate(filtered_list):
        real_idx = st.session_state.bookmarks.index(item)
        
        with st.container(border=True):
            # TẦNG 1: THÔNG TIN TRANG WEB
            if st.session_state.edit_header_idx == real_idx:
                ec1, ec2, ec3, ec4 = st.columns([1, 1.5, 2, 1])
                with ec1:
                    categories_list = ["Công việc", "Học tập", "Giải trí", "Tin tức", "Tài chính", "Khác"]
                    cat_default_idx = categories_list.index(item['category']) if item['category'] in categories_list else 0
                    new_cat = st.selectbox("Danh mục:", categories_list, index=cat_default_idx, key=f"eh_cat_{real_idx}")
                with ec2:
                    new_title = st.text_input("Tên Trang Web:", value=item['title'], key=f"eh_title_{real_idx}")
                with ec3:
                    new_url = st.text_input("Đường dẫn (URL):", value=item['url'], key=f"eh_url_{real_idx}")
                with ec4:
                    st.write("")
                    st.write("")
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        if st.button("💾 Lưu", type="primary", key=f"save_hdr_{real_idx}", use_container_width=True):
                            formatted_url = new_url if new_url.startswith("http") else f"https://{new_url}"
                            st.session_state.bookmarks[real_idx]["category"] = new_cat
                            st.session_state.bookmarks[real_idx]["title"] = new_title
                            st.session_state.bookmarks[real_idx]["url"] = formatted_url
                            st.session_state.edit_header_idx = None
                            st.rerun()
                    with sc2:
                        if st.button("❌ Hủy", key=f"cancel_hdr_{real_idx}", use_container_width=True):
                            st.session_state.edit_header_idx = None
                            st.rerun()
            else:
                hc1, hc2, hc3, hc4, hc5 = st.columns([0.5, 1.2, 3, 1.5, 1.2])
                with hc1:
                    st.subheader(f"#{idx + 1}")
                with hc2:
                    st.caption(f"🏷️ **{item['category']}**")
                    st.caption(f"📅 {item['date']}")
                with hc3:
                    st.subheader(f"🌐 {item['title']}")
                with hc4:
                    st.link_button("🚀 Truy cập Trang Web", item['url'], use_container_width=True)
                with hc5:
                    btn_c1, btn_c2 = st.columns(2)
                    with btn_c1:
                        if st.button("✏️ Sửa Web", key=f"btn_edit_hdr_{real_idx}", use_container_width=True):
                            st.session_state.edit_header_idx = real_idx
                            st.rerun()
                    with btn_c2:
                        if st.button("🗑️ Xóa Web", key=f"btn_del_web_{real_idx}", use_container_width=True):
                            st.session_state.bookmarks.remove(item)
                            st.rerun()

            st.markdown("<hr style='margin: 4px 0; border: 0.2px solid #444;'>", unsafe_allow_html=True)

            # TẦNG 2: DANH SÁCH GHI CHÚ
            notes_data = item.get("notes", [])
            
            if not notes_data:
                st.caption("📝 *Chưa có ghi chú nào cho trang web này.*")
            else:
                for n_idx, n_item in enumerate(notes_data):
                    if st.session_state.edit_note_key == (real_idx, n_idx):
                        with st.container(border=True):
                            edited_note_text = st.text_area("Hiệu chỉnh ghi chú:", value=n_item['text'], key=f"area_note_{real_idx}_{n_idx}")
                            sn1, sn2 = st.columns([1, 1])
                            with sn1:
                                if st.button("💾 Lưu Ghi chú", type="primary", key=f"save_n_{real_idx}_{n_idx}", use_container_width=True):
                                    if edited_note_text.strip():
                                        st.session_state.bookmarks[real_idx]["notes"][n_idx]["text"] = edited_note_text.strip()
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
                                st.session_state.bookmarks[real_idx]["notes"].pop(n_idx)
                                st.rerun()

            if st.session_state.add_note_idx == real_idx:
                with st.container(border=True):
                    new_add_text = st.text_area("Thêm ghi chú cá nhân mới:", key=f"add_text_{real_idx}")
                    sa1, sa2 = st.columns([1, 1])
                    with sa1:
                        if st.button("💾 Thêm Ghi chú", type="primary", key=f"save_add_{real_idx}", use_container_width=True):
                            if new_add_text.strip():
                                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                                st.session_state.bookmarks[real_idx]["notes"].append({"text": new_add_text.strip(), "date": now_str})
                                st.session_state.add_note_idx = None
                                st.rerun()
                    with sa2:
                        if st.button("❌ Hủy", key=f"cancel_add_{real_idx}", use_container_width=True):
                            st.session_state.add_note_idx = None
                            st.rerun()
            else:
                if st.button("➕ Thêm ghi chú mới cho web này", key=f"btn_add_note_{real_idx}"):
                    st.session_state.add_note_idx = real_idx
                    st.rerun()

# ------------------------------------------
# 6. TÍNH NĂNG NHẬP / XUẤT FILE LƯU TRỮ
# ------------------------------------------
st.divider()
st.subheader("⚙️ Quản lý Dữ liệu (Nhập / Xuất File)")

col_io1, col_io2 = st.columns(2)

# CỘT 1: NHẬP/TẢI FILE DỮ LIỆU CŨ LÊN (IMPORT)
with col_io1:
    st.markdown("##### 📤 Chọn File Dữ Liệu Cũ Để Nạp Lại")
    uploaded_file = st.file_uploader("Tải lên file dữ liệu (.json):", type=["json"])
    if uploaded_file is not None:
        try:
            loaded_data = json.load(uploaded_file)
            if isinstance(loaded_data, list):
                if st.button("🔄 Xác nhận nạp dữ liệu này vào ứng dụng", type="primary", use_container_width=True):
                    st.session_state.bookmarks = loaded_data
                    st.success("✅ Đã nạp thành công dữ liệu từ file!")
                    st.rerun()
            else:
                st.error("⚠️ Cấu trúc file JSON không đúng chuẩn danh sách!")
        except Exception as e:
            st.error(f"⚠️ Lỗi đọc file: {e}")

# CỘT 2: XUẤT FILE LƯU TRỮ RA MÁY TÍNH (EXPORT)
with col_io2:
    st.markdown("##### 📥 Xuất File Dữ Liệu Lưu Ra Máy Tính")
    if st.session_state.bookmarks:
        # File JSON
        data_json = json.dumps(st.session_state.bookmarks, ensure_ascii=False, indent=2)
        st.download_button(
            label="📄 Tải về File JSON (Dùng để nạp lại sau này)",
            data=data_json,
            file_name="tool_ql_bookmark_backup.json",
            mime="application/json",
            use_container_width=True
        )
        
        # File CSV/Excel
        export_rows = []
        for b in st.session_state.bookmarks:
            notes_str = " | ".join([f"[{n['date']}] {n['text']}" for n in b.get("notes", [])])
            export_rows.append({
                "Danh mục": b["category"],
                "Tên Trang Web": b["title"],
                "Đường dẫn (URL)": b["url"],
                "Danh sách Ghi chú": notes_str,
                "Ngày tạo": b["date"]
            })
        
        df_export = pd.DataFrame(export_rows)
        csv_data = df_export.to_csv(index=False, encoding="utf-8-sig")
        
        st.download_button(
            label="📊 Tải về File Excel / CSV (Dùng để xem bằng Excel)",
            data=csv_data,
            file_name="tool_ql_bookmark_excel.csv",
            mime="text/csv",
            use_container_width=True
        )
