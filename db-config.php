<?php
// db_config.php
$host = 'localhost'; // MySQL server host
$username = 'root'; // MySQL username
$password = ''; // MySQL password
$database = 'job_app'; // MySQL database name


// Create connection
$conn = new mysqli($host, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// CORS headers (adjust as needed)
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

// Function to sanitize input data
function sanitize($input) {
    global $conn;
    return mysqli_real_escape_string($conn, htmlspecialchars(strip_tags($input)));
}

// Endpoint to fetch all jobs
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $sql = "SELECT * FROM jobs";
    $result = $conn->query($sql);

    $jobs = [];
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $jobs[] = $row;
        }
    }

    echo json_encode($jobs);
}

// Endpoint to create a job
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents("php://input"));

    $name = sanitize($data->name);
    $jobTitle = sanitize($data->jobTitle);
    $description = sanitize($data->description);
    $hazards = sanitize($data->hazards);
    $mitigation = sanitize($data->mitigation);

    $sql = "INSERT INTO jobs (name, job_title, description, hazards, mitigation)
            VALUES ('$name', '$jobTitle', '$description', '$hazards', '$mitigation')";

    if ($conn->query($sql) === TRUE) {
        echo json_encode(array("message" => "Job created successfully."));
    } else {
        echo json_encode(array("message" => "Error: " . $sql . "<br>" . $conn->error));
    }
}

// Close MySQL connection
$conn->close();