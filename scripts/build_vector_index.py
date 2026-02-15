"""
Build FAISS Vector Index from AMU Ordinances
Processes ordinance PDFs and creates searchable vector store
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.services.document_processor import document_processor
from backend.services.vector_store import vector_store
import pdfplumber


def process_ordinance_pdf(pdf_path: Path) -> list:
    """Process ordinance PDF and extract chunks"""
    print(f"📄 Processing: {pdf_path.name}")
    
    chunks = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract all text
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n\n"
            
            # Chunk the document
            text_chunks = document_processor.chunk_document(
                full_text,
                chunk_size=800,
                overlap=100
            )
            
            # Add metadata
            for i, chunk in enumerate(text_chunks):
                chunks.append({
                    "text": chunk,
                    "metadata": {
                        "source": pdf_path.name,
                        "chunk_id": i,
                        "document_type": "ordinance"
                    }
                })
            
            print(f"   ✅ Created {len(chunks)} chunks")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return chunks


def build_vector_index():
    """Build vector index from ordinance PDFs"""
    print("=" * 60)
    print("Building FAISS Vector Index")
    print("=" * 60)
    
    # Find ordinance PDFs
    pdf_dir = Path(__file__).parent.parent / "data" / "raw"
    if not pdf_dir.exists():
        pdf_dir = Path("/mnt/user-data/uploads")
    
    ordinance_files = [
        "btech_23_99.pdf",  # Main ordinances
    ]
    
    all_chunks = []
    
    for filename in ordinance_files:
        pdf_path = pdf_dir / filename
        
        if not pdf_path.exists():
            print(f"⚠️  File not found: {filename}")
            continue
        
        chunks = process_ordinance_pdf(pdf_path)
        all_chunks.extend(chunks)
    
    if not all_chunks:
        print("❌ No documents to index!")
        return
    
    print(f"\n📊 Total chunks: {len(all_chunks)}")
    print("🔨 Building FAISS index...")
    
    # Add to vector store
    texts = [chunk["text"] for chunk in all_chunks]
    metadatas = [chunk["metadata"] for chunk in all_chunks]
    
    vector_store.add_documents(texts, metadatas)
    
    # Save index
    print("💾 Saving vector store...")
    vector_store.save()
    
    # Show stats
    stats = vector_store.get_stats()
    print(f"\n✅ Vector store built successfully!")
    print(f"   📊 Total documents: {stats['total_documents']}")
    print(f"   📊 Index size: {stats['index_size']}")
    print(f"   📊 Dimension: {stats['dimension']}")
    
    # Test search
    print("\n🔍 Testing search...")
    test_query = "promotion requirements credits"
    results = vector_store.similarity_search(test_query, k=2)
    
    if results:
        print(f"   ✅ Found {len(results)} results for: '{test_query}'")
        print(f"   📄 Top result preview: {results[0]['text'][:150]}...")
    else:
        print("   ⚠️  No results found")


if __name__ == "__main__":
    build_vector_index()