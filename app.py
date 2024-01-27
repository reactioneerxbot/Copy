from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask Application!"

#@app.route('/neon', methods=['GET'])
#def admin():
#    return "Hello Komiljon! Here you can use /menu | /stats | /users"
#
@app.route('/run<int:run_number>', methods=['GET', 'POST', 'HEAD'])
def run_command(run_number):
    if request.method in ['GET', 'POST', 'HEAD']:
        command_result = execute_command(f'python3 demo.py for run{run_number}')
        return command_result

def execute_command(command):
    import subprocess
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True)
        return f"Command Output: {result.stdout}\nCommand Error: {result.stderr}\n"
    except Exception as e:
        return f"Error: {str(e)}\n"

#@app.route('/core', methods=['GET'])
#def core():
#    import subprocess
#    if request.method == 'GET':
#        result = subprocess.run('timeout 1 python3 run_infinetely.py', capture_output=True, text=True)
#        return "The command is executed! Results: {result}"

#@app.route('/stats', methods=['GET'])
#def stats():
#    if request.method == 'GET':
#        result = subprocess.run('python3 stats.py', capture_output=True, text=True)
#        return f"Command Output: {result.stdout}\nCommand Error: {result.stderr}\n"
#
#@app.route('/users', methods=['GET'])
#def users():
#    if request.method == 'GET':
#        result = subprocess.run('python3 users.py', capture_output=True, text=True)
#        return f"Command Output: {result.stdout}\nCommand Error: {result.stderr}\n"

if __name__ == '__main__':
    app.run(debug=True)
