# AI Content Waterfall

AI Content Waterfall is a Python application that generates and publishes website articles based on input topics and incorporates images from Unsplash. It utilizes the power of Llama2 to curate and create engaging content for your website.


## Installation
Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/Ivang71/ai-content-waterfall.git
   cd ai-content-waterfall
   ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Activate the virtual environment:
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

   - On Windows:
     ```powershell
     venv\Scripts\activate
     ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
   ```

5. Copy the example environment file
    ```bash
    cp .env.example .env
   ```

6. Open the .env file and add your WordPress credentials:
    ```env
    WP_URL=url_to_your_wp_api
    WP_USERNAME=your_username
    WP_PASSWORD=your_application_password
   ```

7. Prepare a topics.txt file:
    Create a topics.txt file in the project directory and add one topic per line. For example:
    ```
    What is AI
    How to set up your own shadowsocks server
    Guide to crypto for 2034
    ```


## Usage
Run the script with the following command:
```
python3 main.py
```
The script will generate website articles based on the topics provided in topics.txt, fetch related images from Unsplash and upload to your wordpress site using credentials provided in `.env`.


## License

This project is licensed under the MIT License - see the LICENSE file for details.
