import re
import urllib.request

content_path = r"C:\Users\Istiak\.gemini\antigravity\brain\3c87a07b-c0d9-4001-8330-cf1f1b2ff1d8\.system_generated\steps\3\content.md"

with open(content_path, "r", encoding="utf-8") as f:
    text = f.read()

urls = list(set(re.findall(r'https://lh3\.googleusercontent\.com/[^\s\"\'\>]+', text)))
print(f"Found {len(urls)} image URLs:")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for i, url in enumerate(urls):
    print(f"\nURL {i+1}: {url[:60]}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            filename = f"image_{i+1}.jpg"
            with open(filename, "wb") as f_out:
                f_out.write(data)
            print(f"Saved {filename} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed: {e}")
