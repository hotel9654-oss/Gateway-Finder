#!/usr/bin/env python3
"""
Gate Scan Web Dashboard
Real-time analytics and visualization interface
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)
CORS(app)

DB_FILE = 'gateway_results.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total results
        cursor.execute('SELECT COUNT(*) as total FROM results')
        total = cursor.fetchone()['total']
        
        # Results today
        cursor.execute('''
            SELECT COUNT(*) as today FROM results 
            WHERE DATE(found_date) = DATE('now')
        ''')
        today = cursor.fetchone()['today']
        
        # Unique gateways
        cursor.execute('SELECT COUNT(DISTINCT gateway) as gateways FROM results')
        gateways = cursor.fetchone()['gateways']
        
        # Average response time
        cursor.execute('SELECT AVG(response_time) as avg_time FROM results WHERE response_time IS NOT NULL')
        avg_time = cursor.fetchone()['avg_time'] or 0
        
        conn.close()
        
        return jsonify({
            'total_results': total,
            'results_today': today,
            'unique_gateways': gateways,
            'avg_response_time': round(avg_time, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gateways')
def get_gateways():
    """Get gateway statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT gateway, COUNT(*) as count, AVG(response_time) as avg_response_time
            FROM results
            GROUP BY gateway
            ORDER BY count DESC
        ''')
        
        gateways = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(gateways)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results')
def get_results():
    """Get recent results"""
    try:
        limit = request.args.get('limit', 50, type=int)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM results
            ORDER BY found_date DESC
            LIMIT ?
        ''', (limit,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/timeline')
def get_timeline():
    """Get results timeline for last 7 days"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DATE(found_date) as date, COUNT(*) as count
            FROM results
            WHERE found_date >= datetime('now', '-7 days')
            GROUP BY DATE(found_date)
            ORDER BY date
        ''')
        
        timeline = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(timeline)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export')
def export_data():
    """Export results as JSON"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM results ORDER BY found_date DESC')
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
