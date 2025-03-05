from crewai_tools import DirectoryReadTool

# Initialize the tool with the directory you want to explore
tool = DirectoryReadTool(directory='E:/Documents/TEDIES/travaux 2024/document_synth/src/document_synth/data')

# Use the tool to list the contents of the specified directory
directory_contents = tool.run()
print(directory_contents)