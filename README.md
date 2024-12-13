# SIP Calculator

This Streamlit-based SIP (Systematic Investment Plan) Calculator helps users calculate the future value of multiple SIP investments and visualize the allocation of investments. The application provides an intuitive interface for adding, managing, and analyzing multiple SIP funds.

## Features
- **Add Multiple SIP Funds**: Input details such as fund name, monthly investment amount, annual rate of return, and duration in years.
- **Remove Funds**: Remove any SIP fund from the list.
- **Calculate Future Value**: Computes the total future value of each SIP fund based on the provided inputs.
- **Investment Allocation Visualization**: A pie chart shows the proportion of investments across funds.
- **Detailed Summary Table**: Displays invested amount, estimated returns, and total future value for each fund and their totals.

## Instructions
1. Click the **Add Another Fund** button to add a new SIP plan.
2. For each fund, specify:
   - **Fund Name**
   - **Monthly Investment Amount** (in ₹)
   - **Expected Annual Rate of Return** (in %)
   - **Duration** (in years)
3. To remove a fund, click the **Remove Fund** button corresponding to that fund.
4. Once all funds are added, click **Calculate Future Values** to compute the results.
5. View:
   - A pie chart showing investment allocation.
   - A summary table with details of each fund and the totals.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/AkhileshDalvi/sip-calculator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd sip-calculator
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Requirements
- Python 3.7+
- Streamlit
- pandas
- plotly

## How It Works
The application calculates the future value of each SIP investment using the formula for the future value of a series:

\[ FV = P \times \frac{(1 + r)^n - 1}{r} \times (1 + r) \]

Where:
- **P**: Monthly investment amount
- **r**: Monthly rate of return (Annual Rate of Return / 12 / 100)
- **n**: Total number of months (Years × 12)

## Example
If you invest ₹5,000 per month in a fund with an annual return of 10% for 10 years, the SIP calculator computes:
- Total Invested Amount: ₹6,00,000
- Estimated Returns: ₹4,22,136.32
- Future Value: ₹10,22,136.32

## Screenshots
### Input Form
_Add and manage multiple SIP funds:_

![Input Form Screenshot](path/to/input_form.png)

### Results
_View investment allocation and detailed summary:_

![Results Screenshot](path/to/results.png)

## Contributing
Feel free to contribute to this project by submitting issues or pull requests.

## License
This project is licensed under the MIT License.
