import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

# Paths to directories
texture_dir = Path("dev_textures")  # Directory with original textures
render_dir = Path("dev_textures_rendered")  # Directory with rendered images
csv_file_path = sorted(Path("dev_prompts").glob("*.csv"))[-1]  # Latest CSV file with prompts

# Load the CSV file containing prompts
if not csv_file_path.exists():
    st.error(f"CSV file with prompts not found at {csv_file_path}")
else:
    # Read the prompts CSV
    prompts_df = pd.read_csv(csv_file_path)

    # Set up Streamlit app
    st.title("Rendered Images with Prompts and Textures")

    # Ensure the folders exist
    if not render_dir.exists():
        st.error(f"Render directory not found at {render_dir}")
    elif not texture_dir.exists():
        st.error(f"Texture directory not found at {texture_dir}")
    else:
        # Display each rendered image with its corresponding prompt and textures
        for index, row in prompts_df.iterrows():
            image_id = row["bin_id"]  # Adjust the column name to match your CSV structure
            prompt = row["prompt"]  # Adjust the column name to match your CSV structure
            fnames = [f"{image_id:02d}-{i:02d}.png" for i in range(4)]
            render_paths = [render_dir / fname for fname in fnames]  # Rendered image path
            texture_paths = [texture_dir / fname for fname in fnames]  # Original texture path

            # Check if the files exist
            if (
                all([render_path.exists() for render_path in render_paths]) and
                all([texture_path.exists() for texture_path in texture_paths])
            ):
                st.subheader(f"Prompt ID: {image_id}")
                st.text(f"Prompt: {prompt}")

                # Load the images
                render_images = [Image.open(render_path) for render_path in render_paths]
                texture_images = [Image.open(texture_path) for texture_path in texture_paths]

                # Sidebar for texture selection
                st.sidebar.header(f"Select Texture for ID: {image_id}")
                selected_texture = st.sidebar.radio(
                    "Choose a texture:",
                    options=list(range(4)),
                    format_func=lambda i: f"Texture {i+1}",
                    key=f"texture_selector_{image_id}"
                )

                # Display the selected rendered image in the left column
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.image(
                        render_images[selected_texture],
                        caption=f"Rendered image for Texture {selected_texture + 1}",
                        use_container_width=True,
                    )
                with col2:
                    for i in range(4):
                        st.image(
                            texture_images[i],
                            caption=f"Texture {i+1}",
                            use_container_width=True,
                        )
            else:
                st.warning(f"Files not found for ID: {image_id}")

        # Add a footer
        st.markdown("---")
        st.text("End of images.")
