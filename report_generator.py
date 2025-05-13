import csv
from datetime import datetime
from fpdf import FPDF

def read_data(file_path):
    """Read data from CSV file and return as list of dictionaries"""
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def analyze_data(data):
    """Perform simple analysis on the data"""
    analysis = {
        'total_revenue': sum(float(row['Revenue']) for row in data),
        'total_expenses': sum(float(row['Expenses']) for row in data),
        'total_profit': sum(float(row['Profit']) for row in data),
        'avg_profit_margin': sum(float(row['Profit'])/float(row['Revenue']) for row in data) / len(data) * 100,
        'months': len(data)
    }
    return analysis

def generate_report(data, analysis, output_path):
    """Generate PDF report using FPDF"""
    
    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Financial Performance Report', 0, 1, 'C')
    pdf.ln(10)
    
    # Add report date
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
    pdf.ln(15)
    
    # Add summary statistics
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Summary Statistics', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    pdf.cell(0, 8, f"Period Covered: {analysis['months']} months", 0, 1)
    pdf.cell(0, 8, f"Total Revenue: ${analysis['total_revenue']:,.2f}", 0, 1)
    pdf.cell(0, 8, f"Total Expenses: ${analysis['total_expenses']:,.2f}", 0, 1)
    pdf.cell(0, 8, f"Total Profit: ${analysis['total_profit']:,.2f}", 0, 1)
    pdf.cell(0, 8, f"Average Profit Margin: {analysis['avg_profit_margin']:.2f}%", 0, 1)
    pdf.ln(10)
    
    # Add data table
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Monthly Data', 0, 1)
    
    # Table header
    pdf.set_font('Arial', 'B', 10)
    col_widths = [40, 30, 30, 30]
    headers = ['Month', 'Revenue', 'Expenses', 'Profit']
    
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
    pdf.ln()
    
    # Table rows
    pdf.set_font('Arial', '', 10)
    for row in data:
        pdf.cell(col_widths[0], 10, row['Month'], 1, 0, 'L')
        pdf.cell(col_widths[1], 10, f"${float(row['Revenue']):,.2f}", 1, 0, 'R')
        pdf.cell(col_widths[2], 10, f"${float(row['Expenses']):,.2f}", 1, 0, 'R')
        pdf.cell(col_widths[3], 10, f"${float(row['Profit']):,.2f}", 1, 0, 'R')
        pdf.ln()
    
    # Save the PDF
    pdf.output(output_path)

def main():
    input_file = 'data/sample_data.csv'
    output_file = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    print("Reading data...")
    data = read_data(input_file)
    
    print("Analyzing data...")
    analysis = analyze_data(data)
    
    print("Generating report...")
    generate_report(data, analysis, output_file)
    
    print(f"Report generated successfully: {output_file}")

if __name__ == "__main__":
    main()