# Machine Learning E4
AI experiments, including YOLO image detection and a Super Mario Bros AI model based on Q-Learning
For more details about the project, read the .pdf file (french only)

### Try out our AI model for Super Mario Bros:
- Open the Machine_Learning_Model folder
- Execute "pip install -r requirements.txt" in a terminal
- Configure the training settings in settings.py
- By default, a 100% win rate model is loaded, if you wish to start a new training, just delete the qTable.json file
- Execute main.py
- When you swap or delete the qTable, replace all the content in "score_graph.json" by "[]" if you want coherent data in your plots

### Known issues:
- When exiting at the moment the QTable is saved (when the game restarts), there's a risk of JSON data corruption. Don't worry if this happens, there's a system in place to periodically save the QTable, and you can find the backups in the "Backup" folder.
- The same issue may occur with data related to graphs. There's no backup system for this, so if you care about this data, make sure to save them before exiting the training.
- If the JSON file with the graph data ends up corrupted, delete its contents and leave just an empty array like this: "[]".