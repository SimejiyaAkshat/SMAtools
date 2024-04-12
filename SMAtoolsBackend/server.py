from flask  import Flask, request, jsonify
from analyzer import WebsitePerformanceAnalyzer as wp
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/calculate_metrics', methods=['POST'])
@cross_origin()
def calculate_metrics():
    # Get website URL from the request data
    website_url = request.json.get('website_url')

    # Check if website URL is provided
    if not website_url:
        return jsonify({'error': 'Website URL is required'}), 400

    try:
        # Create an instance of WebsitePerformanceAnalyzer
        analyzer = wp(website_url)

        # Calculate performance metrics
        loading_time, time_to_first_byte, page_size, number_of_requests= analyzer.get_loading_time(), analyzer.get_time_to_first_byte(), analyzer.get_page_size(), analyzer.get_number_of_requests()
        percentage = analyzer.calculate_performance_percentage(loading_time, time_to_first_byte, page_size, number_of_requests)
        grade = analyzer.grade_website_performance(percentage)
        total_images, images_size = analyzer.analyze_images()
        # Return metrics as JSON response
        return jsonify({
            'loading_time': loading_time,
            'time_to_first_byte': time_to_first_byte,
            'page_size': page_size,
            'number_of_requests': number_of_requests,
            "percentage_score": percentage,
            "grade": grade,
            "total_images": total_images,
            "images_size": images_size
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500