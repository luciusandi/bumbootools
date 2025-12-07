"use client"

import { Line, LineChart, CartesianGrid, XAxis, YAxis, Legend, ResponsiveContainer } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import type { PriceHistoryItem } from "@/lib/types"

interface PriceChartProps {
  data: PriceHistoryItem[]
}

export function PriceChart({ data }: PriceChartProps) {
  return (
    <ChartContainer
      config={{
        fairprice: {
          label: "Fairprice",
          color: "hsl(var(--chart-1))",
        },
        coldStorage: {
          label: "Cold Storage",
          color: "hsl(var(--chart-2))",
        },
        redmart: {
          label: "Redmart",
          color: "hsl(var(--chart-3))",
        },
      }}
      className="h-[300px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" tick={{ fill: "hsl(var(--muted-foreground))" }} />
          <YAxis stroke="hsl(var(--muted-foreground))" tick={{ fill: "hsl(var(--muted-foreground))" }} />
          <ChartTooltip content={<ChartTooltipContent />} />
          <Legend
            formatter={(value) => {
              const labels: Record<string, string> = {
                fairprice: "Fairprice",
                coldStorage: "Cold Storage",
                redmart: "Redmart",
              }
              return labels[value] || value
            }}
          />
          <Line
            type="monotone"
            dataKey="fairprice"
            stroke="var(--color-fairprice)"
            strokeWidth={2}
            dot={{ fill: "var(--color-fairprice)", r: 3 }}
          />
          <Line
            type="monotone"
            dataKey="coldStorage"
            stroke="var(--color-coldStorage)"
            strokeWidth={2}
            dot={{ fill: "var(--color-coldStorage)", r: 3 }}
          />
          <Line
            type="monotone"
            dataKey="redmart"
            stroke="var(--color-redmart)"
            strokeWidth={2}
            dot={{ fill: "var(--color-redmart)", r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </ChartContainer>
  )
}
