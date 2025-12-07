export interface Product {
  id: string
  brand: string
  name: string
  type: string
  highestPrice: number
  avgPrice: number
  lowestPrice: number
  image: string
  priceHistory: PriceHistoryItem[]
  sitesCount?: number
  sites?: string[]
}

export interface PriceHistoryItem {
  date: string
  fairprice: number | null
  coldStorage: number | null
  redmart: number | null
  reviews?: string
}
