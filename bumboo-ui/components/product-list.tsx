"use client"
import { ScrollArea } from "@/components/ui/scroll-area"
import type { Product } from "@/lib/types"

interface ProductListProps {
  products: Product[]
  selectedProduct: Product
  onSelectProduct: (product: Product) => void
}

export function ProductList({ products, selectedProduct, onSelectProduct }: ProductListProps) {
  return (
    <div className="w-80 border-r border-border bg-card">
      <div className="p-4 border-b border-border">
        <h2 className="text-lg font-semibold text-foreground">Products</h2>
        <p className="text-sm text-muted-foreground">Select a product to view details</p>
      </div>
      <ScrollArea className="h-[calc(100vh-80px)]">
        <div className="p-2">
          {products.map((product) => (
            <button
              key={product.id}
              onClick={() => onSelectProduct(product)}
              className={`w-full text-left p-3 rounded-lg mb-2 transition-colors ${
                selectedProduct.id === product.id
                  ? "bg-accent text-accent-foreground"
                  : "hover:bg-accent/50 text-foreground"
              }`}
            >
              <div className="font-medium text-sm">{product.brand}</div>
              <div className="text-sm text-muted-foreground mt-1">{product.name}</div>
              <div className="text-xs text-muted-foreground mt-1">{product.type} • {product.sitesCount ?? 0} sites</div>
            </button>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}
