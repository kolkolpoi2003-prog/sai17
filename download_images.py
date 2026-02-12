import os
import requests

images = {
    "hero_1.jpg": "https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=2600&auto=format&fit=crop",
    "cat_sunglasses.jpg": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2000&auto=format&fit=crop",
    "cat_optical.jpg": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=1500&auto=format&fit=crop",
    "cat_accessories.jpg": "https://images.unsplash.com/photo-1591076482161-42ce6da69f67?q=80&w=1500&auto=format&fit=crop",
    "cta_bg.jpg": "https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=2000&auto=format&fit=crop",
    "discount_bg.jpg": "https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=2560&auto=format&fit=crop",
    "review_1.jpg": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?fit=crop&w=100&h=100",
    "review_2.jpg": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?fit=crop&w=100&h=100",
    "review_3.jpg": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?fit=crop&w=100&h=100"
}

base_dir = "static/images/home"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

for name, url in images.items():
    path = os.path.join(base_dir, name)
    if not os.path.exists(path):
        print(f"Downloading {name}...")
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(r.content)
                print(f"Saved {name}")
            else:
                print(f"Failed to download {name}: Status {r.status_code}")
        except Exception as e:
            print(f"Error downloading {name}: {e}")
    else:
        print(f"{name} already exists")
