"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { PriceChart } from "@/components/price-chart"
import { PriceTable } from "@/components/price-table"
import type { Product } from "@/lib/types"
import Image from "next/image"
import { ImageWithFallback } from "./image-with-fallback"

interface ProductDetailsProps {
  product: Product
}

export function ProductDetails({ product }: ProductDetailsProps) {
  const [dateRange, setDateRange] = useState<"month" | "lastMonth" | "all">("month")

  const filteredPriceData = product.priceHistory.filter((item) => {
    if (dateRange === "month") return true
    if (dateRange === "lastMonth") return true
    return true
  })

  return (
    <div className="flex-1 overflow-auto">
      <div className="p-8">
        <h1 className="text-2xl font-bold text-foreground mb-6">
          {product.brand} - {product.name}
        </h1>

        <div className="grid grid-cols-3 gap-4 mb-6">
          <Card className="bg-card border-border">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">Highest Price</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-destructive">${product.highestPrice.toFixed(2)}</div>
              <p className="text-xs text-muted-foreground mt-1">Last 30 days</p>
            </CardContent>
          </Card>

          <Card className="bg-card border-border">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">Average Price</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">${product.avgPrice.toFixed(2)}</div>
              <p className="text-xs text-muted-foreground mt-1">Last 30 days</p>
            </CardContent>
          </Card>

          <Card className="bg-card border-border">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">Lowest Price</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">${product.lowestPrice.toFixed(2)}</div>
              <p className="text-xs text-muted-foreground mt-1">Last 30 days</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-3 gap-6 mb-6">
          <Card className="bg-card border-border">
          <CardContent className="p-6">
            <div className="relative aspect-square w-full">
              <ImageWithFallback src={product.image || "/placeholder.jpg"} alt={product.name} />
            </div>
          </CardContent>
          </Card>

          <Card className="col-span-2 bg-card border-border">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-foreground">Price Comparison</CardTitle>
                <div className="flex gap-2">
                  <button
                    onClick={() => setDateRange("month")}
                    className={`px-3 py-1 text-xs rounded ${
                      dateRange === "month"
                        ? "bg-primary text-primary-foreground"
                        : "bg-secondary text-secondary-foreground"
                    }`}
                  >
                    This month
                  </button>
                  <button
                    onClick={() => setDateRange("lastMonth")}
                    className={`px-3 py-1 text-xs rounded ${
                      dateRange === "lastMonth"
                        ? "bg-primary text-primary-foreground"
                        : "bg-secondary text-secondary-foreground"
                    }`}
                  >
                    Last month
                  </button>
                  <button
                    onClick={() => setDateRange("all")}
                    className={`px-3 py-1 text-xs rounded ${
                      dateRange === "all"
                        ? "bg-primary text-primary-foreground"
                        : "bg-secondary text-secondary-foreground"
                    }`}
                  >
                    All time
                  </button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <PriceChart data={filteredPriceData} />
            </CardContent>
          </Card>
        </div>

        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle className="text-foreground">Price History Details</CardTitle>
          </CardHeader>
          <CardContent>
            <PriceTable data={filteredPriceData} />
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
