#!/usr/bin/env python3
"""
EPUB to Markdown Chapter Extractor

Converts EPUB files into chapter-wise markdown files by parsing the EPUB structure
and extracting content from each chapter.

Requirements:
    pip install ebooklib beautifulsoup4 markdownify

Usage:
    python epub_to_markdown.py path/to/book.epub
"""

import argparse
import re
from pathlib import Path
from typing import List, Tuple, Optional
import zipfile

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from markdownify import markdownify as md


class EPUBProcessor:
    def __init__(self, epub_path: Path):
        self.epub_path = Path(epub_path)
        self.book = None
        self.output_dir = self.epub_path.parent / f"{self.epub_path.stem}_chapters"
        
    def load_epub(self):
        """Load the EPUB file."""
        try:
            self.book = epub.read_epub(str(self.epub_path))
            print(f"✓ Loaded EPUB: {self.book.get_metadata('DC', 'title')[0][0]}")
        except Exception as e:
            raise Exception(f"Failed to load EPUB file: {e}")
    
    def get_spine_items(self) -> List[epub.EpubHtml]:
        """Get all HTML items from the book's spine (reading order)."""
        spine_items = []
        for item_id, _ in self.book.spine:
            # Find item by ID in the book's items
            item = None
            for book_item in self.book.get_items():
                if book_item.get_id() == item_id:
                    item = book_item
                    break
            
            if item and isinstance(item, epub.EpubHtml):
                spine_items.append(item)
        return spine_items
    
    def clean_filename(self, title: str) -> str:
        """Clean title to create a valid filename."""
        # Remove HTML tags if any
        title = re.sub(r'<[^>]+>', '', title)
        # Replace problematic characters
        title = re.sub(r'[<>:"/\\|?*]', '_', title)
        # Remove extra whitespace
        title = re.sub(r'\s+', ' ', title).strip()
        # Limit length
        return title[:100] if len(title) > 100 else title
    
    def extract_title_from_content(self, soup: BeautifulSoup) -> str:
        """Extract chapter title from HTML content."""
        # Try different heading tags
        for tag in ['h1', 'h2', 'h3', 'title']:
            element = soup.find(tag)
            if element and element.get_text().strip():
                return element.get_text().strip()
        
        # Fallback: look for any element with common chapter indicators
        for element in soup.find_all(['p', 'div', 'span']):
            text = element.get_text().strip()
            if re.match(r'^(chapter|ch\.?)\s+\d+', text.lower()):
                return text
        
        return "Untitled Chapter"
    
    def html_to_markdown(self, html_content: str) -> str:
        """Convert HTML content to Markdown."""
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'meta', 'link']):
            element.decompose()
        
        # Convert to markdown
        markdown_content = md(
            str(soup),
            heading_style="ATX",
            bullets="-",
            strip=['script', 'style']
        )
        
        # Clean up excessive newlines
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        return markdown_content.strip()
    
    def process_chapters(self) -> List[Tuple[str, str]]:
        """Process all chapters and return list of (title, content) tuples."""
        spine_items = self.get_spine_items()
        chapters = []
        
        print(f"Found {len(spine_items)} items in spine")
        
        for i, item in enumerate(spine_items, 1):
            try:
                # Get HTML content - handle both string and bytes
                content = item.get_content()
                if isinstance(content, bytes):
                    html_content = content.decode('utf-8')
                else:
                    html_content = content
                
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract title
                title = self.extract_title_from_content(soup)
                
                # Skip if content is too short (likely not a chapter)
                text_content = soup.get_text().strip()
                if len(text_content) < 100:
                    print(f"  Skipping item {i}: too short ({len(text_content)} chars)")
                    continue
                
                # Convert to markdown
                markdown_content = self.html_to_markdown(html_content)
                
                if not markdown_content.strip():
                    print(f"  Skipping item {i}: no content after conversion")
                    continue
                
                chapters.append((title, markdown_content))
                print(f"  ✓ Processed: {title}")
                
            except Exception as e:
                print(f"  ✗ Error processing item {i}: {e}")
                continue
        
        return chapters
    
    def save_chapters(self, chapters: List[Tuple[str, str]]):
        """Save chapters as individual markdown files."""
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        print(f"\nSaving chapters to: {self.output_dir}")
        
        # Save each chapter
        for i, (title, content) in enumerate(chapters, 1):
            # Create filename
            clean_title = self.clean_filename(title)
            filename = f"{i:02d}_{clean_title}.md"
            filepath = self.output_dir / filename
            
            # Prepare content with title header
            full_content = f"# {title}\n\n{content}"
            
            # Write file
            try:
                filepath.write_text(full_content, encoding='utf-8')
                print(f"  ✓ Saved: {filename}")
            except Exception as e:
                print(f"  ✗ Error saving {filename}: {e}")
        
        print(f"\n✓ Completed! {len(chapters)} chapters saved to {self.output_dir}")
    
    def get_book_info(self) -> dict:
        """Extract book metadata."""
        if not self.book:
            return {}
        
        info = {}
        try:
            info['title'] = self.book.get_metadata('DC', 'title')[0][0]
        except (IndexError, KeyError):
            info['title'] = 'Unknown'
        
        try:
            info['author'] = ', '.join([author[0] for author in self.book.get_metadata('DC', 'creator')])
        except (IndexError, KeyError):
            info['author'] = 'Unknown'
        
        try:
            info['language'] = self.book.get_metadata('DC', 'language')[0][0]
        except (IndexError, KeyError):
            info['language'] = 'Unknown'
        
        return info
    
    def create_index_file(self, chapters: List[Tuple[str, str]]):
        """Create an index file with book info and chapter list."""
        info = self.get_book_info()
        
        index_content = f"""# {info['title']}

**Author:** {info['author']}  
**Language:** {info['language']}  
**Chapters:** {len(chapters)}

## Table of Contents

"""
        
        for i, (title, _) in enumerate(chapters, 1):
            clean_title = self.clean_filename(title)
            filename = f"{i:02d}_{clean_title}.md"
            index_content += f"{i}. [{title}](./{filename})\n"
        
        index_path = self.output_dir / "README.md"
        index_path.write_text(index_content, encoding='utf-8')
        print(f"  ✓ Created index: README.md")
    
    def process(self):
        """Main processing method."""
        print(f"Processing EPUB: {self.epub_path}")
        
        # Load EPUB
        self.load_epub()
        
        # Process chapters
        chapters = self.process_chapters()
        
        if not chapters:
            print("No chapters found to process!")
            return
        
        # Save chapters
        self.save_chapters(chapters)
        
        # Create index
        self.create_index_file(chapters)


def main():
    parser = argparse.ArgumentParser(
        description="Convert EPUB files to chapter-wise Markdown files"
    )
    parser.add_argument(
        "epub_file",
        type=Path,
        help="Path to the EPUB file to process"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output directory (default: creates folder next to EPUB file)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not args.epub_file.exists():
        print(f"Error: EPUB file not found: {args.epub_file}")
        return 1
    
    if not args.epub_file.suffix.lower() == '.epub':
        print(f"Error: File must have .epub extension: {args.epub_file}")
        return 1
    
    try:
        # Create processor
        processor = EPUBProcessor(args.epub_file)
        
        # Set custom output directory if provided
        if args.output:
            processor.output_dir = args.output
        
        # Process the EPUB
        processor.process()
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())