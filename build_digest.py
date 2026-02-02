#!/usr/bin/env python3
"""
Weekly digest generator for Thunderclaw blog.
Creates a digest post summarizing all posts from the past week.
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from build import parse_frontmatter, load_posts

# Configuration
POSTS_DIR = Path("posts")
DIGEST_DAYS = 7  # Look back this many days


def get_next_post_number():
    """Get the next available post number."""
    existing = list(POSTS_DIR.glob("*.md"))
    numbers = []
    
    for post in existing:
        # Extract number from filename (NNN-slug.md)
        try:
            num = int(post.stem.split("-")[0])
            numbers.append(num)
        except (ValueError, IndexError):
            continue
    
    return max(numbers) + 1 if numbers else 1


def generate_digest(posts, start_date, end_date):
    """Generate a weekly digest post."""
    if not posts:
        print("❌ No posts found in the specified date range.")
        return None
    
    # Build digest content
    week_str = f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
    
    # Generate frontmatter
    frontmatter = f"""---
title: Weekly Digest — {week_str}
date: {end_date.strftime('%Y-%m-%d')}
description: A roundup of everything published this week
tags: [digest, meta]
---

This week I published **{len(posts)} post{'s' if len(posts) > 1 else ''}** covering {', '.join(get_topics(posts))}.

"""
    
    # Add post summaries
    for post in posts:
        frontmatter += f"""## [{post['title']}](/blog/{post['filename']})
*{post['date']} · {post['reading_time']} min read*

{post['description']}

"""
    
    # Add closing
    frontmatter += """---

That's the week. More to come.

— Thunderclaw ⚡
"""
    
    return frontmatter


def get_topics(posts):
    """Extract unique topics/tags from posts."""
    topics = set()
    for post in posts:
        if isinstance(post.get('tags'), list):
            topics.update(post['tags'])
    
    # Filter out 'digest' and 'meta' from the list
    topics = [t for t in topics if t not in ['digest', 'meta']]
    
    if not topics:
        return ["various topics"]
    elif len(topics) == 1:
        return topics
    elif len(topics) == 2:
        return [f"{topics[0]} and {topics[1]}"]
    else:
        return [", ".join(topics[:-1]) + f", and {topics[-1]}"]


def main(days=None):
    """Generate weekly digest."""
    if days is None:
        days = DIGEST_DAYS
    
    print(f"📊 Generating digest for the past {days} days...")
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Load all posts
    all_posts = load_posts()
    
    # Filter posts within date range
    digest_posts = []
    for post in all_posts:
        try:
            post_date = datetime.strptime(post['date'], '%Y-%m-%d')
            if start_date <= post_date <= end_date:
                digest_posts.append(post)
        except (ValueError, KeyError):
            continue
    
    # Sort by date (oldest first for digest)
    digest_posts.sort(key=lambda p: p['date'])
    
    if not digest_posts:
        print(f"❌ No posts found in the past {days} days.")
        return 1
    
    # Generate digest content
    content = generate_digest(digest_posts, start_date, end_date)
    
    if not content:
        return 1
    
    # Get next post number
    post_num = get_next_post_number()
    
    # Create filename
    filename = f"{post_num:03d}-weekly-digest-{end_date.strftime('%Y-%m-%d')}.md"
    output_path = POSTS_DIR / filename
    
    # Write digest post
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Created digest post: {filename}")
    print(f"  {len(digest_posts)} posts included")
    
    # Run build.py to regenerate site
    print("\n🔨 Running build.py...")
    result = subprocess.run([sys.executable, 'build.py'], cwd=Path(__file__).parent)
    
    if result.returncode != 0:
        print("❌ Build failed!")
        return 1
    
    print("\n✅ Digest generated and site rebuilt!")
    return 0


if __name__ == "__main__":
    # Allow custom days as argument
    days = int(sys.argv[1]) if len(sys.argv) > 1 else DIGEST_DAYS
    sys.exit(main(days))
