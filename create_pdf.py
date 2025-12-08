from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Bitacora de Pruebas - Maizimo App', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def create_pdf(input_file, output_file):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_table = False
    col_widths = []
    headers = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if in_table:
                in_table = False
                pdf.ln(5)
            continue
            
        # Headers
        if line.startswith('#'):
            level = line.count('#')
            text = line.replace('#', '').strip()
            pdf.set_font('Arial', 'B', 16 - (level * 2))
            pdf.cell(0, 10, text, 0, 1, 'L')
            
        # Table
        elif line.startswith('|'):
            if '---' in line:
                continue
                
            cells = [c.strip() for c in line.split('|') if c.strip() != '']
            
            if not in_table:
                # Table Header
                in_table = True
                pdf.set_font('Arial', 'B', 9)
                # Calculate widths roughly based on content or fixed
                # Adjust these widths based on your specific table columns
                # Columns: ID, Funcionalidad, Descripción, Entrada, Esperado, Obtenido, Estado, Fechas (8 cols)
                if len(cells) == 8:
                    col_widths = [20, 25, 35, 30, 30, 30, 15, 20] # Total ~205
                else:
                    col_widths = [190 // len(cells)] * len(cells)
                
                # Draw header
                for i, cell in enumerate(cells):
                    pdf.cell(col_widths[i], 10, cell, 1, 0, 'C')
                pdf.ln()
                
            else:
                # Table Row
                pdf.set_font('Arial', '', 8)
                
                # Calc max height for row
                line_height = 5
                max_h = line_height
                
                # Prepare text for each cell to handle wrapping if needed
                # FPDF MultiCell is tricky in a row. 
                # Simplified approach: Just verify row contents.
                # Since tables are complex in FPDF, let's use a simpler fixed height or just truncate for this demo
                # or use multi_cell trick.
                
                # Better approach for rows: Save current position
                x_start = pdf.get_x()
                y_start = pdf.get_y()
                max_y = y_start
                
                for i, cell in enumerate(cells):
                    if i >= len(col_widths): break
                    
                    x_current = x_start + sum(col_widths[:i])
                    pdf.set_xy(x_current, y_start)
                    
                    # Clean markdown bold/break
                    cell_text = cell.replace('**', '').replace('<br>', '\n')
                    
                    pdf.multi_cell(col_widths[i], line_height, cell_text, 1, 'L')
                    
                    if pdf.get_y() > max_y:
                        max_y = pdf.get_y()
                
                # Move to next line (max height of the row)
                pdf.set_xy(x_start, max_y)
                
        # Normal text
        else:
            if in_table:
                in_table = False
                pdf.ln(5)
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 8, line)

    pdf.output(output_file)
    print(f"PDF generado: {output_file}")

if __name__ == "__main__":
    create_pdf('bitacora_pruebas.md', 'bitacora_pruebas.pdf')
