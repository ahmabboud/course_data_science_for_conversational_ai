// pdf-pages.swift: render chosen pages of a PDF to PNG, using macOS's own
// PDFKit (no poppler needed). Used by print-handout.sh so a printed handout
// page can be opened as an image and checked for clipping.
//
//   swift scripts/pdf-pages.swift handout.pdf OUT_DIR 3,4,7   -> OUT_DIR/p3.png ...
import AppKit
import PDFKit

let args = CommandLine.arguments
guard args.count == 4, let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    print("usage: swift pdf-pages.swift FILE.pdf OUT_DIR 3,4,7"); exit(1)
}
print("pages", doc.pageCount)
for item in args[3].split(separator: ",") {
    guard let n = Int(item), let page = doc.page(at: n - 1) else { continue }
    let box = page.bounds(for: .mediaBox)
    let image = page.thumbnail(of: NSSize(width: box.width * 1.2, height: box.height * 1.2), for: .mediaBox)
    let bitmap = NSBitmapImageRep(data: image.tiffRepresentation!)!
    try! bitmap.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[2] + "/p\(n).png"))
    print("wrote p\(n).png")
}
