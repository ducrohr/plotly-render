from flask import Flask, request, jsonify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import io
import base64

app = Flask(__name__)

@app.route('/execute-plot', methods=['POST'])
def execute_plot():
    try:
        data = request.get_json()
        
        # CSV-Daten als DataFrame laden
        csv_data = data.get('csv_data', '')
        df = pd.read_csv(io.StringIO(csv_data))
        
        # Plotly-Code vom AI Agent
        plotly_code = data.get('plotly_code', '')
        
        # Sichere Ausführungsumgebung
        local_vars = {
            'df': df,
            'go': go,
            'px': px,
            'pd': pd
        }
        
        # Code ausführen
        exec(plotly_code, {"__builtins__": {}}, local_vars)
        
        # Figure aus local_vars holen
        fig = local_vars.get('fig')
        
        if fig:
            return jsonify({
                'html': fig.to_html(),
                'status': 'success'
            })
        else:
            return jsonify({
                'error': 'No figure created',
                'status': 'error'
            }), 400
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
