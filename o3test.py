import json, os, urllib.request
body = json.dumps({
    "model": "openai/o3",
    "messages": [{"role":"user","content":"Output only this Lean code in a code block: theorem foo : 1 = 1 := rfl"}],
    "max_tokens": 16000, "reasoning": {"effort": "medium"},
}).encode()
req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
    headers={"Authorization":"Bearer "+os.environ["OPENROUTER_API_KEY"],"Content-Type":"application/json"})
d = json.loads(urllib.request.urlopen(req, timeout=180).read())
m = d["choices"][0]["message"]
print("finish:", d["choices"][0].get("finish_reason"))
print("content:", repr(m.get("content"))[:500])
print("has reasoning field:", "reasoning" in m, "len:", len(m.get("reasoning") or ""))