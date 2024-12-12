import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

class SIPCalculator:
    """A comprehensive SIP (Systematic Investment Plan) calculator with Streamlit interface."""

    @staticmethod
    def calculate_sip_future_value(monthly_investment: float, rate_of_return: float, years: int) -> float:
        """
        Calculate the future value of a monthly SIP investment.

        Args:
            monthly_investment (float): Monthly investment amount
            rate_of_return (float): Annual rate of return in percentage
            years (int): Number of years the investment will grow

        Returns:
            float: Future value of the SIP investment
        """
        months = years * 12
        monthly_rate = rate_of_return / 100 / 12
        future_value = monthly_investment * (
            ((1 + monthly_rate) ** months - 1) / monthly_rate
        ) * (1 + monthly_rate)
        return future_value

    @staticmethod
    def initialize_session_state():
        """Initialize session state for funds if not already present."""
        if "funds" not in st.session_state:
            st.session_state.funds = []

    @classmethod
    def render_instructions(cls):
        """Render detailed instructions for using the SIP calculator."""
        with st.expander("Instructions"):
            st.markdown("""
            ### SIP Calculator Instructions
            - **Add Multiple Funds**: Use the "Add Another Fund" button or upload a CSV
            - **Fund Details**: For each fund, specify:
                * Fund Name
                * Monthly Investment Amount
                * Expected Annual Rate of Return
                * Investment Duration
            - **CSV Upload**: Prepare a CSV with columns:
                * fund_name
                * monthly_investment
                * rate_of_return
                * years
            - **Visualization**: Get instant pie chart of investment allocation and detailed fund analysis
            """)
        
        # Add a divider after instructions
        st.divider()

    @classmethod
    def render_fund_inputs(cls):
        """Render input fields for each fund with dynamic addition, removal, and CSV upload."""
        cls.initialize_session_state()

        st.write("### Add Multiple SIPs")
        st.caption("Configure your Systematic Investment Plans")

        # CSV Upload Section
        uploaded_file = st.file_uploader(
            "Upload SIP Funds CSV", 
            type=['csv'], 
            help="Upload a CSV file with fund details. Required columns: fund_name, monthly_investment, rate_of_return, years"
        )

        # Handle CSV Upload
        if uploaded_file is not None:
            try:
                # Read the uploaded CSV
                df = pd.read_csv(uploaded_file)
                
                # Validate required columns
                required_columns = ['fund_name', 'monthly_investment', 'rate_of_return', 'years']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"Missing columns in CSV: {', '.join(missing_columns)}")
                else:
                    # Convert CSV data to list of dictionaries
                    st.session_state.funds = df.to_dict('records')
                    st.success(f"Successfully uploaded {len(st.session_state.funds)} funds!")
            except Exception as e:
                st.error(f"Error processing CSV: {e}")

        for i, fund in enumerate(st.session_state.funds):
            with st.container():
                st.write(f"#### Fund {i + 1}")
                col1, col2 = st.columns(2)

                with col1:
                    fund["fund_name"] = st.text_input(
                        f"Name of Fund {i + 1}:", 
                        value=fund["fund_name"], 
                        key=f"fund_name_{i}"
                    )
                    fund["monthly_investment"] = st.number_input(
                        f"Monthly Investment (₹):", 
                        min_value=0.0, 
                        value=fund["monthly_investment"], 
                        step=100.0, 
                        key=f"monthly_investment_{i}"
                    )

                with col2:
                    fund["rate_of_return"] = st.number_input(
                        f"Annual Return Rate (%):", 
                        min_value=0.0, 
                        value=fund["rate_of_return"], 
                        step=0.1, 
                        key=f"rate_{i}"
                    )
                    fund["years"] = st.number_input(
                        f"Investment Years:", 
                        min_value=1, 
                        value=fund["years"], 
                        step=1, 
                        key=f"years_{i}"
                    )

                col3, col4 = st.columns(2)
                with col3:
                    if st.button(f"Remove Fund {i + 1}", key=f"remove_{i}"):
                        st.session_state.funds.pop(i)
                        st.rerun()

        # Add Fund Button
        button_text = "Add Fund" if len(st.session_state.funds) == 0 else "Add Another Fund"
        if st.button(button_text):
            st.session_state.funds.append({
                "fund_name": "",
                "monthly_investment": 1000.0,
                "rate_of_return": 7.0,
                "years": 10
            })
            st.rerun()
        
        # Add a divider after fund inputs
        st.divider()

    @classmethod
    def calculate_and_visualize(cls):
        """Calculate SIP future values and create visualizations."""
        if not st.session_state.funds:
            st.warning("Please add at least one fund.")
            return

        total_future_value = 0
        total_invested_amount = 0
        data = []

        for idx, fund in enumerate(st.session_state.funds):
            future_value = cls.calculate_sip_future_value(
                fund["monthly_investment"], 
                fund["rate_of_return"], 
                fund["years"]
            )
            invested_amount = fund["monthly_investment"] * fund["years"] * 12
            total_future_value += future_value
            total_invested_amount += invested_amount

            data.append({
                "Fund Name": fund["fund_name"] or f"Fund {idx + 1}",
                "Invested Amount (₹)": round(invested_amount, 2),
                "Estimated Returns (₹)": round(future_value - invested_amount, 2),
                "Future Value (₹)": round(future_value, 2)
            })

        total_estimated_return = total_future_value - total_invested_amount
        df = pd.DataFrame(data)

        # Investment Allocation Pie Chart
        st.subheader("📊 Investment Allocation")
        fig_pie = px.pie(
            df, 
            values="Invested Amount (₹)", 
            names="Fund Name", 
            title="Investment Allocation Across Funds"
        )
        st.plotly_chart(fig_pie)

        # Divider after pie chart
        st.divider()

        # Metrics Display
        st.subheader("💰 Investment Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Total Invested", 
                value=f"₹{total_invested_amount:,.2f}",
                help="Total amount invested across all funds"
            )
        with col2:
            st.metric(
                label="Estimated Returns", 
                value=f"₹{total_estimated_return:,.2f}",
                delta=f"{(total_estimated_return/total_invested_amount*100):.2f}%",
                help="Total estimated returns from investments"
            )
        with col3:
            st.metric(
                label="Future Value", 
                value=f"₹{total_future_value:,.2f}",
                delta=f"{(total_future_value/total_invested_amount*100):.2f}%",
                help="Total projected value of investments"
            )

        # Divider after metrics
        st.divider()

        # Detailed Fund Details
        st.subheader("📝 Detailed Fund Analysis")
        st.dataframe(df)

        # CSV Download Feature
        st.subheader("💾 Download Data")

        # Prepare CSV download with explicit encoding
        csv = df.to_csv(index=False, encoding='utf-8')

        # Create two columns for download options
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="Download Fund Details as CSV",
                data=csv,
                file_name="sip_investment_details.csv",
                mime="text/csv",
                help="Download a CSV file with detailed investment information"
            )

        with col2:
            # Additional summary CSV
            summary_data = pd.DataFrame([{
                "Total Invested Amount": round(total_invested_amount, 2),
                "Total Estimated Returns": round(total_estimated_return, 2),
                "Total Future Value": round(total_future_value, 2)
            }])

            summary_csv = summary_data.to_csv(index=False, encoding='utf-8')

            st.download_button(
                label="Download Summary as CSV",
                data=summary_csv,
                file_name="sip_investment_summary.csv",
                mime="text/csv",
                help="Download a CSV file with investment summary"
            )

def main():
    """Main Streamlit application entry point."""

    # Set page configuration
    st.set_page_config(
        page_title="SIP Calculator",
        page_icon="💵",  # You can choose any emoji or an icon path
        layout="centered",  # 'centered' or 'wide' for page layout
        initial_sidebar_state="expanded",  # Sidebar state ('auto', 'expanded', 'collapsed')
    )

    st.title("💰 SIP Investment Calculator")
    st.caption("Plan and Visualize Your Systematic Investment Strategy")
    
    sip_calculator = SIPCalculator()
    sip_calculator.render_instructions()
    sip_calculator.render_fund_inputs()

    if st.button("Calculate Future Values"):
        sip_calculator.calculate_and_visualize()

if __name__ == "__main__":
    main()