import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

user_url = "https://api.github.com/users/Ishtiak-Ahmed886"
req_user = urllib.request.Request(user_url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req_user) as resp:
        profile = json.loads(resp.read().decode('utf-8'))
        print("=== GITHUB PROFILE ANALYSIS ===")
        print(f"Username: {profile.get('login')}")
        print(f"Name: {profile.get('name')}")
        print(f"Bio: {profile.get('bio')}")
        print(f"Public Repos: {profile.get('public_repos')}")
        print(f"Followers: {profile.get('followers')}")
        print(f"Location: {profile.get('location')}")
except Exception as e:
    print(f"Profile error: {e}")

repos_url = "https://api.github.com/users/Ishtiak-Ahmed886/repos?sort=updated&per_page=100"
req_repos = urllib.request.Request(repos_url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req_repos) as resp:
        repos = json.loads(resp.read().decode('utf-8'))
        print(f"\n=== REPOSITORIES ({len(repos)}) ===")
        
        languages = {}
        for r in repos:
            name = r['name']
            lang = r.get('language') or 'Other'
            desc = r.get('description') or 'No description'
            updated = r.get('updated_at', '')[:10]
            forks = r.get('forks_count', 0)
            stars = r.get('stargazers_count', 0)
            html_url = r.get('html_url', '')
            
            languages[lang] = languages.get(lang, 0) + 1
            print(f"- {name} [{lang}] | Stars: {stars} | Updated: {updated} | URL: {html_url}")
            if desc != 'No description':
                print(f"  Desc: {desc}")
                
        print("\n=== LANGUAGE BREAKDOWN ===")
        for l, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            print(f"- {l}: {count} repos")

except Exception as e:
    print(f"Repos error: {e}")
