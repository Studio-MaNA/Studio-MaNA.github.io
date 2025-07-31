import os
import re
import sys

def update_html_from_folder():
    """
    Automates the process of populating an HTML file with content (images, text, video)
    based on the current directory's name and its contents.

    The script expects to be run from within a project subfolder (e.g., '1_Pagoda-House').
    It will then look for an HTML file with the same name (e.g., '1_Pagoda-House.html')
    in the parent directory specified by BASE_HTML_PARENT_DIR.
    """

    # --- Configuration ---
    # IMPORTANT: Set this to the absolute path of your 'projects_residential' directory.
    # This is where your HTML files (e.g., 1_Pagoda-House.html) are located.
    BASE_HTML_PARENT_DIR = r"C:\Users\bacch\OneDrive\Desktop\Website-A1\A-Website\projects_residential"

    # The name of the HTML template file located in BASE_HTML_PARENT_DIR
    HTML_TEMPLATE_FILE_NAME = "template.html"

    # Supported image and video file extensions
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
    VIDEO_EXTENSIONS = ('.mp4', '.webm', '.ogg')
    TEXT_FILE_EXTENSION = '.txt'

    # --- Step 1: Determine the current project folder and HTML file path ---
    current_dir = os.getcwd()
    # Extract the last part of the path, which should be the project folder name
    project_folder_name = os.path.basename(current_dir)

    # Construct the path to the HTML file that needs to be updated (the target file)
    html_file_name = f"{project_folder_name}.html"
    html_file_path = os.path.join(BASE_HTML_PARENT_DIR, html_file_name)

    # Construct the path to the HTML template file
    html_template_path = os.path.join(BASE_HTML_PARENT_DIR, HTML_TEMPLATE_FILE_NAME)


    print(f"--- Running Content Automation for: {project_folder_name} ---")
    print(f"Target HTML file path: {html_file_path}")
    print(f"Using HTML template from: {html_template_path}")

    if not os.path.exists(html_template_path):
        print(f"Error: HTML template file '{html_template_path}' not found. Please ensure '{HTML_TEMPLATE_FILE_NAME}' exists in '{BASE_HTML_PARENT_DIR}'.")
        sys.exit(1) # Exit if HTML template not found

    # --- Step 2: Scan the current project folder for content files ---
    video_src = ""
    text_content = ""
    image_paths = []

    # List all files in the current directory
    for filename in os.listdir(current_dir):
        file_path = os.path.join(current_dir, filename)
        if os.path.isfile(file_path):
            # Check for video file
            if filename.lower().endswith(VIDEO_EXTENSIONS) and not video_src:
                video_src = filename # Store just the filename, as it's relative to the HTML file's expected location
                print(f"Found video file: {filename}")
            # Check for text file
            elif filename.lower().endswith(TEXT_FILE_EXTENSION) and not text_content:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                    print(f"Found text file: {filename}")
                except Exception as e:
                    print(f"Warning: Could not read text file {filename}: {e}")
            # Check for image files
            elif filename.lower().endswith(IMAGE_EXTENSIONS):
                image_paths.append(filename) # Store just the filename
                print(f"Found image file: {filename}")

    # Sort images for consistent order (optional, but good practice)
    image_paths.sort()

    if not video_src:
        print("Warning: No video file found in the current directory.")
    if not text_content:
        print("Warning: No text file found in the current directory.")
    if not image_paths:
        print("Warning: No image files found in the current directory.")

    # --- Step 3: Generate HTML snippets for placeholders ---

    # Generate Video Section HTML
    # Remove leading number and underscore, then replace hyphens/underscores with spaces and title case
    cleaned_project_name = re.sub(r"^\d+_", "", project_folder_name)
    video_title = cleaned_project_name.replace('_', ' ').replace('-', ' ').title()
    
    video_html_snippet = f"""
        <div class="video-section">
            <video autoplay loop muted playsinline>
                <source src="./{project_folder_name}/{video_src}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div class="video-overlay">
                <h1 class="video-title">{video_title}</h1>
            </div>
        </div>
    """ if video_src else ""

    # Generate Image Grid HTML
    image_grid_html_snippet = ""
    # Define a cycle of grid item classes for visual variety
    grid_classes = ['default', 'wide', 'tall', 'large']
    class_index = 0

    for img_filename in image_paths:
        # The image path in HTML needs to be relative to the HTML file.
        # If HTML is in projects_residential and images are in 1_Pagoda-House,
        # then the path is ./1_Pagoda-House/image.jpg
        relative_img_path = f"./{project_folder_name}/{img_filename}"
        
        # Assign a grid class from the cycle
        current_grid_class = grid_classes[class_index % len(grid_classes)]
        class_index += 1

        image_grid_html_snippet += f"""
                    <div class="grid-item {current_grid_class}" data-original-src="{relative_img_path}">
                        <img src="{relative_img_path}" alt="{img_filename}" onerror="this.onerror=null;this.src='https://placehold.co/300x400/AAAAAA/FFFFFF?text=Error';">
                    </div>"""
    
    # Ensure the image grid div is present even if no images are found
    if not image_grid_html_snippet:
        image_grid_html_snippet = f"""
                    <!-- No images found for the gallery. Please add images to the project folder. -->
                    <div class="text-content-section">
                        <p>No images available for this project yet. Please add image files (JPG, PNG, GIF) to the '{project_folder_name}' folder.</p>
                    </div>
                """

    # Generate Text Content HTML
    text_paragraphs = [f"<p>{p.strip()}</p>" for p in text_content.split('\n') if p.strip()]
    text_html_snippet = f"""
                <h2>About {video_title}</h2>
                {''.join(text_paragraphs)}
            """ if text_content else f"""
                <h2>About {video_title}</h2>
                <p>No detailed text content found for this project. Please create a .txt file in the '{project_folder_name}' folder with your project description.</p>
            """

    # --- Step 4: Read the HTML template and replace placeholders ---
    try:
        with open(html_template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Replace placeholders
        html_content = html_content.replace('<!-- VIDEO_PLACEHOLDER -->', video_html_snippet)
        html_content = html_content.replace('<!-- IMAGE_GRID_PLACEHOLDER -->', image_grid_html_snippet)
        html_content = html_content.replace('<!-- TEXT_CONTENT_PLACEHOLDER -->', text_html_snippet)

        # --- Step 5: Write the updated HTML back to the target file ---
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Successfully updated '{html_file_name}' with content from '{project_folder_name}'.")

    except FileNotFoundError:
        print(f"Error: HTML file or template not found. Please check paths: Template: {html_template_path}, Target: {html_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_html_from_folder()
