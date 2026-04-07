# pip install graphviz

import os
from graphviz import Digraph

# Ensure an output directory exists
os.makedirs("diagrams", exist_ok=True)

def create_system_architecture_diagram():
    """Generates the high-level System Architecture Diagram."""
    dot = Digraph(comment='System Architecture', format='png')
    dot.attr(rankdir='LR', size='10,6')
    dot.attr('node', shape='box', style='filled', color='lightblue2', fontname='Arial')

    # Define Nodes
    dot.node('UI', 'Frontend Dashboard\n(React.js / HTML)')
    dot.node('API', 'Web Backend Server\n(Flask / FastAPI)')
    
    with dot.subgraph(name='cluster_cad') as c:
        c.attr(style='filled', color='lightgrey')
        c.node('PythonCOM', 'Python Automation\n(pywin32)')
        c.node('SW', 'SolidWorks & CAMWorks\n(AFR & G-Code)')
        c.attr(label='CAD/CAM Integration Module')

    with dot.subgraph(name='cluster_ml') as c:
        c.attr(style='filled', color='lightgreen')
        c.node('CNN_LSTM', 'Deep Learning Model\n(CNN-LSTM)')
        c.node('LIME', 'Explainable AI\n(LIME)')
        c.attr(label='Predictive Maintenance Module')
        
    dot.node('Sensors', 'CNC Sensors\n(Vibration, Acoustic, Temp)', shape='cylinder', color='orange')

    # Define Edges
    dot.edge('UI', 'API', label=' REST/JSON')
    dot.edge('API', 'UI', label=' Dashboard Data')
    
    dot.edge('API', 'PythonCOM', label=' Trigger CAD Script')
    dot.edge('PythonCOM', 'SW', label=' COM Interface')
    dot.edge('SW', 'PythonCOM', label=' Toolpaths / STEP-NC')
    dot.edge('PythonCOM', 'API', label=' Return Machining Data')

    dot.edge('Sensors', 'CNN_LSTM', label=' Live Data Stream')
    dot.edge('API', 'CNN_LSTM', label=' Request RUL')
    dot.edge('CNN_LSTM', 'LIME', label=' Feature Weights')
    dot.edge('LIME', 'API', label=' Interpretable Predictions')

    dot.render('diagrams/system_architecture', cleanup=True)
    print("System Architecture Diagram generated.")


def create_workflow_diagram():
    """Generates the step-by-step Workflow/Process Diagram."""
    dot = Digraph(comment='Workflow Diagram', format='png')
    dot.attr(rankdir='TB', size='8,10')
    dot.attr('node', shape='oval', style='filled', color='lightyellow', fontname='Arial')

    dot.node('Start', 'Operator Uploads CAD / Starts Process', shape='Mdiamond', color='gold')
    
    dot.node('A', 'Backend Receives Request')
    dot.node('B', 'Python Script Invokes SolidWorks API')
    dot.node('C', 'Automated Feature Recognition (AFR) on B-rep')
    dot.node('D', 'Generate STEP-NC / G-Code Toolpaths')
    
    dot.node('E', 'CNC Machining Commences')
    dot.node('F', 'Capture Multi-modal Sensor Data')
    dot.node('G', 'CNN-LSTM Processes Sequence Data')
    dot.node('H', 'LIME Generates Explanations')
    
    dot.node('I', 'Web UI Updates with RUL & Toolpaths')
    dot.node('End', 'Process Complete', shape='Msquare', color='gold')

    # Flow
    dot.edges([('Start', 'A'), ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), 
               ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'I'), ('I', 'End')])

    dot.render('diagrams/workflow_diagram', cleanup=True)
    print("Workflow Diagram generated.")


def create_uml_class_diagram():
    """Generates a simplified UML Class/Component Diagram."""
    dot = Digraph(comment='UML Class Diagram', format='png')
    dot.attr(rankdir='BT', size='10,8')
    dot.attr('node', shape='record', fontname='Arial')

    # Classes
    dot.node('WebUI', '{WebDashboard|+ viewPart()\n+ showPredictions()\n+ startMachining()|- renderCharts()}')
    dot.node('API', '{BackendController|+ route_requests()\n+ trigger_cad_pipeline()\n+ fetch_rul()|- db_connection}')
    dot.node('CADModule', '{CADAutomation|+ extract_brep_features()\n+ generate_gcode()\n+ map_api_calls()|- pywin32_instance}')
    dot.node('MLModule', '{PdM_Predictor|+ load_sensor_data()\n+ predict_rul()\n+ generate_lime_explanation()|- cnn_lstm_weights}')
    dot.node('CNCMachine', '{ShopFloorEquipment|+ execute_toolpath()\n+ stream_telemetry()|- sensor_array}')

    # Relationships (Dependencies / Associations)
    dot.edge('WebUI', 'API', label=' <<uses>>')
    dot.edge('API', 'CADModule', label=' <<invokes>>')
    dot.edge('API', 'MLModule', label=' <<queries>>')
    dot.edge('CADModule', 'CNCMachine', label=' sends G-code')
    dot.edge('CNCMachine', 'MLModule', label=' telemetry stream')

    dot.render('diagrams/uml_class_diagram', cleanup=True)
    print("UML Class Diagram generated.")


if __name__ == "__main__":
    create_system_architecture_diagram()
    create_workflow_diagram()
    create_uml_class_diagram()
    print("All diagrams have been successfully saved to the 'diagrams' folder.")