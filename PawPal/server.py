import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import random

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.create_html().encode())
        elif self.path.startswith('/dogs/'):
            # Serve images directly from the Dogs folder
            return super().do_GET()
        else:
            self.send_response(404)
            self.end_headers()

    def create_html(self):
        # Get list of images from the Dogs folder
        image_folder = 'dogs'  # Ensure this matches your folder name exactly
        images = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

        # Check if there are any images
        if not images:
            return "<html><body><h1>No images found!</h1></body></html>"

        # Create JavaScript to load images dynamically
        image_js = ', '.join([f'"{image_folder}/{img}"' for img in images])

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PAWpal - Innocent Dog Viewer</title>
            <meta name="description" content="Discover adorable and innocent dog images at PAWpal. Click to see a new heartwarming dog picture every time! Perfect for dog lovers and anyone in need of a smile.">
            <meta name="keywords" content="dogs, innocent dogs, dog images, cute dogs, dog lovers, PAWpal">
            <meta name="author" content="Your Name">
            <style>
                body, html {{
                    margin: 0;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: black;
                    color: white;
                    font-size: 24px;
                    text-align: center;
                    cursor: pointer;
                }}
                img {{
                    max-width: 100%;
                    max-height: 100%;
                    display: none;
                    transition: opacity 0.5s;
                }}
            </style>
        </head>
        <body>
            <div id="message">Click to see a new innocent dog looking at you!</div>
            <img id="dogImage" src="" alt="Innocent dog">
            
            <script>
                const message = document.getElementById('message');
                const dogImage = document.getElementById('dogImage');
                const dogImages = [{image_js}];

                let currentIndex = 0;

                function showNextDog() {{
                    if (dogImages.length === 0) return;

                    currentIndex = Math.floor(Math.random() * dogImages.length);
                    dogImage.src = dogImages[currentIndex];
                    dogImage.style.display = 'block';
                    message.style.display = 'none';
                    dogImage.style.opacity = 1;
                }}

                document.body.addEventListener('click', () => {{
                    dogImage.style.opacity = 0;
                    setTimeout(showNextDog, 500);
                }});

                // Initially load the first image with a delay for the transition
                setTimeout(showNextDog, 100);
            </script>
        </body>
        </html>
        """

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving HTTP on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
