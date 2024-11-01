import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import markdown2
from tkinterweb import HtmlFrame
import ttkbootstrap as ttkb
from fpdf import FPDF

# Variable to store HTML content for saving
current_html = ""
current_font_size = 14
dark_mode_enabled = True  # Enable dark mode by default

# Updated tool name
tool_name = "Markdown Maestro"

# Mapping for Markdown options with labels and actual code
markdown_options = {
    "Heading 1": "# Heading 1\n",
    "Heading 2": "## Heading 2\n",
    "Heading 3": "### Heading 3\n",
    "List item": "- List item\n",
    "Numbered item": "1. Numbered item\n",
    "Link": "[Link text](http://example.com)\n",
    "Inline code": "`Inline code`\n",
    "Code block": "```\nBlock of code\n```\n"
}

# Font sizes for specific Markdown options
font_sizes = {
    "Heading 1": 24,
    "Heading 2": 20,
    "Heading 3": 18,
    "List item": 14,
    "Numbered item": 14,
    "Link": 14,
    "Inline code": 14,
    "Code block": 14
}


def update_preview():
    global current_html
    markdown_text = markdown_input.get("1.0", tk.END).strip()
    
    # Convert Markdown with HTML support, including emoji support
    html_text = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables", "strike", "target-blank-links"])

    # Apply dark mode styling if enabled
    if dark_mode_enabled:
        preview_background = "#333"
        preview_color = "#eee"
    else:
        preview_background = "#fff"
        preview_color = "#000"

    # Wrap the HTML in a basic HTML structure with styles, using a font that supports emojis
    styled_html = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: "Segoe UI Emoji", sans-serif; margin: 20px; font-size: {current_font_size}px; background-color: {preview_background}; color: {preview_color}; }}
                h1 {{ color: #eee if dark_mode_enabled else #333; }}
                h2 {{ color: #eee if dark_mode_enabled else #444; }}
                h3 {{ color: #eee if dark_mode_enabled else #555; }}
                pre {{ background-color: #333; border: 1px solid #ddd; padding: 10px; border-radius: 5px; overflow: auto; }}
                code {{ background-color: #444; padding: 2px 4px; border-radius: 3px; font-family: monospace; }}
                blockquote {{ border-left: 2px solid #888; padding-left: 10px; color: {preview_color}; margin: 0 0 10px; }}
                ul, ol {{ margin-left: 20px; }}
                a {{ color: #007BFF; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                img {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            {html_text}
        </body>
    </html>
    """

    current_html = styled_html
    html_frame.load_html(styled_html)


def insert_markdown(label):
    global current_font_size
    markdown_code = markdown_options[label]  # Get the actual Markdown code
    current_font_size = font_sizes.get(label, 14)
    markdown_input.insert(tk.END, markdown_code)
    update_preview()


def download_markdown():
    markdown_text = markdown_input.get("1.0", tk.END).strip()
    if not markdown_text:
        messagebox.showwarning("Warning", "No content to download.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".md",
                                             filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(markdown_text)
        messagebox.showinfo("Success", f"README.md has been downloaded to:\n{file_path}")


def save_as_html():
    global current_html
    if not current_html:
        messagebox.showwarning("Warning", "No HTML content to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".html",
                                             filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(current_html)
        messagebox.showinfo("Success", f"HTML file has been saved to:\n{file_path}")


def save_as_pdf():
    markdown_text = markdown_input.get("1.0", tk.END).strip()
    if not markdown_text:
        messagebox.showwarning("Warning", "No content to save.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, markdown_text)

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        pdf.output(file_path)
        messagebox.showinfo("Success", f"PDF file has been saved to:\n{file_path}")


def import_markdown():
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        markdown_input.delete("1.0", tk.END)
        markdown_input.insert("1.0", content)
        update_preview()


def clear_input():
    markdown_input.delete("1.0", tk.END)
    html_frame.load_html("")
    update_preview()


def toggle_theme():
    global dark_mode_enabled
    dark_mode_enabled = theme_switch.instate(['selected'])
    app.style.theme_use('darkly' if dark_mode_enabled else 'flatly')
    update_preview()


def show_about():
    messagebox.showinfo("About", f"{tool_name}\nVersion 1.0\nA simple tool for writing and previewing Markdown files with style.")


# Create the main window
app = ttkb.Window(themename="darkly")  # Dark mode by default
app.title(tool_name)
app.geometry("1400x800")

# Create Menu Bar
menu_bar = tk.Menu(app)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save as Markdown", command=download_markdown)
file_menu.add_command(label="Save as HTML", command=save_as_html)
file_menu.add_command(label="Save as PDF", command=save_as_pdf)
file_menu.add_command(label="Import Markdown", command=import_markdown)
menu_bar.add_cascade(label="File", menu=file_menu)

# Insert Menu
insert_menu = tk.Menu(menu_bar, tearoff=0)
for label in markdown_options.keys():
    insert_menu.add_command(label=label, command=lambda lbl=label: insert_markdown(lbl))
menu_bar.add_cascade(label="Insert", menu=insert_menu)

# Help Menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Configure menu bar
app.config(menu=menu_bar)

# Frame for input and preview
frame = ttk.Frame(app)
frame.pack(padx=10, pady=10, expand=True, fill="both")

# Titles
input_label = ttk.Label(frame, text="Markdown Input", font=("Segoe UI Emoji", 12, "bold"))
input_label.grid(row=0, column=0, padx=10, sticky="w")
preview_label = ttk.Label(frame, text="Preview", font=("Segoe UI Emoji", 12, "bold"))
preview_label.grid(row=0, column=1, padx=10, sticky="w")

# Input Text Box
markdown_input = scrolledtext.ScrolledText(frame, width=40, height=20, font=("Segoe UI Emoji", 12))
markdown_input.grid(row=1, column=0, padx=10, sticky="nsew")
markdown_input.bind("<KeyRelease>", lambda event: update_preview())

# Preview HTML Frame
html_frame = HtmlFrame(frame, horizontal_scrollbar="auto")
html_frame.grid(row=1, column=1, padx=10, sticky="nsew")
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=2)

# Right Sidebar for Dark Mode, Insert Buttons, and Clear Button
sidebar = ttk.Frame(frame)
sidebar.grid(row=1, column=2, padx=10, sticky="ns")

# Dark Mode Switch
theme_switch = ttk.Checkbutton(sidebar, text="Dark Mode", command=toggle_theme, bootstyle="success-round-toggle")
theme_switch.pack(padx=5, pady=5)
theme_switch.state(['selected'])  # Initialize to dark mode enabled

# Divider line
ttk.Separator(sidebar, orient='horizontal').pack(fill="x", pady=10)

# Insert Markdown Options on Sidebar
insert_label = ttk.Label(sidebar, text="Insert Markdown:", font=("Arial", 10, "bold"))
insert_label.pack(pady=5)

for label in markdown_options.keys():
    button = ttk.Button(sidebar, text=label,
                        command=lambda lbl=label: insert_markdown(lbl), width=20, bootstyle="info")
    button.pack(fill=tk.X, pady=2)

# Divider and Clear Button
ttk.Separator(sidebar, orient='horizontal').pack(fill="x", pady=10)
ttk.Button(sidebar, text="Clear", command=clear_input, bootstyle="danger").pack(pady=5)

# Run the application
app.mainloop()
