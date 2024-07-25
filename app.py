from rembg import remove
from PIL import Image
import os
import streamlit as st

class BackgroundRemover:
    def __init__(self, input_path):
        self.input_path = self.sanitize_path(input_path)
        self.output_path = self.create_output_path(self.input_path)

    def sanitize_path(self, path):
        return path.replace("\\", "\\\\")

    def create_output_path(self, input_path):
        base, ext = os.path.splitext(input_path)
        return base + "bg.png"

    def remove_background(self):
        try:
            img = Image.open(self.input_path)
            result = remove(img)
            result.save(self.output_path)
            return self.output_path
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None

def main():
    st.title("Background Remover by Kashif")

    st.write("<div style='text-align: center;'>Select an image to remove the background</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    if uploaded_file is not None:
        input_path = os.path.join("uploads", uploaded_file.name)
        
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(input_path, caption='Uploaded Image', use_column_width=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Remove Background"):
                remover = BackgroundRemover(input_path)
                output_path = remover.remove_background()
                if output_path:
                    st.image(output_path, caption='Image with Background Removed', use_column_width=True)
                    
                    # Add download button
                    with open(output_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Image",
                            data=file,
                            file_name=os.path.basename(output_path),
                            mime="image/png"
                        )
                else:
                    st.error("Failed to remove background")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
