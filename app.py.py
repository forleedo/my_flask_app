from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# HTML 템플릿 (index.html)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto Makeup App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f9f9f9;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        #app {
            max-width: 600px;
            margin: auto;
            background: #fff;
            padding: 20px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        button {
            padding: 10px 20px;
            margin: 5px;
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        #status-message {
            margin-top: 20px;
            font-weight: bold;
            color: green;
        }
    </style>
</head>
<body>
    <h1>Auto Makeup Application</h1>
    <div id="app">
        <label for="user-id">User ID:</label>
        <input type="text" id="user-id" placeholder="Enter your ID">
        <button id="load-styles">Load Styles</button>
        
        <div id="styles-container"></div>

        <h2>Selected Style: <span id="selected-style"></span></h2>

        <button id="apply-style">Apply Style</button>

        <button id="print-start">Print Start</button>
        <p id="status-message"></p>
    </div>

    <script>
        document.getElementById('load-styles').addEventListener('click', function() {
            fetch('/styles')
            .then(response => response.json())
            .then(styles => {
                let container = document.getElementById('styles-container');
                container.innerHTML = '';

                styles.forEach(style => {
                    let button = document.createElement('button');
                    button.innerText = style;
                    button.addEventListener('click', function() {
                        document.getElementById('selected-style').innerText = style;
                    });
                    container.appendChild(button);
                });
            });
        });

        document.getElementById('apply-style').addEventListener('click', function() {
            let userId = document.getElementById('user-id').value;
            let selectedStyle = document.getElementById('selected-style').innerText;

            if (!userId || !selectedStyle) {
                alert('Please enter a User ID and select a style.');
                return;
            }

            fetch('/apply_style', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: userId, style: selectedStyle })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            });
        });

        document.getElementById('print-start').addEventListener('click', function() {
            let userId = document.getElementById('user-id').value;

            if (!userId) {
                alert('Please enter a User ID.');
                return;
            }

            document.getElementById('status-message').innerText = "Mask Pack is generating now!";

            fetch('/generate_mask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: userId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'generating') {
                    setTimeout(checkStatus, 5000);
                }
            });
        });

        function checkStatus() {
            fetch('/check_status')
            .then(response => response.json())
            .then(data => {
                document.getElementById('status-message').innerText = data.message;
            });
        }
    </script>
</body>
</html>
"""

# 메인 페이지 라우트
@app.route('/')
def index():
    return render_template_string(html_template)

# 스타일 목록을 제공하는 API
@app.route('/styles', methods=['GET'])
def get_styles():
    styles = [
        "Natural Look", "Bold Look", "Evening Glam", "Classic Red",
        "Smoky Eyes", "Summer Fresh", "Winter Cool"
    ]
    return jsonify(styles)

# 얼굴에 스타일 적용을 처리하는 API
@app.route('/apply_style', methods=['POST'])
def apply_style():
    data = request.json
    user_id = data['user_id']
    selected_style = data['style']
    return jsonify({"message": f"Style '{selected_style}' applied for user '{user_id}'!"})

# 마스크팩 생성을 시작하는 API
@app.route('/generate_mask', methods=['POST'])
def generate_mask():
    data = request.json
    user_id = data['user_id']
    return jsonify({"message": "Mask Pack is generating now!", "status": "generating"})

# 마스크팩 생성 완료를 확인하는 API
@app.route('/check_status', methods=['GET'])
def check_status():
    return jsonify({"message": "Complete!", "status": "complete"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)