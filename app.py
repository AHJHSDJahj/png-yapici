import streamlit as st
from rembg import remove
from PIL import Image
import io

# Sayfa ayarları
st.set_page_config(page_title="PNG Yapıcı", page_icon="🖼️")

st.title("🖼️ Arka Plan Silme & PNG Yapma Sitesi")
st.write("Fotoğrafınızı yükleyin, saniyeler içinde arka planı silinsin!")

# Fotoğraf Yükleme
uploaded_file = st.file_uploader("Bir fotoğraf seçin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Resmi aç
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="Yüklenen Resim", width=300)
    
    # Seçenekler
    output_format = st.selectbox("Format:", ["PNG", "JPG"])
    bg_color = st.selectbox("Arka Plan Rengi:", ["Şeffaf", "Kırmızı", "Mavi", "Yeşil", "Beyaz"])
    
    if st.button("Resmi İşle ve Hazırla"):
        with st.spinner("Lütfen bekleyin, yapay zeka arka planı temizliyor..."):
            # Arka plan silme işlemi
            raw_res = remove(input_image)
            
            # Renk ayarı
            if bg_color != "Şeffaf" or output_format == "JPG":
                color_dict = {"Kırmızı": (255,0,0), "Mavi": (0,0,255), "Yeşil": (0,255,0), "Beyaz": (255,255,255)}
                chosen = color_dict.get(bg_color, (255,255,255))
                
                background = Image.new("RGBA", raw_res.size, chosen + (255,))
                final_img = Image.alpha_composite(background, raw_res.convert("RGBA"))
            else:
                final_img = raw_res
                
            if output_format == "JPG":
                final_img = final_img.convert("RGB")
                
            # Sonucu göster
            st.image(final_img, caption="Sonuç", width=300)
            
            # İndirme butonu
            buf = io.BytesIO()
            final_img.save(buf, format=output_format)
            st.download_button(label="📥 İndir", data=buf.getvalue(), file_name=f"sonuc.{output_format.lower()}")