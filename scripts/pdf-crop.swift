// pdf-crop.swift: cut a rectangle out of one PDF page and save it as a PNG,
// using macOS's own PDFKit. Used to take a figure from a paper for a slide.
//
//   swift scripts/pdf-crop.swift paper.pdf PAGE x0 y0 x1 y1 OUT.png [SCALE]
//
// PAGE starts at 1. The rectangle is in fractions of the page, measured from
// the top-left corner (0 0 is top-left, 1 1 is bottom-right). SCALE is the
// render scale (default 3, about 216 dpi). To find the box, first render the
// whole page with: swift scripts/pdf-crop.swift paper.pdf 4 0 0 1 1 page4.png 1.5
import AppKit
import PDFKit

let a = CommandLine.arguments
guard a.count >= 8, let doc = PDFDocument(url: URL(fileURLWithPath: a[1])),
      let pageNo = Int(a[2]), let page = doc.page(at: pageNo - 1),
      let x0 = Double(a[3]), let y0 = Double(a[4]), let x1 = Double(a[5]), let y1 = Double(a[6]) else {
    print("usage: swift pdf-crop.swift FILE.pdf PAGE x0 y0 x1 y1 OUT.png [SCALE]"); exit(1)
}
let scale = a.count > 8 ? Double(a[8])! : 3.0
let box = page.bounds(for: .mediaBox)
let fullW = Int(box.width * scale), fullH = Int(box.height * scale)
let cs = CGColorSpaceCreateDeviceRGB()
guard let ctx = CGContext(data: nil, width: fullW, height: fullH, bitsPerComponent: 8, bytesPerRow: 0, space: cs,
                          bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { print("context failed"); exit(1) }
ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
ctx.fill(CGRect(x: 0, y: 0, width: fullW, height: fullH))
ctx.scaleBy(x: scale, y: scale)
page.draw(with: .mediaBox, to: ctx)
guard let full = ctx.makeImage() else { print("render failed"); exit(1) }
let cropRect = CGRect(x: x0 * Double(fullW), y: y0 * Double(fullH), width: (x1 - x0) * Double(fullW), height: (y1 - y0) * Double(fullH))
guard let cropped = full.cropping(to: cropRect) else { print("crop failed"); exit(1) }
let rep = NSBitmapImageRep(cgImage: cropped)
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[7]))
print("wrote \(a[7]) \(cropped.width)x\(cropped.height)")
