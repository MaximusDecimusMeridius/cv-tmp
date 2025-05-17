from diagrams import Diagram, Cluster, Edge
from diagrams.aws.ml import Sagemaker
from diagrams.aws.general import General
from diagrams.aws.analytics import Analytics
from diagrams.aws.iot import IotSensor
from diagrams.programming.framework import Flask
from diagrams.onprem.client import Users

with Diagram("Project Overview", show=False, filename="project_flowchart", direction="TB"):
    
    # Project Phases
    with Cluster("Development Phases"):
        phases = [
            Flask("Dev Phase 1:\nModel Development"),
            Flask("Dev Phase 2:\nIntegration & NL Summaries")
        ]
    
    # Models Section
    with Cluster("Current Models"):
        with Cluster("GeoFM Model"):
            geofm = Sagemaker("GeoFM\nWhole Season Prediction")
            geofm_inputs = [
                IotSensor("Satellite\nImagery"),
                IotSensor("Weather\nData"),
                IotSensor("Seeding\nData")
            ]
            for inp in geofm_inputs:
                inp >> geofm
        
        with Cluster("Green Earthnet Model"):
            green = Sagemaker("Green Earthnet\nIn-Season Prediction")
            green_inputs = [
                IotSensor("Historical\nSatellite Data"),
                IotSensor("Weather\nData")
            ]
            for inp in green_inputs:
                inp >> green
    
    # Data Limitations
    with Cluster("Data Limitations"):
        limitations = [
            General("Geographic:\nMS Delta Only"),
            General("Temporal:\n1-2 Seasons"),
            General("Crops:\nSoybeans Only"),
            General("Input Issues")
        ]
    
    # Actionable Levers
    with Cluster("Farmer Actions"):
        actions = [
            Users("Seeding"),
            Users("Applications"),
            Users("Irrigation")
        ]
    
    # Next Steps
    with Cluster("Next Steps"):
        next_steps = [
            Analytics("LLM Integration"),
            Analytics("Scale Models"),
            Analytics("Improve Data"),
            Analytics("John Deere\nIntegration")
        ]
    
    # Timeline
    with Cluster("Timeline"):
        timeline = [
            General("Week 12-13:\nExplainability"),
            General("May 12:\nKnowledge Transfer"),
            General("May 19:\nTeam Release")
        ]
    
    # Connect main components
    phases[0] >> geofm
    phases[0] >> green
    phases[1] >> next_steps[0]
    
    # Connect models to next steps
    geofm >> Edge(color="darkgreen") >> next_steps[0]
    green >> Edge(color="darkgreen") >> next_steps[0]
    
    # Connect timeline
    timeline[0] >> timeline[1] >> timeline[2] 