// pdf-text.swift: print the text of a PDF (optionally one page range) using
// macOS's own PDFKit, so a paper can be read without poppler.
//   swift scripts/pdf-text.swift paper.pdf [firstPage lastPage]
import Foundation
import PDFKit

let a = CommandLine.arguments
guard a.count >= 2, let doc = PDFDocument(url: URL(fileURLWithPath: a[1])) else { print("usage: swift pdf-text.swift FILE.pdf [first last]"); exit(1) }
let first = a.count > 3 ? Int(a[2])! : 1
let last = a.count > 3 ? Int(a[3])! : doc.pageCount
print("pages \(doc.pageCount)")
for n in first...min(last, doc.pageCount) {
    print("\n=== PAGE \(n) ===")
    print(doc.page(at: n - 1)?.string ?? "")
}
