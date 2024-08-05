from django.shortcuts import render, get_object_or_404
import os
import requests
from django.utils import timezone
import markdown
from .models import Post, Category  # Ensure Category is imported correctly

def home(request):
    return render(request, 'base/home.html')

def blog(request):
    base_dir = './docs'
    md_files = {}
    # Traverse the directory and read markdown files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                category_name = os.path.basename(root)
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                    html_content = markdown.markdown(md_content)
                    if category_name not in md_files:
                        md_files[category_name] = []
                    md_files[category_name].append({'filename': file, 'content': html_content})

    return render(request, 'base/blog.html', {'md_files': md_files})

def category(request, category_id):
    # Fetch the category object based on the category_id
    category = get_object_or_404(Category, id=category_id)
    
    # Format the category name to use it as a directory name
    category_name = category.name.lower().replace(' ', '_')
    
    # Create the directory path using the formatted category name
    md_files_directory = os.path.join('docs', f'category_{category_id}')
    
    # Initialize an empty dictionary to store markdown files' content
    md_files = {}
    
    # Check if the directory exists
    if os.path.exists(md_files_directory):
        # Iterate over each file in the directory
        for filename in os.listdir(md_files_directory):
            # Check if the file has a '.md' extension
            if filename.endswith('.md'):
                # Construct the full path to the markdown file
                filepath = os.path.join(md_files_directory, filename)
                
                # Open and read the content of the markdown file
                with open(filepath, 'r', encoding='utf-8') as file:
                    md_content = file.read()
                    
                    # Convert the markdown content to HTML
                    html_content = markdown.markdown(md_content)
                    
                    # Store the HTML content in the dictionary with the filename as the key
                    md_files[filename] = html_content

    # Get all categories for the dropdown menu
    all_categories = Category.objects.all()

    # Fetch posts for the current category using the correct field name
    posts = Post.objects.filter(categories=category)

    # Prepare the context to be passed to the template
    context = {
        'category': category,
        'posts': posts,
        'md_files': md_files if md_files else None,
        'all_categories': all_categories,
    }
    
    # Render the 'category.html' template with the context data
    return render(request, 'base/category.html', context)

from datetime import timedelta

def upcoming_events(request):
    # Get the current timestamp
    current_timestamp = int(timezone.now().timestamp())

    # Define how many days ahead to look for events
    days_ahead =360  # Adjust this value as needed
    future_date = timezone.now() + timedelta(days=days_ahead)
    future_timestamp = int(future_date.timestamp())

    # Define the API endpoint and parameters
    url = "https://ctftime.org/rss"
    params = {
        'limit': 100,  # Adjust the limit as needed
        'start': current_timestamp,
        'finish': future_timestamp,
    }

    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response

        # Print the raw data for debugging purposes
        print(f"Raw API Response: {data}")

        # Check if 'results' key exists and contains events
        events = data.get('results', [])
        
        if not events:
            print("No upcoming events found.")

    except requests.RequestException as e:
        # Handle exceptions or errors during the API request
        print(f"An error occurred: {e}")
        events = []

    # Render the template with the events data
    return render(request, 'base/upcoming_events.html', {'events': events})
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'base/post_details.html', {'post': post})
