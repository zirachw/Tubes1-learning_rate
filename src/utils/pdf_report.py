from fpdf import FPDF
import os
from datetime import datetime

class SchedulePDF(FPDF):
    
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Class Scheduler - Algorithm Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title: str):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(59, 130, 246)  
        self.set_text_color(255, 255, 255) 
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.set_text_color(0, 0, 0)  
        self.ln(3)
    
    def add_monospace_text(self, text: str):
        self.set_font('Courier', '', 8)
        lines = text.split('\n')
        for line in lines:
            if self.get_y() > 250:
                self.add_page()
            self.cell(0, 4, line, 0, 1)
        self.ln(2)
    
    def add_info_box(self, label: str, value: str):
        self.set_font('Arial', 'B', 11)
        self.cell(60, 8, f'{label}:', 0, 0)
        self.set_font('Arial', '', 11)
        self.cell(0, 8, value, 0, 1)


def generate_pdf_report(
    algorithm_name: str,
    initial_state_text: str,
    final_state_text: str,
    initial_objective: float,
    final_objective: float,
    duration: float,
    iterations: int,
    plot_image_path: str,
    extra_image_path: str = None,
    output_path: str = None,
) -> str:
    pdf = SchedulePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.chapter_title('Algorithm Information')
    pdf.add_info_box('Algorithm', algorithm_name)
    pdf.add_info_box('Total Iterations', str(iterations))
    pdf.add_info_box('Search Duration', f'{duration:.2f} seconds')
    pdf.ln(5)
    
    pdf.chapter_title('Objective Function Results')
    pdf.add_info_box('Initial Objective Value', f'{initial_objective:.2f}')
    pdf.add_info_box('Final Objective Value', f'{final_objective:.2f}')
    
    improvement = initial_objective - final_objective
    improvement_pct = (improvement / initial_objective * 100) if initial_objective > 0 else 0
    pdf.add_info_box('Improvement', f'{improvement:.2f} ({improvement_pct:.2f}%)')
    pdf.ln(5)
    
    if plot_image_path and os.path.exists(plot_image_path):
        pdf.chapter_title('Objective Function Plot')
        try:
            pdf.image(plot_image_path, x=10, w=190)
            pdf.ln(5)
        except Exception as e:
            pdf.set_font('Arial', 'I', 10)
            pdf.cell(0, 10, f'Error loading plot image: {str(e)}', 0, 1)
    
    if extra_image_path and os.path.exists(extra_image_path):
        if(algorithm_name == "Genetic Algorithm"):
            pdf.chapter_title('Fitness Plot')
        else: # Simulated Annealing
            pdf.chapter_title('Probability Plot')

        try:
            pdf.image(extra_image_path, x=10, w=190)
            pdf.ln(5)
        except Exception as e:
            pdf.set_font('Arial', 'I', 10)
            pdf.cell(0, 10, f'Error loading plot image: {str(e)}', 0, 1)
    
    pdf.add_page()
    pdf.chapter_title('Initial State')
    pdf.add_monospace_text(initial_state_text)
    
    pdf.add_page()
    pdf.chapter_title('Final State')
    pdf.add_monospace_text(final_state_text)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_algo_name = algorithm_name.replace(' ', '_').lower()
    output_path = f'output/report/{safe_algo_name}_report_{timestamp}.pdf'
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pdf.output(output_path)
    
    return output_path
    