from typing import Dict, List
from fpdf import FPDF
import os
from datetime import datetime
from ..core.state import State

class SchedulePDF(FPDF):
    
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Class Scheduler - Algorithm Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'{self.page_no()}', 0, 0, 'R')
    
    def chapter_title(self, title: str):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(34, 139, 34)
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

    def add_list_section(self, items: List[str]):
        self.set_font('Arial', '', 9)
        for item in items:
            if self.get_y() > 260:
                self.add_page()
            self.cell(10, 6, '-', 0, 0)
            self.multi_cell(0, 6, item)
        self.ln(2)

    def add_schedule_table(self, schedule_data: List[Dict]):
        days = ["Senin", 'Selasa', 'Rabu', 'Kamis', 'Jumat']

        table_count = 0
        for item in schedule_data:
            if item.get('type') == 'header':
                if table_count > 0 and table_count % 2 == 0:
                    self.add_page()
                elif table_count > 0:
                    self.ln(5)

                table_count += 1

                self.set_font('Arial', 'B', 12)
                self.cell(0, 8, f"Ruang: {item['room']}",0 ,1, 'L', 0)
                self.set_text_color(0,0,0)

                self.set_font('Arial', 'B', 9)
                self.cell(15, 7, 'Jam', 1, 0, 'C', 1)
                for day in days:
                    self.cell(35, 7, day, 1, 0, 'C', 1)
                self.ln()
            else:
                self.set_font('Courier', '', 8)
                hour = item['hour']
                self.cell(15, 6, str(hour), 1,0, 'C')

                for day in days:
                    cell_content = item.get(day, '-')
                    self.cell(35, 6, cell_content, 1, 0, 'C')
                self.ln()

        self.ln(3)
        


def generate_pdf_report(
    algorithm_name: str,
    initial_state: State,
    final_state: State,
    initial_objective: float,
    final_objective: float,
    duration: float,
    iterations: int,
    plot_image_path: str,
    extra_image_path: str = None,
    output_path: str = None,
    algorithm_instance = None,
    input_basename: str = "default"
) -> str:
    pdf = SchedulePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.chapter_title('Data Summary')

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, f'Courses ({len(initial_state.courses)}):', 0, 1)
    pdf.set_font('Courier', '', 8)
    course_data = ', '.join([c.code for c in initial_state.courses])
    pdf.multi_cell(0, 5, course_data)
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, f'Rooms ({len(initial_state.rooms)}):', 0, 1)
    pdf.set_font('Courier', '', 8)
    room_data = ', '.join([r.code for r in initial_state.rooms])
    pdf.multi_cell(0, 5, room_data)
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, f'Students ({len(initial_state.students)}):', 0, 1)
    pdf.set_font('Courier', '', 8)
    student_data = ', '.join([s.NIM for s in initial_state.students])
    pdf.multi_cell(0, 5, student_data)

    pdf.ln(5)

    pdf.chapter_title('Algorithm Information')
    pdf.add_info_box('Algorithm', algorithm_name)
    pdf.add_info_box('Total Iterations', str(iterations))
    pdf.add_info_box('Search Duration', f'{duration:.2f} seconds')
    
    if algorithm_instance:
        if hasattr(algorithm_instance, 'max_sideways'):
            pdf.add_info_box('Max Sideways Moves', str(algorithm_instance.max_sideways))
            pdf.add_info_box('Sideways Moves', f'{algorithm_instance.sideways_count}/{algorithm_instance.max_sideways}')
        
        if hasattr(algorithm_instance, 'max_restart'):
            pdf.add_info_box('Max Restarts', str(algorithm_instance.max_restart))
            if hasattr(algorithm_instance, 'iteration_per_restart'):
                pdf.add_info_box('Iterations per Restart', f'{algorithm_instance.iteration_per_restart}')
        
        if hasattr(algorithm_instance, 'initial_temp'):
            pdf.add_info_box('Initial Temperature (auto)', f'{algorithm_instance.initial_temp:.4f}')
            pdf.add_info_box('Alpha (adaptive cooling)', f'{algorithm_instance.cooling_rate}')
            pdf.add_info_box('Stuck at Local Optima', f'{algorithm_instance.stuck_count} times')
        
        if hasattr(algorithm_instance, 'population_size'):
            pdf.add_info_box('Population Size', str(algorithm_instance.population_size))
            pdf.add_info_box('Max Generations', str(algorithm_instance.max_iteration))
    
    pdf.ln(5)

    pdf.chapter_title('Objective Function Results')

    if initial_objective is not None:
        pdf.add_info_box('Initial Objective Value', f'{initial_objective:.2f}')

    pdf.add_info_box('Final Objective Value', f'{final_objective:.2f}')

    if initial_objective is not None:
        improvement = initial_objective - final_objective
        improvement_pct = (improvement / initial_objective * 100) if initial_objective > 0 else 0
        pdf.add_info_box('Improvement', f'{improvement:.2f} ({improvement_pct:.2f}%)')

    pdf.ln(5)
    
    pdf.add_page()
    if plot_image_path and os.path.exists(plot_image_path):
        pdf.chapter_title('Objective Function Plot')
        try:
            pdf.image(plot_image_path, x=20, w=160)
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
            pdf.image(extra_image_path, x=20, w=160)
            pdf.ln(5)
        except Exception as e:
            pdf.set_font('Arial', 'I', 10)
            pdf.cell(0, 10, f'Error loading plot image: {str(e)}', 0, 1)
    
    pdf.add_page()
    pdf.chapter_title('Initial State')
    pdf.add_schedule_table(initial_state.output_visualize_table())
    
    pdf.add_page()
    pdf.chapter_title('Final State')
    pdf.add_schedule_table(final_state.output_visualize_table())
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_algo_name = algorithm_name.replace(' ', '_').lower()
    output_dir = f'output/report/{input_basename}'
    output_path = f'{output_dir}/{safe_algo_name}_report_{timestamp}.pdf'

    os.makedirs(output_dir, exist_ok=True)
    
    pdf.output(output_path)
    
    return output_path
    