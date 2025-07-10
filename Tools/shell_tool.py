from langchain_community.tools import ShellTool

shell_tool = ShellTool()
result = shell_tool.invoke('mkdir robin')
print(result)

print(shell_tool.name)
print(shell_tool.description)
print(shell_tool.args)