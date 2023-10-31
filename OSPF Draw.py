#Programmed by Garrett Strahan
#@   Test Your Script:
#  Ensure that you have a testbed.yaml file with information about your network devices, and that your network is properly configured for OSPF. Replace 'testbed.yaml' with the path to your own testbed file.
#   Run the Script:
#    Execute the script using Python. It will generate a network graph in DOT and PNG formats and create a PDF document with the network topology.

#This script will give you a basic network graph of OSPF neighbors, but you can customize it further based on your specific requirements and the information you want to display in the PDF report.
#MAKE SURE YOU CREATE A testbed.yaml file for the credentials!!!

#This can create a Python script that uses Genie to gather OSPF information from your network devices and then use Graphviz to create a network graph and ReportLab to generate a PDF document.


from genie.testbed import load
from genie.libs.graphs.ops import ospf
from graphviz import Digraph
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Define your testbed file (testbed.yaml) to specify your network devices
testbed = load('testbed.yaml')

# Create a Genie OSPF object to gather OSPF information
ospf_graph = ospf.Ospf(testbed)

# Gather OSPF information from the network
ospf_graph.learn()

# Create a Graphviz Digraph to visualize the network graph
dot = Digraph('Network Graph')
dot.attr(rankdir='LR')  # Horizontal layout

for device, data in ospf_graph.info.items():
    # Add nodes for each device
    dot.node(device)

    for neighbor, neighbor_data in data.get('neighbors', {}).items():
        # Add edges for OSPF neighbors
        dot.edge(device, neighbor)

# Save the network graph as a picture (e.g., in DOT or PNG format)
dot.save('network_graph.dot')
dot.render('network_graph', format='png')

# Create a PDF document with the network graph
def create_pdf_with_graph(pdf_filename, graph_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, 'Network OSPF Topology')
    c.drawImage(graph_filename, 100, 100, width=400, height=300)
    c.showPage()
    c.save()

create_pdf_with_graph('network_topology.pdf', 'network_graph.png')
