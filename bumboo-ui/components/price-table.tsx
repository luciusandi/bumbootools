import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import type { PriceHistoryItem } from "@/lib/types"

interface PriceTableProps {
  data: PriceHistoryItem[]
}

export function PriceTable({ data }: PriceTableProps) {
  return (
    <div className="overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow className="border-border">
            <TableHead className="text-muted-foreground">Date</TableHead>
            <TableHead className="text-muted-foreground">Fairprice</TableHead>
            <TableHead className="text-muted-foreground">Cold Storage</TableHead>
            <TableHead className="text-muted-foreground">Redmart</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((item, index) => (
            <TableRow key={index} className="border-border">
              <TableCell className="font-medium text-foreground">{item.date}</TableCell>
              <TableCell className="text-foreground">{item.fairprice != null ? `$${item.fairprice.toFixed(2)}` : ""}</TableCell>
              <TableCell className="text-foreground">{item.coldStorage != null ? `$${item.coldStorage.toFixed(2)}` : ""}</TableCell>
              <TableCell className="text-foreground">{item.redmart != null ? `$${item.redmart.toFixed(2)}` : ""}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
