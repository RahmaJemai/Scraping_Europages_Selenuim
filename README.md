<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scraping Europages Companies</title>
</head>
<body>
    <h1>Scraping Europages Companies</h1>

    <h2>Overview</h2>
    <p>This project is aimed at scraping company information related to web development in France from Europages website using Selenium WebDriver. It collects data such as company name, address, contact details, and other relevant information available on Europages.</p>

    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li>Selenium WebDriver</li>
        <li>Web browser (Chrome, Firefox, etc.)</li>
        <li>Chromedriver or geckodriver (depending on the browser)</li>
    </ul>

    <h2>Setup</h2>
    <ol>
        <li>Clone this repository to your local machine.</li>
        <li>Install the required Python packages using pip:</li>
    </ol>
    <pre><code>pip install -r requirements.txt</code></pre>
    <ol start="3">
        <li>Download and install the appropriate WebDriver for your browser:</li>
        <ul>
            <li>For Chrome: <a href="https://sites.google.com/a/chromium.org/chromedriver/" target="_blank">Chromedriver</a></li>
            <li>For Firefox: <a href="https://github.com/mozilla/geckodriver/releases" target="_blank">geckodriver</a></li>
        </ul>
        <li>Update the <code>config.py</code> file with your browser driver's path and other configurations if needed.</li>
    </ol>

    <h2>Usage</h2>
    <p>Run the <code>main.py</code> script:</p>
    <pre><code>python main.py</code></pre>
    <p>The script will launch the web browser, navigate to Europages, and start scraping the companies' data.</p>
    <p>Once the scraping is complete, the data will be stored in a CSV file named <code>companies_data.csv</code>.</p>

    <h2>Disclaimer</h2>
    <p>This project is for educational purposes only. Make sure to comply with Europages' terms of service and usage policy while scraping their website. Be respectful of their servers and avoid sending too many requests in a short period.</p>

    <h2>Contributions</h2>
    <p>Contributions to this project are welcome! Feel free to fork this repository, make improvements, and submit pull requests.</p>
</body>
</html>
