import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os

PORT = 8000
API_KEY = "sk-3b1d8f0e52a3433ca61747c40221924a"
API_URL = "https://api.deepseek.com/chat/completions"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/analyze':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                username = data.get('username', '用户')
                scores = data.get('scores', {})
                user_answers = data.get('answers', [])

                # Construct the prompt
                prompt = f"用户名称：{username}\n"
                prompt += "用户刚刚完成了一套数据分析师职业性格测试。请根据他们对以下问题的具体回答，生成一段幽默、深刻且富有洞察力的评价。\n\n"
                prompt += "用户回答记录：\n"
                for idx, item in enumerate(user_answers):
                    prompt += f"{idx+1}. 问：{item['q']}\n   答：{item['a']}\n"
                
                prompt += "\n请严格按照以下 HTML 结构返回内容（不要包含 markdown 代码块标记，不要包含 ```html，直接返回 div）：\n"
                prompt += """
                <div class="ai-result animate-fade-in">
                    <h2 class="text-3xl font-bold text-blue-600 mb-4">[这里填生成的创意称号]</h2>
                    <div class="bg-blue-50 p-6 rounded-lg mb-6 text-left">
                        <h3 class="font-bold text-gray-700 mb-2">💡 性格画像</h3>
                        <p class="text-gray-600 leading-relaxed mb-4">[这里填性格描述，基于用户的具体选择进行分析，约100字，幽默一点]</p>
                        
                        <h3 class="font-bold text-gray-700 mb-2">🚀 职业建议</h3>
                        <ul class="list-disc list-inside text-gray-600 mb-4 space-y-1">
                            <li>[建议1]</li>
                            <li>[建议2]</li>
                            <li>[建议3]</li>
                        </ul>
                    </div>
                </div>
                """

                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是一个资深、幽默的数据分析师职业顾问。请只返回 HTML 代码，不要任何解释。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 1.3,
                    "stream": False
                }

                req = urllib.request.Request(API_URL, data=json.dumps(payload).encode('utf-8'), headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {API_KEY}'
                })

                with urllib.request.urlopen(req) as response:
                    res_body = response.read()
                    res_json = json.loads(res_body.decode('utf-8'))
                    ai_content = res_json['choices'][0]['message']['content']
                    
                    # Clean up if AI returns markdown code blocks
                    if ai_content.startswith("```html"):
                        ai_content = ai_content[7:]
                    if ai_content.startswith("```"):
                        ai_content = ai_content[3:]
                    if ai_content.endswith("```"):
                        ai_content = ai_content[:-3]
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"result": ai_content}).encode('utf-8'))

            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                print(f"HTTP Error {e.code}: {error_body}")
                self.send_response(e.code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"API Error: {e.reason}", "details": error_body}).encode('utf-8'))

            except Exception as e:
                print(f"Error: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            super().do_POST()

# Allow address reuse
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
