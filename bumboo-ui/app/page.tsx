"use client"

import { useEffect, useState } from "react"
import { ProductList } from "@/components/product-list"
import { ProductDetails } from "@/components/product-details"
import type { Product, PriceHistoryItem } from "@/lib/types"

function basicAuthHeader(): string | null {
  if (typeof window === "undefined") return null
  const u = window.localStorage.getItem("bumboo_user")
  const p = window.localStorage.getItem("bumboo_pass")
  if (u && p) return "Basic " + btoa(`${u}:${p}`)
  return null
}

export default function DashboardPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    async function load() {
      setLoading(true)
      let auth = basicAuthHeader()
      if (!auth) {
        const u = prompt("API user")
        const p = prompt("API pass")
        if (!u || !p) { setLoading(false); return }
        window.localStorage.setItem("bumboo_user", u)
        window.localStorage.setItem("bumboo_pass", p)
        auth = basicAuthHeader()
      }
      try {
      const API_BASE = "http://localhost:8000"
      const res = await fetch(`${API_BASE}/api/products?days=30`, { headers: { Authorization: auth! } })
        if (!res.ok) throw new Error(res.statusText)
        const data = await res.json()
        const mapped: Product[] = data.map((d: any, idx: number) => ({
          id: `${d.brand}-${d.description}-${d.size || ""}-${idx}`,
          brand: d.brand,
          name: d.description,
          type: d.size || "",
          highestPrice: d.max_price ?? 0,
          avgPrice: d.avg_price ?? 0,
          lowestPrice: d.min_price ?? 0,
          image: d.image || "/placeholder.jpg",
          priceHistory: [] as PriceHistoryItem[],
          sitesCount: d.sites_count ?? d.count ?? 0,
          sites: d.sites ?? [],
        }))
        setProducts(mapped)
        setSelectedProduct(mapped[0] ?? null)
      } catch (err) {
        console.error(err)
        alert("Failed to load products: " + err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  // when selected product changes, load its price history
  useEffect(() => {
    async function loadHistory(product: Product) {
      const auth = basicAuthHeader()
      if (!auth) return
      try {
        const API_BASE = "http://localhost:8000"
        const res = await fetch(`${API_BASE}/api/price-history?brand=${encodeURIComponent(product.brand)}&description=${encodeURIComponent(product.name)}&days=30`, { headers: { Authorization: auth } })
        if (!res.ok) throw new Error(res.statusText)
        const data = await res.json()
        const history = data
          .map((d: any) => ({
            date: d.date,
            fairprice: d.fairprice ?? null,
            coldStorage: d.coldStorage ?? null,
            redmart: d.redmart ?? null,
            reviews: d.reviews ?? null,
          }))
          .filter((h) => h.fairprice != null || h.coldStorage != null || h.redmart != null) as PriceHistoryItem[]
        // compute overall stats across all sites
        const values = history.flatMap(h => [h.fairprice, h.coldStorage, h.redmart].filter((v) => v != null) as number[])
        const stats = {
          max: values.length ? Math.max(...values) : 0,
          min: values.length ? Math.min(...values) : 0,
          avg: values.length ? values.reduce((a,b) => a + b, 0) / values.length : 0,
        }
        // update product in list and selectedProduct
        setProducts((prev) => prev.map(p => p.id === product.id ? { ...p, priceHistory: history, highestPrice: stats.max, avgPrice: stats.avg, lowestPrice: stats.min } : p))
        setSelectedProduct((prev) => prev ? { ...prev, priceHistory: history, highestPrice: stats.max, avgPrice: stats.avg, lowestPrice: stats.min } : prev)
      } catch (err) {
        console.error(err)
      }
    }
    if (selectedProduct) {
      loadHistory(selectedProduct)
    }
  }, [selectedProduct?.id])

  return (
    <div className="flex h-screen bg-background">
      <ProductList products={products} selectedProduct={selectedProduct ?? ({} as Product)} onSelectProduct={(p)=>setSelectedProduct(p)} />
      {selectedProduct ? <ProductDetails product={selectedProduct} /> : <div className="flex-1 p-8"> {loading ? "Loading..." : "No product selected"} </div>}
    </div>
  )
}
